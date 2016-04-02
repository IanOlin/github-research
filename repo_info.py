"""
With a given list of repos, has methods to extract the list of collaborators, contributors, or forks
Writes each repo's data to a separate file in a given directory
"""
import pattern.web
import json
import os
import requests
from mimetools import Message
from StringIO import StringIO
import time

repo_collabs = [('Theano', 'Theano'), ('caffe', 'BVLC'), ('CNTK', 'Microsoft'), ('tensorflow', 'tensorflow'), ('torch7', 'torch'), ('deeplearning4j', 'deeplearning4j')]

keyfile = open('keyfile.txt')
KEY = keyfile.read()
keyfile.close()

API_DOMAIN = 'https://api.github.com'

CONTRIBUTORS = 0
FORKERS = 1
#DOES NOT WORK UNLESS YOU HAVE PUSH ACCESS
COLLABORATORS = 10

URL_PATH = {CONTRIBUTORS:'contributors', COLLABORATORS:'collaborators', FORKERS:'forks'}
JSON_PATH = {CONTRIBUTORS:('login',), COLLABORATORS:('login',), FORKERS:('owner', 'login')}

def get_repos(users, dirName=None, forks=False):
	"""
	Gets all the repos of the users
	Returns dictionary {user:reponamelist}
	or if forks is True, returns {user:(nonforknamelist, forknamelist)}
	"""
	if dirName!=None:
		if not os.path.exists(dirName):
			os.mkdir(dirName)
	filenames = []
	all_repos = {}

	for u in users:
		repos = []
		forked = []
		page = 1

		while page>0:

			URLstr = 'https://api.github.com/users/{}/repos'.format(u)
			newURL = api_get(URLstr, parameters={'page':page, 'access_token':KEY, 'per_page':100})
			# print page
			index=str(newURL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			repo_data = json.loads(newURL.text)
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

		fname = u + 'repos.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in repo_contributors:
				f.write(contributor + '\n')
			f.close()
		if forks:
			all_repos[u] = (repos,forked)
		else:
			all_repos[u] = repos
		
	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos

def parent_repo(repo,user):
	"""check for contributor"""
	repo_URL = "{}/repos/{}/{}".format(API_DOMAIN, user, repo)
	page = json.loads(api_get(baseURL=repo_URL, parameters={'access_token':KEY}).text)

	name = JSON_access(page,('parent','name'))
	owner = JSON_access(page, ('parent','owner','login'))
	if name != None and owner != None:
		parent_repo = (name, owner)
	else:
		parent_repo = None

	return parent_repo

def api_get(baseURL, parameters = {}, minRemaining=1):
	"""If there are not enough calls remaining, wait until they refresh"""
	while True:
		try:
			#get rate limit
			URLstr = "https://api.github.com/rate_limit"
			response = requests.get(URLstr, params={'access_token':KEY})
			try:
				remaining = int(json.loads(response.text)['resources']['core']['remaining'])
			except KeyError as e:
				try:
					errorfile = open('ERROR.txt', 'w')
					errorfile.write(response.text)
					errorfile.close()
				except:
					print 'could not write to file'
				raise e
			#if there are not enough calls left
			if remaining < minRemaining:
				print 'waiting'
				time_sec = int(json.loads(response.text)['resources']['core']['reset'])
				time.sleep(time_sec+5-int(time.time()))
				print 'done waiting'
			#return original request
			return requests.get(baseURL, params=parameters)

		except requests.exceptions.ConnectionError:
			print 'ConnectionError, trying again'
			continue
		break

def JSON_access(jsonString, keyTuple):
	"""
	returns the element or json object from the tuple of keys
	returns None if repo is blocked
	"""
	try:
		breakdown = jsonString
		#grabbing each section--subsequent keys will be nested in the parent keys
		for key in keyTuple:
			breakdown = breakdown[key]
		return breakdown
	except (KeyError, TypeError) as e:
		#if repository is blocked, return nothing
		try:
			if "blocked" in jsonString['message']:
				return None
		except:
			print 'not blocked'
		#key errors
		try:
			errorFile = open('ERROR.txt', 'w')
			errorFile.write(json.dumps(jsonString))
			errorFile.close()
		except:
			print 'COULD NOT WRITE TO FILE'
		raise e

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
			newURL = api_get(baseURL=URLstr, parameters={'page':page, 'access_token':KEY, 'per_page':100})
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
			if type(responsePage) is not list and 'Not Found' in responsePage['message']:
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

if __name__=='__main__':
	print repoPeople([('EmptyTest','poosomooso')], group=CONTRIBUTORS)
	pass