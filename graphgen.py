import numpy as np
#import networkx as netx

#csv file = csv
dir = 'mlcontrib/'
names = open(dir+'files.txt','r').read()
filelist = names.split()
print filelist
allcommon = []
f = open(dir+'ml-collaborators.txt', 'w')
allCollaborators = {}
projects = []
matrix = []
allcommon = []
for i in range(len(filelist)):
    projectName = filelist[i].split('contributors')[0]
    projects.append(projectName)
    data1 = open(dir+filelist[i], 'r').read()
    data1 = data1.split()
    matrix.append([0]*len(allCollaborators))
    for c in data1:
        if c not in allCollaborators:
            allCollaborators[c] = len(allCollaborators)#next index
            for j in range(len(matrix)):
                matrix[j].append(0)
        else:
            print allCollaborators[c]
        matrix[i][allCollaborators[c]] = 1


    for j in range(i+1,len(filelist)):
        #if j <= i: #not taking any common pairs
        #name = tuple(filelist[i],filelist[j-i])
        
        data2 = open(dir+filelist[j], 'r').read()


        #data2 - file.open(filelist[j-(i+1), 'r'])
        
        data2 = data2.split()
        common = list(set(data1).intersection(data2))
        #allcommon[name]  = common
        allcommon.append(common)
        #commented out list generate a dictionary of common contributors for every pair of files, including equivalent pairs(returns all contributors)
print allcommon
print len(allCollaborators)
for row in matrix:
    print row
f.write("dl nr={} nc={} format=fullmatrix\n".format(len(projects),len(allCollaborators)))
f.write("row labels:\n")
for p in projects:
    f.write(p+' ')
f.write('\n')
f.write('column labels:\n')
for x in sorted(allCollaborators.items(),key=lambda x:x[1]):
    f.write(x[0]+' ')
f.write('\n')
for row in matrix:
    for i in row:
        f.write(str(i)+' ')
    f.write('\n')
f.close()