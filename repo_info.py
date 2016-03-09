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
#Generate a list of repos & username associated with that particular repo: list = [(repo1, un1), (repo2, un2), etc.]

repo_collabs = [('Theano', 'Theano'), ('caffe', 'BVLC'), ('CNTK', 'Microsoft'), ('tensorflow', 'tensorflow'), ('torch7', 'torch'), ('deeplearning4j', 'deeplearning4j')]


#Use that list's info to get api info/obtain list of collaborators

#Obtain json stuffz from api info

#grab specific pieces of data & store it

"""list of repos with the format (reponame, ownername)"""
def contributors(repos,dirName):
	if not os.path.exists(dirName):
		os.mkdir(dirName)
	filenames = []
	all_repos = {}
	for collabs in repos:
		repo_contributors = []
		page = 1

		while page>0:

			URL_str = 'https://api.github.com/repos/{}/{}/contributors?page={}'.format(collabs[1], collabs[0],page)
			new_URL = requests.get(URL_str)#pattern.web.URL(URL_str).download()
			print new_URL.headers
			index=str(new_URL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1
			contributor_data = json.loads(new_URL.text)
			for contributor in contributor_data:
				repo_contributors.append(contributor['login'])
		fname = collabs[0] + 'contributors.txt'
		filenames.append(fname)
		f = open(dirName+'/'+fname, 'w')
		for contributor in repo_contributors:
			f.write(contributor + '\n')
		f.close()
		all_repos[collabs[0]] = repo_contributors
		

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

			URL_str = 'https://api.github.com/users/{}}/repos'.format(collabs)
			new_URL = requests.get(URL_str)
			print new_URL.headers
			index=str(new_URL.headers).find('rel="next"')
			if index<0:
				page = -1
			else:
				page+=1

			repo_data = json.loads(new_URL.text)
			for repo in repo_data:
				repos.append(repo['name'])
				if repos['fork']:
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


#if __name__=='__main__':
#h=contributors(repo_collabs,'mlcontrib')
	# collaborators(repo_collabs,'mlcollabs')
	# forks(repo_collabs,'mlforks')
print get_repos('poosomooso')
