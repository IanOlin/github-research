# This Python file uses the following encoding: utf-8
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

PATHtoLinkedInJSONs = "/home/anne/github-research/company-affiliation/resources/linkedin_info/"
DEBUG = True
pending = []


"""
Takes in all the results of the json file and returns the info we really need in a tuple
returns: (date list, sha list, name list)
Keep in mind the names aren't in their final, simplified form. There are duplicates in this names list.
"""
def obtainDatesShasNames(filename):
	commits = json.load(open(filename, 'r'))
	shas = []
	names = []
	dates = []
	companies = []
	for c in commits:
		#TODO:
		#store dates in dates
		dates.append(c["commit"]["author"]["date"].encode("utf-8"))
		#store sha in shas
		commiturl = c["commit"]["url"]
		commiturl_list = commiturl.split("/")
		shas.append(commiturl_list[-1].encode("utf-8"))
		#store name in names
		names.append(c["commit"]["author"]["name"])
		pass
	filterLists(dates, shas, names)
	return (dates, shas, names)

"""
Gets one of each name and stores the results into a list
"""
def simplifyNameList(comprehensiveNameList):
	newNameSet = Set()
	for name in comprehensiveNameList:
		newNameSet.add(name)
	return list(newNameSet)

def num_of_10percent(companyfile):
	(dates, shas, names) = obtainDatesShasNames(companyfile)
	total_committer_list = simplifyNameList(names)
	return len(total_committer_list)*.1
def num_of_20percent(companyfile):
	(dates, shas, names) = obtainDatesShasNames(companyfile)
	total_committer_list = simplifyNameList(names)
	return len(total_committer_list)*.2

"""
Gets the number of commits this person has for this particular project
"""
def findNumCommits(name, companyfile):
	numcommits = 0
	(dates, shas, names) = obtainDatesShasNames(companyfile)
	for currentname in names:
		if name == currentname:
			numcommits += 1
	return numcommits

"""
eliminate Jenkins, OpenStack Proposal Bot, and Openstack Jenkins
"""
def filterLists(dates, shas, names):
	for i in range(len(names) - 1, -1, -1):
		n = names[i]
		if (n == 'OpenStack Proposal Bot') or (n == 'Jenkins') or (n == 'OpenStack Jenkins') or (n == "A Unique TensorFlower"):
			index_location = names.index(n)
			del names[index_location]
			del shas[index_location]
			del dates[index_location]

# Find this person's work history if it's saved. If not, save it to a file called "pending"
def findHistory(name):
	global pending
	personalHistory = []
	readablename = name.split(" ")
	# print readablename
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
		with open('companyaffiliation.json', 'r') as data_file:
			data = json.load(data_file)
			# print data_file
			try:
				return data[name_key]
			except KeyError, Argument:
				pending.append(name)
	except IOError, Argument:
		print "companyaffiliation.json doesn't exist yet", Argument
	except UnicodeEncodeError, Argument:
		pending.append(name)
		print "we can't decode {}".format(name), Argument


"""
Helper function: get the top 10% of committers at a company and saves it to a file
"""
def frequentcommitters(companyfile, company):
	# Obtain info for all commits
	(dates, shas, names) = obtainDatesShasNames(companyfile)
	# Obtain list of names with each name only once
	uniquenames = simplifyNameList(names)
	frequentcommitters = {}
	print "going through {}'s committers. progress: \n".format(companyfile)
	for name_index in range(len(uniquenames)):
		name = uniquenames[name_index]
		print name_index + 1, "out of ", len(uniquenames), " total committers"
		if (findNumCommits(name, companyfile) > 2):
			frequentcommitters[name] = findNumCommits(name, companyfile)
	# For debugging:
	# print frequentcommitters
	# Sort the frequent committers by making a histogram:	
	num_20percent = num_of_20percent(companyfile)
	resultinglist = []
	# We do this every time until we get 10% of the committers for this companyfile
	while (num_20percent > 0):
		committer_name = ""
		max_commits = 3
		# Getting the top committer in this list
		for name in frequentcommitters:
			if frequentcommitters[name] > max_commits:
				committer_name = name
				max_commits = frequentcommitters[name]
		# add the name to the resulting list
		resultinglist.append(committer_name)
		# delete the highest # of commits result to get the next one
		del(frequentcommitters[committer_name])
		# Decrement the num_20percent so the while loop doesn't last forever
		num_20percent -= 1
	# save resultinglist into a json file with companyfile as the key
	jsondict = {}
	jsondict["overall"] = resultinglist
	with open('{}_frequentcommitters.json'.format(company), 'w') as f:
		json.dump(jsondict, f)
	return resultinglist

