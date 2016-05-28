import repo_info
import json

"""
Gets the repos each of the 675 contributors owns + fored repos
matrix contains owned repos and parent repos of the repos the contributors forked
not included:
    local forks of repos
    repos where user has contributed via collaborator commit rights, but nobody ahs forked
    organization repos
"""
dir = 'mlcontrib/'
names = open(dir+'files.txt','r').read()
filelist = names.split()
print filelist

repo_collabs = {'Theano': 'Theano','caffe': 'BVLC','CNTK': 'Microsoft','tensorflow': 'tensorflow', 'torch7': 'torch', 'deeplearning4j': 'deeplearning4j'}

#all collaborators mapped name:index
#collaborator name : index in matrix
allCollaborators = {}
#names of all projects, indexes corresponding with the index in matrix
#project name : index in matrix
projects = {}
#{parentrepo:[list of repos froked from parent]}
forkFamilyTree = {}
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
    print '\nrepo'
    allContribRepos = {}
    projectName = filelist[i].split('contributors')[0]
    projects[(projectName, repo_collabs[projectName])]=i
    data1 = open(dir+filelist[i], 'r').read()
    data1 = data1.split()
    for c in data1:
        #collaboartor index in matrix
        if c not in allCollaborators:
            allCollaborators[c] = addCol(matrix)#next index
        matrix[i][allCollaborators[c]] = 1

        individualRepos = repo_info.get_repos([c], forks=True)[c] # get all the repos the person has
        owned = individualRepos[0]
        forked = individualRepos[1]

        for own in owned:
            index = extraIndexes
            if (own,c) in projects.keys():
                index = projects[(own, c)]
            else:
                extraIndexes+=1
                projects[(own, c)]=index
                matrix.append([0]*len(allCollaborators.keys()))
            #matrix[projects[fork]][allCollaborators[c]] = 1
            #^^^do it at the end?

        for fork in forked:
            parent = repo_info.parent_repo(fork, c)
            if parent != None:
                forkFamilyTree[parent] = forkFamilyTree.get(parent, [])+[fork]
            	index = extraIndexes
            	if parent in projects.keys():
            		index = projects[parent]
            	else:
            		extraIndexes+=1
            		projects[parent]=index
            		matrix.append([0]*len(allCollaborators.keys()))
        	#matrix[projects[fork]][allCollaborators[c]] = 1
            #^^^same here

        allContribRepos[c] = individualRepos

    #write contributor's repos
    rawfile = open(projectName+'ContribRepos', 'w')
    json.dump(obj=allContribRepos,fp=rawfile)
    rawfile.close()

#build matrix
fileset = set(filelist)
for matrixRepo in projects.keys():
    if matrixRepo not in fileset:
        contributors = set(repo_info.repoPeople([matrixRepo], group = repo_info.CONTRIBUTORS)[matrixRepo])
        usefulConributors = contributors.intersection(set(allCollaborators.keys()))
        for c in usefulConributors:
            matrix[projects[matrixRepo]][allCollaborators[c]] = 1

#write matrix
f=open('extendedcontributorsnew.txt','w')
f.write("dl nr={} nc={} format=fullmatrix\n".format(len(projects),len(allCollaborators)))
f.write("row labels:\n")
for p in sorted(projects.items(),key=lambda x:x[1]):
    f.write('{}:{} '.format(p[0][0],p[0][1]))
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
