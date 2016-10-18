from repo_info import *
import json

ML = 0
STACKS = 1

currentRepos = CLOUD_STACK

#directory
dirName = ''
if currentRepos == ML:
    dirName = 'mlCommits'
elif currentRepos == STACKS:
    dirName = 'stackCommits'


if not os.path.exists(dirName):
    os.mkdir(dirName)

#getting correct repos
repo_dict = {}
if currentRepos == ML:
    repo_dict = mlRepos
elif currentRepos == OPEN_STACK:
    repo_dict = stackRepos

#getting commits
for repo_tup in repo_dict.items():
    repo = repo_tup[0]
    user = repo_tup[1]

    output_file = open("{}/{}-{}-commits.json".format(dirName, repo, user), 'w')

    commits = get_all_commits(repo, user)
    json.dump(commits, output_file)
    output_file.close()