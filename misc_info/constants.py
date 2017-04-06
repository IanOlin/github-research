from datetime import date

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
ml_repos.append({"name": 'incubator-systemml',  "user": 'apache'})

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

__ST_CONSTANTS["repos"] = ml_repos

# Jenkins names
__ML_CONSTANTS["jenkins"] = ("A. Unique TensorFlower")
__ST_CONSTANTS["jenkins"] = ("Jenkins", 'OpenStack Proposal Bot')

__ML_CONSTANTS["earliest-commit"] = 

### PUBLIC --------------------------------------------------------------

# flags
ML = 0
STACK = 1

def return_constants(flag):
    """
    Given a flag, returns the correct dictionary of constants
    """
    if flag == ML:
        return __ML_CONSTANTS
    if flag == STACK:
        return __ST_CONSTANTS
    raise Exception("unknown flag")