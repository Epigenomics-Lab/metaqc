# import matplotlib
# matplotlib.use('agg')

import numpy as np
import pandas as pd
from subprocess import Popen, PIPE
import os
import sys
# from matplotlib import pyplot as plt
# import seaborn as sns
# from time import sleep, time
def treat_peak_add(sample=None, path=None):
    # bed = '/media/chaigs/softwares/data/hoper_test_04221120/peak/W6_S27.bam.peak.bed'

    # sample_name = sample.strip().split('/')[-1]
    # sample_name = '.'.join(sample_name.split('.')[:-1])
    bed = path + '/peak/' + sample + '.peak.bed'
    fh = open(bed)
    fh.readline()
    Peak_List = []
    for i in fh:
        chrom, start, end, length, txID, geneID, pvalue, foldErichment, fdr = i.strip().split('\t')[:]
        Peak_List.append([chrom, start, end, geneID, txID])

    peak_data = pd.DataFrame(data=np.array(Peak_List), columns=["chr", "start", "end", "geneID", "txID"])
    # print len(peak_data.index)

    peak_start_end_list = []
    ## chrom as unit
    chrom_set = set(peak_data.chr)
    for chrom in chrom_set:
        # print chrom
        # sleep(1)
        single_chrom = peak_data.loc[peak_data.chr == chrom].copy()

        gene_set = set(single_chrom.geneID)
        for gene in gene_set:
            # print gene
            # sleep(1)
            single_gene = single_chrom.loc[single_chrom.geneID == gene].copy()
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

    # df.to_csv(path + '/tmp/' + sample + 'treated.peak.bed', sep='\t', encoding='utf-8', index=False, header=False)
    peak_treat.to_csv(path + '/tmp/' + sample + '.treated.peak.bed', sep='\t', encoding='utf-8', index=False,
                      header=False)
    return

def peak_treat(sample=None, path=None):
    # bed = path + '/peak/' + sample + '_peak.xls'
    bed = path + '/tmp/' + sample + '.treated.peak.bed'

    if os.path.exists(bed):
        fh = open(bed)
        # fh.readline()
        # fh = open(path + '/peak/' + sample + '.treated.peak.bed')

    else:
        sys.exit('<peakOvlerlapLength> ' + bed + ' No exists!')
    #fh.readline()
    peak_length_all = 0
    # start_end_info = []

    for i in fh:
        chrom, start, end = i.strip().split('\t')[:]
        peakLength = int(end) - int(start)
        # peakLength = int(i.strip().split('\t')[-5])
        peak_length_all += peakLength
    # chrom, start, end = i.strip().split('\t')[:]
    #     peak_length_all += int(length)
    #
    #     start_list = start.split(',')
    #     end_list = end.split(',')
    #
    #     for i in range(len(start_list)):
    #         start_end_info.append([chrom, start_list[i], end_list[i]])
    # start_end_info_data = pd.DataFrame(data=np.array(start_end_info), columns=["chrom", "start", "end"])
    #
    # start_end_info_data.to_csv(path + '/tmp/' + sample + '.peak.bed', sep='\t', encoding='utf-8', index=False, header=False)

    return peak_length_all


