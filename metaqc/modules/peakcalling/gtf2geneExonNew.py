# import numpy as np
import pandas as pd
#from time import sleep
from subprocess import Popen, PIPE
import sys
import os



def chunks(L, n):
    """
    Yield successive n-sized chunks from L.
    """
    for i in range(0, len(L), n):
        yield L[i:i + n]



def getExonCoordinate(gtf=None, path = None, rRNA_tRNA_bed = None):
    '''

    :param gtf: gtf file
    :param path: file path
    :return: a treated gtf file
    '''

    gtf_filename = gtf.strip().split('/')[-1]

    ## read the gtf content into dataframe
    # data = pd.read_csv(gtf, sep='\t', names=['chr', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute'])
    # data_new = data[['chr', 'start', 'end', 'source', 'feature', 'score', 'strand', 'frame', 'attribute']]
    # data = 0
    # data_new.to_csv(path + '/tmp/' + gtf_filename + '.txt', sep='\t', encoding='utf-8', index=False, header=False)
    # data_new = 0
    fh = open(gtf)
    out = open(path + '/tmp/' + gtf_filename + '.txt', 'w')
    # big_list = []
    for i in fh:
        line_list = i.strip().split('\t')
        if 'exon' in line_list:
            tmp_dict = dict()
            attr = line_list[-1].split(';')
            attr.pop()
            for i in attr:
                tmp_list = i.split()
                tmp_dict[tmp_list[0]] = tmp_list[1].strip('\"')
            # gene_id = attr[0].split()[-1].strip("\"")
            gene_id = tmp_dict['gene_id']
            # transcript_id = '_'.join(attr[1].split()[-1].strip("\"").split('_')[:2])
            transcript_id = '_'.join(tmp_dict['transcript_id'].split('_')[:2])
            out.write('\t'.join([line_list[0], line_list[3], line_list[4], gene_id, transcript_id, line_list[6]]))
            out.write('\n')
    # for j in big_list:
    #     out.write('\t'.join(j))
    #     out.write('\n')
    out.close()

    # gtf_file_line_list = []
    if os.path.exists(path + '/tmp/' + gtf_filename + '.txt'):
        out2 = open(path + '/tmp/' + gtf_filename + '_filtered.txt', 'w')
        cmd = 'coverageBed -a ' + path + '/tmp/' + gtf_filename + '.txt -b ' + rRNA_tRNA_bed + ' -counts'
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        for i in proc.stdout:
            tmp_list = i.decode().strip().split('\t')
            if tmp_list[-1] == '0':
                tmp_list.pop()
                out2.write('\t'.join(tmp_list))
                out2.write('\n')
        out2.close()

    else:
        sys.exit('<callpeak> ' + path + '/tmp/' + gtf_filename + '.txt no exists!')

    # gtf_file_data = pd.DataFrame(data=np.array(gtf_file_line_list), columns=['chr', 'start', 'end', 'source', 'feature', 'score', 'strand', 'frame', 'attribute', 'counts'])
    #
    # gtf_file_line_list = 0
    #
    # gtf_file_data.counts = gtf_file_data.counts.apply(int)
    #
    # ## no overlap with rRNA or tRNA
    # gtf_file_data_new = gtf_file_data[gtf_file_data.counts == 0].copy()
    # gtf_file_data = 0

    ## view the result, can be cancled.
    #gtf_file_data_new.to_csv(path + '/tmp/' + gtf_filename + '.txt.tmp.bed', sep='\t', encoding='utf-8', index=False, header=False)


    # fh = open(gtf)
    # gene_list=[]
    # #for i in fh:
    # for index, row in gtf_file_data_new.iterrows():
    #     row_list = list(row)
    #     if 'exon' in row_list:
    #         #chrom, source, feature, start, end, score, strand, frame, attribute = i.strip().split('\t')
    #         chrom, start, end, source, feature, score, strand, frame, attribute, counts = row_list[:]
    #         # print(attribute)
    #         # print(type(attribute))
    #         # i = attribute
    #
    #         tmp_dict = dict()
    #
    #         l1 = attribute.split(';')
    #         l1.pop()
    #         # print(l1)
    #         for i in l1:
    #             i = i.strip()
    #             i = i.strip("\"")
    #             l2 = i.split()
    #             # print(l2)
    #             tmp_dict[l2[0]] = l2[1].strip("\"")
    #             # print(tmp_dict)
    #
    #         # for m in l1:
    #         #     l2 = m.strip().split(' ')
    #         #     # print(l2)
    #         #     # n = '_'.join(l2[1].strip("\"").split('_')[:2])
    #         #     # print(n)
    #         #     try:
    #         #         tmp_dict[l2[0]] = l2[1]
    #         #     # print(tmp_dict)
    #         #     except Exception as e:
    #         #         print(m)
    #         #         print(l1)
    #         #         sys.exit(e)
    #
    #         # gene_id = attribute.split(";")[0].split()[1].strip("\"")
    #         # tx_id = attribute.split(";")[1].strip().split()[1].strip("\"")
    #         # tx_id = '_'.join(tx_id.split('_')[:2])
    #         gene_id = tmp_dict['gene_id']
    #         tx_id = '_'.join(tmp_dict['transcript_id'].split('_')[:2])
    #         # gene_id = tmp_dict['gene_id']
    #         # tx_id = tmp_dict['transcript_id']
    #         # print tx_id
    #         # sleep(1)
    #         #tmp_list = [chrom, start, end, gene_id]
    #         gene_list.append([chrom, start, end, gene_id, tx_id])


    # dataframe structure
    if os.path.exists(path + '/tmp/' + gtf_filename + '_filtered.txt'):
        column_types = {'chr': "category", 'start': 'int32', 'end': 'int32', 'geneID':'category', 'txID':'category', 'strand':'category'}
        df = pd.read_csv(path + '/tmp/' + gtf_filename + '_filtered.txt', sep='\t', names=['chr', 'start', 'end', 'geneID', 'txID', 'strand'],
                         dtype=column_types)

        out3 = open(path + '/tmp/' + gtf_filename + '.bed', 'w')
        # df = pd.DataFrame(data=np.array(gene_list), columns=["chr", "start", "end", "geneID", "txID"])
    #print len(df.index)
    # gene_list = 0

    # df.start = df.start.apply(int)
    # df.end = df.end.apply(int)


    # remove the same start and end in the same geneID
    #df = df.drop_duplicates(subset=['chr', 'start', 'end', 'geneID'], keep='first')
    #print len(d.index)
    #print d.loc[d.geneID == 'SYS1']


    # chrom as unit
        chrom_set = set(df.chr)
    #print chrom_set

    #exones_accord = []
        # gtf_file = []
        for chrom in chrom_set:
            b = df.loc[df.chr == chrom].copy()

            # geneID as unit
            geneID_set = set(b.geneID)
            #print geneID_set


            for gene_id in geneID_set:
                #one_gene_exon = []

                single_gene = b.loc[b.geneID == gene_id].copy()
                #print single_gene
                #sleep(1)

                ## txID as unit
                txID_set = set(single_gene.txID)

                for tx in txID_set:
                    one_tx_exon = []

                    single_tx = single_gene.loc[single_gene.txID == tx].copy()
                    strand = list(single_tx.strand)[0]

                    # print single_tx
                    # sleep(1)
                    start = list(single_tx.start)
                    end = list(single_tx.end)
                    #print single_gene

                    start_end = zip(start, end)
                    #print start_end

                    for item in start_end:
                        one_tx_exon.extend(range(item[0], item[1]+1))
                    #print len(one_gene_exon)
                    one_tx_exon_list = list(set(one_tx_exon))
                    one_tx_exon_list.sort()

                    for m in chunks(one_tx_exon_list, 25):
                        if len(m) == 25:
                            m_2 = m[1:]
                            start_new = []
                            end_new = []
                            start_new.append(m[0])
                            for i in range(len(m_2)):
                                if m_2[i] - m[i] > 1:
                                    end_new.append(m[i])
                                    start_new.append(m_2[i])
                            end_new.append(m[-1])

                            for n in range(len(start_new)):
                                length = end_new[n] - start_new[n] + 1
                                out3.write('\t'.join([chrom, str(start_new[n]), str(end_new[n]), str(length), gene_id, tx, strand]))
                                out3.write('\n')
        out3.close()
    else:
        sys.exit('<callpeak> ' + path + '/tmp/' + gtf_filename + '_filtered.txt No exists!')
        # path + '/tmp/' + gtf_filename + '_filtered.txt'
    # gtf_data = pd.DataFrame(data=np.array(gtf_file), columns=["chr", "start", "end", "length", "geneID", "txID"])
    # gtf_file = 0
    #
    #
    # gtf_data.to_csv(path + '/tmp/' + gtf_filename + '.bed', sep='\t', encoding='utf-8', index=False, header=False)

    ## sort gtf
    file_path = path + '/tmp/' + gtf_filename + '.bed'
    if os.path.exists(file_path):
        cmd2 = 'sort -k1,1 -k2,2n ' + file_path + ' > ' + path + '/tmp/' + gtf_filename + '_sorted.bed'
        proc2 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
        for i in proc2.stderr:
        # print('bam2bed error:')
            print(i.decode())
    else:
        sys.exit('<callpeak> ' + file_path + ' No exists!')
    #gtf_data.to_csv(path + '/tmp/genes.gtf.bed', sep='\t', encoding='utf-8', index=False, header=False)
    return

if __name__ == '__main__':
    getExonCoordinate(gtf='/media/chaigs/softwares/data/genes.gtf', path= '.')
