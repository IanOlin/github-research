
from repo_info import get_pulls, mlRepos
import json

for repo, owner in mlRepos.items():
    f = open("mlpulls/{}_pulls.json".format(repo), "w")
    pull_req = get_pulls(repo, owner)
    json.dump(pull_req, f)
    f.close()
