#Save the file


import pattern.web
import json 
#Generate a list of repos & username associated with that particular repo: list = [(repo1, un1), (repo2, un2), etc.]

repo_collabs = [('Theano', 'Theano'), ('caffe', 'BVLC'), ('CNTK', 'Microsoft'), ('tensorflow', 'tensorflow'), ('torch7', 'torch'), ('deeplearning4j', 'deeplearning4j')]


#Use that list's info to get api info/obtain list of collaborators

#Obtain json stuffz from api info 

#grab specific pieces of data & store it

for collabs in repo_collabs:
	repo_contributors = []
	URL_str = 'https://api.github.com/repos/{}/{}/stats/contributors'.format(collabs[1], collabs[0])
	new_URL = pattern.web.URL(URL_str).download()
	contributor_data = json.loads(new_URL)
	for contributor in contributor_data:
		repo_contributors.append(contributor['author']['login'])
	f = open(collabs[0] + '.txt', 'w')
	for contributor in repo_contributors:
		f.write(contributor + '\n')
	f.close()
