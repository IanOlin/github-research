"""
With a given list of repos, has methods to extract the list of collaborators, contributors, or forks
Writes each repo's data to a separate file in a given directory
"""
#Save the file

import pattern.web
import json
import os
import requests
from mimetools import Message
from StringIO import StringIO
import time
#Generate a list of repos & username associated with that particular repo: list = [(repo1, un1), (repo2, un2), etc.]

repo_collabs = [('Theano', 'Theano'), ('caffe', 'BVLC'), ('CNTK', 'Microsoft'), ('tensorflow', 'tensorflow'), ('torch7', 'torch'), ('deeplearning4j', 'deeplearning4j')]
keyfile = open('keyfile.txt')
KEY = keyfile.read()
keyfile.close()

API_DOMAIN = 'https://api.github.com'

#Use that list's info to get api info/obtain list of collaborators

#Obtain json stuffz from api info

#grab specific pieces of data & store it

"""list of repos with the format (reponame, ownername)"""
def contributors(repos,dirName=None):
	#print repos
	if dirName!=None:
		if not os.path.exists(dirName):
			os.mkdir(dirName)
	filenames = []
	all_repos = {}
	for collabs in repos:
		repo_contributors = []
		page = 1

		while page>0:

			URL_str = 'https://api.github.com/repos/{}/{}/contributors'.format(collabs[1], collabs[0])
			new_URL = api_get(base_URL=URL_str, parameters={'page':page, 'access_token':KEY, 'per_page':100})

			index=str(new_URL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1
			contributor_data = json.loads(new_URL.text)
			try:
				for contributor in contributor_data:
					# print 'start'
					# for k in contributor.keys():
					# 	print '{} {}'.format(k, contributor[k])
					# print ''
					repo_contributors.append(contributor['login'])
			except (KeyError, TypeError) as e:
				if "Repository access blocked" in contributor_data['message']:
					continue
				try:
					errorfile = open('ERROR.txt', 'w')
					errorfile.write(json.dumps(contributor_data))
					errorfile.close()
				except:
					print 'could not write to file'
				raise e

		fname = collabs[0] + 'contributors.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in repo_contributors:
				f.write(contributor + '\n')
			f.close()

		all_repos[collabs] = repo_contributors

	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos


def collaborators(repos,dirName):
	if not os.path.exists(dirName):
		os.mkdir(dirName)
	filenames = []
	for collabs in repos:
		repo_contributors = []
		URL_str = 'https://api.github.com/repos/{}/{}/contributors'.format(collabs[1], collabs[0])
		new_URL = pattern.web.URL(URL_str).download()
		contributor_data = json.loads(new_URL)
		for contributor in contributor_data:
			repo_contributors.append(contributor['login'])
		fname = collabs[0] + 'collaborators.txt'
		filenames.append(fname)
		f = open(dirName+'/'+fname, 'w')
		for contributor in repo_contributors:
			f.write(contributor + '\n')
		f.close()
	f = open(dirName+'/'+'files.txt','w')
	for n in filenames:
		f.write(n+'\n')
	f.close()

def forks(repos,dirName):
	if not os.path.exists(dirName):
		os.mkdir(dirName)
	filenames = []
	for collabs in repos:
		repo_contributors = []
		URL_str = 'https://api.github.com/repos/{}/{}/forks'.format(collabs[1], collabs[0])
		new_URL = pattern.web.URL(URL_str).download()
		contributor_data = json.loads(new_URL)
		for contributor in contributor_data:
			repo_contributors.append(contributor['owner']['login'])
		fname = collabs[0] + 'forks.txt'
		filenames.append(fname)
		f = open(dirName+'/'+fname, 'w')
		for contributor in repo_contributors:
			f.write(contributor + '\n')
		f.close()
	f = open(dirName+'/'+'files.txt','w')
	for n in filenames:
		f.write(n+'\n')
	f.close()

def get_repos(users, dirName=None):
	"""Gets all the repos of a user"""
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

			URL_str = 'https://api.github.com/users/{}/repos'.format(u)
			new_URL = requests.get(URL_str, params={'page':page, 'access_token':KEY, 'per_page':100})
			# print page
			index=str(new_URL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			repo_data = json.loads(new_URL.text)
			for repo in repo_data:
				repos.append(repo['name'])
				if repo['fork']:
					forked.append(repo['name'])
		fname = u + 'repos.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in repo_contributors:
				f.write(contributor + '\n')
			f.close()
		all_repos[u] = (repos,forked)
		
	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos

def get_contributions(users, dirName = None):
	"""
	Take repos
	if fork, go to repo page
	go to parent repo
	if original user is a contributor in parent, add to list of that users contributions
	"""
	if dirName!=None:
		if not os.path.exists(dirName):
			os.mkdir(dirName)
	filenames = []
	all_repos = {}

	for u in users:
		repos = []
		page = 1

		while page>0:

			URL_str = '{}/users/{}/repos'.format(API_DOMAIN, u)
			new_URL = api_get(base_URL=URL_str, parameters={'page':page, 'access_token':KEY, 'per_page':100})
			# print page
			index=str(new_URL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			repo_data = json.loads(new_URL.text)
			try:
				for repo in repo_data:
					if repo['fork']:
						repos.append(repo['name'])
			except (KeyError,TypeError) as e:
				try:
					errorfile = open('ERROR.txt', 'w')
					errorfile.write(json.dumps(repo_data))
					errorfile.close()
				except:
					print 'could not write to file'
				raise e
		fname = u + 'repos.txt'
		filenames.append(fname)
		if dirName != None:
			f = open(dirName+'/'+fname, 'w')
			for contributor in repo_contributors:
				f.write(contributor + '\n')
			f.close()

		
		contributed = []
		for fork in repos:
			"""check for contributor"""
			repo_URL = "{}/repos/{}/{}".format(API_DOMAIN, u,fork)
			page = json.loads(api_get(base_URL=repo_URL, parameters={'access_token':KEY}).text)
			try:
				parent_repo = (page['parent']['name'], page['parent']['owner']['login'])
			except (KeyError, TypeError) as e:
				if "Repository access blocked" in page['message']:
					continue
				try:
					errorfile = open('ERROR.txt', 'w')
					errorfile.write(json.dumps(page))
					errorfile.close()
				except:
					print 'could not write to file'
				raise e

			people = contributors([parent_repo])
			#print people
			if u in people[parent_repo]:
				contributed.append(parent_repo)

		all_repos[u] = contributed
		
	if dirName!=None:
		f = open(dirName+'/'+'files.txt','w')
		for n in filenames:
			f.write(n+'\n')
		f.close()
	
	return all_repos

def api_get(base_URL, parameters = {}, min_remaining=1):
	"""If there are not enough calls remaining, wait until they refresh"""
	while True:
		try:
			URL_str = "https://api.github.com/rate_limit"
			response = requests.get(URL_str, params={'access_token':KEY})
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

			if remaining < min_remaining:
				print 'waiting'
				time_sec = int(json.loads(response.text)['resources']['core']['reset'])
				time.sleep(time_sec+5-int(time.time()))
				print 'done waiting'
			return requests.get(base_URL, params=parameters)
		except requests.exceptions.ConnectionError:
			print 'ConnectionError, trying again'
			continue
		break


if __name__=='__main__':
	print get_contributions(['Yangqing'])
	pass

#h=contributors(repo_collabs,'mlcontrib')
	# collaborators(repo_collabs,'mlcollabs')
	# forks(repo_collabs,'mlforks')
	# print get_repos(['poosomooso'])
