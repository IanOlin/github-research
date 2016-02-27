import numpy as np
import networkx as netx
#csv file = csv
names = open('files.txt','r').read()
filelist = names.split()
print filelist
allcommon = []
#allcommon = {}
for i in range(len(filelist)):
    for j in range(len(filelist)-1):
        if j <= i: #not taking any common pairs
            #name = tuple(filelist[i],filelist[j-i])
            data1 = open(filelist[i], 'r').read()
            data2 = open(filelist[j+1-i], 'r').read()
            #data2 - file.open(filelist[j-(i+1), 'r'])
            data1 = data1.split()
            data2 = data2.split()
            common = list(set(data1).intersection(data2))
            #allcommon[name]  = common
            allcommon.append(common)
            #commented out list generate a dictionary of common contributors for every pair of files, including equivalent pairs(returns all contributors)
print allcommon
