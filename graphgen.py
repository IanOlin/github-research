import numpy as np
import networkx as netx
#csv file = csv
names = file.open('files.txt','r')
filelist = names.split()
allcommon = []
#allcommon = {}
for i in xrange(filelist):
    for j in xrange(filelist):
        #name = tuple(filelist[i],filelist[j-i])
        data1 = file.open(filelist[i], 'r')
        data2 = file.open(filelist[j-i], 'r')
        #data2 - file.open(filelist[j-(i+1), 'r'])
        data1 = data1.split()
        data2 = data2.split()
        common = list(set(data1).intersection(data2))
        #allcommon[name]  = common
        allcommon.append(common)
        #commented out list generate a dictionary of common contributors for every pair of files, including equivalent pairs(returns all contributors)

netx.to_networkx_graph(allcommon[])
