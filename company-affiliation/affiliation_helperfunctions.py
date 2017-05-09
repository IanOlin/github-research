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

# PATHtoLinkedInJSONs = "/home/anne/github-research/company-affiliation/resources/linkedin_info/"

DEBUG = True
pending = []

def obtainCommittersandCount(companyfile): 
	filepath = "/home/anne/github-research/committer_csvs"
	name_commits_dict = {}
	for root, _, files in os.walk(filepath):
		for f in files:
			fullpath = os.path.join(root, f)
			if (f == companyfile):
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

def num_of_percent(companyfile, percent):
	name_commits_dict = obtainCommittersandCount(companyfile)
	if (percent > 100):
		print "\ninvalid percentage. Try again\n"
		return 0
	return int(len(name_commits_dict)*(percent*.01))

"""
Gets the number of commits this person has for this particular project
"""
def findNumCommits(name, companyfile):
	name_commits_dict = obtainCommittersandCount(companyfile)
	return name_commits_dict[name]

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
				# print data[name_key]
				print data
				print name_key
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
def frequentcommitters(companyfile, company, percent):
	name_commits_dict = obtainCommittersandCount(companyfile)
	num_percent = num_of_percent(companyfile, percent)
	# Loop through name_commits_dict num_percent times. (Inefficient, I know)
	committers = []
	count_max = 1
	# get the values (commit count) of the dictionary
	commit_number_list = sorted(name_commits_dict.values())[-1*num_percent:]
	print commit_number_list
	for name in name_commits_dict:
		count = name_commits_dict[name]
		if (count in commit_number_list):
			committers.append(name)
	jsondict = {"frequent": committers}
	with open('{}_frequentcommitters.json'.format(company), 'w') as f:
		json.dump(jsondict, f)
	return jsondict

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
def findNumEmployees(companyfile, repo, percent):
	numEmployees = 0
	employeeList = []
	company = ""
	# company is the phrase to look for in the linkedin data or email domain association
	if (repo == "tensorflow"):
		company += "Google"
	elif (repo == "CNTK"):
		company += "Microsoft"
	elif (repo == "deeplearning4j"):
		company += "Skymind"
	elif (repo == "Theano"):
		company += "Montr"
	elif (repo == "caffe"):
		company += "Berkeley"

	committers_list = frequentcommitters(companyfile, repo, percent)["frequent"]
	#looping through frequentcommitters to see if this person has worked at the company
	for name_index in range(len(committers_list)):
		name = committers_list[name_index] 
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
	repo = "Theano"
	csv_file = "Theano-Theano-dict.csv"
	percent = 10

	# print obtainCommittersandCount(csv_file)
	# print frequentcommitters(csv_file, repo, percent)

	print findNumEmployees(csv_file, repo, percent)[0]
	print findHistory("Frédéric Bastien")
	# json_file = '{}_frequentcommitters.json'.format(repo)
	# with open(json_file, 'r') as data_file:
	# 	jsondict = json.load(json_file)
	# 	committers = jsondict["frequent"]

	# affiliatedcommitters = findNumEmployees(csv_file, repo, percent)[0]
	# print "affiliated, ", affiliatedcommitters
