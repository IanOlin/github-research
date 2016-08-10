"""
With a given list of repos, has methods to extract the list of collaborators, contributors, or forks
Writes each repo's data to a separate file in a given directory
"""
import pattern.web
import json
import os
from mimetools import Message
from StringIO import StringIO
from github_util import *
import time
import sys

##### 
# CONSTANTS
#####

# the repos we are looking at
repo_collabs = [('Theano', 'Theano'), ('caffe', 'BVLC'), ('CNTK', 'Microsoft'), ('tensorflow', 'tensorflow'), ('torch7', 'torch'), ('deeplearning4j', 'deeplearning4j')]

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

def get_repos(users, dirName=None, forks=False):
	"""
	Gets all the repos of the users
	Returns dictionary {user:reponamelist}
	or if forks is True, returns {user:(nonforknamelist, forknamelist)}
	"""
	#if writing to a file, use this directory
	if dirName!=None:
		if not os.path.exists(dirName):
			os.mkdir(dirName)

	#a list of filenames to write to -- each user gets their own file?
	filenames = []
	#a dictionary to store all the {users:repos}
	all_repos = {}

	for u in users:
		repos = []
		forked = []
		page = 1


		while page>0:	#api has multiple pages

			URLstr = 'https://api.github.com/users/{}/repos'.format(u)
			response = api_get(URLstr, parameters={'page':page, 'per_page':100})

			#if there is a next page, increment, else make the page -1 (break out of the loop)
			index=str(response.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			#read the data of the current page
			repo_data = json.loads(response.text)
			if type(repo_data) is not list:		#if it returns something else, there was an error
				print URLstr
				break
			for repo in repo_data:
				#get name of the repo
				repoName = JSON_access(repo, ('name',))
				if repoName == None: #some error for whatever reason
					continue			
				#split forks and non-forks, if necessary
				if forks and JSON_access(repo, ('fork',)):
					forked.append(repoName)
				else:
					repos.append(repoName)
		#writes each user's repo into a different file
		#TODO: figure out how to make this more intuitive and less cluttered
		fname = u + 'repos.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in repo_contributors:
				f.write(contributor + '\n')
			f.close()
		#add to the allRepos dictionary
		if forks:
			all_repos[u] = (repos,forked)
		else:
			all_repos[u] = repos
	
	#write the names of all the files
	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos

"""list of repos with the format (reponame, ownername)"""
def repoPeople(repos,group=CONTRIBUTORS,dirName=None):
	#print repos
	if dirName!=None:
		if not os.path.exists(dirName):
			os.mkdir(dirName)
	filenames = []
	all_repos = {}
	for collabs in repos:
		people = []
		page = 1

		while page>0:
			URLstr = 'https://api.github.com/repos/{}/{}/{}'.format(collabs[1], collabs[0], URL_PATH[group])
			newURL = api_get(baseURL=URLstr, parameters={'page':page,'per_page':100})
			index=str(newURL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			try:
				responsePage = json.loads(newURL.text)
			except ValueError:
				if len(newURL.text) == 0:
					continue
				else:
					print newURL
					print newURL.text
					raise e
			#print responsePage
			if type(responsePage) is not list: #and 'Not Found' in responsePage['message']:
				print URLstr
				continue

			for contributor in responsePage:
				username = JSON_access(contributor, JSON_PATH[group])
				if username != None:
					people.append(username)

		fname = collabs[0] + URL_PATH[group] + '.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in people:
				f.write(contributor + '\n')
			f.close()

		all_repos[collabs] = people

	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos

def parent_repo(repo,user):
    """
    check if a repo is forked, and if so, return the parent repo in a tuple (reponame, ownername)
    else, return None
    """
    repoURL = "https://api.github.com/repos/{}/{}".format(user, repo)
    page = json.loads(api_get(baseURL=repoURL).text)
    if type(page) is not dict: #and 'Not Found' in responsePage['message']:
            print repoURL
            parentRepo = None
    if JSON_access(page, ('fork',)):
        name = JSON_access(page,('parent','name'))
        owner = JSON_access(page, ('parent','owner','login'))
        if name != None and owner != None:
            parentRepo = (name, owner)
        else:
            parentRepo = None
    else:
        parentRepo=None

    return parentRepo

#####
# TESTS
# make sure I didn't break anything
#####

if __name__=='__main__':
	print parent_repo('ReadingJournal', 'poosomooso')
	print repoPeople([('EmptyTest','poosomooso')], group=CONTRIBUTORS)
	print repoPeople([('Codestellation2015', 'IanOlin')], group=CONTRIBUTORS)
	print get_repos(("poosomooso", ))
	pass
