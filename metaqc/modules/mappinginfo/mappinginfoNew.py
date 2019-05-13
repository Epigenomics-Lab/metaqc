# import matplotlib
# matplotlib.use('agg')

from subprocess import Popen, PIPE
import numpy as np
import pandas as pd
# from time import time, sleep
import os
import sys
# from matplotlib import pyplot as plt
# import seaborn as sns

def check_integrity(bamfile=None):
    if os.path.exists(bamfile):
        cmd = 'samtools quickcheck -v ' + bamfile
        fh = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        s1 = fh.stdout.read()
        if s1:
            print('<mappingInfo> Samtools quickcheck detects incomplete files:')
            print(s1)
            sys.exit("Please make sure your bam file(s) is (are) complete!")
        else:
            print('Samtools quickcheck detects that ' + bamfile + ' is complete!')
    else:
        sys.exit('<mappingInfo> ' + bamfile + 'not exists!')
    #print('Samtools quickcheck detects that all the bam files are complete!')


# start_time = time()
def test(bamfile=None, path=None, seq_type=None):
    # file = 'W1_S21.bam'

    ## get total read counts

    cmd1 = 'samtools view -@ 4 ' + bamfile
    fh1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
    TotalReads = set()
    for i in fh1.stdout:
        qname = i.decode().split('\t')[0]
        TotalReads.add(qname)

    if seq_type == 'SE':
        TotalReadCounts = len(TotalReads)
    # print TotalReadCounts
    elif seq_type == 'PE':
        TotalReadCounts = len(TotalReads) * 2
    TotalReads = 0


    ## convert bam file into bed file
    bam_filename = bamfile.strip().split('/')[-1]
    bam_filename = '.'.join(bam_filename.split('.')[:-1])
    #cmd2 = 'bamToBed -i ' + bamfile + ' > ' + path + '/' + bam_filename + '.bed'
    cmd2 = 'samtools view -@ 4 -q 30 -b ' + bamfile + ' | bamToBed -i - | cut -f 1,2,3,4 > ' + path + '/' + bam_filename + '_q30.bed'
    fh = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
    ## print errors
    for i in fh.stderr:
        print (i.decode())
    # import dataframe
    if os.path.exists(path + '/' + bam_filename + '_q30.bed'):
        ## Reduce memory consumption
        ## The unique qname is more than half, so no type is specified, using default object data type
        column_types = {'chr':"category", 'start':'int32', 'end':'int32'}
        data = pd.read_csv(path + '/' + bam_filename + '_q30.bed', sep='\t',
                           names=['chr', 'start', 'end', 'qname'],
                           dtype=column_types)
    else:
        sys.exit('<mappingInfo> ' + path + '/' + bam_filename + '_q30.bed not exists!')

    # data = data[['chr', 'start', 'end']]
    # print len(data.index)
    # print data.dtypes
    # print len(set(data.qname))

    # uniquelyMappedReadCounts
    # a = data.loc[data.mapq >= 30]
    UniquelyMappedReadCounts = len(data.index)

    # UniquelyMappedReadCounts = len(set(a.qname))
    # print UniquelyMappedReadCounts
    # print len(set(a.qname))
    # data = ''  # release memory

    # UniquelyMappedLocationCount
    b = data.drop_duplicates(subset=['chr', 'start', 'end'], keep='first')
    UniquelyMappedLocationCounts = len(b.index)
    b = 0
    # UniquelyMappedLocationCounts = len(set(b.qname))
    # print UniquelyMappedLocationCounts
    # print len(set(b.qname))

    # one location one read
    c = data.drop_duplicates(subset=['chr', 'start', 'end'], keep=False)
    OneReadMappedLocationCounts = len(c.index)
    c = 0
    data = 0 ## release memory
    # OneReadMappedLocationCounts = len(set(c.qname))
    # print OneReadMappedLocationCounts
    # a = ''  # release memory
    # b = ''
    # c = ''
    NRF = '{:.2%}'.format(float(UniquelyMappedLocationCounts) / UniquelyMappedReadCounts)
    PBC = '{:.4f}'.format(float(OneReadMappedLocationCounts) / UniquelyMappedLocationCounts)
    uniMappingRatio = '{:.2%}'.format(float(UniquelyMappedReadCounts) / TotalReadCounts)

    # print 'NRF: ', NRF
    # print 'PBC: ', PBC
    # print 'uniquelyMappingRatio: ', uniMappingRatio
    uniquelyMappedRatioList = [UniquelyMappedReadCounts, TotalReadCounts, uniMappingRatio]
    NRFlist = [UniquelyMappedLocationCounts, UniquelyMappedReadCounts, NRF]
    PBClist = [OneReadMappedLocationCounts, UniquelyMappedLocationCounts, PBC]
    # return [bam_filename, UniquelyMappedReadCounts, UniquelyMappedLocationCounts, OneReadMappedLocationCounts, TotalReadCounts,
    #         uniMappingRatio, NRF, PBC]
    return uniquelyMappedRatioList, NRFlist, PBClist


