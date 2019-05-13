# import matplotlib
# matplotlib.use('agg')

# from matplotlib import pyplot as plt
import numpy as np
# import seaborn as sns
# from time import time, sleep
#import pylab
import pandas as pd
import os
import sys
from collections import Counter



def metagene(sample = None, mrna_file = None, path = None):

    sample_name = sample.strip().split('/')[-1]
    sample_name = '.'.join(sample_name.split('.')[:-1])
    peak_file = path + '/peak/' + sample_name + '_peak.xls'
    #peak_file = path + '/' + sample + '.bed'
    #print peak_file
    if os.path.exists(peak_file):
        fh_peak = open(peak_file)
    else:
        sys.exit('<metagene> ' + path + '/peak/' + sample_name + '_peak.xls No exists!')
    fh_tx = open(mrna_file)
    # peak annotation
    peak_dict=dict()
    fh_peak.readline()
    #print first_line
    for i in fh_peak:
        tmp_list=i.strip().split('\t')
        #chrom, peak_start, peak_end, gene_name = tmp_list[:4]
        # chrom, start, end, length, tx, geneID, pvalue, foldEnrichment, fdr = tmp_list[:]
        # chrom, start, end, length, tx, geneID, pvalue, foldEnrichment, fdr = tmp_list[:]

        chrom, chromStart, chromEnd, geneID, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes, \
        blockStarts, start, end, length, tx, pvalue, foldEnrichment, fdr = tmp_list[:]

        #print peak_start, peak_end
        #tmp_list1=[]

        ###############################################
        ### peak start maybe be '61451322,61452532,61452858,61453108,61453462'
        ### fix a bug
        ###############################################
        peak_start = [int(i) for i in start.split(',')]
        peak_end = [int(i) for i in end.split(',')]
        start_end = list(zip(peak_start, peak_end))

        if chrom+'_'+tx not in peak_dict:
            peak_dict[chrom+'_'+tx] = start_end
            #print peak_dict[chrom+'_'+gene_name]
        elif chrom+'_'+tx in peak_dict:
            peak_dict[chrom + '_' + tx].extend(start_end)
    # print peak_dict
    # print peak_dict['chr20_RBCK1']
    #-----------------------------------------------------------------
    rel_pos_list=[]
    fh_tx.readline()
    for i in fh_tx:
        tmp_list = i.strip().split()
        #print tmp_list
        #sleep(1)
        (chrom, gene_name, tx, strand, fiveUTRstarts, fiveUTRends, CDSstarts, CDSends, threeUTRstarts, threeUTRends, fiveUTRlength,
         CDSlength, threeUTRlength) = tmp_list[:]
        fiveUTRlength=int(fiveUTRlength)
        CDSlength=int(CDSlength)
        threeUTRlength = int(threeUTRlength)
        #print 'The 5UTR length is: ', fiveUTRlength
        if chrom+'_'+tx in peak_dict:
            fiveUTRstarts_list = fiveUTRstarts.split(',')
            CDSstarts_list = CDSstarts.split(',')
            threeUTRstarts_list = threeUTRstarts.split(',')
            fiveUTR_interval = []
            CDS_interval = []
            threeUTR_interval =[]
            for j in range(len(fiveUTRstarts_list)):
                fiveUTR_interval.append((fiveUTRstarts_list[j], fiveUTRends.split(',')[j]))
            for k in range(len(CDSstarts_list)):
                CDS_interval.append((CDSstarts_list[k], CDSends.split(',')[k]))
            for m in range(len(threeUTRstarts_list)):
                threeUTR_interval.append((threeUTRstarts_list[m], threeUTRends.split(',')[m]))

            for item in peak_dict[chrom+'_'+tx]:
                #print item
                #####################################################
                ## each_peak is a tuple, the element is start and end
                ## fix a bug
                #####################################################
                #mrna_pos = 0
                if strand == '+':
                    # print item
                    # sleep(1)

                    cds_pos = 0
                    utr5_pos = 0
                    utr3_pos = 0
                    for i in fiveUTR_interval:
                        for coord in range(int(i[0])+1, int(i[1])+1):
                            #mrna_pos += 1
                            utr5_pos += 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = utr5_pos / float(fiveUTRlength)
                                rel_pos_list.append(rel_pos)
                    for j in CDS_interval:
                        for coord in range(int(j[0])+1, int(j[1])+1):
                            cds_pos += 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = cds_pos / float(CDSlength)
                                rel_pos += 1
                                #print rel_pos
                                rel_pos_list.append(rel_pos)
                    for k in threeUTR_interval:
                        for coord in range(int(k[0])+1, int(k[1])+1):
                            utr3_pos += 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = utr3_pos / float(threeUTRlength)
                                rel_pos += 2
                                #print rel_pos
                                rel_pos_list.append(rel_pos)
                elif strand == '-':
                    cds_pos = CDSlength
                    utr5_pos = fiveUTRlength
                    utr3_pos = threeUTRlength

                    for i in fiveUTR_interval:
                        # print i
                        # sleep(1)

                        for coord in range(int(i[0]) + 1, int(i[1]) + 1):
                            # mrna_pos += 1
                            utr5_pos -= 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = utr5_pos / float(fiveUTRlength)
                                rel_pos_list.append(rel_pos)
                    for j in CDS_interval:
                        for coord in range(int(j[0]) + 1, int(j[1]) + 1):
                            cds_pos -= 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = cds_pos / float(CDSlength)
                                rel_pos += 1
                                # print rel_pos
                                rel_pos_list.append(rel_pos)
                    for k in threeUTR_interval:
                        for coord in range(int(k[0]) + 1, int(k[1]) + 1):
                            utr3_pos -= 1
                            if coord > item[0] and coord <= item[1]:
                                rel_pos = utr3_pos / float(threeUTRlength)
                                rel_pos += 2
                                # print rel_pos
                                rel_pos_list.append(rel_pos)


    # rel_pos_list_data = pd.DataFrame(data=np.array(rel_pos_list), columns=["relPos"])
    # # rel_pos_list_data = rel_pos_list_data.astype()
    # # #peak_data = pd.DataFrame(data=np.array(Peak_List), columns=["chr", "start", "end", "geneID", "txID"])
    # rel_pos_list_data.to_csv(path + '/file/' + sample_name + '.rel_pos.txt', sep='\t', encoding='utf-8', index=False, header=False)

    return rel_pos_list

