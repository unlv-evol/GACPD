import os
import sys
from GACPD.GACPD import  GACPD


token_list = []
token_file = 'tokens.txt'
with open(token_file, 'r') as f:
    for line in f.readlines():
        token_list.append(line.strip('\n'))

data = ('1', 'apache/kafka', 'linkedin/kafka', token_list, '', '')

example = GACPD(data)

example.get_dates()

prs_source = example.extractPatches('2022-06-02T17:08:43Z', '2022-06-18T17:08:43Z')

example.dfPatches()

example.runClassification(prs_source)

example.dfPatchClass()
example.dfFileClass()
example.dfFileClass().to_csv('test-GACPD.csv')

