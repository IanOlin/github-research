import repo_info
import json

"""
Deprecated
Snowballs, but I think this only grabs the repos that a user forked. And it's not particularly accurate either. 
See snowballing.py
"""

dir = 'mlcontrib/'
names = open(dir+'files.txt','r').read()
filelist = names.split()
print filelist


def addCol(adjMatrix):
    """Adds a column to the end of adjMatrix and returns the index of the comlumn that was added"""
    for j in range(len(adjMatrix)):
        adjMatrix[j].append(0)
    return len(adjMatrix[0])-1

#all collaborators mapped name:index
#collaborator name : index in matrix
allCollaborators = {}
#names of all projects, indexes corresponding with the index in matrix
#project name : index in matrix
projects = {}
#matrix of projects (rows) and contributors (columns)
matrix = []

for i in range(len(filelist)): #len(filelist) is the number of main projects
    matrix.append([0]*len(allCollaborators))
#index of the next new repo introduced via contributor
extraIndexes = len(filelist)

for i in range(len(filelist)):
    #grabs the name of the project
    projectName = filelist[i].split('contributors')[0]
    
    #open json file
    rawfile = open(projectName+'ContribRepos', 'r')
    jsondata = json.load(fp=rawfile)
    rawfile.close()

    #current project
    projects[projectName]=i

    for user in jsondata.keys():
        if user not in allCollaborators:
            allCollaborators[user] = addCol(matrix)#next index
            #grabs all their repos, adds to matrix
            individualReposForked = jsondata[user][1] #change to 0 if you want all repos; change to 1 if you want forked repos
            for fork in individualReposForked:
                index = extraIndexes
                if fork in projects.keys():
                    index = projects[fork]
                else:
                    extraIndexes+=1
                    projects[fork]=index
                    matrix.append([0]*len(allCollaborators))
                matrix[projects[fork]][allCollaborators[user]] = 1

        matrix[i][allCollaborators[user]] = 1
        
        
        
    
f=open('extendedcontributors.txt','w')

f.write("dl nr={} nc={} format=fullmatrix\n".format(len(projects),len(allCollaborators)))

f.write("row labels:\n")
for p in sorted(projects.items(),key=lambda x:x[1]):
    f.write(p[0]+' ')
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