def multiple_metagene(samples = None, mrna_file = None, path = None):

    # samples = {'ip': [('W5_S26.bam', 'W7_S28.bam'), ('W6_S27.bam', 'W8_S24.bam')],
    #            'input': [('W1_S21.bam', 'W3_S25.bam'), ('W2_S22.bam', 'W4_S23.bam')]}
    # start_time = time()
    # print('MetaQC is plotting metagene...')

    metagene_dict=dict()
    for i in samples['ip']:
        # print(samples)
        replicate_num = 0
        for sample in i:
            #print sample
            replicate_num += 1
            sample_name = sample.strip().split('/')[-1]
            sample_name = '.'.join(sample_name.split('.')[:-1])
            peak_base_list = metagene(sample=sample, mrna_file=mrna_file, path=path)
            if len(peak_base_list) > 0:
                metagene_dict['rep'+str(replicate_num)] = peak_base_list
            else:
                print()
                print('Rep'+str(replicate_num) + 'samples cannot produce metagene plot!')
                print()

    # replicate_num = 0
    # plt.figure(figsize=(18, 9), dpi=120)
    # plt.figure(figsize=(7.06, 3.58), dpi=720)
    if len(metagene_dict) > 0:
        out = open(path + '/file/metagenePlot.txt', 'w')
        for key in metagene_dict:
            # replicate_num += 1
            l1 = []
            for i in metagene_dict[key]:
                j = float(format(float(i), '.2f'))
                l1.append(j)
            l1.sort()
            # print(len(l1))
            d1 = Counter(l1)
            ## test start
            # print(d1)
            # print(d1.values())
            ## test end
            max_values = max(d1.values())
            # print(max_values)
            l2 = [i / 100 for i in list(range(301))]
            for k in l2:
                if k in d1:
                    fraction = d1[k] / max_values
                    value_divided_by_max = float(format(fraction, '.3f'))
                    out.write('\t'.join([str(k), str(d1[k]), str(value_divided_by_max), key]))
                    out.write('\n')
                elif k not in d1:
                    out.write('\t'.join([str(k), '0', '0', key]))
                    out.write('\n')
        out.close()



    #     x = np.array(metagene_dict[key])
    #     ax = sns.kdeplot(x, label= 'rep'+str(replicate_num))
    #
    # ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    # ax.set_xticklabels(["", "5'UTR", "start codon", "CDS", "stop codon", "3'UTR", ""])
    # #plt.title('Metagene')
    # #plt.xlabel('categories')
    # # Hide grid lines
    # ax.grid(False)
    # plt.ylabel('Peak density', fontsize = 12)
    #
    # plt.xticks(fontsize=10)
    # plt.yticks(fontsize=10)
    #
    # plt.xlim(0, 3)
    # #plt.ylim(0, 1)
    #
    # plt.axvline(x=1.0, linestyle='--')
    # plt.axvline(x=2.0, linestyle='--')
    # plt.legend()
    # #plt.show()
    #
    # plt.savefig(path + '/img/metagene.png')

    IP = []
    INPUT = []

    for i in samples['ip']:
        for j in i:
            IP.append(j)
    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    IP_INPUT = list(zip(IP, INPUT))

    metagene_info = []
    replicate_number = 0
    for each in IP_INPUT:
        replicate_number += 1
        ip_name = each[0].strip().split('/')[-1]
        input_name = each[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])
        metagene_info.append(['rep' + str(replicate_number), ip_name, input_name, ip_name + '_peak.bed'])

    metagene_data = pd.DataFrame(data=np.array(metagene_info), columns=["replicates", "sampleIP", "sampleINPUT", "peakFileName"])
    metagene_data.to_csv(path + '/file/metageneInfo.txt', sep='\t', encoding='utf-8', index=False, header=False)


    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    return












