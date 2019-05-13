# import matplotlib
# matplotlib.use('agg')

from subprocess import Popen, PIPE
# from time import time, sleep
import numpy as np
import pandas as pd
import os
import sys
# from matplotlib import pyplot as plt
# import seaborn as sns


## treat peak file
## No need more
def treat_peak(sample=None, path=None):
    # bed = '/media/chaigs/softwares/data/hoper_test_04221120/peak/W6_S27.bam.peak.bed'

    sample_name = sample.strip().split('/')[-1]
    sample_name = '.'.join(sample_name.split('.')[:-1])
    bed = path + '/peak/' + sample_name + '.peak.bed'
    Peak_List = []
    if os.path.exists(bed):
        fh = open(bed)
    else:
        #print('Error: ' + path + '/peak/' + sample_name + '.peak.bed not exists!')
        sys.exit('<frip> ' + bed + 'No exists!')

    fh.readline()
    # Peak_List = []
    for i in fh:
        chrom, start, end, length, txID, geneID, pvalue, foldErichment, fdr = i.strip().split('\t')[:]
        Peak_List.append([chrom, start, end, geneID, txID])


    peak_data = pd.DataFrame(data=np.array(Peak_List), columns=["chr", "start", "end", "geneID", "txID"])
    # print len(peak_data.index)
    Peak_List = 0

    peak_start_end_list = []
    ## chrom as unit
    chrom_set = set(peak_data.chr)
    for chrom in chrom_set:
        # print chrom
        # sleep(1)
        single_chrom = peak_data.loc[peak_data.chr == chrom]

        gene_set = set(single_chrom.geneID)
        for gene in gene_set:
            # print gene
            # sleep(1)
            single_gene = single_chrom.loc[single_chrom.geneID == gene]
            # print single_gene
            # sleep(1)
            start_str = '\t'.join(list(single_gene.start))
            # print start_str
            end_str = '\t'.join(list(single_gene.end))
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
    peak_treat = pd.DataFrame(data=np.array(peak_start_end_list), columns=["chr", "start", "end"])
    # print len(peak_treat.index)

    peak_start_end_list = 0

    # df.to_csv(path + '/tmp/' + sample + 'treated.peak.bed', sep='\t', encoding='utf-8', index=False, header=False)
    peak_treat.to_csv(path + '/peak/' + sample_name + '.treated.peak.bed', sep='\t', encoding='utf-8', index=False,
                      header=False)
    return


