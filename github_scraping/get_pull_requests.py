
from repo_info import get_pulls, mlRepos
import json
from github_util import api_get, JSON_access, is_successful_response

def is_merged_systemml(pull_request):
    url = JSON_access(pull_request,("comments_url",))
    response = api_get(url)
    if not is_successful_response(response):
        print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
        return False
    comments = json.loads(response.text)
    for c in comments:
        msg = JSON_access(c, ("body",))
        if "LGTM" in msg:
            return True
    return False

if __name__ == "__main__":
    for repo, owner in mlRepos.items():
        f = open("mlpulls/{}_pulls.json".format(repo), "w")
        pull_req = get_pulls(repo, owner)
        json.dump(pull_req, f)
        f.close()
