import repo_info

dir = 'mlcontrib/'
names = open(dir+'files.txt','r').read()
filelist = names.split()
print filelist

#dictionary: 
#base repo name : list of forked repos
#maybe??

#all collaborators mapped name:index
allCollaborators = {}
#names of all projects, indexes corresponding with the index in matrix
projects = {}
#matrix of projects (rows) and contributors (columns)
matrix = []
for i in range(len(filelist)):
	matrix.append([0]*len(allCollaborators))

extraIndexes = len(filelist)
for i in range(len(filelist)):
    projectName = filelist[i].split('contributors')[0]
    projects[projectName]=i
    data1 = open(dir+filelist[i], 'r').read()
    data1 = data1.split()
    for c in data1:
        if c not in allCollaborators:
            allCollaborators[c] = addCol(matrix)#next index
        else:
            print allCollaborators[c]
        matrix[i][allCollaborators[c]] = 1
        individualReposForked = repo_info.get_repos(c)[c][1]
        for fork in individualReposForked:
        	index = extraIndexes
        	if fork in projects.keys():
        		index = project[fork]
        	else:
        		extraIndexes+=1
        		projects[fork]=index
        		matrix.append([0]*len(allCollaborators)))
        	matrix[projects[fork]][allCollaborators[c]] = 1
f=open('extendedcontributors.txt','w'ml)
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


def addCol(adjMatrix):
	"""Adds a column to the end of adjMatrix and returns the index of the comlumn that was added"""
	for j in range(len(matrix)):
        matrix[j].append(0)
    return len(matrix[0])-1

