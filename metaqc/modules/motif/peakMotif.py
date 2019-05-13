import numpy as np
import pandas as pd
# from time import time, sleep
from subprocess import Popen, PIPE
import scipy.stats as stats
#import statsmodels.stats.multitest as multitest
import requests
import random
import sys
import re
import os

def peak(sample=None, path=None):
    #file = '/media/chaigs/softwares/data/hoper_result/847372_20180530/peak/847372.bam.peak.bed'

    # data = pd.read_csv(file, sep='\t', names=['chr', 'start', 'end', 'length', 'txID', 'geneID', 'pvalue', 'foldEnrichment', 'fdr'], header=False)
    bed = path + '/peak/' + sample + '.treated.peak.bed'
    if os.path.exists(bed):
        data = pd.read_csv(path + '/peak/' + sample + '.treated.peak.bed', sep='\t', names=['chr', 'start', 'end'])
    else:
        sys.exit('<peakMotif> ' + bed + ' No exists!')

    # print (len(data.index))
    # print(data.dtypes)
    #print(data)

    ## sort
    # data = data.sort_values(by=['fdr'])

    #print(list(data.fdr)[:500])

    ## extract first 1000 rows
    if len(data.index) > 1000:
        data = data.head(1000)

    # l1 = []
    #
    # for index, row in data.iterrows():
    #     row_list = list(row)
    #     chrom, start, end = row_list[:]
    #     # # print (end)
    #     # # # sleep(1)
    #     # start_list = start.strip().split(',')
    #     # end_list = end.strip().split(',')
    #     # start_end_list = list(zip(start_list, end_list))
    #     # # print(start_end_list)
    #     # for item in start_end_list:
    #     l1.append([chrom, start, end, int(end)-int(start)])
    #
    # peak = pd.DataFrame(data=np.array(l1), columns=["chr", "start", "end", "length"])
    #
    # peak.length = peak.length.apply(int)
    #
    # # print(peak.dtypes)
    # # print(len(peak.index))
    #
    # ## remove the same chr, start, end peaks
    # b = peak.drop_duplicates(subset=['chr', 'start', 'end'], keep='first')
    # # print(len(b.index))
    #
    # ## remove same start
    # # c = peak.drop_duplicates(subset=['chr', 'start'], keep='first')
    # #print(len(c.index))
    #
    # ## remove same end
    # # d = c.drop_duplicates(subset=['chr', 'end'], keep='first')
    # #print(len(d.index))
    #
    # ## peak length >= 10 bp
    # finalPeak = b.loc[(b.length >= 10)]

    peak_list = []
    for index, row in data.iterrows():
        peak_list.append(list(row))
    return peak_list





def getText(url=None):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print (e)
        sys.exit()

def getFasta(species=None, peak_list=None):


    peak_sequence = dict()
    # file = '/media/chaigs/softwares/data/hoper_result/847372_20180530/peak_sequence.fa'
    # out = open(file, 'w')

    #peak_list = peak()
    # print(len(peak_list))

    # n1 = 0
    for i in peak_list:
        # n1 += 1
        # print (n1)
        chrom, start, end = i[:]

        url = 'http://genome.ucsc.edu/cgi-bin/das/' + species + '/dna?segment=' + chrom + ':' + str(start) + ',' + str(end)

        #print(url)
        text = getText(url)

        #print(text)

        l1 = text.split('>\n')
        #print (l1)

        info = l1[3].strip('<')
        seq = l1[5].strip('\n</DNA')

        # print(info)
        # print(seq)

        #print(info.split())
        info_list = info.split()
        id = info_list[1].split('=')[1].strip('\"')
        # print(id)
        start = info_list[2].split('=')[1].strip('\"')
        end = info_list[3].split('=')[1].strip('\"')
        # print(start)
        # print(end)
        head = '>' + id + ':' + start + '-' + end
        # print (head)

        seq_info = ''.join(seq.strip().split('\n')).upper()
        # print(seq_info)
        # print(len(seq_info))
        # out.write(head+'\n')
        # out.write(seq_info+'\n')
        peak_sequence[head] = seq_info
    # out.close()

    return peak_sequence

#getFasta(species='hg19')

def getDinucleotideShuffle(sequence=None):
    sequence_shuffle = dict()
    for key in sequence:
        #seq = 'AACAAAACAAAAAGTTGGGTAGTTTGAGAAC'
        seq = sequence[key]
        #print(seq)
        seq = [seq[x:x+2] for x in range(0,len(seq),2)]
        random.shuffle(seq)
        # print (''.join(seq))
        # print(len(seq))
        sequence_shuffle[key] = ''.join(seq)
    return sequence_shuffle

def reverseComplement(sequence=None):
    sequence_reverse_complement = dict()
    complement = {'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    for key in sequence:
        seq = sequence[key][::-1]
        bases = list(seq)
        letters = [complement[base] for base in bases if base in complement]
        sequence_reverse_complement[key] = ''.join(letters)
    return sequence_reverse_complement

def T2U(sequence=None):
    sequence_t2u = dict()
    t2u = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'U', 'N': 'N'}
    for key in sequence:
        sequence_t2u[key] = ''.join([t2u[base] for base in list(sequence[key]) if base in t2u])
    return sequence_t2u




