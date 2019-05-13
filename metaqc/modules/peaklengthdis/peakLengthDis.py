# import matplotlib
# matplotlib.use('agg')
#
# from matplotlib import pyplot as plt
# import numpy as np
# # from time import sleep, time
# import pandas as pd
import os
import sys
from collections import Counter




def length_dis(sample=None, path=None):
    # bed = path + '/peak/' + sample + '.peak.bed'
    bed = path + '/peak/' + sample + '_peak.xls'

    if os.path.exists(bed):
        fh = open(bed)
    else:
        sys.exit('<peakLengthDis> ' + bed + 'No exists!')

    fh.readline()
    length_list = []
    for i in fh:
        length_list.append(int(i.strip().split('\t')[-5]))

    # length_dict = dict()
    # for length in length_list:
    #     if length not in length_dict:
    #         length_dict[length] = 1
    #
    #     elif length in length_dict:
    #         length_dict[length] += 1
    #
    # peakLength_list = []
    # counts = []
    #
    # for key, value in length_dict.items():
    #     peakLength_list .append(key)
    #     counts.append(value)
    #
    # counts.sort()
    # #print (counts)
    # maxLengthCounts = counts[-1]
    #
    # peakLength = [str(key) for key, value in length_dict.items() if value == maxLengthCounts]
    # peak_length = ','.join(peakLength)
    peak_counts = len(length_list)

    # print (length_list)
    return length_list, peak_counts

def peak_length_dis(samples=None, path=None):
    # start_time = time()
    # print('MetaQC is calculating peak length distribution...')

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
    # peak_length_list = []
    # legend_labels=[]
    # peak_info = []
    out_info = open(path + '/file/peakLengthInfo.txt', 'w')
    out_plot = open(path + '/file/peakLength.txt', 'w')

    for item in IP_INPUT:
        replicate_num += 1

        ip_name = item[0].strip().split('/')[-1]
        input_name = item[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        length_list, peak_counts = length_dis(sample=ip_name, path=path)
        out_info.write('\t'.join(['rep'+str(replicate_num), ip_name, input_name, str(peak_counts)]))
        out_info.write('\n')

        length_list.sort()
        d1 = Counter(length_list)
        for key in d1:
            out_plot.write('\t'.join([str(key), str(d1[key]), 'rep' + str(replicate_num)]))
            out_plot.write('\n')
    out_info.close()
    out_plot.close()

    #     peak_length_list.append(np.array(length_list))
    #     # legend_labels.append(ip_name)
    #     legend_labels.append('rep'+str(replicate_num))
    # ## save table info
    # peak_data = pd.DataFrame(data=np.array(peak_info), columns=["replicates", "sampleIP", "sampleINPUT", "peakFileName",
    #                                                             "PeakLength", "PeakCounts"])
    # peak_data.to_csv(path + '/file/peakLengthInfo.txt', sep='\t', encoding='utf-8', index=False, header=False)
    #
    # # plt.figure(figsize=(18, 9), dpi=120)
    # # plt.figure(figsize=(18, 9), dpi=720)
    # # plt.figure(figsize=(7.06, 3.58), dpi=720)
    # plt.figure(figsize=(7.06, 4), dpi=720)
    # # plt.hist(peak_length_list, bins=120, label=legend_labels)
    # plt.hist(peak_length_list, bins= 60, label=legend_labels)
    #
    # plt.xticks(fontsize=10)
    # plt.yticks(fontsize=10)
    #
    # plt.xlabel('Peak Length (bp)', fontsize=12)
    # plt.ylabel('Peak Counts', fontsize=12)
    #
    # # plt.axes(grid = False)
    # plt.grid(False)
    # plt.legend()
    # plt.savefig(path + '/img/peakLengthDis.png')

    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    return