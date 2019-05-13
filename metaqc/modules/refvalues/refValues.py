import os
import sys


def ref_values(path = None, species = None):
    Ref_values = {'hg19': ['>15%', '>20%', '>11M', '>17000', '>8000', '<21%'],
                  'mm10': ['>2%', '>14%', '>5M', '>13000', '>5000', '<46%']}

    if species == 'hg19' or species == 'hg38':
        reference_values = Ref_values['hg19']
        title_list = ['Quality Control Metrics', 'Reference Values (hg19)']

    elif species == 'mm9' or species == 'mm10':
        reference_values = Ref_values['mm10']
        title_list = ['Quality Control Metrics', 'Reference Values (mm10)']

    frip_list = ['Fraction of Reads in Peaks (FRiP)', reference_values[0]]
    NRF_list = ['Nonredundant Fraction (NRF)', reference_values[1]]
    uniqueRead_list = ['Uniquely Mapping Read Counts', reference_values[2]]
    geneCount_list = ['Detected Gene Counts', reference_values[3]]
    peakCounts_list = ['Detected m6A Peak Counts', reference_values[4]]
    contaminationRatio_list = ['rRNA & tRNA Contamination Ratio', reference_values[5]]

    ## frip
    frip_file = path + '/file/frip.txt'
    # frip_list = []
    if os.path.exists(frip_file):
        fh_frip = open(frip_file)
        for i in fh_frip:
            l1 = i.strip().split('\t')
            if 'IP' in l1:
                frip_list.append(l1[-1])
    else:
        sys.exit('<refvalues> ' + frip_file + ' No exists!')

    ## NRF
    NRF_file = path + '/file/NRF.txt'
    # NRF_list = []
    if os.path.exists(NRF_file):
        fh_NRF = open(NRF_file)
        for i in fh_NRF:
            tmp_list = i.strip().split('\t')
            if 'IP' in tmp_list:
                NRF_list.append(tmp_list[-1])
    else:
        sys.exit('<refvalues> ' + NRF_file + ' No exists!')

    ## Uniquely mapping read counts
    uniqueRead_file = path + '/file/uniquelyMappingRatio.txt'
    # uniqueRead_list = []
    if os.path.exists(uniqueRead_file):
        fh_uniqueRead = open(uniqueRead_file)
        for i in fh_uniqueRead:
            l2 = i.strip().split('\t')
            if 'IP' in l2:
                uniqueRead_list.append(l2[3])
    else:
        sys.exit('<refvalues> ' + uniqueRead_file + ' No exists!')

    ## detected gene counts
    geneCount_file = path + '/file/saturationInfo_table.txt'
    # geneCount_list = []
    if os.path.exists(geneCount_file):
        fh_geneCount = open(geneCount_file)
        for i in fh_geneCount:
            l1 = i.strip().split('\t')
            if 'IP' in l1:
                geneCount_list.append(l1[-1])
    else:
        sys.exit('<refvalues> ' + geneCount_file + ' No exists!')

    ## detected m6A peak counts
    peakCounts_file = path + '/file/peakLengthInfo.txt'
    # peakCounts_list = []
    if os.path.exists(peakCounts_file):
        fh_peakCounts = open(peakCounts_file)
        for i in fh_peakCounts:
            l1 = i.strip().split('\t')
            peakCounts_list.append(l1[-1])

    else:
        sys.exit('<refvalues> ' + peakCounts_file + ' No exists!')

    ## rRNA & tRNA contamination ratio
    contaminationRatio_file = path + '/file/contamination.txt'
    # contaminationRatio_list = []
    if os.path.exists(contaminationRatio_file):
        fh = open(contaminationRatio_file)
        for i in fh:
            l1 = i.strip().split('\t')
            if 'IP' in l1:
                contaminationRatio_list.append(l1[-1])
    else:
        sys.exit('<refvalues> ' + contaminationRatio_file + ' No exists!')

    n1 = len(frip_list)
    for i in range(n1-2):
        title_list.append('Rep' + str(i + 1))


    out = open(path + '/file/referenceValues.txt', 'w')

    l3 = [title_list, frip_list, NRF_list, uniqueRead_list, geneCount_list, peakCounts_list, contaminationRatio_list]
    for i in l3:
        s1 = '\t'.join(i)
        out.write(s1)
        out.write('\n')
    out.close()

    return


























