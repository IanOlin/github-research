from datetime import date
import os

### PRIVATE -------------------------------------------------------------

# Dictionaries of constants; use the `return_constants()` function
# to access
__ML_CONSTANTS = {}
__ST_CONSTANTS = {}

# Adding repo names and repo users
ml_repos = []
ml_repos.append({"name": 'Theano',              "user": 'Theano'})
ml_repos.append({"name": 'caffe',               "user": 'BVLC'})
ml_repos.append({"name": 'CNTK',                "user": 'Microsoft'})
ml_repos.append({"name": 'tensorflow',          "user": 'tensorflow'})
ml_repos.append({"name": 'torch7',              "user": 'torch'})
ml_repos.append({"name": 'deeplearning4j',      "user": 'deeplearning4j'})
# ml_repos.append({"name": 'incubator-systemml',  "user": 'apache'})

__ML_CONSTANTS["repos"] = ml_repos

stack_repos = []
stack_repos.append({"name": 'cinder',           "user": 'openstack'})
stack_repos.append({"name": 'glance',           "user": 'openstack'})
stack_repos.append({"name": 'horizon',          "user": 'openstack'})
stack_repos.append({"name": 'keystone',         "user": 'openstack'})
stack_repos.append({"name": 'nova',             "user": 'openstack'})
stack_repos.append({"name": 'neutron',          "user": 'openstack'})
stack_repos.append({"name": 'swift',            "user": 'openstack'})
stack_repos.append({"name": 'cloudstack',       "user": 'apache'})

__ST_CONSTANTS["repos"] = stack_repos

# Jenkins names
__ML_CONSTANTS["jenkins"] = set(("A. Unique TensorFlower",))
__ST_CONSTANTS["jenkins"] = set(("Jenkins", 'OpenStack Proposal Bot'))

# date of the first commit of any of the repos in the category
__ML_CONSTANTS["earliest-commit"] = date(2008, 1, 1)
__ST_CONSTANTS["earliest-commit"] = date(2010, 5, 1)

# absolute filepath to the directory with commit jsons
# "/home/anne/ResearchJSONs/"
# "/home/serena/GithubResearch/mlCommits-new/"
# "/home/jwb/Documents/Json/"
# reeeeeeeeaaaaaally jank solution to set the path to the data correctly, no 
# matter where the calling module may be within 'github-research'
path = ""
while(not os.path.exists(os.path.join(path, "github_data"))):
    path = os.path.join(path, "..")

__ML_CONSTANTS["data-fpath"] = os.path.abspath(os.path.join(path, "github_data", "ml"))
__ML_CONSTANTS["commits-fpath"] = os.path.join(__ML_CONSTANTS["data-fpath"], "commits")
__ML_CONSTANTS["pulls-fpath"] = os.path.join(__ML_CONSTANTS["data-fpath"], "pulls")
__ST_CONSTANTS["data-fpath"] = os.path.abspath(os.path.join(path, "github_data", "stack"))
__ST_CONSTANTS["commits-fpath"] = os.path.join(__ST_CONSTANTS["data-fpath"], "commits")
__ST_CONSTANTS["pulls-fpath"] = os.path.join(__ST_CONSTANTS["data-fpath"], "pulls")

### PUBLIC --------------------------------------------------------------

# flags
ML = 0
STACK = 1

def return_filename(repo):
    return "{}-{}-commits.json".format(repo["name"], repo["user"])


# misc constants
CURRENT_DATE = date.today() #date(2016, 11, 1)    # current date according to the github things;
                                    # may change it to the actual current date
                                    # after we automate github scraping also



def return_constants(flag):
    """
    Given a flag, returns the correct dictionary of constants
    """
    if flag == ML:
        return __ML_CONSTANTS
    if flag == STACK:
        return __ST_CONSTANTS
    raise Exception("unknown flag")