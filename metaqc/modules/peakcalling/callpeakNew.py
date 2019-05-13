import numpy as np
import pandas as pd
from subprocess import Popen, PIPE
import scipy.stats as stats
import statsmodels.stats.multitest as multitest
# from time import time, sleep
import os
import sys
# import math
# #from scipy.stats.stats import pearsonr
# from matplotlib import pyplot as plt
from time import sleep

#from cutExones import cut_exones
from metaqc.modules.peakcalling.bam2bed import bam2Bed
from metaqc.modules.peakcalling.gtf2geneExonNew import getExonCoordinate


def chunks(L, n):
    """
    Yield successive n-sized chunks from L.
    """
    for i in range(0, len(L), n):
        yield L[i:i + n]



def readCounts(gtfile = None, sample = None, path = None):
    #target = "coverageBed -a genes_chr20_04141428.bed -b " + bed + " -counts"

    #### sample is a tuple (IP, INPUT)
    sample_IP=sample[0]
    sample_INPUT=sample[1]
    gtfile_name = gtfile.strip().split('/')[-1]
    sample_IP_name = sample_IP.strip().split('/')[-1]
    sample_INPUT_name = sample_INPUT.strip().split('/')[-1]
    sample_IP_name = '.'.join(sample_IP_name.split('.')[:-1])
    sample_INPUT_name = '.'.join(sample_INPUT_name.split('.')[:-1])

    if os.path.exists(path + '/tmp/' + gtfile_name + '_sorted.bed'):
        if os.path.exists(path + '/tmp/' + sample_IP_name + '.treated_sorted.bed'):
            out_ip = open(path + '/tmp/' + sample_IP_name + '_read_counts.txt', 'w')
            ip = "coverageBed -sorted -counts -a " + path + '/tmp/' + gtfile_name + '_sorted.bed -b ' + path + '/tmp/' + sample_IP_name + '.treated_sorted.bed'
            IP = Popen(ip, stdout=PIPE, stderr=PIPE, shell=True)

            # IP_list=[]
            for i in IP.stdout:
                l1 = i.decode().strip().split('\t')
                out_ip.write(i.decode())
                if len(l1) != 8:
                    # print(l1)
                    # print("Peak calling early termination!")
                    out_ip.close()
                    sys.exit('<callpeak> ' + l1)
            out_ip.close()
                # IP_list.append(i.decode().strip().split('\t'))
        else:
            sys.exit('<callpeak> ' + path + '/tmp/' + sample_IP_name + '.treated_sorted.bed No exists!')


    # data = pd.DataFrame(data=np.array(IP_list), columns=["chr", "start", "end", "length", "geneID", "txID", "readCountsIP"])
    # print data.dtypes
    # print len(data.index)
    # IP_list = 0

        if os.path.exists(path + '/tmp/' + sample_INPUT_name + '.treated_sorted.bed'):
            out_input = open(path + '/tmp/' + sample_INPUT_name + '_read_counts.txt', 'w')
            input = "coverageBed -sorted -counts -a " + path + '/tmp/' + gtfile_name + '_sorted.bed -b ' + path + '/tmp/' + sample_INPUT_name + '.treated_sorted.bed'
            INPUT = Popen(input, stdout=PIPE, stderr=PIPE, shell=True)

            # INPUT_readCounts=[]
            for i in INPUT.stdout:
                l2 = i.decode().strip().split('\t')
                out_input.write(i.decode())
                if len(l2) != 8:
                    out_input.close()
                    sys.exit('<callpeak> ' + l2)
            out_input.close()
                # INPUT_readCounts.append(i.decode().strip().split('\t')[-1])
        else:
            sys.exit('<callpeak> ' + path + '/tmp/' + sample_INPUT_name + '.treated_sorted.bed No exists!')
    else:
        sys.exit('<calllpeak> ' + path + '/tmp/' + gtfile_name + '_sorted.bed No exists!')

    ## IP sample read counts
    column_types_ip = {'chr': "category", 'start': 'int32', 'end': 'int32', 'length':'int8', 'geneID': 'category',
                       'txID': 'category', 'strand':'category', 'readCountsIP':'int32'}
    column_types_input = {'chr': "category", 'start': 'int32', 'end': 'int32', 'length':'int8', 'geneID': 'category',
                          'txID': 'category', 'strand':'category', 'readCountsInput':'int32'}

    data = pd.read_csv(path + '/tmp/' + sample_IP_name + '_read_counts.txt', sep='\t', names=['chr', 'start', 'end', 'length', 'geneID',
                                                                                              'txID', 'strand', 'readCountsIP'],
                       dtype=column_types_ip)
    data_input = pd.read_csv(path + '/tmp/' + sample_INPUT_name + '_read_counts.txt', sep='\t', names=['chr', 'start', 'end', 'length',
                                                                                                       'geneID', 'txID', 'strand', 'readCountsInput'],
                             dtype=column_types_input)

    data['readCountsINPUT'] = data_input.readCountsInput
    data_input = 0
    # INPUT_readCounts = 0

    ## save the data for SSD
    data.to_csv(path + '/tmp/' + sample_IP_name + '.readCounts.bed', sep='\t', encoding='utf-8', index=False, header=False)


    # print data.dtypes

    # data.readCountsIP = data.readCountsIP.apply(int)
    # data.readCountsINPUT = data.readCountsINPUT.apply(int)
    # data.start = data.start.apply(int)
    # data.end = data.end.apply(int)
    # data.length = data.length.apply(int)
    #print data.dtypes

    ## SSD & PCC
    # samples_read_counts = dict()
    # samples_read_counts[sample_IP_name] = list(data.readCountsIP)
    # samples_read_counts[sample_INPUT_name] = list(data.readCountsINPUT)


    # save peaks in all Chromosomes
    final_peak_list = []

    # chrom as unit
    chrom_set = set(data.chr)
    for chrom in chrom_set:
        #b = peak_small_IP.loc[peak_small_IP['chrGene'] == i].copy()
        single_chrom = data.loc[data.chr == chrom]
        #print len(single_chrom.index)

        # gene as unit
        gene_set = set(single_chrom.geneID)
        for gene in gene_set:
            single_gene = single_chrom.loc[single_chrom.geneID == gene]
            #print len(single_gene.index)

            ## tx as unit
            tx_set = set(single_gene.txID)
            for tx in tx_set:
                single_tx = single_gene.loc[single_gene.txID == tx]
                # strand = list(single_tx.strand)[0]


                single_tx_read_counts_IP = single_tx.readCountsIP.sum()

                ## filter ip readCounts == 0
                if single_tx_read_counts_IP > 0:
                    #print single_tx
                    #sleep(1)
                    strand = list(single_tx.strand)[0]

                    single_tx_read_counts_INPUT = single_tx.readCountsINPUT.sum()
                    single_tx_exones_length = single_tx.length.sum()

                    start_dict=dict()
                    for index, row in single_tx.iterrows():
                        row_list = list(row)
                        start_dict[row_list[1]] = row_list
                    #print len(start_dict)


                    start_list = list(single_tx.start)
                    end_list = list(single_tx.end)
                    start_end_list = zip(start_list, end_list)

                    coordinate = []
                    for item in start_end_list:
                        coordinate.extend(range(item[0], item[1] + 1))

                    new_line_list=[]
                    for each in chunks(coordinate, 25):
                    # each is a list

                        each_2 = each[1:]
                        small_segment_start=[]
                        small_segment_end=[]
                        small_segment_start.append(str(each[0]))
                        for i in range(len(each_2)):
                            if each_2[i] - each[i] > 1:
                                small_segment_end.append(str(each[i]))
                                small_segment_start.append(str(each_2[i]))
                        small_segment_end.append(str(each[-1]))


                        new_line_start=','.join(small_segment_start)
                        new_line_end=','.join(small_segment_end)
                        new_line_length=0
                        new_line_readCountsIP=0
                        new_line_readCountsINPUT =0
                        for j in small_segment_start:
                            tmp_list=start_dict[int(j)]
                            new_line_length += tmp_list[3]
                            new_line_readCountsIP += tmp_list[-2]
                            new_line_readCountsINPUT += tmp_list[-1]
                        new_line_list.append([chrom, new_line_start, new_line_end, new_line_length, gene, tx,
                                              strand, new_line_readCountsIP, new_line_readCountsINPUT])
                    single_tx_new = pd.DataFrame(data=np.array(new_line_list), columns=["chr", "start", "end", "length",
                                                                                        "geneID", "txID", "strand",
                                                                                        "readCountsIP", "readCountsINPUT"])
                    new_line_list = 0
                    data_type = {'chr': "category", 'length':'int32', 'geneID': 'category',
                                 'txID': 'category', 'strand':'category', 'readCountsIP':'int32', 'readCountsINPUT':'int32'}
                    single_tx_new = single_tx_new.astype(data_type)
                    # print single_tx_new
                    # sleep(1)

                    #print single_tx_new.dtypes

                    # single_tx_new.readCountsIP = single_tx_new.readCountsIP.apply(int)
                    # single_tx_new.readCountsINPUT = single_tx_new.readCountsINPUT.apply(int)
                    # print single_tx_new.dtypes

                    single_tx_read_counts_IP_mean = int(single_tx_new.readCountsIP.mean())
                    single_tx_read_counts_INPUT_mean = int(single_tx_new.readCountsINPUT.mean())

                    pvalue_small=[]
                    #ratio_small=[]

                    ## small segment fisher exact test
                    for index, row in single_tx_new.iterrows():
                        row_list_new = list(row)
                        each_line_IP = row_list_new[-2]
                        each_line_INPUT = row_list_new[-1]
                        oddsratio, pvalue = stats.fisher_exact(np.array([[each_line_IP, single_tx_read_counts_IP_mean],
                                                                         [each_line_INPUT, single_tx_read_counts_INPUT_mean]]),
                                                               alternative="greater")
                        #ratio = (IP_each * input_mean) / float(IP_mean * input_each)
                        # each_line_INPUT += 1
                        # single_gene_read_counts_IP_mean += 1
                        # ratio = (each_line_IP * single_gene_read_counts_INPUT_mean) / float(single_gene_read_counts_IP_mean * each_line_INPUT)
                        #print pvalue
                        pvalue_small.append(pvalue)
                        #ratio_small.append(ratio)
                    single_tx_new['pvalue'] = pvalue_small
                    pvalue_small = 0
                    #single_gene_new['foldEnrichment'] = ratio_small
                    #print single_tx_new.dtypes
                    # print single_tx_new
                    # sleep(1)

                    ## extract the line of p value <= 0.05
                    single_tx_peak = single_tx_new.loc[single_tx_new.pvalue <= 0.05].copy()
                    single_tx_new = 0

                    if len(single_tx_peak.index) > 1:
                        index_list = list(single_tx_peak.index)
                        index_list_2 = index_list[1:]

                        n1 = 1
                        flag = [n1]

                        for i in range(len(index_list_2)):
                            if index_list_2[i] - index_list[i] == 1:
                                flag.append(n1)
                            elif index_list_2[i] - index_list[i] > 1:
                                n1 += 1
                                flag.append(n1)
                        single_tx_peak["flag"] = flag
                        single_tx_peak = single_tx_peak.astype({"flag":'int32'})

                        #print single_tx_peak.dtypes
                        # print single_tx_peak
                        # sleep(1)

                        flag_set = set(single_tx_peak.flag)

                        for f in flag_set:
                            peak = single_tx_peak.loc[single_tx_peak.flag == f].copy()

                            if len(peak.index) > 1:
                                # print peak
                                # print peak.dtypes

                                # peak.length = peak.length.apply(int)


                                peak_read_counts_IP = peak.readCountsIP.sum()
                                peak_read_counts_INPUT = peak.readCountsINPUT.sum()
                                peak_length = peak.length.sum()
                                peak_read_counts_IP_mean = int(single_tx_read_counts_IP / (single_tx_exones_length / peak_length))
                                peak_read_counts_INPUT_mean = int(single_tx_read_counts_INPUT / (single_tx_exones_length / peak_length))

                                oddsratio, pvalue = stats.fisher_exact(np.array([[peak_read_counts_IP, peak_read_counts_IP_mean],
                                                                                 [peak_read_counts_INPUT, peak_read_counts_INPUT_mean]]),
                                                                       alternative="greater")

                                # ZeroDivisionError: float division by zero
                                peak_read_counts_IP_mean += 1
                                peak_read_counts_INPUT += 1
                                ratio = (peak_read_counts_IP * peak_read_counts_INPUT_mean) / float(peak_read_counts_IP_mean * peak_read_counts_INPUT)

                                peak_start_list = list(peak.start)
                                peak_start_list_str = '\t'.join(peak_start_list)

                                # if ',' not in peak_start_list_str:
                                #     peak_start = str(int(list(peak.start)[0]) - 1)
                                #     peak_end = list(peak.end)[-1]
                                #
                                # elif ',' in peak_start_list_str:
                                peak_end_list = list(peak.end)
                                peak_end_list_str = '\t'.join(peak_end_list)

                                # remove ',' mark
                                start_new_list = '\t'.join(peak_start_list_str.split(',')).split('\t')
                                end_new_list = '\t'.join(peak_end_list_str.split(',')).split('\t')

                                start_end_new_list = list(zip(start_new_list, end_new_list))

                                start_end_new_list_2 = start_end_new_list[1:]

                                peak_start_new = []
                                peak_end_new = []

                                peak_start_new.append(start_new_list[0])

                                for n in range(len(start_end_new_list_2)):
                                    if int(start_end_new_list_2[n][0]) - int(start_end_new_list[n][1]) > 1:
                                        peak_end_new.append(start_end_new_list[n][1])
                                        peak_start_new.append(start_end_new_list_2[n][0])

                                peak_end_new.append(end_new_list[-1])

                                peak_start = ','.join([str(int(start)-1) for start in peak_start_new])
                                peak_end = ','.join(peak_end_new)

                                ## add peak_read_counts_IP to compute FRiP value  This way has some problems.

                                small_peak = [chrom, peak_start, peak_end, peak_length, tx, gene, strand, pvalue, ratio]

                                final_peak_list.append(small_peak)
    final_peak = pd.DataFrame(data=np.array(final_peak_list), columns=["chr", "start", "end", "length", "txID", "geneID", "strand", "pvalue", "foldEnrichment"])
    final_peak_list = 0
    final_peak = final_peak.astype({"chr":"category", "length": "int32", "txID":"category", "geneID":"category",
                                    "strand":"category", "pvalue":"float64", "foldEnrichment":"float64"})

    # print len(final_peak.index)
    # print final_peak.dtypes
    #peak.length = peak.length.apply(int)

    # final_peak.pvalue = final_peak.pvalue.apply(float)
    # final_peak.length = final_peak.length.apply(int)
    # final_peak.foldEnrichment = final_peak.foldEnrichment.apply(float)
    #final_peak.readCountsIP = final_peak.readCountsIP.apply(int)
    #print final_peak.dtypes

    # Benjamini-Hochberg method for P-Value Correction
    array_fdr = multitest.multipletests(list(final_peak.pvalue), method='fdr_bh')

    final_peak['fdr'] = array_fdr[1]

    ## minimum peak length is 100 bp, fdr <= 0.05, maximum peak length is 1000bp

    finalPeak = final_peak.loc[(final_peak.length >= 100) & (final_peak.fdr <= 0.05) & (final_peak.length <= 1000) & (final_peak.foldEnrichment > 1)].copy()
    final_peak = 0
    finalPeak = finalPeak.sort_values(by=['fdr'])
    # data = data.sort_values(by=['fdr'])
    # columns = ["#chr", "start", "end", "length", "txID", "geneID", "strand", "pvalue", "foldEnrichment", "fdr"]
    out1 = open(path + '/peak/' + sample_IP_name + '_peak.bed', 'w')
    out2 = open(path + '/peak/' + sample_IP_name + '_peak.xls', 'w')
    l1 = ['#Chr', 'chromStart', 'chromEnd', 'name', 'score', 'strand', 'thickStart', 'thickEnd', 'itemRgb',
          'blockCount', 'blockSizes', 'blockStarts']
    s1 = '\t'.join(l1)
    l2 = ['chr', 'chromStart', 'chromEnd', 'name', 'score', 'strand', 'thickStart', 'thickEnd', 'itemRgb',
          'blockCount', 'blockSizes', 'blockStarts', 'exonStart', 'exonEnd', 'peakLength', 'txID', 'pvalue',
          'foldEnrichment', 'fdr']
    s2 = '\t'.join(l2)
    out1.write(s1)
    out1.write('\n')

    out2.write(s2)
    out2.write('\n')

    for index, row in finalPeak.iterrows():
        chrom, start, end, length, txID, geneID, strand, pvalue, foldEnrichment, fdr = list(row)[:]
        exonStart_list = start.split(',')
        ChromStart = int(exonStart_list[0])
        exonEnd_list = end.split(',')
        ChromEnd = int(exonEnd_list[-1])

        blockCount = len(exonStart_list)
        blockSize = []
        for j in range(blockCount):
            Size = int(exonEnd_list[j]) - int(exonStart_list[j])
            blockSize.append(str(Size))
        blockSizes = ','.join(blockSize)

        blockStart = []
        for k in exonStart_list:
            blockStart.append(str(int(k) - ChromStart))
        blockStarts = ','.join(blockStart)
        itemRgb = '0'
        l3 = [chrom, str(ChromStart), str(ChromEnd), geneID, str(pvalue), strand, str(ChromStart), str(ChromEnd), itemRgb,
              str(blockCount), blockSizes, blockStarts]
        s3 = '\t'.join(l3)

        l4 = [chrom, str(ChromStart), str(ChromEnd), geneID, str(pvalue), strand, str(ChromStart), str(ChromEnd), itemRgb,
              str(blockCount), blockSizes, blockStarts, start, end, str(length), txID, str(pvalue), str(foldEnrichment),
              str(fdr)]
        s4 = '\t'.join(l4)

        out1.write(s3)
        out1.write('\n')

        out2.write(s4)
        out2.write('\n')
    out1.close()
    out2.close()

    # finalPeak.to_csv(path + '/peak/' + sample_IP_name + '.peak.bed', sep='\t', encoding='utf-8', index=False)
    #return samples_read_counts
    return


