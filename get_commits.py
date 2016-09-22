from repo_info import *
import json

dirName = 'mlCommits'

if not os.path.exists(dirName):
    os.mkdir(dirName)

for ml_repo in mlRepos.items():
    repo = ml_repo[0]
    user = ml_repo[1]

    output_file = open("{}/{}-{}-commits.json".format(dirName, repo, user), 'w')

    commits = get_all_commits(repo, user)
    json.dump(commits, output_file)
    output_file.close()