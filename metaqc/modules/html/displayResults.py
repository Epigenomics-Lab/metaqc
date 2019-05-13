# import os
def makeHtml(path = None, htmlTemplate = None, replicateNumber = None):
    fh = open(htmlTemplate)
    l1 = fh.readlines()
    if replicateNumber == 1:
        # fh = open(htmlTemplate)
        # l1 = fh.readlines()
        ## uniquely mapping ratio
        # uniquelyMappingRatio.txt
        fh_mappingRatio = open(path + '/file/uniquelyMappingRatio.txt')
        mappingRatio_dict = dict()
        for i in fh_mappingRatio:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            mappingRatio_dict[Key] = tmp_list
        ## rep1 IP
        # print(l1[136:142])
        l1[136:142] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['IP_rep1'][5] + '</td>\n']
        # print(l1[158:159])
        l1[158:159] = ['                                            y:[' + mappingRatio_dict['IP_rep1'][5].strip('%') + '],\n']
        ## rep1 input
        # print(l1[144:150])
        l1[144:150] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + mappingRatio_dict['INPUT_rep1'][5] + '</td>\n']
        # print(l1[168:169])
        l1[168:169] = ['                                            y:[' + mappingRatio_dict['INPUT_rep1'][5].strip('%') + '],\n']
        ## NRF
        ## NRF.txt
        fh_NRF = open(path + '/file/NRF.txt')
        NRF_dict = dict()
        for i in fh_NRF:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            NRF_dict[Key] = tmp_list
        # print(NRF_dict)
        ## rep1 IP
        # print(l1[225:231])
        l1[225:231] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['IP_rep1'][5] + '</td>\n']
        # print(l1[246:247])
        l1[246:247] = ['                                            y:[' + NRF_dict['IP_rep1'][5].strip('%') + '],\n']
        ## rep1 input
        # print(l1[233:239])
        l1[233:239] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + NRF_dict['INPUT_rep1'][5] + '</td>\n']
        # print(l1[256:257])
        l1[256:257] = ['                                            y:[' + NRF_dict['INPUT_rep1'][5].strip('%') + '],\n']
        ## PBC
        ## PBC.txt
        fh_PBC = open(path + '/file/PBC.txt')
        PBC_dict = dict()
        for i in fh_PBC:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + "_" + tmp_list[0]
            PBC_dict[Key] = tmp_list
        # print(PBC_dict)
        ## rep1 IP
        # print(l1[313:319])
        l1[313:319] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['IP_rep1'][5] + '</td>\n']
        # print(l1[334:335])
        l1[334:335] = ['                                            y:[' + PBC_dict['IP_rep1'][5] + '],\n']
        ## rep1 input
        # print(l1[321:327])
        l1[321:327] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + PBC_dict['INPUT_rep1'][5] + '</td>\n']
        # print(l1[343:344])
        l1[343:344] = ['                                            y:[' + PBC_dict['INPUT_rep1'][5] + '],\n']
        ## contamination
        ## contamination.txt
        fh_contamination = open(path + '/file/contamination.txt')
        contamination_dict = dict()
        for i in fh_contamination:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + "_" + tmp_list[0]
            contamination_dict[Key] = tmp_list
        # print(contamination_dict)
        ## rep1 IP
        # print(l1[399:406])
        l1[399:406] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][0] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][1] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][2] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][3] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][4] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][5] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['IP_rep1'][6] + "</td>\n"]
        # print(l1[422:423])
        l1[422:423] = ['                                            y:[' + contamination_dict['IP_rep1'][6].strip('%') + '],\n']
        ## rep1 input
        # print(l1[408:415])
        l1[408:415] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][0] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][1] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][2] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][3] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][4] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][5] + "</td>\n",
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + contamination_dict['INPUT_rep1'][6] + "</td>\n"]
        # print(l1[431:432])
        l1[431:432] = ['                                            y:[' + contamination_dict['INPUT_rep1'][6].strip('%') + '],\n']
        ## saturation
        # rep1 IP
        ## saturationInfo_table.txt
        fh_saturationInfo = open(path + '/file/saturationInfo_table.txt')
        saturationInfo_dict = dict()
        for i in fh_saturationInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0] + '_' + tmp_list[2]
            if Key not in saturationInfo_dict:
                saturationInfo_dict[Key] = tmp_list
        # print(saturationInfo_dict)

        # print(l1[485:489])
        l1[485:489] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_IP'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_IP'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_IP'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_IP'][3] + '</td>\n']
        ## rep1 input
        # print(l1[491:495])
        l1[491:495] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_INPUT'][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_INPUT'][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_INPUT'][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + saturationInfo_dict['rep1_INPUT'][3] + '</td>\n']
        ## saturationInfo_plot.txt
        fh_saturationPlot = open(path + '/file/saturationInfo_plot.txt')
        saturationPlot_dict = dict()
        for i in fh_saturationPlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            if Key not in saturationPlot_dict:
                saturationPlot_dict[Key] = [[tmp_list[3]], [tmp_list[4]]]
            elif Key in saturationPlot_dict:
                saturationPlot_dict[Key][0].append(tmp_list[3])
                saturationPlot_dict[Key][1].append(tmp_list[4])
        # print(saturationPlot_dict)
        # print(l1[501:503])
        l1[501:503] = ['                                            x: [' + ','.join(saturationPlot_dict['IP_rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['IP_rep1'][1]) + '],\n']
        # print(l1[504:505])
        l1[504:505] = ["                                            name: 'IP_rep1',\n"]
        # print(l1[511:513])
        l1[511:513] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep1'][1]) + '],\n']
        # print(l1[514:515])
        l1[514:515] = ["                                            name: 'INPUT_rep1',\n"]
        ## RDD
        ## rep1
        ## stdevInfo.txt
        fh_RDDinfo = open(path + '/file/stdevInfo.txt')
        RDDinfo_list = []
        for i in fh_RDDinfo:
            RDDinfo_list.append(i.strip().split('\t'))
        # print(RDDinfo_list)
        # print(l1[576:581])
        l1[576:581] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + RDDinfo_list[0][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + RDDinfo_list[0][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + RDDinfo_list[0][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + RDDinfo_list[0][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + RDDinfo_list[0][4] + '</td>\n']
        ## stdevPlot.txt
        fh_RDDplot = open(path + '/file/stdevPlot.txt')
        RDDplot_dict = dict()
        for i in fh_RDDplot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0] + '_' + tmp_list[1]
            if Key not in RDDplot_dict:
                RDDplot_dict[Key] = [tmp_list[3]]
            elif Key in RDDplot_dict:
                RDDplot_dict[Key].append(tmp_list[3])
        # print(RDDplot_dict)
        ## IP
        # print(l1[589:590])
        n1, n2, n3, n4, n5 = RDDplot_dict['rep1_IP'][:]
        RDDplot_IP1 = [n1, n2, n2, n3, n4, n4, n5]
        l1[589:590] = ['                                            y: [' + ','.join(RDDplot_IP1) + '],\n']
        ## input
        n1, n2, n3, n4, n5 = RDDplot_dict['rep1_INPUT'][:]
        RDDplot_Input1 = [n1, n2, n2, n3, n4, n4, n5]
        # print(l1[598:599])
        l1[598:599] = ['                                            y: [' + ','.join(RDDplot_Input1) + '],\n']
        ## FRiP
        ## rep1 IP
        ## frip.txt
        fh_frip = open(path + '/file/frip.txt')
        frip_list = []
        for i in fh_frip:
            frip_list.append(i.strip().split('\t'))
        # print(frip_list)
        # print(l1[655:661])
        l1[655:661] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[0][5] + '</td>\n']
        ## rep1 input
        # print(l1[663:669])
        l1[663:669] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][3] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][4] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + frip_list[1][5] + '</td>\n']

        ## IP
        # print(l1[676:677])
        l1[676:677] = ['                                            y:[' + frip_list[0][5].strip('%') + '],\n']
        ## input
        # print(l1[685:686])
        l1[685:686] = ['                                            y:[' + frip_list[1][5].strip('%') + '],\n']

        ## metagene
        ## metageneInfo.txt
        fh_metageneInfo = open(path + '/file/metageneInfo.txt')
        metageneInfo_list = []
        for i in fh_metageneInfo:
            metageneInfo_list.append(i.strip().split('\t'))
        # print(metageneInfo_list)
        # print(l1[739:743])
        l1[739:743] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + metageneInfo_list[0][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + metageneInfo_list[0][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + metageneInfo_list[0][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + metageneInfo_list[0][3] + '</td>\n']

        ## metagenePlot.txt
        fh_metagenePlot = open(path + '/file/metagenePlot.txt')
        metagene_x = []
        metagene_y = []
        for i in fh_metagenePlot:
            tmp_list = i.strip().split('\t')
            metagene_x.append(tmp_list[0])
            metagene_y.append(tmp_list[2])
        # print(metagene_x)
        # print(metagene_y)

        # print(l1[750:752])
        l1[750:752] = ['                                            x: [' + ','.join(metagene_x) + '],\n',
                       '                                            y: [' + ','.join(metagene_y) + '],\n']

        ## peak length distribution
        ## peakLengthInfo.txt
        fh_peakInfo = open(path + '/file/peakLengthInfo.txt')
        peakInfo_list = []
        for i in fh_peakInfo:
            peakInfo_list.append(i.strip().split('\t'))
        # print(peakInfo_list)

        # print(l1[843:847])
        l1[843:847] = ['\t\t\t\t\t\t\t\t\t\t\t<td>' + peakInfo_list[0][0] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + peakInfo_list[0][1] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + peakInfo_list[0][2] + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t<td>' + peakInfo_list[0][3] + '</td>\n']
        ## peakLength.txt
        fh_peakLen = open(path + '/file/peakLength.txt')
        peakLen_x = []
        peakLen_y = []

        for i in fh_peakLen:
            tmp_list = i.strip().split('\t')
            peakLen_x.append(tmp_list[0])
            peakLen_y.append(tmp_list[1])
        # print(peakLen_x)
        # print(peakLen_y)
        # print(l1[854:856])

        l1[854:856] = ['                                            x: [' + ','.join(peakLen_x) + '],\n',
                       '                                            y: [' + ','.join(peakLen_y) + '],\n']

        ## reference values
        ## referenceValues.txt
        fh_ref = open(path + '/file/referenceValues.txt')
        refValues_list = []
        for i in fh_ref:
            refValues_list.append(i.strip().split('\t'))
        # if (len(refValues_list)) == 7:
        #     print(refValues_list)

        # print(l1[916:917])
        l1[916:917] = ['\t\t\t\t\t\t\t\t\t\t\t<th>' + refValues_list[0][1] + '</th>\n']

        ## FRiP
        # print(l1[923:925])
        l1[923:925] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[1][1].strip('>') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][2] + '</td>\n']

        ## NRF
        # print(l1[928:930])
        l1[928:930] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[2][1].strip('>') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][2] + '</td>\n']
        ## Uniquely mapping read counts
        # print(l1[933:935])
        l1[933:935] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[3][1].strip('>') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][2] + '</td>\n']
        ## Detected gene counts
        # print(l1[938:940])
        l1[938:940] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[4][1].strip('>') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][2] + '</td>\n']
        ## Detected m6A peaks
        # print(l1[943:945])
        l1[943:945] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[5][1].strip('>') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][2] + '</td>\n']
        ## contamination ratio
        # print(l1[948:950])

        l1[948:950] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&lt;' + refValues_list[6][1].strip('<') + '</td>\n',
                       '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][2] + '</td>\n']

    elif replicateNumber == 2:
        # fh = open(htmlTemplate)
        # l1 = fh.readlines()
        ## uniquely mapping ratio
        fh_mappingRatio = open(path + '/file/uniquelyMappingRatio.txt')
        mappingRatio_dict = dict()
        for i in fh_mappingRatio:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            mappingRatio_dict[Key] = tmp_list
        # print(mappingRatio_dict)

        ## NRF
        fh_NRF = open(path + '/file/NRF.txt')
        NRF_dict = dict()
        for i in fh_NRF:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            NRF_dict[Key] = tmp_list
        # print(NRF_dict)

        ## PBC
        fh_PBC = open(path + '/file/PBC.txt')
        PBC_dict = dict()
        for i in fh_PBC:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            PBC_dict[Key] = tmp_list
        # print(PBC_dict)

        ## contamination
        fh_contamination = open(path + '/file/contamination.txt')
        contamination_dict = dict()
        for i in fh_contamination:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            contamination_dict[Key] = tmp_list
        # print(contamination_dict)

        ## FRiP
        fh_frip = open(path + '/file/frip.txt')
        frip_dict = dict()
        for i in fh_frip:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            frip_dict[Key] = tmp_list
        # print(frip_dict)

        ## uniquely mapping ratio
        # print(l1[136:142])
        ## IP_rep1
        l2 = []
        for item in mappingRatio_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[136:142] = l2
        ## input_rep1
        l2 = []
        for item in mappingRatio_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[144:150])
        l1[144:150] = l2
        ## IP_rep2
        l2 = []
        for item in mappingRatio_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[152:158])
        l1[152:158] = l2
        ## input_rep2
        l2 = []
        for item in mappingRatio_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[160:166])
        l1[160:166] = l2

        # print(l1[174:175])
        l1[174:175] = ['                                            y:[' + mappingRatio_dict['IP_rep1'][5].strip('%') + ', ' + mappingRatio_dict['IP_rep2'][5].strip('%') + '],\n']
        # print(l1[184:185])
        l1[184:185] = ['                                            y:[' + mappingRatio_dict['INPUT_rep1'][5].strip('%') + ', ' + mappingRatio_dict['INPUT_rep2'][5].strip('%') + '],\n']
        ## NRF
        ## IP_rep1
        l2 = []
        for item in NRF_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[241:247])
        l1[241:247] = l2

        ## input_rep1
        l2 = []
        for item in NRF_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[249:255])
        l1[249:255] = l2

        ## IP_rep2
        l2 = []
        for item in NRF_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[257:263])
        l1[257:263] = l2

        ## input_rep2
        l2 = []
        for item in NRF_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        # print(l1[265:271])
        l1[265:271] = l2

        # print(l1[278:279])
        l1[278:279] = ['                                            y:[' + NRF_dict['IP_rep1'][5].strip('%') + ', ' + NRF_dict['IP_rep2'][5].strip('%') + '],\n']
        # print(l1[288:289])
        l1[288:289] = ['                                            y:[' + NRF_dict['INPUT_rep1'][5].strip('%') + ', ' + NRF_dict['INPUT_rep2'][5].strip('%') + '],\n']

        ## PBC
        l2 = []
        # print(l1[345:351])
        for item in PBC_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[345:351] = l2

        l2 = []
        # print(l1[353:359])
        for item in PBC_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[353:359] = l2

        l2 = []
        # print(l1[361:367])
        for item in PBC_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[361:367] = l2

        l2 = []
        # print(l1[369:375])
        for item in PBC_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[369:375] = l2

        # print(l1[382:383])
        l1[382:383] = ['                                            y:[' + PBC_dict['IP_rep1'][5] + ', ' + PBC_dict['IP_rep2'][5] + '],\n']
        # print(l1[391:392])
        l1[391:392] = ['                                            y:[' + PBC_dict['INPUT_rep1'][5] + ', ' + PBC_dict['INPUT_rep2'][5] + '],\n']

        ## contamination ratio
        l2 = []
        # print(l1[447:454])
        for item in contamination_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[447:454] = l2

        l2 = []
        # print(l1[456:463])
        for item in contamination_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[456:463] = l2

        l2 = []
        # print(l1[465:472])
        for item in contamination_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[465:472] = l2

        l2 = []
        # print(l1[474:481])
        for item in contamination_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[474:481] = l2

        # print(l1[488:489])
        # print(l1[497:498])

        l1[488:489] = ['                                            y:[' + contamination_dict['IP_rep1'][6].strip('%') + ', ' + contamination_dict['IP_rep2'][6].strip('%') + '],\n']
        l1[497:498] = ['                                            y:[' + contamination_dict['INPUT_rep1'][6].strip('%') + ', ' + contamination_dict['INPUT_rep1'][6].strip('%') + '],\n']

        ## FRiP
        l2 = []
        # print(l1[759:765])
        for item in frip_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[759:765] = l2

        l2 = []
        # print(l1[767:773])
        for item in frip_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[767:773] = l2

        l2 = []
        # print(l1[775:781])
        for item in frip_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[775:781] = l2

        l2 = []
        # print(l1[783:789])
        for item in frip_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[783:789] = l2

        # print(l1[796:797])
        # print(l1[805:806])

        l1[796:797] = ['                                            y:[' + frip_dict['IP_rep1'][5].strip('%') + ', ' + frip_dict['IP_rep2'][5].strip('%') + '],\n']
        l1[805:806] = ['                                            y:[' + frip_dict['INPUT_rep1'][5].strip('%') + ', ' + frip_dict['INPUT_rep2'][5].strip('%') + '],\n']

        ## library saturation
        fh_saturationInfo = open(path + '/file/saturationInfo_table.txt')
        saturationInfo_dict = dict()
        for i in fh_saturationInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            saturationInfo_dict[Key] = tmp_list
        # print(saturationInfo_dict)

        # print(l1[551:555])
        l2 = []
        for item in saturationInfo_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[551:555] = l2

        # print(l1[557:561])
        l2 = []
        for item in saturationInfo_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[557:561] = l2

        # print(l1[563:567])
        l2 = []
        for item in saturationInfo_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[563:567] = l2

        l2 = []
        # print(l1[569:573])
        for item in saturationInfo_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[569:573] = l2

        ## saturation plot
        fh_saturationPlot = open(path + '/file/saturationInfo_plot.txt')
        saturationPlot_dict = dict()
        for i in fh_saturationPlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            if Key not in saturationPlot_dict:
                saturationPlot_dict[Key] = [[tmp_list[3]], [tmp_list[4]]]
            elif Key in saturationPlot_dict:
                saturationPlot_dict[Key][0].append(tmp_list[3])
                saturationPlot_dict[Key][1].append(tmp_list[4])
        # print(saturationPlot_dict)
        # IP_rep1
        # print(l1[579:581])
        # print(l1[582:583])
        l1[579:581] = ['                                            x: [' + ','.join(saturationPlot_dict['IP_rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['IP_rep1'][1]) + '],\n']
        l1[582:583] = ["                                            name: 'IP_rep1',\n"]
        ## input_rep1
        # print(l1[589:591])
        # print(l1[592:593])
        l1[589:591] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep1'][1]) + '],\n']
        l1[592:593] = ["                                            name: 'INPUT_rep1',\n"]
        ## IP_rep2
        # print(l1[599:601])
        # print(l1[602:603])
        l1[599:601] = ['                                            x: [' + ','.join(saturationPlot_dict['IP_rep2'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['IP_rep2'][1]) + '],\n']
        l1[602:603] = ["                                            name: 'IP_rep2',\n"]
        ## input_rep2
        # print(l1[609:611])
        # print(l1[612:613])
        l1[609:611] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep2'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep2'][1]) + '],\n']
        l1[612:613] = ["                                            name: 'INPUT_rep2',\n"]

        ## RDD
        fh_RDDinfo = open(path + '/file/stdevInfo.txt')
        RDDinfo_dict = dict()
        for i in fh_RDDinfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            RDDinfo_dict[Key] = tmp_list
        # print(RDDinfo_dict)

        ## rep1
        l2 = []
        # print(l1[673:678])
        for item in RDDinfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[673:678] = l2
        ## rep2
        l2 = []
        # print(l1[680:685])
        for item in RDDinfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[680:685] = l2

        fh_RDDplot = open(path + '/file/stdevPlot.txt')
        RDDplot_dict = dict()
        for i in fh_RDDplot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[1] + '_' + tmp_list[0]
            if Key not in RDDplot_dict:
                RDDplot_dict[Key] = [tmp_list[3]]
            elif Key in RDDplot_dict:
                RDDplot_dict[Key].append(tmp_list[3])
        # print(RDDplot_dict)

        n1, n2, n3, n4, n5 = RDDplot_dict['IP_rep1'][:]
        m1, m2, m3, m4, m5 = RDDplot_dict['IP_rep2'][:]
        RDDplot_IP = [n1, n2, n2, n3, n4, n4, n5, m1, m2, m2, m3, m4, m4, m5]
        # print(l1[693:694])
        l1[693:694] = ['                                            y: [' + ','.join(RDDplot_IP) + '],\n']
        # print(l1[702:703])
        n1, n2, n3, n4, n5 = RDDplot_dict['INPUT_rep1'][:]
        m1, m2, m3, m4, m5 = RDDplot_dict['INPUT_rep2'][:]
        RDDplot_input = [n1, n2, n2, n3, n4, n4, n5, m1, m2, m2, m3, m4, m4, m5]
        l1[702:703] = ['                                            y: [' + ','.join(RDDplot_input) + '],\n']

        ## metagene
        fh_metageneInfo = open(path + '/file/metageneInfo.txt')
        metageneInfo_dict = dict()
        for i in fh_metageneInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            metageneInfo_dict[Key] = tmp_list
        # print(metageneInfo_dict)
        l2 = []
        # print(l1[859:863])
        for item in metageneInfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[859:863] = l2

        l2 = []
        # print(l1[865:869])
        for item in metageneInfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[865:869] = l2

        fh_metagenePlot = open(path + '/file/metagenePlot.txt')
        metagenePlot_dict = dict()
        for i in fh_metagenePlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[3]
            if Key not in metagenePlot_dict:
                metagenePlot_dict[Key] = [[tmp_list[0]], [tmp_list[2]]]
            elif Key in metagenePlot_dict:
                metagenePlot_dict[Key][0].append(tmp_list[0])
                metagenePlot_dict[Key][1].append(tmp_list[2])
        # print(metagenePlot_dict)

        ## rep1
        # print(l1[876:878])
        l1[876:878] = ['                                            x: [' + ','.join(metagenePlot_dict['rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(metagenePlot_dict['rep1'][1]) + '],\n']
        ## rep2
        # print(l1[887:889])
        l1[887:889] = ['                                            x: [' + ','.join(metagenePlot_dict['rep2'][0]) + '],\n',
                       '                                            y: [' + ','.join(metagenePlot_dict['rep2'][1]) + '],\n']

        ## peak length
        fh_peakLenInfo = open(path + '/file/peakLengthInfo.txt')
        peakLenInfo_dict = dict()
        for i in fh_peakLenInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            peakLenInfo_dict[Key] = tmp_list
        # print(peakLenInfo_dict)
        ## rep1
        # print(l1[980:984])
        l2 = []
        for item in peakLenInfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[980:984] = l2
        ## rep2
        # print(l1[986:990])
        l2 = []
        for item in peakLenInfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[986:990] = l2

        fh_peakLenPlot = open(path + '/file/peakLength.txt')
        peakLenPlot_dict = dict()
        for i in fh_peakLenPlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2]
            if Key not in peakLenPlot_dict:
                peakLenPlot_dict[Key] = [[tmp_list[0]], [tmp_list[1]]]
            elif Key in peakLenPlot_dict:
                peakLenPlot_dict[Key][0].append(tmp_list[0])
                peakLenPlot_dict[Key][1].append(tmp_list[1])
        # print(peakLenPlot_dict)
        ## rep1
        # print(l1[997:999])
        l1[997:999] = ['                                            x: [' + ','.join(peakLenPlot_dict['rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(peakLenPlot_dict['rep1'][1]) + '],\n']
        ## rep2
        # print(l1[1008:1010])
        l1[1008:1010] = [
            '                                            x: [' + ','.join(peakLenPlot_dict['rep2'][0]) + '],\n',
            '                                            y: [' + ','.join(peakLenPlot_dict['rep2'][1]) + '],\n']

        ## overlapping peak length
        fh_overlapPeak = open(path + '/file/peak_overlap_length_fraction.txt')
        ovelapPeak_dict = dict()
        for i in fh_overlapPeak:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            ovelapPeak_dict[Key] = tmp_list
        # print(ovelapPeak_dict)
        ## rep1
        # print(l1[1072:1078])
        l2 = []
        for item in ovelapPeak_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1072:1078] = l2
        ## rep2
        # print(l1[1080:1086])
        l2 = []
        for item in ovelapPeak_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1080:1086] = l2
        ## reference values
        fh_refValues = open(path + '/file/referenceValues.txt')
        refValues_list = []
        for i in fh_refValues:
            refValues_list.append(i.strip().split('\t'))
        # print(refValues_list)

        # print(l1[1097:1098])
        l1[1097:1098] = ['\t\t\t\t\t\t\t\t\t\t\t<th>' + refValues_list[0][1] + '</th>\n']
        # FRiP
        # print(l1[1105:1108])
        l1[1105:1108] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[1][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][3] + '</td>\n']
        # NRF
        # print(l1[1111:1114])
        l1[1111:1114] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[2][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][3] + '</td>\n']
        # Uniquely Mapping Read Counts
        # print(l1[1117:1120])
        l1[1117:1120] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[3][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][3] + '</td>\n']
        # Detected Gene Counts
        # print(l1[1123:1126])
        l1[1123:1126] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[4][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][3] + '</td>\n']
        # Detected m6A Peak Counts
        # print(l1[1129:1132])
        l1[1129:1132] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[5][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][3] + '</td>\n']
        # Contamination Ratio
        # print(l1[1135:1138])
        l1[1135:1138] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&lt;' + refValues_list[6][1].strip('<') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][3] + '</td>\n']

    elif replicateNumber == 3:
        # fh = open(htmlTemplate)
        # l1 = fh.readlines()
        ## uniquely mapping ratio
        fh_mappingRatio = open(path + '/file/uniquelyMappingRatio.txt')
        mappingRatio_dict = dict()
        for i in fh_mappingRatio:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            mappingRatio_dict[Key] = tmp_list
        # print(mappingRatio_dict)

        ## NRF
        fh_NRF = open(path + '/file/NRF.txt')
        NRF_dict = dict()
        for i in fh_NRF:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            NRF_dict[Key] = tmp_list
        # print(NRF_dict)

        ## PBC
        fh_PBC = open(path + '/file/PBC.txt')
        PBC_dict = dict()
        for i in fh_PBC:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            PBC_dict[Key] = tmp_list
        # print(PBC_dict)

        ## contamination
        fh_contamination = open(path + '/file/contamination.txt')
        contamination_dict = dict()
        for i in fh_contamination:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            contamination_dict[Key] = tmp_list
        # print(contamination_dict)

        ## FRiP
        fh_frip = open(path + '/file/frip.txt')
        frip_dict = dict()
        for i in fh_frip:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            frip_dict[Key] = tmp_list
        # print(frip_dict)

        ## Uniquely Mapping Ratio
        # IP_rep1
        # print(l1[138:144])
        l2 = []
        for item in mappingRatio_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[138:144] = l2
        ## input_rep1
        # print(l1[146:152])
        l2 = []
        for item in mappingRatio_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[146:152] = l2
        ## IP_rep2
        # print(l1[154:160])
        l2 = []
        for item in mappingRatio_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[154:160] = l2
        ## input_rep2
        # print(l1[162:168])
        l2 = []
        for item in mappingRatio_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[162:168] = l2
        ## IP_rep3
        # print(l1[170:176])
        l2 = []
        for item in mappingRatio_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[170:176] = l2
        ## input_rep3
        # print(l1[178:184])
        l2 = []
        for item in mappingRatio_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[178:184] = l2

        # print(l1[192:193])
        l1[192:193] = ['                                            y:[' + mappingRatio_dict['IP_rep1'][5].strip('%') + ', ' + mappingRatio_dict['IP_rep2'][5].strip('%') + ', ' + mappingRatio_dict['IP_rep3'][5].strip('%') + '],\n']
        # print(l1[202:203])
        l1[202:203] = ['                                            y:[' + mappingRatio_dict['INPUT_rep1'][5].strip('%') + ', ' + mappingRatio_dict['INPUT_rep2'][5].strip('%') + ', ' + mappingRatio_dict['INPUT_rep3'][5].strip('%') + '],\n']
        # NRF
        # IP_rep1
        # print(l1[259:265])
        l2 = []
        for item in NRF_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[259:265] = l2
        # input_rep1
        # print(l1[267:273])
        l2 = []
        for item in NRF_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[267:273] = l2
        ## IP_rep2
        # print(l1[275:281])
        l2 = []
        for item in NRF_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[275:281] = l2
        ## input_rep2
        # print(l1[283:289])
        l2 = []
        for item in NRF_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[283:289] = l2
        ## IP_rep3
        # print(l1[291:297])
        l2 = []
        for item in NRF_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[291:297] = l2
        ## input_rep3
        # print(l1[299:305])
        l2 = []
        for item in NRF_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[299:305] = l2
        # print(l1[313:314])
        l1[313:314] = ['                                            y:[' + NRF_dict['IP_rep1'][5].strip('%') + ', ' + NRF_dict['IP_rep2'][5].strip('%') + ', ' + NRF_dict['IP_rep3'][5].strip('%') + '],\n']
        # print(l1[323:324])
        l1[323:324] = ['                                            y:[' + NRF_dict['INPUT_rep1'][5].strip('%') + ', ' + NRF_dict['INPUT_rep2'][5].strip('%') + ', ' + NRF_dict['INPUT_rep3'][5].strip('%') + '],\n']
        # PBC
        ## IP_rep1
        # print(l1[379:385])
        l2 = []
        for item in PBC_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[379:385] = l2
        ## input_rep1
        # print(l1[387:393])
        l2 = []
        for item in PBC_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[387:393] = l2
        ## IP_rep2
        # print(l1[395:401])
        l2 = []
        for item in PBC_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[395:401] = l2
        ## input_rep2
        # print(l1[403:409])
        l2 = []
        for item in PBC_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[403:409] = l2
        ## IP_rep3
        # print(l1[411:417])
        l2 = []
        for item in PBC_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[411:417] = l2
        ## input_rep3
        # print(l1[419:425])
        l2 = []
        for item in PBC_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[419:425] = l2
        # print(l1[432:433])
        l1[432:433] = ['                                            y:[' + PBC_dict['IP_rep1'][5] + ', ' + PBC_dict['IP_rep2'][5] + ', ' + PBC_dict['IP_rep3'][5] + '],\n']
        # print(l1[441:442])
        l1[441:442] = ['                                            y:[' + PBC_dict['INPUT_rep1'][5] + ', ' + PBC_dict['INPUT_rep2'][5] + ', ' + PBC_dict['INPUT_rep3'][5] + '],\n']
        ## contamination ratio
        # IP_rep1
        # print(l1[497:504])
        l2 = []
        for item in contamination_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[497:504] = l2
        # input_rep1
        # print(l1[506:513])
        l2 = []
        for item in contamination_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[506:513] = l2
        # IP_rep2
        # print(l1[515:522])
        l2 = []
        for item in contamination_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[515:522] = l2
        # input_rep2
        # print(l1[524:531])
        l2 = []
        for item in contamination_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[524:531] = l2
        # IP_rep3
        # print(l1[533:540])
        l2 = []
        for item in contamination_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[533:540] = l2
        # input_rep3
        # print(l1[542:549])
        l2 = []
        for item in contamination_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[542:549] = l2
        # print(l1[556:557])
        l1[556:557] = ['                                            y:[' + contamination_dict['IP_rep1'][6].strip('%') + ', ' + contamination_dict['IP_rep2'][6].strip('%') + ', ' + contamination_dict['IP_rep3'][6].strip('%') + '],\n']
        # print(l1[565:566])
        l1[565:566] = ['                                            y:[' + contamination_dict['INPUT_rep1'][6].strip('%') + ', ' + contamination_dict['INPUT_rep2'][6].strip('%') + ', ' + contamination_dict['INPUT_rep3'][6].strip('%') + '],\n']
        ## FRiP
        # IP_rep1
        # print(l1[865:871])
        l2 = []
        for item in frip_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[865:871] = l2
        # input_rep1
        # print(l1[873:879])
        l2 = []
        for item in frip_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[873:879] = l2
        # IP_rep2
        # print(l1[881:887])
        l2 = []
        for item in frip_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[881:887] = l2
        # input_rep2
        # print(l1[889:895])
        l2 = []
        for item in frip_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[889:895] = l2
        # IP_rep3
        # print(l1[897:903])
        l2 = []
        for item in frip_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[897:903] = l2
        # input_rep3
        # print(l1[905:911])
        l2 = []
        for item in frip_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[905:911] = l2
        # print(l1[918:919])
        l1[918:919] = ['                                            y:[' + frip_dict['IP_rep1'][5].strip('%') + ', ' + frip_dict['IP_rep2'][5].strip('%') + ', ' + frip_dict['IP_rep3'][5].strip('%') + '],\n']
        # print(l1[927:928])
        l1[927:928] = ['                                            y:[' + frip_dict['INPUT_rep1'][5].strip('%') + ', ' + frip_dict['INPUT_rep2'][5].strip('%') + ', ' + frip_dict['INPUT_rep3'][5].strip('%') + '],\n']
        ## library saturation
        fh_saturationInfo = open(path + '/file/saturationInfo_table.txt')
        saturationInfo_dict = dict()
        for i in fh_saturationInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            saturationInfo_dict[Key] = tmp_list
        # print(saturationInfo_dict)
        # IP_rep1
        # print(l1[619:623])
        l2 = []
        for item in saturationInfo_dict['IP_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[619:623] = l2
        ## IP_rep2
        # print(l1[625:629])
        l2 = []
        for item in saturationInfo_dict['IP_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[625:629] = l2
        ## IP_rep3
        # print(l1[631:635])
        l2 = []
        for item in saturationInfo_dict['IP_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[631:635] = l2
        ## input_rep1
        # print(l1[637:641])
        l2 = []
        for item in saturationInfo_dict['INPUT_rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[637:641] = l2
        ## input_rep2
        # print(l1[643:647])
        l2 = []
        for item in saturationInfo_dict['INPUT_rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[643:647] = l2
        ## input_rep3
        # print(l1[649:653])
        l2 = []
        for item in saturationInfo_dict['INPUT_rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[649:653] = l2
        fh_saturationPlot = open(path + '/file/saturationInfo_plot.txt')
        saturationPlot_dict = dict()
        for i in fh_saturationPlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2] + '_' + tmp_list[0]
            if Key not in saturationPlot_dict:
                saturationPlot_dict[Key] = [[tmp_list[3]], [tmp_list[4]]]
            elif Key in saturationPlot_dict:
                saturationPlot_dict[Key][0].append(tmp_list[3])
                saturationPlot_dict[Key][1].append(tmp_list[4])
        # print(saturationPlot_dict)
        ## IP_rep1
        # print(l1[659:661])
        # print(l1[662:663])
        l1[659:661] = [
            '                                            x: [' + ','.join(saturationPlot_dict['IP_rep1'][0]) + '],\n',
            '                                            y: [' + ','.join(saturationPlot_dict['IP_rep1'][1]) + '],\n']
        l1[662:663] = ["                                            name: 'IP_rep1',\n"]
        ## input_rep1
        # print(l1[669:671])
        # print(l1[672:673])
        l1[669:671] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep1'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep1'][1]) + '],\n']
        l1[672:673] = ["                                            name: 'INPUT_rep1',\n"]
        ## IP_rep2
        # print(l1[679:681])
        # print(l1[682:683])
        l1[679:681] = [
            '                                            x: [' + ','.join(saturationPlot_dict['IP_rep2'][0]) + '],\n',
            '                                            y: [' + ','.join(saturationPlot_dict['IP_rep2'][1]) + '],\n']
        l1[682:683] = ["                                            name: 'IP_rep2',\n"]
        ## input_rep2
        # print(l1[689:691])
        # print(l1[692:693])
        l1[689:691] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep2'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep2'][1]) + '],\n']
        l1[692:693] = ["                                            name: 'INPUT_rep2',\n"]
        ## IP_rep3
        # print(l1[699:701])
        # print(l1[702:703])
        l1[699:701] = [
            '                                            x: [' + ','.join(saturationPlot_dict['IP_rep3'][0]) + '],\n',
            '                                            y: [' + ','.join(saturationPlot_dict['IP_rep3'][1]) + '],\n']
        l1[702:703] = ["                                            name: 'IP_rep3',\n"]
        ## input_rep3
        # print(l1[709:711])
        # print(l1[712:713])
        l1[709:711] = ['                                            x: [' + ','.join(saturationPlot_dict['INPUT_rep3'][0]) + '],\n',
                       '                                            y: [' + ','.join(saturationPlot_dict['INPUT_rep3'][1]) + '],\n']
        l1[712:713] = ["                                            name: 'INPUT_rep3',\n"]
        ## RDD
        fh_RDDinfo = open(path + '/file/stdevInfo.txt')
        RDDinfo_dict = dict()
        for i in fh_RDDinfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            RDDinfo_dict[Key] = tmp_list
        # print(RDDinfo_dict)
        # rep1
        # print(l1[773:778])
        l2 = []
        for item in RDDinfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[773:778] = l2
        # rep2
        # print(l1[780:785])
        l2 = []
        for item in RDDinfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[780:785] = l2
        # rep3
        # print(l1[787:792])
        l2 = []
        for item in RDDinfo_dict['rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[787:792] = l2
        fh_RDDplot = open(path + '/file/stdevPlot.txt')
        RDDplot_dict = dict()
        for i in fh_RDDplot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[1] + '_' + tmp_list[0]
            if Key not in RDDplot_dict:
                RDDplot_dict[Key] = [tmp_list[3]]
            elif Key in RDDplot_dict:
                RDDplot_dict[Key].append(tmp_list[3])
        # print(RDDplot_dict)
        n1, n2, n3, n4, n5 = RDDplot_dict['IP_rep1'][:]
        m1, m2, m3, m4, m5 = RDDplot_dict['IP_rep2'][:]
        k1, k2, k3, k4, k5 = RDDplot_dict['IP_rep3'][:]
        RDDplot_IP = [n1, n2, n2, n3, n4, n4, n5, m1, m2, m2, m3, m4, m4, m5, k1, k2, k2, k3, k4, k4, k5]
        # print(l1[800:801])
        l1[800:801] = ['                                            y: [' + ','.join(RDDplot_IP) + '],\n']
        # print(l1[809:810])
        n1, n2, n3, n4, n5 = RDDplot_dict['INPUT_rep1'][:]
        m1, m2, m3, m4, m5 = RDDplot_dict['INPUT_rep2'][:]
        k1, k2, k3, k4, k5 = RDDplot_dict['INPUT_rep3'][:]
        RDDplot_input = [n1, n2, n2, n3, n4, n4, n5, m1, m2, m2, m3, m4, m4, m5, k1, k2, k2, k3, k4, k4, k5]
        l1[809:810] = ['                                            y: [' + ','.join(RDDplot_input) + '],\n']
        ## metagene
        fh_metageneInfo = open(path + '/file/metageneInfo.txt')
        metageneInfo_dict = dict()
        for i in fh_metageneInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            metageneInfo_dict[Key] = tmp_list
        # print(metageneInfo_dict)
        # rep1
        # print(l1[981:985])
        l2 = []
        for item in metageneInfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[981:985] = l2
        # rep2
        # print(l1[987:991])
        l2 = []
        for item in metageneInfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[987:991] = l2
        # rep3
        # print(l1[993:997])
        l2 = []
        for item in metageneInfo_dict['rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[993:997] = l2
        fh_metagenePlot = open(path + '/file/metagenePlot.txt')
        metagenePlot_dict = dict()
        for i in fh_metagenePlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[3]
            if Key not in metagenePlot_dict:
                metagenePlot_dict[Key] = [[tmp_list[0]], [tmp_list[2]]]
            elif Key in metagenePlot_dict:
                metagenePlot_dict[Key][0].append(tmp_list[0])
                metagenePlot_dict[Key][1].append(tmp_list[2])
        # print(metagenePlot_dict)
        # rep1
        # print(l1[1004:1006])
        l1[1004:1006] = [
            '                                            x: [' + ','.join(metagenePlot_dict['rep1'][0]) + '],\n',
            '                                            y: [' + ','.join(metagenePlot_dict['rep1'][1]) + '],\n']
        # rep2
        # print(l1[1015:1017])
        l1[1015:1017] = [
            '                                            x: [' + ','.join(metagenePlot_dict['rep2'][0]) + '],\n',
            '                                            y: [' + ','.join(metagenePlot_dict['rep2'][1]) + '],\n']
        # rep3
        # print(l1[1026:1028])
        l1[1026:1028] = [
            '                                            x: [' + ','.join(metagenePlot_dict['rep3'][0]) + '],\n',
            '                                            y: [' + ','.join(metagenePlot_dict['rep3'][1]) + '],\n']
        ## peak length
        fh_peakLenInfo = open(path + '/file/peakLengthInfo.txt')
        peakLenInfo_dict = dict()
        for i in fh_peakLenInfo:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[0]
            peakLenInfo_dict[Key] = tmp_list
        # print(peakLenInfo_dict)
        # rep1
        # print(l1[1119:1123])
        l2 = []
        for item in peakLenInfo_dict['rep1']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1119:1123] = l2
        # rep2
        # print(l1[1125:1129])
        l2 = []
        for item in peakLenInfo_dict['rep2']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1125:1129] = l2
        # rep3
        # print(l1[1131:1135])
        l2 = []
        for item in peakLenInfo_dict['rep3']:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1131:1135] = l2
        fh_peakLenPlot = open(path + '/file/peakLength.txt')
        peakLenPlot_dict = dict()
        for i in fh_peakLenPlot:
            tmp_list = i.strip().split('\t')
            Key = tmp_list[2]
            if Key not in peakLenPlot_dict:
                peakLenPlot_dict[Key] = [[tmp_list[0]], [tmp_list[1]]]
            elif Key in peakLenPlot_dict:
                peakLenPlot_dict[Key][0].append(tmp_list[0])
                peakLenPlot_dict[Key][1].append(tmp_list[1])
        # print(peakLenPlot_dict)
        # rep1
        # print(l1[1142:1144])
        l1[1142:1144] = [
            '                                            x: [' + ','.join(peakLenPlot_dict['rep1'][0]) + '],\n',
            '                                            y: [' + ','.join(peakLenPlot_dict['rep1'][1]) + '],\n']
        # rep2
        # print(l1[1153:1155])
        l1[1153:1155] = [
            '                                            x: [' + ','.join(peakLenPlot_dict['rep2'][0]) + '],\n',
            '                                            y: [' + ','.join(peakLenPlot_dict['rep2'][1]) + '],\n']
        # rep3
        # print(l1[1164:1166])
        l1[1164:1166] = [
            '                                            x: [' + ','.join(peakLenPlot_dict['rep3'][0]) + '],\n',
            '                                            y: [' + ','.join(peakLenPlot_dict['rep3'][1]) + '],\n']
        fh_overlapPeak = open(path + '/file/peak_overlap_length_fraction.txt')
        overlapPeak_list = []
        for i in fh_overlapPeak:
            overlapPeak_list.append(i.strip().split('\t'))
        # print(overlapPeak_list)
        ## rep1 & rep2
        # rep1
        # print(l1[1228:1234])
        l2 = []
        for item in overlapPeak_list[0]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1228:1234] = l2
        # rep2
        # print(l1[1236:1242])
        l2 = []
        for item in overlapPeak_list[1]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1236:1242] = l2
        ## rep1 & rep3
        # rep1
        # print(l1[1252:1258])
        l2 = []
        for item in overlapPeak_list[2]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1252:1258] = l2
        # rep3
        # print(l1[1260:1266])
        l2 = []
        for item in overlapPeak_list[3]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1260:1266] = l2
        ## rep2 & rep3
        # rep2
        # print(l1[1276:1282])
        l2 = []
        for item in overlapPeak_list[4]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1276:1282] = l2
        # rep3
        # print(l1[1284:1290])
        l2 = []
        for item in overlapPeak_list[5]:
            line = '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + item + '</td>\n'
            l2.append(line)
        l1[1284:1290] = l2
        ## reference values
        fh_refValues = open(path + '/file/referenceValues.txt')
        refValues_list = []
        for i in fh_refValues:
            refValues_list.append(i.strip().split('\t'))
        # print(refValues_list)
        # header
        # print(l1[1301:1302])
        l1[1301:1302] = ['\t\t\t\t\t\t\t\t\t\t\t<th>' + refValues_list[0][1] + '</th>\n']
        # frip
        # print(l1[1310:1314])
        l1[1310:1314] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[1][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[1][4] + '</td>\n']
        # NRF
        # print(l1[1317:1321])
        l1[1317:1321] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[2][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[2][4] + '</td>\n']
        # Uniquely Mapping Read Counts
        # print(l1[1324:1328])
        l1[1324:1328] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[3][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[3][4] + '</td>\n']
        # Detected Gene Counts
        # print(l1[1331:1335])
        l1[1331:1335] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[4][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[4][4] + '</td>\n']
        # Detected m6A Peak Counts
        # print(l1[1338:1342])
        l1[1338:1342] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&gt;' + refValues_list[5][1].strip('>') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[5][4] + '</td>\n']
        # Contamination Ratio
        # print(l1[1345:1349])
        l1[1345:1349] = ['\t\t\t\t\t\t\t\t\t\t\t\t<td>&lt;' + refValues_list[6][1].strip('<') + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][2] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][3] + '</td>\n',
                         '\t\t\t\t\t\t\t\t\t\t\t\t<td>' + refValues_list[6][4] + '</td>\n']
    ## output
    out = open(path + '/QC_reports.html', 'w')
    for i in l1:
        out.write(i)
    out.close()
    return



















