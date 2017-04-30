from datetime import date
import os
import time
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

# absolute filepath to the directory with commit jsons & pull request jsons
# reeeeeeeeaaaaaally jank solution to set the path to the data correctly, no 
# matter where the calling module may be within 'github-research'
path = ""
timeout = time.time() + 5 #5 second timeout
while((not os.path.exists(os.path.join(path, "github_data")))):
    if (time.time() > timeout):
        raise IOError("No data here, boss")
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

# dict of name merging
DUP_DICT = {"Frederic" : "Frederic Bastien", "Frédéric Bastien":"Frederic Bastien", "nouiz" : "Frederic Bastien",
        "lamblin" : "Pascal Lamblin", 
        "abergeron" : "Arnaud Bergeron",
        "carriepl" : "Pierre Luc Carrier",
        "Jon Long" : "Jonathan L Long", "longjon" : "Jonathan L Long",
        "Sergio" : "Sergio Guadarrama",
        "frankseide" : "Frank Seide",
        "terrytangyuan" : "Yuan (Terry) Tang",
        "caisq" : "Shanqing Cai",
        "yifeif" : "Yifei Feng",
        "Daniel W Mane" : "Dan Mané",
        "soumith" : "Soumith Chintala",
        "Nicholas Léonard" : "Nicholas Leonard", "nicholas-leonard" : "Nicholas Leonard",
        "GeorgOstrovski" : "Georg Ostrovski",
        "agibsonccc" : "Adam Gibson",
        "raver" : "raver119", "raver119@gmail.com" : "raver119",
        "nyghtowl" : "Melanie Warrick", 
        "jyt109" : "Jeffrey Tang",
        "bergstrj@iro.umontreal.ca" :"James Bergstra", "bergstra@ip05.m" : "James Bergstra" }
 
def return_constants(flag):
    """
    Given a flag, returns the correct dictionary of constants
    """
    if flag == ML:
        return __ML_CONSTANTS
    if flag == STACK:
        return __ST_CONSTANTS
    raise Exception("unknown flag")
