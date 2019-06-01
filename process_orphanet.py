# -*- coding: UTF-8 -*-
#
# process_orphanet.py es_product1.xml
#
# Extracts term data from orphanet XML file.
#
#  <JDBOR date="2018-07-01 04:07:17" version="1.2.11 / 4.1.6 [2018-04-12] (orientdb version)" copyright="Orphanet (c) 2018">
#   <DisorderList count="9545">
#    <Disorder id="102">
# Term string: <Name lang="es">Epilepsia mioclónica ast?tica</Name>
# Synonyms: <SynonymList count="2">
#           <Synonym lang="es">Epilepsia miocl?nica progresiva tipo 2</Synonym>
#           </SynonymList>
#
# Codes in reference terminologies (UMLS cui, codes in terminologies)
#           <ExternalReferenceList count="14">
#               <ExternalReference id="104833">
#               <Source>MeSH</Source>
#               <Reference>D020190</Reference>
#           (...)
#           </ExternalReference>
#           <ExternalReference id="104834">
#               <Source>UMLS</Source>
#               <Reference>C0270853</Reference>
#           (...)
#           </ExternalReference>
#           <ExternalReference id="104835">
#               <Source>MedDRA</Source>
#               <Reference>10071082</Reference>
#           (...)
#           <ExternalReference id="11902">  => Puede haber varios elementos OMIM
#                <Source>OMIM</Source>
#                <Reference>604827</Reference>
#           (...)
#           <ExternalReference id="104837">
#                <Source>ICD-10</Source>
#                <Reference>G40.3</Reference>
#
# Output:
#
#   C0751783|epilepsia mioclónica progresiva tipo 2|epilepsia mioclónica progresiva tipo 2; epilepsias mioclónicas progresivas tipo 2|OMIM:254780;MSHSPA:D020192;MDRSPA:10054030;ICD10SPA2016:G40.3|
#
#
# Note that Python 3 has processed better the UTF8 characters.
#
# NLPMedTerm project, funded by European Union’s Horizon 2020 research and innovation programme
# Marie Skodowska-Curie grant agreement No. 713366 (Intertalentum UAM)
# L. Campillos
# 2019
#
#########################################################################

import re
import io
import os
import sys
# Use the following lines to avoid encoding errors with UTF8
#reload(sys)
#sys.setdefaultencoding('utf8')
import time
from xml.etree.ElementTree import parse as ET

# Indicate encoding as 'iso-8859-1' or 'utf-8'

PrintFileName = re.sub("\..+", "", sys.argv[1]) + ".processed"

print("Processing...")

count_lines = 0

entry_id = 0

Data = {}

tree = ET(sys.argv[1])

root = tree.getroot()

for opening_tag in root.iter('JDBOR'):
    for list in opening_tag.iter('DisorderList'):
        for disorder in list.iter('Disorder'):
            entry_id += 1
            name = disorder.find('Name').text
            # Synonyms
            SynList = []
            for syn_list in disorder.findall('SynonymList'):
                Syns = syn_list.findall('Synonym')
                for syn in Syns:
                    syn = syn.text
                    SynList.append(syn.lower())
            # Codes in terminologies
            Codes=[]
            CUI = ""
            for ref_list in disorder.findall('ExternalReferenceList'):
                for ref in ref_list.findall('ExternalReference'):
                    source = ref.find('Source').text
                    source_code = ref.find('Reference').text
                    if source == "UMLS":
                        CUI = source_code
                    else:
                        Codes.append(source + ":" +source_code)
            if CUI != "":
                Data[entry_id] = {'name': name.lower(), 'syns':SynList, 'codes':Codes, 'cui':CUI}

PrintFile = open(PrintFileName,'w',encoding='utf-8')

for k in Data:
    name = Data[k]['name']
    cui = Data[k]['cui']
    codes = ";".join(Data[k]['codes'])
    print(cui + "|" + name + "|" + str(codes) + "|", file=PrintFile)
    SynList = Data[k]['syns']
    for syn in SynList:
        print(cui + "|" + syn + "|" + str(codes) + "|", file=PrintFile)

PrintFile.close()

print("Done!")