import json
import csv
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
from misc_info.constants import ML, STACK, CURRENT_DATE, return_constants, return_filename

# fileList = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json", "incubator-systemml-apache-commits.json")

constants_dict = {}

"""
Returns a dict of {committer name : number of commits}
"""
def count_commits_per_user(filename):
    global constants_dict
    raw = openJSON(constants_dict["commits-fpath"] + filename)
    userCommitHist = {}
    for commit in raw:
        # simple fields
        name = commit["commit"]["author"]["name"].encode("utf-8")
        if(name not in constants_dict["jenkins"]):
            userCommitHist[name] = userCommitHist.get(name, 0) + 1
    return userCommitHist

def openJSON(fname):
    return json.load(open(fname, "r"))

if __name__ == "__main__":
    constants_dict = return_constants(ML)
    for repo in constants_dict["repos"]:
        #print fn
        # obtain a dictionary of commiters: # commits :
        commit_dict = count_commits_per_user(return_filename(repo))
        #print len(commit_dict.keys())
        output_file = "csvs_new/{}-{}-dict.csv".format(repo["name"], repo["user"])
        with open(output_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for k, v in commit_dict.items():
                writer.writerow([k, v])
