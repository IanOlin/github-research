# This Python file uses the following encoding: utf-8
#-*- coding: utf-8 -*-
import os, sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime, time
from pattern.web import *
from pattern.web import URL, extension, download
from sets import Set
import json
import re
import csv
import unicodedata

stack_committercount_dict = {"cinder": "cinder-openstack-dict.csv", "glance": "glance-openstack-dict.csv", "horizon": "horizon-openstack-dict.csv","keystone": "keystone-openstack-dict.csv", "neutron": "neutron-openstack-dict.csv", "nova": "nova-openstack-dict.csv", "swift": "swift-openstack-dict.csv", "cloudstack": "cloudstack-apache-dict.csv"}
ml_committercount_dict = {"Theano": "Theano-Theano-dict.csv", "CNTK": "CNTK-Microsoft-dict.csv", "caffe": "caffe-BVLC-dict.csv", "deeplearning4j": "deeplearning4j-deeplearning4j-dict.csv", "tensorflow": "tensorflow-tensorflow-dict.csv"}


"""
Opens the csv file specified and loads the result into a dictionary

input: a filename
output: a python dictionary with names as keys and commit counts as values
"""
def obtainCommittersandCount(repocommitfile): 
	filepath = "/home/anne/github-research/committer_csvs"
	name_commits_dict = {}
	for root, _, files in os.walk(filepath):
		for f in files:
			fullpath = os.path.join(root, f)
			if (f == repocommitfile):
				try:
					with open(fullpath, "rt") as f_obj:
						reader = csv.reader(f_obj)
						for row in reader:
							name = row[0].decode('utf-8')
							commitcount = int(row[1])
							name_commits_dict[name] = commitcount
				except ValueError:
					print fullpath, " has this error: ", ValueError
				except TypeError:
					print fullpath, " has this error: ", TypeError
	return name_commits_dict

"""
Calculates what 10% of the # of committers for a repo is

input: a filename (string), a percentage (int or float, like 10 or 10.0 for 10%)
output: 10% of the # of committers
"""
def num_of_percent(repocommitfile, percent):
	name_commits_dict = obtainCommittersandCount(repocommitfile)
	if (percent > 100) or ((type(percent) != int) and (type(percent) != float)):
		print "\ninvalid percentage. Try again\n"
		return 0
	return int(len(name_commits_dict)*(percent*.01))

"""
Gets the number of commits a person has for this particular project

input: name of committer (string), the repo's committer count filename (string representing .csv file)
output: number of commits by committer, if any
"""
def findNumCommits(name, repocommitfile):
	name_commits_dict = obtainCommittersandCount(repocommitfile)
	try:
		if (type(name) == str):
			return name_commits_dict[name]
		elif (type(name) == unicode):
			return name_commits_dict[name.decode("utf-8")]
	except KeyError, Argument:
		return 0

"""
Finds the available company affiliation of the committer

input: committer's name (string)
output: organizations this person worked at (list)
"""
def findHistory(name):
	pending = []
	personalHistory = []
	readablename = name.split(" ")

	try:
		name_key = ""
		if len(readablename) == 3:
			name_key += '{}{}{}'.format(readablename[0], readablename[1], readablename[2])
		elif len(readablename) == 2:
			name_key += '{}{}'.format(readablename[0], readablename[1])
		elif len(readablename) == 1:
			name_key += '{}'.format(readablename[0])
		elif len(readablename) == 4:
			name_key += '{}{}{}{}'.format(readablename[0], readablename[1], readablename[2], readablename[3])
		
		name_key_unicode = name_key.decode('utf-8')
		
		with open('companyaffiliation.json', 'r') as data_file:
			data = json.load(data_file)
			# print data_file
			try:
				return data[name_key_unicode]
			except KeyError, Argument:
				return
	except IOError, Argument:
		print "companyaffiliation.json doesn't exist yet", Argument
	except UnicodeEncodeError, Argument:
		pending.append(name)
		print "we can't decode {}".format(name), Argument

"""
Gets a list of the most prolific committers in the repo

input: repocommitfile(string representing name of csv file input), percent(int or float, the top percent of commiters we want)
output: a list of the most prolific committers in top 'percent' percent
"""
def frequentcommitters(repocommitfile, percent):
	name_commits_dict = obtainCommittersandCount(repocommitfile)
	num_percent = num_of_percent(repocommitfile, percent)
	# Loop through name_commits_dict num_percent times. (Inefficient, I know)
	committers = []
	count_max = 1
	# get the values (commit count) of the dictionary
	commit_number_list = sorted(name_commits_dict.values())[-1*num_percent:]
	for name in name_commits_dict:
		count = name_commits_dict[name]
		if (count in commit_number_list):
			committers.append(name)
	return committers