def treat_peak(sample=None, path=None):
    # bed = '/media/chaigs/softwares/data/hoper_test_04221120/peak/W6_S27.bam.peak.bed'

    sample_name = sample.strip().split('/')[-1]
    sample_name = '.'.join(sample_name.split('.')[:-1])
    bed = path + '/peak/' + sample_name + '_peak.xls'
    if os.path.exists(bed):
        column_types = {'chr':'category', 'chromStart':'int32', 'chromEnd':'int32', 'name':'category', 'score':'float',
                        'strand':'category', 'thickStart':'int32', 'thickEnd':'int32', 'itemRgb':'category',
                        'blockCount':'uint8', 'peakLength':'int16', 'txID':'category', 'pvalue':'float',
                        'foldEnrichment':'float', 'fdr':'float'}
        peak_data = pd.read_csv(bed, sep='\t', dtype=column_types)
        out = open(path + '/tmp/' + sample_name + '.treated.peak.bed', 'w')
        # fh = open(bed)
    # else:
    #     sys.exit('<callpeak> ' + bed + ' No exists!')
    # fh.readline()
    # Peak_List = []
    # for i in fh:
    #     chrom, start, end, length, txID, geneID, pvalue, foldErichment, fdr = i.strip().split('\t')[:]
    #     Peak_List.append([chrom, start, end, geneID, txID])
    #
    # peak_data = pd.DataFrame(data=np.array(Peak_List), columns=["chr", "start", "end", "geneID", "txID"])
    # # print len(peak_data.index)
    # Peak_List = 0

        peak_start_end_list = []
        ## chrom as unit
        chrom_set = set(peak_data.chr)
        for chrom in chrom_set:
            # print chrom
            # sleep(1)
            single_chrom = peak_data.loc[peak_data.chr == chrom].copy()

            gene_set = set(single_chrom.name)
            for gene in gene_set:
                # print gene
                # sleep(1)
                single_gene = single_chrom.loc[single_chrom.name == gene].copy()
                # print single_gene
                # sleep(1)
                start_str = '\t'.join(list(single_gene.exonStart))
                # print start_str
                end_str = '\t'.join(list(single_gene.exonEnd))
                start_list = '\t'.join(start_str.split(',')).split('\t')
                # print start_list
                end_list = '\t'.join(end_str.split(',')).split('\t')
                start_end_list = zip(start_list, end_list)

                single_gene_peak_coord = []
                for item in start_end_list:
                    # print item
                    single_gene_peak_coord.extend(range(int(item[0]), int(item[1]) + 1))
                single_gene_peak_list = list(set(single_gene_peak_coord))
                single_gene_peak_list.sort()
                single_gene_peak_list_2 = single_gene_peak_list[1:]
                peak_start = []
                peak_end = []

                peak_start.append(single_gene_peak_list[0])
                for i in range(len(single_gene_peak_list_2)):
                    if single_gene_peak_list_2[i] - single_gene_peak_list[i] > 1:
                        peak_end.append(single_gene_peak_list[i])
                        peak_start.append(single_gene_peak_list_2[i])
                peak_end.append(single_gene_peak_list[-1])
                for j in range(len(peak_start)):
                    peak_start_end_list.append([chrom, peak_start[j], peak_end[j]])
                    out.write('\t'.join([chrom, str(peak_start[j]), str(peak_end[j])]))
                    out.write('\n')
        out.close()
    else:
        # out.close()
        sys.exit('<callpeak> ' + bed + ' No exists!')

        # peak_treat = pd.DataFrame(data=np.array(peak_start_end_list), columns=["chr", "start", "end"])
        # # print len(peak_treat.index)
        #
        # peak_start_end_list = 0
        #
        # # df.to_csv(path + '/tmp/' + sample + 'treated.peak.bed', sep='\t', encoding='utf-8', index=False, header=False)
        # peak_treat.to_csv(path + '/peak/' + sample_name + '.treated.peak.bed', sep='\t', encoding='utf-8', index=False,
        #                   header=False)
    return


