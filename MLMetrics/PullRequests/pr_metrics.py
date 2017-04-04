import json
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
from github_scraping.get_pull_requests import is_merged_systemml
from constants import ML, STACK, return_constants

directory = '../../github_scraping/mlpulls/'

systemml_name = 'incubator-systemml'

def sort_by_val_return_str(d):
    """
    Takes a dict, sorts it by the value, and returns the string with key:value
    in reverse order by value
    """
    string = ""
    for u in sorted(d.items(), key=lambda x:x[1], reverse=True):
        string += " {}:{}".format(u[0], u[1])
    return string

def print_prs(project_flag):
    """
    Calculates the number of merged and closed pull requests, as well as the high
    frequency pull requesters, and prints to stdout. Takes in a flag, defined by
    constants.py, that determines whether to look at stack repos or ml repos.
    """
    repos = return_constants(project_flag)["repos"]
    for repo_dict in repos:
        repo = repo_dict["name"]
        owner = repo_dict["user"]
        print repo, owner

        # grab pull requests
        pulls = json.load(open(directory + "{}_pulls.json".format(repo)))
        print 'num_pulls,{}'.format(len(pulls))

        # sort
        merged = 0
        closed = 0
        open_pulls = 0
        merged_users = {}
        closed_users = {}
        for p in pulls:
            merged_at = p["merged_at"]
            closed_at = p["closed_at"]
            username = p["user"]["login"]
            # make an exception for systemml
            if closed_at != None and repo == systemml_name:
                merged_at = 1 if is_merged_systemml(p) else None

            # count
            if merged_at != None:
                merged += 1
                merged_users[username] = merged_users.get(username, 0) + 1
            elif closed_at != None:
                closed += 1
                closed_users[username] = closed_users.get(username, 0) + 1
            else:
                open_pulls += 1

        # sort all users who have had merged prs
        merged_users_str = sort_by_val_return_str(merged_users)

        # sort all users that have closed prs (unmerged)
        closed_users_str = sort_by_val_return_str(closed_users)

        # statistics for that repo
        print 'num_merged,{}'.format(merged)
        print 'merged_users,{}'.format(merged_users_str)
        print 'num_open,{}'.format(open_pulls)
        print 'num_closed,{}'.format(closed)
        print 'closed_users,{}'.format(closed_users_str)
        print ''

print_prs(ML)
