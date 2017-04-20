import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
from misc_info.constants import ML, STACK

from github_scraping import get_commits, get_pull_requests

def get_flag():
    project_str = "ml"
    if len(sys.argv) > 1:
        project_str = sys.argv[1]

    if project_str.lower() == "ml":
        project_flag = ML
    elif project_str.lower() == "stack":
        project_flag = STACK
    else:
        raise ValueError("Invalid argument")
    return project_flag

if __name__ == "__main__":
    flag = get_flag()

    get_commits.get_commits(flag)
    get_pull_requests.get_pull_requests(flag)