#Emergency linkedin processing. if we ever need this method again
def getLinkedInInfo(name, url):
	driver = webdriver.Firefox(capabilities=firefox_capabilities)
	if DEBUG:
		print driver
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
	time.sleep(2)
	readablename = name.encode("utf-8").split(" ")
	fileOpener = ""
	if (len(readablename) == 1):
		fileOpener += PATHtoLinkedInJSONs + '{}_linkedin.json'.format(readablename[0])
	elif (len(readablename) == 2):
		fileOpener += PATHtoLinkedInJSONs + '{}{}_linkedin.json'.format(readablename[0], readablename[1])
	elif (len(readablename) == 3):
		fileOpener += PATHtoLinkedInJSONs + '{}{}{}_linkedin.json'.format(readablename[0], readablename[1], readablename[2])
	elif (len(readablename) == 4):
		fileOpener += PATHtoLinkedInJSONs + '{}{}{}_linkedin.json'.format(readablename[0], readablename[1], readablename[2], readablename[3])
	f = open(fileOpener, 'w')
	json.dump(orgsAndCompanies, f)
	f.close()
	return name + str(orgsAndCompanies)

#Given company & work history, look for the word "Tensorflow", or "Google" for the tensorflow project
#Look for "CNTK" or "Microsoft" for the CNTK project
def findNumEmployees(project, committers_list):
	numEmployees = 0
	employeeList = []
	company = ""
	# company is the phrase to look for in the linkedin data or email domain association
	if (project == "/home/anne/ResearchJSONs/tensorflow-tensorflow-commits.json"):
		company += "Google"
	elif (project == "/home/anne/ResearchJSONs/CNTK-Microsoft-commits.json"):
		company += "Microsoft"
	elif (project == "/home/anne/ResearchJSONs/deeplearning4j-deeplearning4j-commits.json"):
		company += "Skymind"
	elif (project == "/home/anne/ResearchJSONs/Theano-Theano-commits.json"):
		company += "Montr"
	elif (project == "/home/anne/ResearchJSONs/caffe-BVLC-commits.json"):
		company += "Berkeley"

	print "frequent committers: ", committers_list
	#looping through frequentcommitters to see if this person has worked at the company
	for name_index in range(len(committers_list)):
		name = committers_list[name_index] 
		# print name_index, " out of ", len(committers_list), "frequent committers"
		try:
			# Find this person's linkedin history
			personalHistory = findHistory(name) #pulls up the personal work history of this person
			if personalHistory == None:
				pending.append(name)
			else:
				for alist_index in range(len(personalHistory)):
					currentCompany = personalHistory[alist_index] #a list in the form of [company, dates]
					if (company in currentCompany):
						employeeList.append(name)
						numEmployees += 1
						# So we don't double count:
						break
		except IOError, Argument:
			pending.append(name)
			# print "this person's file doesn't exist yet", Argument
		except UnicodeEncodeError, Argument:
			pending.append(name)
			# print "we can't decode this name", Argument
	return employeeList, numEmployees

if __name__ == '__main__':
	# frequentcommitterslist = frequentcommitters(companyfile)
	# Getting last minute linkedin data
	# committerprofiles = {u'sonaliii': "https://www.linkedin.com/in/sonali-dayal"}
	# for name in committerprofiles:
	# 	print name
	# 	getLinkedInInfo(name, committerprofiles[name])

	companyfilepath = "/home/anne/ResearchJSONs/" + "deeplearning4j-deeplearning4j-commits.json"
	repo = 'deeplearning4j'
	
	# frequentcommitters(companyfilepath, repo)


	resultingfile = '{}_frequentcommitters.json'.format(repo)
	with open(resultingfile, 'r') as data_file:
		jsondict = json.load(data_file)
		committers = jsondict["overall"]

	affiliatedcommitters = findNumEmployees(companyfilepath, committers)[0]
	print affiliatedcommitters

	jsondict["affiliated"] = affiliatedcommitters

	f = open(resultingfile, 'w')
	json.dump(jsondict, f)
	f.close()
