"""
Gets the repos each of the 675 contributors owns + forked repos
matrix contains owned repos and parent repos of the repos the contributors forked
not included:
    contributions to forks of repos
    repos where user has contributed via collaborator commit rights, but nobody in this set has owned or forked
    organization repos
Currently not going to extend to stack since this code is not in use.
"""

import repo_info
import json
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join('..')))
from misc_info.constants import ML, STACK, return_constants


dir = 'mlcontrib/'
# names = open(dir+"files.txt", 'r').read()
# mlFileNames = names.split()
# print mlFileNames

constants = return_constants(ML)
reponames = constants["repos"]

#matrix of projects (rows) and contributors (columns)
matrix = []

#collaborator name : index in matrix
allContributors = {}

#(project name, projectOwner) : index in matrix
projects = {}

#parentrepo : [list of repos forked from parent]
forkFamilyTree = {}

###
# HELPER METHODS
###

"""
Adds a column to the end of adjMatrix and returns the index of the column that was added
"""
def add_col(adjMatrix):
    for j in range(len(adjMatrix)):
        adjMatrix[j].append(0)
    return len(adjMatrix[0])-1

"""
Takes a tuple (projectname, ownername), the same as the keys to the projects dictionary
If the repo is registered in the projects dict, do nothing, else add a new row
"""
def add_project_to_matrix(repo):
    if repo not in projects:
        projects[repo] = len(matrix)
        matrix.append([0]*len(allContributors.keys()))

"""
for a given tuple of lists (ownedRepos, forkedRepos), make sure that the owned repos and the parents of the
forked repos are in the matrix
"""
def register_repos(repos, contributor):
    ownedRepos = repos[0]
    forkedRepos = repos[1]

    for owned in ownedRepos:
        add_project_to_matrix((owned, contributor))

    for fork in forkedRepos:
        parent = repo_info.parent_repo(fork, contributor)
        if parent != None:
            forkFamilyTree[parent] = forkFamilyTree.get(parent, [])+[fork]
            add_project_to_matrix(parent)

"""
gets the contributors of a repo that also appear in the setToChooseFrom
"""
def get_actual_contributors(repo, setToChooseFrom = None):
    if setToChooseFrom == None:
        setToChooseFrom = set(allContributors.keys())

    repoContributors = repo_info.repoPeople([{"name": repo[0], "user":repo[1]}], group = repo_info.CONTRIBUTORS)[repo[0]]
    usefulConributors = set(repoContributors).intersection(setToChooseFrom)
    return usefulConributors

def sort_by_value(dictionaryToSort):
    return sorted(dictionaryToSort.items(), key=lambda x:x[1])


###
# ACTUAL SCRIPT
###

for i in range(len(reponames)): #number of ml repos
    matrix.append([0]*len(allContributors))

for i in [2]:#range(len(reponames)):
    projectName = reponames[i]["name"]
    projectOwner = reponames[i]["user"]
    projects[(projectName, projectOwner)] = i
    print '\n{}'.format(projectName)

    contributors = open("{}{}contributors.txt".format(dir, projectName), 'r').read()
    contributors = contributors.split()

    allContribRepos = {}
    for person in contributors:
        #get collaborator index in matrix
        if person not in allContributors:
            allContributors[person] = add_col(matrix)#next index

            individualRepos = repo_info.get_repos([person], forks=True)[person] # get all the repos the person has
            register_repos(individualRepos, person)
            allContribRepos[person] = individualRepos

        matrix[i][allContributors[person]] = 1

    #write a file with all the repos that a ml repo's contributors also own
    rawfile = open(os.path.join("snowballcontrib", projectName+'ContribRepos'), 'w')
    json.dump(obj=allContribRepos,fp=rawfile)
    rawfile.close()

#build matrix
fileset = set([ (repo["name"], repo["user"]) for repo in reponames ])
for repo in projects.keys():
    if repo not in fileset:
        usefulConributors = get_actual_contributors(repo)

        for person in usefulConributors:
            matrix[projects[repo]][allContributors[person]] = 1

projectLabels = ['{}:{}'.format(p[0][0],p[0][1]) for p in sort_by_value(projects)]
contributorLabels = [c[0] for c in sort_by_value(allContributors)]

repo_info.write_dl_file(os.path.join("snowballcontrib", 'extendedcontributorsnew.txt'), projectLabels, contributorLabels, matrix)