"""
Finds the # of prolific committers affiliated with the repo's organization 
(for example, how many of tensorflow's committers are affiliated with Google?)

input: the repo's committer count filename (string representing .csv file), the repo's name (string), percent (float or int, representing top % of prolificcommitters)
output: the committers who are affiliated with the repo's organization (list)
"""
def findNumEmployees(companyfile, repo, percent):
	employeeList = []
	# company is the phrase to look for in the linkedin data or email domain association
	association = {"tensorflow":["oogle", "Google"], \
					"CNTK": ["icrosoft", "Microsoft"], \
					"deeplearning4j": ["kymind", "Skymind.io"], \
					"Theano": ["Montr", "Univ. of Montreal"], \
					"caffe": ["erkeley", "Berkeley Vision and Learning Center"], \
					"cinder": ["penstack", "Openstack"], \
					"cloudstack": ["pache", "Apache Foundation"], \
					"glance": ["penstack", "Openstack"], \
					"horizon": ["penstack", "Openstack"], \
					"keystone": ["penstack", "Openstack"], \
					"neutron": ["penstack", "Openstack"], \
					"nova": ["penstack", "Openstack"], \
					"swift": ["penstack", "Openstack"]
					}
	
	company_searchterm = association[repo][0]
	company = association[repo][1]
	committers_list = frequentcommitters(companyfile, percent)
	#looping through frequentcommitters to see if this person has worked at the company
	for name_index in range(len(committers_list)):
		name = committers_list[name_index] 
		name_unicode = name.encode("utf-8")
		personalHistory = findHistory(name_unicode) #pulls up the personal work history of this person
		if personalHistory == None:
			continue
		else:
			for alist_index in range(len(personalHistory)):
				currentCompany = personalHistory[alist_index] #a list in the form of [company, dates]
				if (company_searchterm in currentCompany):
					employeeList.append(name)
					# So we don't double count:
					break
	jsondict = {}
	jsondict[percent] = {}
	jsondict[percent]["frequent"] = [len(committers_list), committers_list]
	jsondict[percent]["affiliated"] = [len(employeeList), employeeList]
	try:
		affiliated_over_overall = (len(employeeList)*100.0)/len(committers_list)
		print "Out of top {} percent of {}'s committers, at least {} percent of them are affiliated with {}".format(percent, repo, affiliated_over_overall, company)
	except ZeroDivisionError, Argument:
		print "More Commit Data needed for {}'s commits".format(repo)

	return employeeList

"""
Optional Helper Function
Scrapes the committer's linkedin profile and stores it into the file, companyaffiliation.json

input: committer's name (string), url of committer's linkedin profilei (string)
output: committer's name and work history (a tuple containing a string and a list)
"""
def getLinkedInInfo(name, url):
	driver = webdriver.Firefox(capabilities=firefox_capabilities)
	driver.get(url)
	time.sleep(2)
	title = driver.title
	orgs_worklife = driver.find_elements_by_class_name("item-subtitle")
	dateranges = driver.find_elements_by_class_name("date-range")
	orgsAndCompanies = []
	for i in range(len(dateranges)):
		try:
			daterange = dateranges[i]
			one_daterange = daterange.text.encode('ascii', 'ignore').decode('ascii')
			# print i
			one_org = orgs_worklife[i].text.encode('ascii', 'ignore').decode('ascii')
			# print one_org
			orgsAndCompanies.append((one_org, one_daterange))
		except IndexError as e:
			break
	driver.quit()
	readablename = name.encode("utf-8").split(" ")
	try:
		name_key = ""
		if len(readablename) == 3:
			name_key += '{}{}{}'.format(readablename[0], readablename[1], readablename[2])
		elif len(readablename) == 2:
			name_key += '{}{}'.format(readablename[0], readablename[1])
		elif len(readablename) == 1:
			name_key += '{}'.format(readablename[0])
		elif len(readablename) == 4:
			name_key += '{}{}{}{}'.format(readablename[0], readablename[1], readablename[2], readablename[3])
		name_key += "\n"
		name_key_unicode = name_key.decode('utf-8')

		with open('companyaffiliation.json', 'r') as data_file:
			affiliations = json.load(data_file)
		affiliations[name_key] = orgsAndCompanies

		with open('companyaffiliation.json', 'w') as data_file:
			json.dump(affiliations, data_file)
	except IOError, Argument:
		print "companyaffiliation.json doesn't exist yet", Argument
	except UnicodeEncodeError, Argument:
		print "we can't decode {}".format(name), Argument
	return name, orgsAndCompanies

if __name__ == '__main__':
	stack_committercount_dict = {"cinder": "cinder-openstack-dict.csv", "glance": "glance-openstack-dict.csv", "horizon": "horizon-openstack-dict.csv","keystone": "keystone-openstack-dict.csv", "neutron": "neutron-openstack-dict.csv", "nova": "nova-openstack-dict.csv", "swift": "swift-openstack-dict.csv", "cloudstack": "cloudstack-apache-dict.csv"}
	ml_committercount_dict = {"Theano": "Theano-Theano-dict.csv", "CNTK": "CNTK-Microsoft-dict.csv", "caffe": "caffe-BVLC-dict.csv", "deeplearning4j": "deeplearning4j-deeplearning4j-dict.csv", "tensorflow": "tensorflow-tensorflow-dict.csv"}
	percent = 100
	for repo in ml_committercount_dict:
		csv_file = ml_committercount_dict[repo]
		findNumEmployees(csv_file, repo, percent)
	print "\n"