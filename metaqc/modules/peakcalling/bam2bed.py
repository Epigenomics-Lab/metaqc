# import numpy as np
# import pandas as pd
from subprocess import Popen, PIPE
import sys
import os
#from time import time, sleep

def bam2Bed(seq_type = None, bamfile = None, path = None):

    bamfile_name = bamfile.strip().split('/')[-1]
    bamfile_name = '.'.join(bamfile_name.split('.')[:-1])

    # single end sequencing
    if seq_type == 'SE':
        # cmd1 = 'samtools view -@ 4 -q 30 -b ' + bamfile + ' | bamToBed -i - > ' + path + '/tmp/' + bamfile_name + '_peak_q30.bed'
        # proc1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
        # for i in proc1.stderr:
        #     #print('bam2bed error:')
        #     print(i.decode())

        ## get the information of read length
        cmd2 = 'samtools view ' + bamfile
        fh1 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
        # TotalReads = set()
        # readLength = 0
        for i in fh1.stdout:
            SEQ = i.decode().split('\t')[9]
            readLength = len(SEQ)
            # print(SEQ)
            break
        extend_length = 250 - readLength
        print(bamfile_name + ' read length: ' + str(readLength))

        if os.path.exists(path + '/tmp/' + bamfile_name + '_q30.bed'):
            fh = open(path + '/tmp/' + bamfile_name + '_q30.bed')
            out = open(path + '/tmp/' + bamfile_name + '.treated.bed', 'w')
            for i in fh:
                tmp_list = i.strip().split('\t')
                if int(tmp_list[2]) - int(tmp_list[1]) == readLength and extend_length >= 0:
                    s1 = '\t'.join([tmp_list[0], tmp_list[1], str(int(tmp_list[2]) + extend_length)])
                    out.write(s1)
                    out.write('\n')
            out.close()
            # column_types = {'chr': "category", 'start': 'int32', 'end': 'int32'}
            # data = pd.read_csv(path + '/tmp/' + bamfile_name + '_q30.bed', sep='\t', names=['chr', 'start', 'end'],
            #                    dtype=column_types)

        else:
            sys.exit('<callpeak> ' + path + '/tmp/' + bamfile_name + '_q30.bed No exists!')
        #
        # print data.dtypes
        # print len(data.index)
        # data_mapq30 = data.loc[data.mapq >= 30].copy()
        # data = ''  # release memory
        # print data_mapq30.dtypes
        # print len(data_mapq30.index)
        # print set(data_mapq30.strand)

        ## FRiP value
        #mapped_read_counts = len(set(data_mapq30.qname))
        # mapped_read_counts = len(data_mapq30.index)

        #read_length = list(data_mapq30.end)[1] - list(data_mapq30.start)[1]


        #print read_length

        # data_mapq30_positive_strand = data_mapq30.loc[data_mapq30.strand == '+'].copy()
        # data_mapq30_negative_strand = data_mapq30.loc[data_mapq30.strand == '-'].copy()
        # data_mapq30 = ''  # release memory
        #
        # data_mapq30_positive_strand.end = [i + extend_length for i in list(data_mapq30_positive_strand.end)]
        #data_mapq30_negative_strand.start = [i - extend_length for i in list(data_mapq30_negative_strand.start)]

        #### start point is not negative. if negative, convert it into 0.
        # start = []
        # for i in list(data_mapq30_negative_strand.start):
        #     start_new = i - extend_length
        #     if start_new < 0:
        #         start.append(0)
        #     else:
        #         start.append(start_new)
        # data_mapq30_negative_strand.start = start

        # data_list = []
        # for index, row in data.iterrows():
        #     tmp_list = list(row)
        #     if int(tmp_list[2]) - int(tmp_list[1]) == int(readLength) and extend_length >= 0:
        #         data_list.append([tmp_list[0], int(tmp_list[1]), int(tmp_list[2]) + extend_length])
        #
        # data = 0
        # #data_mapq30.end = [i + extend_length for i in list(data_mapq30.end)]
        # data_30 = pd.DataFrame(data=np.array(data_list),
        #                              columns=['chr', 'start', 'end'],
        #                        dtype=column_types)
        # data_list = 0

        # merge two dataframes
        #result = data_mapq30_positive_strand.append(data_mapq30_negative_strand)
        #result = data_mapq30_positive_strand.append(data_mapq30_negative_strand)


        # data_30.to_csv(path + '/tmp/' + bamfile_name + '.treated.bed', sep='\t', encoding='utf-8', index=False, header=False)
        # data_30 = 0

        if os.path.exists(path + '/tmp/' + bamfile_name + '.treated.bed'):
            cmd3 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + bamfile_name + '.treated.bed > ' + path + '/tmp/' + bamfile_name + '.treated_sorted.bed'
            proc2 = Popen(cmd3, stdout=PIPE, stderr=PIPE, shell=True)
            for i in proc2.stderr:
                #print('bam2bed error:')
                print(i.decode())
        else:
            sys.exit('<callpeak> ' + path + '/tmp/' + bamfile_name + '.treated.bed No exists!')

    # pair end sequencing
    elif seq_type == 'PE':

        bam_list = []
        cmd1 = 'samtools view -@ 4 -q 30 -b ' + bamfile + ' | samtools sort -@ 4 -n - | bamToBed -bedpe -i - > ' + path + '/tmp/' + bamfile_name + '.bedpe'
        fh1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
        for i in fh1.stderr:
            pass
            # print(i)
            # sys.exit()


        # cmd2 = 'bamToBed -bedpe -i ' + path + '/tmp/' + bamfile_name + '.sort.by.name.bam > ' + path + '/tmp/' + bamfile_name + '.bedpe'
        # #cmd2 = 'bamToBed -bedpe -i ' + bamfile
        # fh = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
        # for i in fh.stderr:
        #     pass

        # for i in fh.stdout:
        #     print i
        #     #sleep(1)
        #     chrom1, start1, end1, chrom2, start2, end2, qname, mapq, strand1, strand2 = i.strip().split('\t')[:]
        #     if int(mapq) >= 30:
        #         bam_list.append([chrom1, start1, end1, chrom2, start2, end2, qname, mapq])
        # data = pd.DataFrame(data=np.array(bam_list), columns=["chr1", "start1", "end1", "chr2", "start2", 'end2', "qname", "mapq"])
        #
        # print data.dtypes
        if os.path.exists(path + '/tmp/' + bamfile_name + '.bedpe'):
            command1 = 'cut -f 1,2,4,6 ' + path + '/tmp/' + bamfile_name + '.bedpe > ' + path + '/tmp/' + bamfile_name + '_treated.bedpe'
            os.system(command1)
            if os.path.exists(path + '/tmp/' + bamfile_name + '_treated.bedpe'):
                fh = open(path + '/tmp/' + bamfile_name + '_treated.bedpe')
                out = open(path + '/tmp/' + bamfile_name + '.treated.bed', 'w')
                # column_types = {'chr1': "category", 'chr2': 'category', 'start': 'int32', 'end': 'int32'}
                # data = pd.read_csv(path + '/tmp/' + bamfile_name + '_treated.bedpe', sep='\t',
                #                    names=["chr1", "start", "chr2", "end"],
                #                    dtype=column_types)
                for i in fh:
                    chr1, start, chr2, end = i.strip().split('\t')[:]
                    if chr1 != '.' and chr1 == chr2:
                        out.write('\t'.join([chr1, start, end]))
                        out.write('\n')
                out.close()


            else:
                sys.exit('<callpeak> ' + path + '/tmp/' + bamfile_name + '_treated.bedpe No exists!')
        else:
            sys.exit('<callpeak> ' + path + '/tmp/' + bamfile_name + '.bedpe No exists!')
        # print data.dtypes
        # print len(data.index)

        # extract mapq >= 30 line
        # data_mapq30 = data.loc[data.mapq >= 30].copy()
        # data = '' # release memory
        # print len(data_mapq30.index)
        # print set(data_mapq30.chr1)
        # for i in set(data_mapq30.chr1):
        #     print i

        #
        # bamtobed_list = []
        # for index, row in data_mapq30.iterrows():
        #     chrom1, start1, end1, chrom2, start2, end2, qname, mapq, strand1, strand2 = list(row)[:]
        #     if chrom1 != '.' or chrom2 != '.':
        #         if chrom1 == chrom2:
        #             bamtobed_list.append([chrom1, start1, end2, qname, mapq])
        #
        # data_mapq30.drop(data_mapq30[data_mapq30.chr1 != '.'].index, inplace=True)
        # print len(data_mapq30.index)

        # data = data.loc[(data.chr1 != '.') & (data.chr1 == data.chr2)]
        # data = 0

        # data_mapq30 = ''
        #print len(bamtobed.index)

        # columns = ['end1', 'chr2', 'start2', 'strand1', 'strand2']
        #
        # # 1 is the axis number (0 for rows and 1 for columns.)
        # bamtobed.drop(columns, inplace=True, axis=1)
        # #print len(bamtobed.index)
        # data = data[['chr1', 'start', 'end']]



        #bamtobed = pd.DataFrame(data=np.array(bamtobed_list), columns=["chr", "start", "end", "qname", "mapq"])

        # print len(bamtobed.index)
        # print bamtobed.dtypes
        #
        # data.to_csv(path + '/tmp/' + bamfile_name + '.treated.bed', sep='\t', encoding='utf-8', index=False, header=False)
        # bamtobed = 0
        # data = 0

        if os.path.exists(path + '/tmp/' + bamfile_name + '.treated.bed'):
            cmd3 = 'sort -k1,1 -k2,2n ' + path + '/tmp/' + bamfile_name + '.treated.bed > ' + path + '/tmp/' + bamfile_name + '.treated_sorted.bed'
            proc2 = Popen(cmd3, stdout=PIPE, stderr=PIPE, shell=True)
            for i in proc2.stderr:
                #print('bam2bed error:')
                print(i.decode())

        ## FRiP value
        # df = pd.read_csv(path + '/tmp/' + bamfile + '.bed', sep='\t',
        #                    names=['chr', 'start', 'end', 'qname', 'mapq', 'strand'])
        #
        # df_mapq30 = df.loc[df.mapq >= 30].copy()
        # df = ''
        #
        # #mapped_read_counts = len(set(df_mapq30.qname))
        # mapped_read_counts = len(df_mapq30.inidex)

    return



if __name__ == '__main__':
    bam2Bed(seq_type = 'PE', bamfile='D1_raw_hg19_hisat2.sort.byname.bam', path='.')