def peak_overlap_length_fraction(samples=None, path=None):
    # start_time = time()
    # print('MetaQC is calculating fraction of overlapping-peak length between replicates...')
    IP = []
    INPUT = []

    for i in samples['ip']:
        for j in i:
            IP.append(j)
    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    IP_INPUT = list(zip(IP, INPUT))
    # replicate_num = 0

    peak_length_all_dict = dict()

    if len(IP_INPUT) > 1:
        for item in IP_INPUT:
            # replicate_num += 1
            ip_name = item[0].strip().split('/')[-1]
            input_name = item[1].strip().split('/')[-1]
            ip_name = '.'.join(ip_name.split('.')[:-1])
            # treat_peak_add(sample=ip_name, path=path)
            peak_length_all = peak_treat(sample=ip_name, path=path)
            peak_length_all_dict[ip_name] = peak_length_all
    else:
        print ('No Replicate Samples!')
        return
    out = open(path + '/file/peak_overlap_length_fraction.txt', 'w')
    # peak_info = []
    INPUT_name = [i.strip().split('/')[-1] for i in INPUT]
    INPUT_name = ['.'.join(i.split('.')[:-1]) for i in INPUT_name]
    if len(IP) == 2:
        ip_name_1 = IP[0].strip().split('/')[-1]
        ip_name_2 = IP[1].strip().split('/')[-1]
        ip_name_1 = '.'.join(ip_name_1.split('.')[:-1])
        ip_name_2 = '.'.join(ip_name_2.split('.')[:-1])

        cmd = 'bedtools intersect -wo -a ' + path + '/tmp/' + ip_name_1 + '.treated.peak.bed -b ' + path + '/tmp/' + ip_name_2 + '.treated.peak.bed'
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        # overlap_length = 0
        overlap_length_dict = dict()
        for i in proc.stdout:
            tmp_list = i.decode().strip().split('\t')
            chrom, start, end = tmp_list[:3]
            Length = int(tmp_list[-1])
            key = chrom + '_' + start + '_' + end
            if key not in overlap_length_dict:
                overlap_length_dict[key] = Length
            elif key in overlap_length_dict:
                if Length > overlap_length_dict[key]:
                    overlap_length_dict[key] = Length
        overlap_length = sum(overlap_length_dict.values())
        overlap_length_dict = 0


            # chrom1, start1, end1, length1, chrom2, start2, end2, length2, overlap = i.decode().strip().split('\t')[:]
            # chrom1, start1, end1 = i.decode().strip().split('\t')[:]
            # overlap = int(i.decode().strip().split('\t')[-1])
            # # if int(overlap) <= int(length1):
            # # overlap = int(end1) - int(start1)
            # overlap_length += overlap
            # else:
            #     print(i)
        # for i in proc.stderr:
        #     print(i.decode())

        ratio_ip_1 = '{:.2%}'.format(float(overlap_length) / peak_length_all_dict[ip_name_1])
        ratio_ip_2 = '{:.2%}'.format(float(overlap_length) / peak_length_all_dict[ip_name_2])

        # if overlap_length >= peak_length_all_dict[ip_name_1]:
        #     overlap_length = peak_length_all_dict[ip_name_1]
        # peak_info.append(
        #     ['rep1', ip_name_1, INPUT_name[0], overlap_length, peak_length_all_dict[ip_name_1], ratio_ip_1])
        # peak_info.append(
        #     ['rep2', ip_name_2, INPUT_name[1], overlap_length, peak_length_all_dict[ip_name_2], ratio_ip_2])
        out.write('\t'.join(['rep1', ip_name_1, INPUT_name[0], str(overlap_length), str(peak_length_all_dict[ip_name_1]), str(ratio_ip_1)]))
        out.write('\n')
        out.write('\t'.join(['rep2', ip_name_2, INPUT_name[1], str(overlap_length), str(peak_length_all_dict[ip_name_2]), str(ratio_ip_2)]))
        out.write('\n')
        out.close()

    elif len(IP) == 3:
        ip_name_1 = IP[0].strip().split('/')[-1]
        ip_name_2 = IP[1].strip().split('/')[-1]
        ip_name_3 = IP[2].strip().split('/')[-1]

        ip_name_1 = '.'.join(ip_name_1.split('.')[:-1])
        ip_name_2 = '.'.join(ip_name_2.split('.')[:-1])
        ip_name_3 = '.'.join(ip_name_3.split('.')[:-1])
        ## samples 1 and 2
        cmd12 = 'bedtools intersect -wo -a ' + path + '/tmp/' + ip_name_1 + '.treated.peak.bed -b ' + path + '/tmp/' + ip_name_2 + '.treated.peak.bed'
        proc12 = Popen(cmd12, stdout=PIPE, stderr=PIPE, shell=True)

        # tmp_list = []
        # overlap_length_12 = 0
        overlap_length_dict = dict()
        for i in proc12.stdout:
            tmp_list = i.decode().strip().split('\t')
            chrom, start, end = tmp_list[:3]
            Length = int(tmp_list[-1])
            key = chrom + '_' + start + '_' + end
            if key not in overlap_length_dict:
                overlap_length_dict[key] = Length
            elif key in overlap_length_dict:
                if Length > overlap_length_dict[key]:
                    overlap_length_dict[key] = Length
        overlap_length_12 = sum(overlap_length_dict.values())
        ## release memory
        overlap_length_dict = 0
            # chrom1, start1, end1 = i.decode().strip().split('\t')[:]
            # overlap12 = int(i.decode().strip().split('\t')[-1])
            # overlap_length_12 += overlap12
            # if int(overlap) > 0 and int(overlap) <= int(length1):
            #     new_start = max([int(start1), int(start2)])
            #     new_end = min([int(end1), int(end2)])
            #     length = int(new_end)-int(new_start)
            # tmp_list.append([chrom1, start1, end1])
        # new_start_end_data = pd.DataFrame(data=np.array(tmp_list), columns=["chrom", "start", "end"])
        # tmp_list = 0
        # new_start_end_data.to_csv(path + '/tmp/tmp.peak.bed', sep='\t', encoding='utf-8', index=False,
        #                           header=False)
        # new_start_end_data = 0
        ratio_ip_12_1 = '{:.2%}'.format(float(overlap_length_12) / peak_length_all_dict[ip_name_1])
        ratio_ip_12_2 = '{:.2%}'.format(float(overlap_length_12) / peak_length_all_dict[ip_name_2])
        out.write('\t'.join(
            ['rep1', ip_name_1, INPUT_name[0], str(overlap_length_12), str(peak_length_all_dict[ip_name_1]), str(ratio_ip_12_1)]))
        out.write('\n')
        out.write('\t'.join(
            ['rep2', ip_name_2, INPUT_name[1], str(overlap_length_12), str(peak_length_all_dict[ip_name_2]), str(ratio_ip_12_2)]))
        out.write('\n')
        ## samples 1 and 3
        cmd13 = 'bedtools intersect -wo -a ' + path + '/tmp/' + ip_name_1 + '.treated.peak.bed -b ' + path + '/tmp/' + ip_name_3 + '.treated.peak.bed'
        proc13 = Popen(cmd13, stdout=PIPE, stderr=PIPE, shell=True)
        # overlap_length_13 = 0
        overlap_length_dict = dict()
        for i in proc13.stdout:
            tmp_list = i.decode().strip().split('\t')
            chrom, start, end = tmp_list[:3]
            Length = int(tmp_list[-1])
            key = chrom + '_' + start + '_' + end
            if key not in overlap_length_dict:
                overlap_length_dict[key] = Length
            elif key in overlap_length_dict:
                if Length > overlap_length_dict[key]:
                    overlap_length_dict[key] = Length
        overlap_length_13 = sum(overlap_length_dict.values())
        ## release memory
        overlap_length_dict = 0
            # overlap13 = int(i.decode().strip().split('\t')[-1])
            # overlap_length_13 += overlap13
        ratio_ip_13_1 = '{:.2%}'.format(float(overlap_length_13) / peak_length_all_dict[ip_name_1])
        ratio_ip_13_3 = '{:.2%}'.format(float(overlap_length_13) / peak_length_all_dict[ip_name_3])
        out.write('\t'.join(
            ['rep1', ip_name_1, INPUT_name[0], str(overlap_length_13), str(peak_length_all_dict[ip_name_1]), str(ratio_ip_13_1)]))
        out.write('\n')
        out.write('\t'.join(
            ['rep3', ip_name_3, INPUT_name[2], str(overlap_length_13), str(peak_length_all_dict[ip_name_3]), str(ratio_ip_13_3)]))
        out.write('\n')
        ## samples 2 and 3
        cmd23 = 'bedtools intersect -wo -a ' + path + '/tmp/' + ip_name_2 + '.treated.peak.bed -b ' + path + '/tmp/' + ip_name_3 + '.treated.peak.bed'
        proc23 = Popen(cmd23, stdout=PIPE, stderr=PIPE, shell=True)
        # overlap_length_23 = 0
        overlap_length_dict = dict()
        for i in proc23.stdout:
            tmp_list = i.decode().strip().split('\t')
            chrom, start, end = tmp_list[:3]
            Length = int(tmp_list[-1])
            key = chrom + '_' + start + '_' + end
            if key not in overlap_length_dict:
                overlap_length_dict[key] = Length
            elif key in overlap_length_dict:
                if Length > overlap_length_dict[key]:
                    overlap_length_dict[key] = Length
        overlap_length_23 = sum(overlap_length_dict.values())
        ## release memory
        overlap_length_dict = 0
            # overlap23 = int(i.decode().strip().split('\t')[-1])
            # overlap_length_23 += overlap23
        ratio_ip_23_2 = '{:.2%}'.format(float(overlap_length_23) / peak_length_all_dict[ip_name_2])
        ratio_ip_23_3 = '{:.2%}'.format(float(overlap_length_23) / peak_length_all_dict[ip_name_3])
        out.write('\t'.join(
            ['rep2', ip_name_2, INPUT_name[1], str(overlap_length_23), str(peak_length_all_dict[ip_name_2]), str(ratio_ip_23_2)]))
        out.write('\n')
        out.write('\t'.join(
            ['rep3', ip_name_3, INPUT_name[2], str(overlap_length_23), str(peak_length_all_dict[ip_name_3]), str(ratio_ip_23_3)]))
        out.write('\n')
        out.close()
    return


        # cmd2 = 'bedtools intersect -a ' + path + '/tmp/tmp.peak.bed -b ' + path + '/peak/' + ip_name_3 + '.treated.peak.bed'
        # proc2 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
        # overlap_length = 0
        # for i in proc2.stdout:
        #     chrom1, start1, end1 = i.decode().strip().split('\t')[:]
        #     overlap = int(end1) - int(start1)
        #     overlap_length += int(overlap)
        # for i in proc2.stderr:
        #     print(i.decode())

        # ratio_ip_1 = '{:.2%}'.format(float(overlap_length) / peak_length_all_dict[ip_name_1])
        # ratio_ip_2 = '{:.2%}'.format(float(overlap_length) / peak_length_all_dict[ip_name_2])
        # ratio_ip_3 = '{:.2%}'.format(float(overlap_length) / peak_length_all_dict[ip_name_3])
        # peak_info.append(
        #     ['rep1', ip_name_1, INPUT_name[0], overlap_length, peak_length_all_dict[ip_name_1], ratio_ip_1])
        # peak_info.append(
        #     ['rep2', ip_name_2, INPUT_name[1], overlap_length, peak_length_all_dict[ip_name_2], ratio_ip_2])
        # peak_info.append(
        #     ['rep3', ip_name_3, INPUT_name[2], overlap_length, peak_length_all_dict[ip_name_3], ratio_ip_3])

    # peak_info_data = pd.DataFrame(data=np.array(peak_info),
    #                               columns=["replicates", "sample_ip", "sample_input", "ovlerlapLength", "allPeakLength",
    #                                        "ratio"])
    # peak_info_data.to_csv(path + '/file/peak_overlap_length_fraction.txt', sep='\t', encoding='utf-8', index=False, header=False)

    # peak_info_data.ratio = [i.strip('%') for i in list(peak_info_data.ratio)]
    # peak_info_data.ratio = peak_info_data.ratio.apply(float)
    #
    # sample_number = len(peak_info_data.index)
    #
    # plt.figure(figsize=(18, 9), dpi=120)
    # # legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.barplot(x="replicates", y="ratio", data=peak_info_data, palette="Set3")
    # ax.set_xlabel("Sample Replicates", fontsize=16)
    # ax.set_ylabel("Peak Overlap Length Fraction (%)", fontsize=16)
    #
    # widthbars = [0.25] * sample_number
    # for bar, newwidth in zip(ax.patches, widthbars):
    #     x = bar.get_x()
    #     width = bar.get_width()
    #     centre = x + width / 2.
    #     bar.set_x(centre - newwidth / 2.)
    #     bar.set_width(newwidth)
    #
    # # plt.legend(loc='best')
    # plt.savefig(path + '/peakOverlapLength.png')
    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    # return








