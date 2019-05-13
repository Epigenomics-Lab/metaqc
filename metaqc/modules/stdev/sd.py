# import matplotlib
# matplotlib.use('agg')

import numpy as np
import pandas as pd
# from time import time, sleep
from statistics import *
# from matplotlib import pyplot as plt
# import seaborn as sns
#from multiprocessing.dummy import Pool as ThreadPool
import os
import sys

###########
## Rely on callpeakNew readCounts function
##########

def stdev_value(sample = None, path = None):

    sample_name = sample.strip().split('/')[-1]
    sample_name = '.'.join(sample_name.split('.')[:-1])

    # start_time = time()
    # file1 = '/media/chaigs/softwares/data/hoper_test_04272234/tmp/847372.bam.readCounts.bed'
    # file2 = '/media/chaigs/softwares/data/hoper_test_05022156/tmp/W6_S27_chr20_new.bam.readCounts.bed'


    readCounts_IP_dict = dict()
    readCounts_INPUT_dict = dict()

    if os.path.exists(path + '/tmp/' + sample_name + '.readCounts.bed'):
        fh = open(path + '/tmp/' + sample_name + '.readCounts.bed')
    else:
        #print('Error: ' + path + '/tmp/' + sample_name + '.readCounts.bed not exists!')
        sys.exit('<stdev> ' + path + '/tmp/' + sample_name + '.readCounts.bed No exists!')
    for i in fh:
        # print (i)
        # sleep(1)
        chrom, start, end, length, geneID, txID, strand, readCountsIP, readCountsINPUT = i.strip().split('\t')[:]
        #print (geneID)
        if txID not in readCounts_IP_dict:

            readCounts_IP_dict[txID] = [int(readCountsIP)]
            readCounts_INPUT_dict[txID] = [int(readCountsINPUT)]
        elif txID in readCounts_IP_dict:
            readCounts_IP_dict[txID].append(int(readCountsIP))
            readCounts_INPUT_dict[txID].append(int(readCountsINPUT))

    # print (len(readCounts_IP_dict))
    # print (len(readCounts_INPUT_dict))
    # print (readCounts_IP_dict['SNAI1'])
    # print (len(readCounts_IP_dict['SNAI1']))
    IP_readCounts_stdev = [stdev(value) for key, value in readCounts_IP_dict.items() if len(value) > 1]
    INPUT_readCounts_stdev = [stdev(value) for key, value in readCounts_INPUT_dict.items() if len(value) > 1]
    # print (len(IP_readCounts_stdev))
    # print (len(INPUT_readCounts_stdev))

    # remove 0 value
    # float(format(k, '.2f'))
    IP_readCounts_stdev_remove_0 = [float(format(k, '.2f')) for k in IP_readCounts_stdev if k != 0]
    INPUT_readCounts_stdev_remove_0 = [float(format(k, '.2f')) for k in INPUT_readCounts_stdev if k != 0]
    #a = [x for x in a if x != 20]

    # stdev_median_ip = median(IP_readCounts_stdev)
    # stdev_median_input = median(INPUT_readCounts_stdev)
    # print ('**'*20)
    # print (stdev_median_ip)
    # print (stdev_median_input)
    # print ('**'*20)
    # return IP_readCounts_stdev, INPUT_readCounts_stdev
    return IP_readCounts_stdev_remove_0, INPUT_readCounts_stdev_remove_0