def callPeak(gtffile = None, samples = None, path = None, seq_type = None, rRNA_tRNA_bed=None):

    # samples = {'ip': [('W5_S26.bam', 'W7_S28.bam'), ('W6_S27.bam', 'W8_S24.bam')],
    #            'input': [('W1_S21.bam', 'W3_S25.bam'), ('W2_S22.bam', 'W4_S23.bam')]}

    # start_time = time()
    # print ("MetaQC is calling peaks...\n  This step may take several hours...")
    sleep(5)



    # create a prak directory
    os.mkdir(path + '/peak')

    # cut exones into 25 bp
    if os.path.exists(gtffile):
        getExonCoordinate(gtf=gtffile, path=path, rRNA_tRNA_bed=rRNA_tRNA_bed)
    else:
        sys.exit('<callpeak> ' + gtffile + ' no exists!')


    IP=[]
    INPUT=[]
    for i in samples['ip']:
        for j in i:
            IP.append(j)

    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    ## treat bam files
    for m in IP:
        # bam2Bed(seq_type=seq_type, bamfile=m, path=path, read_length=read_length)
        if os.path.exists(m):
            bam2Bed(seq_type=seq_type, bamfile=m, path=path)
        else:
            sys.exit('<callpeak> ' + m + ' No exists!')

    for n in INPUT:
        if os.path.exists(n):
            bam2Bed(seq_type=seq_type, bamfile=n, path=path)
        # bam2Bed(seq_type=seq_type, bamfile=n, path=path, read_length=read_length)
        else:
            sys.exit('<callpeak> ' + n + ' No exists!')


    # print IP
    # print INPUT

    ## call peak
    IP_INPUT = zip(IP, INPUT)

    ## SSD & PCC
    #read_counts_dict=dict()


    ## FRiP values
    # readCountsInPeaks_dict = dict()

    for item in IP_INPUT:
        ## peak calling
        # IP_sample_name = item[0].strip().split('/')[-1]
        # INPUT_sample_name = item[1].strip().split('/')[-1]
        # print ("IP sample: " + IP_sample_name + '\tINPUT sample: ' + INPUT_sample_name)
        readCounts(gtfile=gtffile, sample=item, path=path)
        treat_peak(sample=item[0], path=path)
        #read_counts_dict.update(samples_read_counts)
        # readCountsInPeaks_dict[item[0]] = readCountsInPeaks
    #     print ("--"*20)
    #
    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    return

