import repo_info
import json

dir = 'mlcontrib/'
names = open(dir+'files.txt','r').read()
filelist = names.split()

print filelist

repo_collabs = {'Theano': 'Theano','caffe': 'BVLC','CNTK': 'Microsoft','tensorflow': 'tensorflow', 'torch7': 'torch', 'deeplearning4j': 'deeplearning4j'}

# for n in filelist:
#     x = n.split('contributors')[0]
#     print x
#     print repo_collabs[x]

#dictionary: 
#base repo name : list of forked repos
#maybe?? 


#all collaborators mapped name:index
#collaborator name : index in matrix
allCollaborators = {}
#names of all projects, indexes corresponding with the index in matrix
#project name : index in matrix
projects = {}
#matrix of projects (rows) and contributors (columns)
matrix = []
for i in range(len(filelist)):
	matrix.append([0]*len(allCollaborators))
#index of the next new repo introduced via contributor
extraIndexes = len(filelist)

def addCol(adjMatrix):
    """Adds a column to the end of adjMatrix and returns the index of the comlumn that was added"""
    for j in range(len(adjMatrix)):
        adjMatrix[j].append(0)
    return len(adjMatrix[0])-1


for i in range(len(filelist)):
    print 'repo'
    allContribRepos = {}
    projectName = filelist[i].split('contributors')[0]
    projects[(projectName, repo_collabs[projectName])]=i
    data1 = open(dir+filelist[i], 'r').read()
    data1 = data1.split()
    for c in data1:
        if c not in allCollaborators:
            allCollaborators[c] = addCol(matrix)#next index
        matrix[i][allCollaborators[c]] = 1
        individualRepos = repo_info.get_contributions([c])[c]
        for fork in individualRepos:
        	index = extraIndexes
        	if fork in projects.keys():
        		index = projects[fork]
        	else:
        		extraIndexes+=1
        		projects[fork]=index
        		matrix.append([0]*len(allCollaborators.keys()))
        	matrix[projects[fork]][allCollaborators[c]] = 1
        allContribRepos[c] = individualRepos
    rawfile = open(projectName+'ContribRepos', 'w')
    json.dump(obj=allContribRepos,fp=rawfile)
    rawfile.close()
f=open('extendedcontributorsnew.txt','w')
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