def mappingInfo(samples=None, path=None, seq_type=None):
    # samples={'ip': [('W5_S26.bam', 'W7_S28.bam'), ('W6_S27.bam', 'W8_S24.bam')],
    #  'input': [('W1_S21.bam', 'W3_S25.bam'), ('W2_S22.bam', 'W4_S23.bam')]}

    # start_time = time()
    # print('MetaQC is calculating uniquely mapping ratio, NRF and PBC values')

    # create a tmp directory
    os.mkdir(path + '/tmp')
    ## save result files
    os.mkdir(path + '/file')
    ## save css file
    os.mkdir(path + '/css')
    ## save js file
    os.mkdir(path + '/js')
    ## save image file
    # os.mkdir(path + '/img')

    path1 = path + '/tmp'

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

    for each in IP_INPUT:
        check_integrity(bamfile=each[0])
        check_integrity(bamfile=each[1])

    uniquelyMappedRatio_dict = dict()
    NRFlist_dict = dict()
    PBClist_dict = dict()

    for item in IP_INPUT:
        ip_name = item[0].strip().split('/')[-1]
        input_name = item[1].strip().split('/')[-1]

        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = '.'.join(input_name.split('.')[:-1])

        uniquelyMappedRatioList_IP, NRFlist_IP, PBClist_IP = test(bamfile=item[0], path=path1, seq_type=seq_type)
        uniquelyMappedRatioList_INPUT, NRFlist_INPUT, PBClist_INPUT = test(bamfile=item[1], path=path1, seq_type=seq_type)

        uniquelyMappedRatio_dict[ip_name] = uniquelyMappedRatioList_IP
        uniquelyMappedRatio_dict[input_name] = uniquelyMappedRatioList_INPUT

        NRFlist_dict[ip_name] = NRFlist_IP
        NRFlist_dict[input_name] = NRFlist_INPUT

        PBClist_dict[ip_name] = PBClist_IP
        PBClist_dict[input_name] = PBClist_INPUT

    uniquelyMappedRatio_info = []
    NRFlist_info = []
    PBClist_info = []
    replicate_num = 0

    for each in IP_INPUT:
        replicate_num += 1
        ip_name = each[0].strip().split('/')[-1]
        ip_name = '.'.join(ip_name.split('.')[:-1])
        input_name = each[1].strip().split('/')[-1]
        input_name = '.'.join(input_name.split('.')[:-1])

        uniquelyMappedRatioList_IP = uniquelyMappedRatio_dict[ip_name]
        uniquelyMappedRatioList_INPUT = uniquelyMappedRatio_dict[input_name]
        uniquelyMappedRatio_info.append(['rep' + str(replicate_num), ip_name, 'IP', uniquelyMappedRatioList_IP[0],
                                         uniquelyMappedRatioList_IP[1], uniquelyMappedRatioList_IP[2]])
        uniquelyMappedRatio_info.append(
            ['rep' + str(replicate_num), input_name, 'INPUT', uniquelyMappedRatioList_INPUT[0],
             uniquelyMappedRatioList_INPUT[1], uniquelyMappedRatioList_INPUT[2]])

        NRFlist_IP = NRFlist_dict[ip_name]
        NRFlist_INPUT = NRFlist_dict[input_name]
        NRFlist_info.append(['rep' + str(replicate_num), ip_name, 'IP', NRFlist_IP[0], NRFlist_IP[1], NRFlist_IP[2]])
        NRFlist_info.append(
            ['rep' + str(replicate_num), input_name, 'INPUT', NRFlist_INPUT[0], NRFlist_INPUT[1], NRFlist_INPUT[2]])

        PBClist_IP = PBClist_dict[ip_name]
        PBClist_INPUT = PBClist_dict[input_name]
        PBClist_info.append(['rep' + str(replicate_num), ip_name, 'IP', PBClist_IP[0], PBClist_IP[1], PBClist_IP[2]])
        PBClist_info.append(
            ['rep' + str(replicate_num), input_name, 'INPUT', PBClist_INPUT[0], PBClist_INPUT[1], PBClist_INPUT[2]])

    ## uniquely mapping ratio
    uniquelyMappedRatio_data = pd.DataFrame(data=np.array(uniquelyMappedRatio_info),
                                            columns=["replicates", "samples", "type", "UniquelyMappedReadCounts",
                                                     "TotalReadCounts", "ratio"])
    uniquelyMappedRatio_data.to_csv(path + '/file/uniquelyMappingRatio.txt', sep='\t', encoding='utf-8', index=False, header=False)




    # uniquelyMappedRatio_data.ratio = [i.strip('%') for i in list(uniquelyMappedRatio_data.ratio)]
    #
    # uniquelyMappedRatio_data.ratio = uniquelyMappedRatio_data.ratio.apply(float)
    #
    # sample_number = len(uniquelyMappedRatio_data.index)
    #
    # ## uniquely mapping ratio figure
    # plt.figure(figsize=(18, 9), dpi=120)
    # # legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.barplot(x="replicates", y="ratio", hue="type", data=uniquelyMappedRatio_data, palette="Set1")
    # ax.set_xlabel("Sample Replicates", fontsize=16)
    # ax.set_ylabel("Uniquely Mapping Ratio (%)", fontsize=16)
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
    # plt.savefig(path + '/uniquelyMappingRatio.png')

    ## NRF
    NRF_data = pd.DataFrame(data=np.array(NRFlist_info),
                            columns=["replicates", "samples", "type", "UniquelyMappedLocationCounts",
                                     "UniquelyMappedReadCounts", "ratio"])

    NRF_data.to_csv(path + '/file/NRF.txt', sep='\t', encoding='utf-8', index=False, header=False)

    # NRF_data.ratio = [i.strip('%') for i in list(NRF_data.ratio)]
    # NRF_data.ratio = NRF_data.ratio.apply(float)
    #
    # plt.figure(figsize=(18, 9), dpi=120)
    # # legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.barplot(x="replicates", y="ratio", hue="type", data=NRF_data, palette="Set2")
    # ax.set_xlabel("Sample Replicates", fontsize=16)
    # ax.set_ylabel("Nonredundant Fraction (%)", fontsize=16)
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
    # plt.savefig(path + '/NRF.png')

    ## PBC
    PBC_data = pd.DataFrame(data=np.array(PBClist_info),
                            columns=["replicates", "samples", "type", "OneReadMappedLocationCounts",
                                     "UniquelyMappedLocationCounts", "ratio"])
    PBC_data.to_csv(path + '/file/PBC.txt', sep='\t', encoding='utf-8', index=False, header=False)

    # PBC_data.ratio = [i.strip('%') for i in list(PBC_data.ratio)]
    # PBC_data.ratio = PBC_data.ratio.apply(float)
    #
    # plt.figure(figsize=(18, 9), dpi=120)
    # # legend = ["IP", "INPUT"]
    # sns.set_style("whitegrid")
    # ax = sns.barplot(x="replicates", y="ratio", hue="type", data=PBC_data, palette="Set3")
    # ax.set_xlabel("Sample Replicates", fontsize=16)
    # ax.set_ylabel("PCR Bottleneck Coefficient", fontsize=16)
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
    # plt.savefig(path + '/PBC.png')

    # print('Done! Time taken: {:.4f} min'.format((time() - start_time) / 60.0))
    # print('#####' * 20)

    # return uniquelyMappedRatio_info, NRFlist_info, PBClist_info
    return


