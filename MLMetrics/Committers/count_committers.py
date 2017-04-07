import json
import csv
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
from misc_info.constants import ML, STACK, CURRENT_DATE, return_constants

pathToJSON = "/home/jwb/Documents/Json/"
# pathToJSON = "/home/anne/ResearchJSONs/"
fileList = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json", "incubator-systemml-apache-commits.json")

TENSORFLOWER_GARDENER_NAME = "A. Unique TensorFlower"

constants_dict = {}

"""
Returns a dict of {committer name : number of commits}
"""
def count_commits_per_user(filename):
    raw = openJSON(pathToJSON + filename)
    userCommitHist = {}
    for commit in raw:
        # simple fields
        name = commit["commit"]["author"]["name"].encode("utf-8")
        if(name != TENSORFLOWER_GARDENER_NAME):
            userCommitHist[name] = userCommitHist.get(name, 0) + 1
    return userCommitHist

def getRepoID(fname):
    filePieces = fname.split("-")
    repo = filePieces[0]+"-"+filePieces[1]
    return repo

def openJSON(fname):
    return json.load(open(fname, "r"))

if __name__ == "__main__":
    constants_dict = return_constants(ML)
    for fn in fileList:
        #print fn
        commit_dict = count_commits_per_user(fn)
        #print len(commit_dict.keys())
        with open(pathToJSON + "csvs/"+fn[:-5]+'-dict.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for k, v in commit_dict.items():
                writer.writerow([k.decode('utf8'), v])