def motif(samples=None, path=None, species=None):
    # start_time = time()

    IP = []
    INPUT = []

    for i in samples['ip']:
        for j in i:
            IP.append(j)
    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    IP_INPUT = list(zip(IP, INPUT))
    replicate_num = 0

    motif_info = []
    for item in IP_INPUT:
        replicate_num += 1

        ip_name = item[0].strip().split('/')[-1]
        input_name = item[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        peak_list = peak(sample=ip_name, path=path)

        peak_sequence = getFasta(species=species, peak_list=peak_list)
        peak_sequence_reverse_complement = reverseComplement(sequence=peak_sequence)

        ## convert T to U
        peak_sequence = T2U(sequence=peak_sequence)

        peak_sequence_shuffle = getDinucleotideShuffle(sequence=peak_sequence)
        peak_sequence_reverse_complement_shuffle = getDinucleotideShuffle(sequence=peak_sequence_reverse_complement)

        seq_num = len(peak_sequence)

        peak_sequence_motif = []
        peak_sequence_shuffle_motif = []

        peak_sequence_reverse_complement_motif = []
        peak_sequence_reverse_complement_shuffle_motif = []

        for key in peak_sequence:
            l1 = re.findall("[G|A][G|A]AC[A|C|U]", peak_sequence[key])
            l2 = re.findall("[G|A][G|A]AC[A|C|U]", peak_sequence_shuffle[key])

            peak_sequence_motif.extend(l1)
            peak_sequence_shuffle_motif.extend(l2)

            l3 = re.findall("[G|A][G|A]AC[A|C|U]", peak_sequence_reverse_complement[key])
            l4 = re.findall("[G|A][G|A]AC[A|C|U]", peak_sequence_reverse_complement_shuffle[key])
            peak_sequence_reverse_complement_motif.extend(l3)
            peak_sequence_reverse_complement_shuffle_motif.extend(l4)

        peak_sequence_motif_num = len(peak_sequence_motif)
        peak_sequence_shuffle_motif_num = len(peak_sequence_shuffle_motif)
        oddsratio, peak_sequence_motif_pvalue = stats.fisher_exact(np.array([[peak_sequence_motif_num, seq_num], [peak_sequence_shuffle_motif_num, seq_num]]),
                                               alternative="greater")

        peak_sequence_rc_motif_num = len(peak_sequence_reverse_complement_motif)
        peak_sequence_rc_shuffle_motif_num = len(peak_sequence_reverse_complement_shuffle_motif)
        oddsratio, peak_sequence_rc_motif_pvalue = stats.fisher_exact(np.array([[peak_sequence_rc_motif_num, seq_num], [peak_sequence_rc_shuffle_motif_num, seq_num]]),
                                               alternative="greater")

        if float(peak_sequence_motif_pvalue) >= float(peak_sequence_rc_motif_pvalue):

            peak_sequence_rc_motif_pvalue = "{:.2e}".format(float(peak_sequence_rc_motif_pvalue))
            motif_info.append(['rep' + str(replicate_num), ip_name, input_name, ip_name + '.peak.bed', peak_sequence_rc_motif_num, peak_sequence_rc_shuffle_motif_num,
                               peak_sequence_rc_motif_pvalue])
            out = open(path + '/tmp/' + ip_name + '.motif.fa', 'w')
            n1 = 0
            for i in peak_sequence_reverse_complement_motif:
                n1 += 1
                out.write('>' + str(n1) + '\n')
                out.write(i + '\n')
            out.close()

        elif float(peak_sequence_motif_pvalue) < float(peak_sequence_rc_motif_pvalue):

            peak_sequence_motif_pvalue = "{:.2e}".format(float(peak_sequence_motif_pvalue))
            motif_info.append(['rep' + str(replicate_num), ip_name, input_name, ip_name + '.peak.bed', peak_sequence_motif_num, peak_sequence_shuffle_motif_num,
                               peak_sequence_motif_pvalue])

            out = open(path + '/tmp/' + ip_name + '.motif.fa', 'w')
            n1 = 0
            for i in peak_sequence_motif:
                n1 += 1
                out.write('>' + str(n1) + '\n')
                out.write(i + '\n')
            out.close()

    n2 = 0
    for i in IP_INPUT:
        n2 += 1
        ip_name = i[0].strip().split('/')[-1]
        ip_name = '.'.join(ip_name.split('.')[:-1])
        # cmd = "weblogo --format PNG --resolution 600 --size large --annotate '1,2,3,4,5' --rotate-numbers YES --title " + ip_name + " --title-fontsize 6 < " + \
        #       path + "/tmp/" + ip_name + ".motif.fa " + "> " + path + "/motif_" + str(n2) + ".png"

        if os.path.exists(path + "/tmp/" + ip_name + ".motif.fa"):
            cmd = "weblogo --format PNG --resolution 600 --size large --annotate '1,2,3,4,5' --rotate-numbers YES < " + \
                path + "/tmp/" + ip_name + ".motif.fa " + "> " + path + "/img/motif_" + str(n2) + ".png"

            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            for i in proc.stderr:
                print(i.decode())
                #sys.exit()
        else:
            sys.exit('<peakMotif> ' + path + "/tmp/" + ip_name + ".motif.fa No exists!")
    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    peak_motif_data = pd.DataFrame(data=np.array(motif_info),
                                   columns=["replicates", "sampleIP", "sampleINPUT", "PeakFileName", "motifCounts",
                                            "motifCountsRandom", "pvalue"])

    peak_motif_data.to_csv(path + '/file/motifInfo.txt', sep='\t', encoding='utf-8', index=False, header=False)
    return






