"""
Methods to get certain kinds of data from the Github API.
Writes each repo's data to a separate file in a given directory
"""
import json
from mimetools import Message
from StringIO import StringIO
from github_util import *
import time
import sys, os


#####
# CONSTANTS
#####

#constants to specify parameters when calling methods
CONTRIBUTORS = 0
FORKERS = 1
#DOES NOT WORK UNLESS YOU HAVE PUSH ACCESS
COLLABORATORS = 10

#the url path to the information in the api
URL_PATH = {CONTRIBUTORS:'contributors', COLLABORATORS:'collaborators', FORKERS:'forks'}
#the path to the following information in the json
JSON_PATH = {CONTRIBUTORS:('login',), COLLABORATORS:('login',), FORKERS:('owner', 'login')}


#####
# METHODS
#####
"""
Gets all the repos of the users
Returns dictionary {user:reponamelist}
or if forks is True, returns {user:(nonforknamelist, forknamelist)}
"""
def get_repos(users, forks=False):
    #a dictionary to store all the {users:repos}
    all_repos = {}

    for u in users:
        repos = []
        forked = []
        page = 1


        while page>0:   #api has multiple pages

            URLstr = 'https://api.github.com/users/{}/repos'.format(u)
            response = api_get(URLstr, parameters={'page':page, 'per_page':100})
            if not is_successful_response(response):
                print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
                break

            if has_next_page(response):
                page += 1
            else:
                page = -1

            #read the data of the current page
            try:
                repo_data = json.loads(response.text)
            except:
                error_dump("{}\n{}\n{}".format(response, URLstr, response.text))
                raise e

            for repo in repo_data:
                #get name of the repo
                repoName = JSON_access(repo, ('name',))
                #split forks and non-forks, if necessary
                isFork = JSON_access(repo, ('fork',))
                if forks and isFork:
                    forked.append(repoName)
                else:
                    repos.append(repoName)
        #add to the allRepos dictionary
        if forks:
            all_repos[u] = (repos,forked)
        else:
            all_repos[u] = repos

    return all_repos

"""
grabs a list of all (contributors|collaborators|forkers) of all the repos
returns a dict of {repo_name : list of people}
"""
def repoPeople(repo_list,group=CONTRIBUTORS):
    all_repos = {}
    for repo in repo_list:
        people = []
        page = 1

        while page>0:
            URLstr = 'https://api.github.com/repos/{}/{}/{}'.format(repo["user"], repo["name"], URL_PATH[group])
            response = api_get(baseURL=URLstr, parameters={'page':page,'per_page':100})
            if not is_successful_response(response):
                print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
                break

            if has_next_page(response):
                page += 1
            else:
                page = -1

            try:
                responsePage = json.loads(response.text)
            except:
                error_dump("{}\n{}\n{}".format(response, URLstr, response.text))
                raise e

            for contributor in responsePage:
                username = JSON_access(contributor, JSON_PATH[group])
                if username != None:
                    people.append(username)

        all_repos[repo["name"]] = people

    return all_repos

"""
Gets all the pull requests for a repo
"""
def get_pulls(repo):
    URLstr = "https://api.github.com/repos/{}/{}/pulls".format(repo["user"], repo["name"])
    page = 1
    pulls = []
    while page>0:
        response = api_get(baseURL=URLstr, parameters={'page':page, 'per_page':100, "state":"all"})
        if not is_successful_response(response):
            print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
            break
        if has_next_page(response):
            page += 1
        else:
            page = -1
        try:
            responsePage = json.loads(response.text)
        except:
            error_dump("{}\n{}\n{}".format(response, URLstr, response.text))
            raise e
        pulls.extend(responsePage)
    return pulls


"""
check if a repo is forked, and if so, return the parent repo in a tuple (reponame, ownername)
else, return None
"""
def parent_repo(repo,user):

    URLstr = "https://api.github.com/repos/{}/{}".format(user, repo)
    response = api_get(baseURL=URLstr)

    if not is_successful_response(response):
        print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
        return None

    page = json.loads(response.text)
    parentRepo = None

    if JSON_access(page, ('fork',)):
        name = JSON_access(page,('parent','name'))
        owner = JSON_access(page, ('parent','owner','login'))
        if name != None and owner != None:
            parentRepo = (name, owner)

    return parentRepo

"""
Returns all the commits of a given repo
"""
def get_all_commits(repo):
    URLstr = "https://api.github.com/repos/{}/{}/commits".format(repo["user"], repo["name"])
    commits = []
    page = 1
    while page>0:
        response = api_get(baseURL=URLstr, parameters={'page':page,'per_page':100})
        if not is_successful_response(response):
            print "{}\n{}\n{}\n".format(URLstr, response.status_code, response.text)
            break

        if has_next_page(response):
            page += 1
        else:
            page = -1

        try:
            responsePage = json.loads(response.text)
        except:
            error_dump("{}\n{}\n{}".format(response, URLstr, response.text))
            raise e
        commits.extend(responsePage)
    return commits

#####
# TESTS
# make sure I didn't break anything
#####

if __name__=='__main__':
    print parent_repo('ReadingJournal', 'poosomooso')
    print parent_repo('QingTingCheat', "felixonmars") #should return None and print error because DMCA takedown
    print repoPeople([{"name":'EmptyTest', "user":'poosomooso'}], group=CONTRIBUTORS) #print error code and also empty list in dict
    print repoPeople([{"name":'Codestellation2015', "user":'IanOlin'}], group=CONTRIBUTORS)
    print get_repos(("poosomooso", ))
    repos = get_repos(("sindresorhus", )) #guy's got a lot of repos
    print len(repos["sindresorhus"]) #over 700
    print len(get_all_commits({"name":'CNTK', "user":'Microsoft'})) #check on github for actual number; as of 9/22/16 7899
    ai_pulls = get_pulls({"name":"ToolBox-AI", "user":"sd16fall"})
    print len(ai_pulls) #4
    # print ai_pulls[0]
    pass