def calculate_num(sample=None, path=None, tp=None):
    ## calculate the read counts mapped to genome
    sample_name_ip = sample[0].strip().split('/')[-1]
    sample_name_input = sample[1].strip().split('/')[-1]
    sample_name_ip = '.'.join(sample_name_ip.split('.')[:-1])
    sample_name_input = '.'.join(sample_name_input.split('.')[:-1])

    # sample_name = sample.strip().split('/')[-1]
    sample_bed_ip = path + '/tmp/' + sample_name_ip + '.bed'
    if os.path.exists(sample_bed_ip):
        column_types = {'chr': 'category', 'start': 'int32', 'end': 'int32', 'mapq': 'int16', 'strand': 'category'}
        data_ip = pd.read_csv(sample_bed_ip, sep='\t', names=['chr', 'start', 'end', 'qname', 'mapq', 'strand'],
                              dtype=column_types)
    else:
        sys.exit('<frip> ' + sample_bed_ip + ' No exists!')
    mappedReadCounts_IP = len(set(data_ip.qname))
    data_ip = 0  # release memory

    sample_bed_input = path + '/tmp/' + sample_name_input + '.bed'
    if os.path.exists(sample_bed_input):
        data_input = pd.read_csv(sample_bed_input, sep='\t', names=['chr', 'start', 'end', 'qname', 'mapq', 'strand'],
                                 dtype=column_types)
    else:
        sys.exit('<frip> ' + sample_bed_input + ' No exists!')

    mappedReadCounts_INPUT = len(set(data_input.qname))
    data_input = 0

    ## calculate the read counts in peaks
    peak_bed = path + '/tmp/' + sample_name_ip + '.treated.peak.bed'
    command3 = 'sort -k1,1 -k2,2n ' + peak_bed + ' > ' + path + '/tmp/' + sample_name_ip + '.treated.sorted.peak.bed'
    os.system(command3)
    peak_bed = path + '/tmp/' + sample_name_ip + '.treated.sorted.peak.bed'

    sample_bed_ip_q30 = path + '/tmp/' + sample_name_ip + '_q30.bed'

    if os.path.exists(peak_bed):
        if os.path.exists(sample_bed_ip_q30):
            # command1 = ''
            command1 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + sample_name_ip + '_q30.bed > ' + path + '/tmp/' + sample_name_ip + '_q30_sorted.bed'
            os.system(command1)
            # command3 = 'sort -k1,1 -k2,2n ' + peak_bed + ' > ' + path + '/tmp/' + sample_name_ip + '.treated.sorted.peak.bed'
            # os.system(command3)
            # peak_bed = path + '/tmp/' + sample_name_ip + '.treated.sorted.peak.bed'
            target_ip = 'bedtools intersect -wo -sorted -a ' + peak_bed + ' -b ' + path + '/tmp/' + sample_name_ip + '_q30_sorted.bed'
        else:
            sys.exit('<frip> ' + sample_bed_ip_q30 + ' No exists!')
    else:
        sys.exit('<frip> ' + peak_bed + ' No exists!')
    # target = 'coverageBed -a ' + peak_bed + ' -b ' + sample_bed + ' -counts'
    proc_ip = Popen(target_ip, stdout=PIPE, stderr=PIPE, shell=True)

    qname_ip = []
    # readCounts = 0
    for i in proc_ip.stdout:
        # readCounts += int(i.strip().split('\t')[-1])
        tmp_list = i.decode().strip().split('\t')
        # qname_ip.append(tmp_list[3])
        qname_ip.append(tmp_list[-2])


    read_counts_ip_in_peaks = len(set(qname_ip))
    ratio_IP = '{:.2%}'.format(float(read_counts_ip_in_peaks) / mappedReadCounts_IP)

    sample_bed_input_q30 = path + '/tmp/' + sample_name_input + '_q30.bed'
    if os.path.exists(sample_bed_input_q30):
        command2 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + sample_name_input + '_q30.bed > ' + path + '/tmp/' + sample_name_input + '_q30_sorted.bed'
        os.system(command2)
        target_input = 'bedtools intersect -wo -sorted -a ' + peak_bed + ' -b ' + path + '/tmp/' + sample_name_input + '_q30_sorted.bed'
    else:
        sys.exit('<frip> ' + sample_bed_input_q30 + ' No exists!')

    proc_input = Popen(target_input, stdout=PIPE, stderr=PIPE, shell=True)
    qname_input = []
    for i in proc_input.stdout:
        tmp_list = i.decode().strip().split('\t')
        # qname_input.append(tmp_list[3])
        qname_input.append(tmp_list[-2])

    read_counts_input_in_peaks = len(set(qname_input))
    ratio_INPUT = '{:.2%}'.format(float(read_counts_input_in_peaks) / mappedReadCounts_INPUT)

    return [sample_name_ip, 'IP', read_counts_ip_in_peaks, mappedReadCounts_IP, ratio_IP], \
           [sample_name_input, 'INPUT', read_counts_input_in_peaks, mappedReadCounts_INPUT, ratio_INPUT]


def frip(samples=None, path=None):
    # samples={'ip': [('W6_S27_chr20.bam', 'W8_S24_chr20.bam')],
    #  'input': [('W2_S22_chr20.bam', 'W4_S23_chr20.bam')]}

    # start_time = time()
    # print('MetaQC is calculating FRiP value...')

    IP = []
    INPUT = []
    for i in samples['ip']:
        for j in i:
            IP.append(j)

    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    frip_list = []

    IP_INPUT = zip(IP, INPUT)
    replicate_number = 0
    for item in IP_INPUT:
        replicate_number += 1
        # treat_peak(sample=item[0], path=path)
        frip_IP, frip_INPUT = calculate_num(sample=item, path=path)
        frip_list.append(['rep' + str(replicate_number), frip_IP[0], frip_IP[1], frip_IP[2], frip_IP[3], frip_IP[4]])
        frip_list.append(
            ['rep' + str(replicate_number), frip_INPUT[0], frip_INPUT[1], frip_INPUT[2], frip_INPUT[3], frip_INPUT[4]])

    frip_data = pd.DataFrame(data=np.array(frip_list),
                             columns=["replicates", "samples", "type", "readCountsInPeaks",
                                      "MappedReadCounts", "ratio"])

    frip_data.to_csv(path + '/file/frip.txt', sep='\t', encoding='utf-8', index=False, header=False)


    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    return