def sd(sample = None, path = None):

    # samples = {'ip': [('W5_S26.bam', 'W7_S28.bam'), ('W6_S27.bam', 'W8_S24.bam')],
    #            'input': [('W1_S21.bam', 'W3_S25.bam'), ('W2_S22.bam', 'W4_S23.bam')]}
    # start_time = time()
    # print ("MetaQC is calculating read distribution dispersion...")
    IP = []
    INPUT = []
    for i in sample['ip']:
        for j in i:
            IP.append(j)

    for i in sample['input']:
        for j in i:
            INPUT.append(j)

    IP_INPUT = list(zip(IP, INPUT))
    read_counts_stdev_dict = dict()


    for item in IP_INPUT:
        ip_name = item[0].strip().split('/')[-1]
        input_name = item[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        IP_readCounts_stdev, INPUT_readCounts_stdev = stdev_value(sample=item[0], path=path)

        read_counts_stdev_dict[ip_name] = IP_readCounts_stdev
        read_counts_stdev_dict[input_name] = INPUT_readCounts_stdev

    # stdev_info = []
    #readCountsVaList = []
    replicate_num = 0
    # tx_readCounts_stdev = []

    out1 = open(path + '/file/stdevPlot.txt', 'w')
    out2 = open(path + '/file/stdevInfo.txt', 'w')

    for each in IP_INPUT:
        replicate_num += 1
        ip_name = each[0].strip().split('/')[-1]
        input_name = each[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        # stdev_median_ip = median(read_counts_stdev_dict[ip_name])
        # stdev_median_ip = '{:.4f}'.format(stdev_median_ip)
        stdev_median_ip = float(format(np.median(read_counts_stdev_dict[ip_name]), '.2f'))
        stdev_median_input = float(format(np.median(read_counts_stdev_dict[input_name]), '.2f'))
        # stdev_median_input = median(read_counts_stdev_dict[input_name])
        # stdev_median_input = '{:.4f}'.format(stdev_median_input)
        upper_quartile_ip = float(format(np.percentile(read_counts_stdev_dict[ip_name], 75), '.2f'))
        upper_quartile_input = float(format(np.percentile(read_counts_stdev_dict[input_name], 75), '.2f'))

        lower_quartile_ip = float(format(np.percentile(read_counts_stdev_dict[ip_name], 25), '.2f'))
        lower_quartile_input = float(format(np.percentile(read_counts_stdev_dict[input_name], 25), '.2f'))

        iqr_ip = upper_quartile_ip - lower_quartile_ip
        iqr_input = upper_quartile_input - lower_quartile_input

        upper_whisker_ip = float(format(upper_quartile_ip + 1.5 * iqr_ip, '.2f'))
        upper_whisker_input = float(format(upper_quartile_input + 1.5 * iqr_input, '.2f'))

        lower_whisker_ip = float(format(lower_quartile_ip - 1.5 * iqr_ip, '.2f'))
        if lower_whisker_ip < 0:
            lower_whisker_ip = 0

        lower_whisker_input = float(format(lower_quartile_input - 1.5 * iqr_input, '.2f'))
        if lower_whisker_input < 0:
            lower_whisker_input = 0
        values_ip = [['rep' + str(replicate_num), 'IP', 'lower_whisker', str(lower_whisker_ip)],
                      ['rep' + str(replicate_num), 'IP', 'lower_quartile', str(lower_quartile_ip)],
                      ['rep' + str(replicate_num), 'IP', 'median_value', str(stdev_median_ip)],
                      ['rep' + str(replicate_num), 'IP', 'upper_quartile', str(upper_quartile_ip)],
                      ['rep' + str(replicate_num), 'IP', 'upper_whisker', str(upper_whisker_ip)]
                      ]
        values_input = [['rep' + str(replicate_num), 'INPUT', 'lower_whisker', str(lower_whisker_input)],
                      ['rep' + str(replicate_num), 'INPUT', 'lower_quartile', str(lower_quartile_input)],
                      ['rep' + str(replicate_num), 'INPUT', 'median_value', str(stdev_median_input)],
                      ['rep' + str(replicate_num), 'INPUT', 'upper_quartile', str(upper_quartile_input)],
                      ['rep' + str(replicate_num), 'INPUT', 'upper_whisker', str(upper_whisker_input)]
                      ]
        for i in values_ip:
            s1 = '\t'.join(i)
            out1.write(s1)
            out1.write('\n')
        for j in values_input:
            s2 = '\t'.join(j)
            out1.write(s2)
            out1.write('\n')



        out2.write('\t'.join(['rep' + str(replicate_num), ip_name, input_name, str(stdev_median_ip), str(stdev_median_input)]))
        out2.write('\n')
    out1.close()
    out2.close()


    #     for i in range(len(read_counts_stdev_dict[ip_name])):
    #
    #         tx_readCounts_stdev.append(['rep' + str(replicate_num), 'IP', read_counts_stdev_dict[ip_name][i]])
    #         tx_readCounts_stdev.append(['rep' + str(replicate_num), 'INPUT', read_counts_stdev_dict[input_name][i]])
    #
    # tx_stdev_data = pd.DataFrame(data=np.array(tx_readCounts_stdev),
    #                            columns=["replicates", "type", "stdev"])
    #
    # tx_stdev_data.to_csv(path + '/file/stdev.txt', sep='\t', encoding='utf-8', index=False, header=False)

    ## save table info to file
    # stdev_info_data = pd.DataFrame(data=np.array(stdev_info), columns=["replicates", "sampleIP", "sampleINPUT", "medianIP", "medianINPUT"])
    # stdev_info_data.to_csv(path + '/file/stdevInfo.txt', sep='\t', encoding='utf-8', index=False, header=False)


    #print (len(tx_stdev_data.index))
    #print (gene_stdev_data.dtypes)

    # tx_stdev_data.stdev = tx_stdev_data.stdev.apply(float)

    # print (tx_stdev_data.dtypes)
    #
    # print (stdev_info)

    # print('Done! Time taken: {:.4f} min'.format((time() - start_time)/60.0))
    # print('#####' * 20)

    # plt.figure(figsize=(18, 9), dpi=120)
    # plt.figure(figsize=(18, 9), dpi=720)
    # plt.figure(figsize=(7.06, 3.58), dpi=720)
    # # plt.figure(figsize=(7.06, 3.58), dpi=360)
    # #legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.boxplot(x="replicates", y="stdev", hue="type", data=tx_stdev_data, palette="Set3", showfliers=False,  width=.45)
    #
    # ax.set_xlabel("")
    # ax.set_ylabel("Standard Deviation", fontsize=12)
    # #plt.legend(legend)
    # ## this sentence is important for hiding legend title
    # plt.xticks(fontsize=12)
    # plt.yticks(fontsize=10)
    #
    # plt.grid(False)
    # plt.legend(loc='best')
    #
    #
    # #plt.show()
    # plt.savefig(path + '/img/stdev.png')
    return




