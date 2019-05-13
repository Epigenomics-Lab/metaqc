# import argparse
# import matplotlib
# matplotlib.use('agg')
import os
import sys
from subprocess import Popen, PIPE
# from multiprocessing.dummy import Pool as ThreadPool
from time import time, sleep
import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns

'''
-Reads which map to genome overlap with corresponding tRNA & rRNA coordinate
'''


def test(sample=None, rRNA_tRNA_bed=None, path=None):
    # calculate mapped reads count
    # sample_name = sample.strip().split('/')[-1]
    sample_bed = path + '/tmp/' + sample + '_sorted.bed'
    column_types = {'chr':'category', 'start':'int32', 'end':'int32', 'mapq':'int16', 'strand':'category'}
    data = pd.read_csv(sample_bed, sep='\t', names=['chr', 'start', 'end', 'qname', 'mapq', 'strand'],
                       dtype=column_types)
    mappedReadCounts = len(set(data.qname))
    data = 0  # release memory

    # calculate Reads count which map to genome overlap with corresponding tRNA & rRNA coordinate
    target = 'bedtools intersect -wo -sorted -b ' + sample_bed + ' -a ' + rRNA_tRNA_bed
    proc = Popen(target, stdout=PIPE, stderr=PIPE, shell=True)

    qname = []
    for i in proc.stdout:
        tmp_list = i.decode().strip().split('\t')
        qname.append([tmp_list[-4], tmp_list[3]])

    overlap = pd.DataFrame(data=np.array(qname), columns=["qname", "type"])
    overlap = overlap.astype({'type':'category'})
    overlap_tRNA = overlap.loc[overlap.type == 'tRNA']
    overlap_rRNA = overlap.loc[overlap.type == 'rRNA']

    tRNAmappedReadCounts = len(set(overlap_tRNA.qname))
    # print tRNAmappedReadCounts
    rRNAmappedReadCounts = len(set(overlap_rRNA.qname))
    # print rRNAmappedReadCounts


    ratio = '{:.2%}'.format(float(rRNAmappedReadCounts + tRNAmappedReadCounts) / mappedReadCounts)
    return [rRNAmappedReadCounts, tRNAmappedReadCounts, mappedReadCounts, ratio]


def contamination(samples=None, bed=None, path=None):
    # start_time = time()
    # print('MetaQC is calculating library contamination ratio...')
    sleep(5) ## wait for tmp directory

    IP = []
    INPUT = []

    for i in samples['ip']:
        for j in i:
            IP.append(j)
    for i in samples['input']:
        for j in i:
            INPUT.append(j)

    IP_INPUT = list(zip(IP, INPUT))

    contamination_dict = dict()

    for item in IP_INPUT:
        ip_name = item[0].strip().split('/')[-1]
        input_name = item[1].strip().split('/')[-1]
        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])
        if os.path.exists(item[0]):
            cmd1 = 'bamToBed -i ' + item[0] + ' > ' + path + '/tmp/' + ip_name + '.bed'
            proc1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
            for i in proc1.stderr:
                print(i.decode())
            command1 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + ip_name + '.bed > ' + path + '/tmp/' + ip_name + '_sorted.bed'
            os.system(command1)
        else:
            sys.exit('<contamination> ' + item[0] + 'not exists!')

        if os.path.exists(item[1]):
            cmd2 = 'bamToBed -i ' + item[1] + ' > ' + path + '/tmp/' + input_name + '.bed'
            proc2 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
            for j in proc2.stderr:
                print(j.decode())

            command2 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + input_name + '.bed > ' + path + '/tmp/' + input_name + '_sorted.bed'
            os.system(command2)
        else:
            sys.exit('<contamination> ' + item[1] + 'not exists!')

        if os.path.exists(path + '/tmp/' + ip_name + '_sorted.bed'):
            contamination_IP = test(sample=ip_name, rRNA_tRNA_bed=bed, path=path)
        else:
            sys.exit('<contamination> ' + path + '/tmp/' + ip_name + '_sorted.bed No exists!')

        if os.path.exists(path + '/tmp/' + input_name + '_sorted.bed'):
            contamination_INPUT = test(sample=input_name, rRNA_tRNA_bed=bed, path=path)
        else:
            sys.exit('<contamination> ' + path + '/tmp/' + input_name + '_sorted.bed No exists!')
        contamination_dict[ip_name] = contamination_IP
        contamination_dict[input_name] = contamination_INPUT

    replicate_num = 0
    contamination_info = []
    for each in IP_INPUT:
        replicate_num += 1
        ip_name = each[0].strip().split('/')[-1]
        input_name = each[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        contamination_IP_list = contamination_dict[ip_name]
        contamination_INPUT_list = contamination_dict[input_name]

        contamination_info.append(
            ['rep' + str(replicate_num), ip_name, 'IP', contamination_IP_list[0], contamination_IP_list[1],
             contamination_IP_list[2], contamination_IP_list[3]])
        contamination_info.append(
            ['rep' + str(replicate_num), input_name, 'INPUT', contamination_INPUT_list[0], contamination_INPUT_list[1],
             contamination_INPUT_list[2], contamination_INPUT_list[3]])

    contamination_data = pd.DataFrame(data=np.array(contamination_info),
                                      columns=["replicates", "samples", "type", "rRNAmappedReadCounts",
                                               "tRNAmappedReadCounts", "mappedReadCounts", "ratio"])

    # save info to file for database
    contamination_data.to_csv(path + '/file/contamination.txt', sep='\t', encoding='utf-8', index=False, header=False)


    # contamination_data.ratio = [i.strip('%') for i in list(contamination_data.ratio)]
    # contamination_data.ratio = contamination_data.ratio.apply(float)
    #
    # sample_number = len(contamination_data.index)
    #
    # ## contamination rate
    # plt.figure(figsize=(18, 9), dpi=120)
    # # legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.barplot(x="replicates", y="ratio", hue="type", data=contamination_data, palette="Set1")
    # ax.set_xlabel("Sample Replicates", fontsize=16)
    # ax.set_ylabel("Contamination Ratio (%)", fontsize=16)
    #
    # widthbars = [0.25] * sample_number
    # for bar, newwidth in zip(ax.patches, widthbars):
    #     x = bar.get_x()
    #     width = bar.get_width()
    #     centre = x + width / 2.
    #     bar.set_x(centre - newwidth / 2.)
    #     bar.set_width(newwidth)
    #
    # plt.legend(loc='best')
    # plt.savefig(path + '/contamination.png')

    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)
    return



