
from repo_info import get_pulls
import json
from github_util import api_get, JSON_access, is_successful_response
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join('..')))
from misc_info.constants import ML, STACK, return_constants, CURRENT_DATE

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

def get_pull_requests(project=ML):
    constants = return_constants(project)
    repo_list = constants["repos"]
    output_dir = constants["pulls-fpath"]

    # record the date of data retrieval
    date_file = open(os.path.join(output_dir, "date.txt"), 'w')
    date_file.write(CURRENT_DATE.strftime("%b %d, %Y"))
    date_file.close()

    for repo in repo_list:
        pull_req = get_pulls(repo)
        print "writing data..."
        f = open(os.path.join(output_dir, "{}_pulls.json".format(repo["name"])), "w")
        json.dump(pull_req, f)
        f.close()
        print "done writing data."
