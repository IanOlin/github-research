import json
import os

directory = '../../github-scraping/mlpulls/'
# /home/serena/GithubResearch/github-research/github-scraping/mlpulls/CNTK_pulls.json

# hard copied from repo_info
mlRepos = {'Theano' : 'Theano',
    'caffe' : 'BVLC',
    'CNTK' : 'Microsoft',
    'tensorflow' : 'tensorflow',
    'torch7' : 'torch',
    'deeplearning4j': 'deeplearning4j',
    'incubator-systemml' : 'apache'}

"""
Metrics overall
"""
for repo, owner in mlRepos.items():
    print repo, owner
    pulls = json.load(open(directory + "{}_pulls.json".format(repo)))
    print 'num_pulls,{}'.format(len(pulls))
    merged = 0
    closed = 0
    open_pulls = 0
    merged_users = {}
    closed_users = {}
    for p in pulls:
        merged_at = p["merged_at"]
        closed_at = p["closed_at"]
        username = p["user"]["login"]
        if merged_at != None:
            merged += 1
            merged_users[username] = merged_users.get(username, 0) + 1
        elif closed_at != None:
            closed += 1
            closed_users[username] = closed_users.get(username, 0) + 1
        else:
            open_pulls += 1

    merged_users_str = ""
    for u in sorted(merged_users.items(), key=lambda x:x[1], reverse=True):
        merged_users_str += " {}:{}".format(u[0], u[1])

    closed_users_str = ""
    for u in sorted(closed_users.items(), key=lambda x:x[1], reverse=True):
        closed_users_str += " {}:{}".format(u[0], u[1])

    print 'num_merged,{}'.format(merged)
    print 'merged_users,{}'.format(merged_users_str)
    print 'num_open,{}'.format(open_pulls)
    print 'num_closed,{}'.format(closed)
    print 'closed_users,{}'.format(closed_users_str)
    print ''
