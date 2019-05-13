# import matplotlib
# matplotlib.use('agg')

from subprocess import Popen, PIPE
# import argparse
from multiprocessing.dummy import Pool as ThreadPool
# from matplotlib import pyplot as plt
from time import sleep, time
# from scipy.interpolate import spline
import numpy as np
import pandas as pd
import os
import sys



def test(args):
    fraction, inputfile, bed = args
    cmd = 'samtools view -b -s ' + str(fraction) + ' ' + inputfile + ' | bamToBed -i - | bedtools intersect -wo -a - -b ' + bed
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    geneID_dict = dict()
    n1 = 0
    for i in proc.stdout:
        tmp_list = i.decode().strip().split()
        geneID = tmp_list[-2]
        # overlap=tmp_list[-1]
        if geneID not in geneID_dict:
            geneID_dict[geneID] = 1
        else:
            geneID_dict[geneID] += 1
    # print(len(transcript_dict))
    for key in geneID_dict:
        if geneID_dict[key] >= 5: # the reads number of a gene must more than or equal to 5.
            n1 += 1
    # return str(fraction)+'\t'+ str(n1)
    fraction = int(fraction * 100)
    inputfile_name = inputfile.strip().split('/')[-1]
    return (inputfile_name, fraction, n1)




def accelaration(sample=None, bed=None):
    proportion = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                  0.12, 0.14, 0.16, 0.18, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                  0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    #proportion = [0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
    #proportion = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    sample_list=[]
    bed_list=[]
    sample_list.append(sample)
    bed_list.append(bed)
    sample_list=sample_list * len(proportion)
    bed_list=bed_list * len(proportion)
    #start_time = time()
    fraction_x=[]
    transcript_y=[]

    ## add 0 for plotting in html
    fraction_x.append(0)
    transcript_y.append(0)

    # Make the Pool of workers  Manually change to 6, get from config.ini file

    ## parallel -> 2,  or -> 4
    pool = ThreadPool(4)
    # Open the urls in their own threads
    # and return the results list
    #results = pool.map(test, zip(proportion, sample_list, bed_list))

    results = pool.map(test, zip(proportion, sample_list, bed_list))
    #close the pool and wait for the work to finish
    pool.close()
    pool.join()
    #print results
    #print(type(results))
    for i in results:
        sample=i[0]
        fraction_x.append(i[1])
        transcript_y.append(i[2])
    # print fraction_x
    # print transcript_y
    # print sample
    return sample, fraction_x, transcript_y

def saturation(sample_dict=None, bed=None, path=None):
    # start_time = time()
    # print('MetaQC is calculating library saturation...')

    sleep(5)  ## wait for the tmp directory

    saturation_info = []

    file_info = []

    # plt.figure(figsize=(18, 9), dpi=120)
    for key in sample_dict:
        if key == 'ip':
            replicate_number = 0
            for sample_tuple in sample_dict[key]:
                for sample in sample_tuple:
                    sample_label_name = sample.strip().split('/')[-1]
                    sample_label_name = '.'.join(sample_label_name.split('.')[:-1])
                    if os.path.exists(sample):
                        cmd1 = 'samtools view -@ 4 -q 30 -b -o ' + path + '/tmp/' + sample_label_name + '_q30.bam ' + sample
                        proc2 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)

                        for i in proc2.stderr:
                            print(i.decode())
                    else:
                        sys.exit('<saturation> ' + sample + 'not exists!')

                    sample = path + '/tmp/' + sample_label_name + '_q30.bam'
                    replicate_number += 1

                    if os.path.exists(sample):
                        sample_name, fraction_x, transcript_y = accelaration(sample=sample, bed=bed)
                        saturation_info.append(['rep'+ str(replicate_number), sample_label_name, 'IP', transcript_y[-1]])
                        for i in range(len(fraction_x)):
                            file_info.append(['rep'+ str(replicate_number), sample_label_name, 'IP', fraction_x[i], transcript_y[i]])
                    else:
                        sys.exit('<saturation> ' + sample + 'not exists!')

        elif key == 'input':
            replicate_number = 0
            for sample_tuple in sample_dict[key]:
                for sample in sample_tuple:
                    sample_label_name = sample.strip().split('/')[-1]
                    sample_label_name = '.'.join(sample_label_name.split('.')[:-1])
                    if os.path.exists(sample):
                        cmd1 = 'samtools view -@ 4 -q 30 -b -o ' + path + '/tmp/' + sample_label_name + '_q30.bam ' + sample
                        proc2 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)

                        for i in proc2.stderr:
                            print(i.decode())
                    else:
                        sys.exit('<saturation> ' + sample + 'not exists!')

                    sample = path + '/tmp/' + sample_label_name + '_q30.bam'

                    replicate_number += 1
                    # sample_label_name = sample.strip().split('/')[-1]
                    # sample_label_name = '.'.join(sample_label_name.split('.')[:-1])
                    if os.path.exists(sample):
                        sample_name, fraction_x, transcript_y = accelaration(sample=sample, bed=bed)
                        saturation_info.append(['rep' + str(replicate_number), sample_label_name, 'INPUT', transcript_y[-1]])
                        for i in range(len(fraction_x)):
                            file_info.append(['rep'+ str(replicate_number), sample_label_name, 'INPUT', fraction_x[i], transcript_y[i]])
                    else:
                        sys.exit('<saturation> ' + sample + 'not exists!')
    # plt.xlabel('Reads Fraction (%)')
    # plt.ylabel('Detected Transcripts')
    # plt.legend()
    # plt.show()
    # plt.xlabel('Reads Fraction (%)', fontsize=16)
    # plt.ylabel('Detected Gene Counts', fontsize=16)
    # plt.legend()
    # #plt.xlim([1, 102])
    # plt.xlim([0, 102])
    # #plt.show()
    # plt.savefig(path+'/saturation.png')

    saturation_info_data = pd.DataFrame(data=np.array(saturation_info),
                               columns=["replicates", "samples", "type", "geneCounts"])
    saturation_info_data.to_csv(path+'/file/saturationInfo_table.txt', sep='\t', encoding='utf-8', index=False, header=False)

    #print (file_info)
    file_info_data = pd.DataFrame(data=np.array(file_info),
                               columns=["replicates", "samples", "type", "fraction", "geneCounts"])
    file_info_data.to_csv(path+'/file/saturationInfo_plot.txt', sep='\t', encoding='utf-8', index=False, header=False)


    # print('Done! Time taken: {:.4f} min'.format((time() - start_time)/60.0))
    # print('#####' * 20)
    return

def saturation_info(path = None):
    saturation_info_list = []
    fh = open(path+'/file/saturationInfo_table.txt')
    for i in fh:
        saturation_info_list.append(i.strip().split('\t'))
    saturation_info_list.sort()
    return saturation_info_list



