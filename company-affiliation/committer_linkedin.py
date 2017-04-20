# This Python file uses the following encoding: utf-8

# Make one big happy JSON file that has everybody's company list

import os, sys, os.path
from datetime import datetime, time
from pattern.web import *
from pattern.web import URL, extension, download
from sets import Set
import json
import re
PATHtoLinkedInJSONs = "resources/linkedin_info/"

def getLinkedInJSON(path):
	# readablename = name.encode("utf-8").split(" ")
	fileOpener = path
	with open(path) as json_data:
		d = json.load(json_data)
	return d

def get_committer_workhistory(path):
	companies = []
	committer_history = getLinkedInJSON(path)
	for item in range(len(committer_history)):
		companies.append(committer_history[item][0])
	return companies

if __name__ == '__main__':
	JSONdump = {}
	# print get_committer_workhistory("/home/anne/github-research/company-affiliation/resources/linkedin_info/AdamGibson_linkedin.json")
	for root, _, files in os.walk("/home/anne/github-research/company-affiliation/resources/linkedin_info"):
	    for f in files:
	        fullpath = os.path.join(root, f)
	        try:
	        	workhistory = get_committer_workhistory(fullpath)
	        	# Get the name of the file & cut out the "_linkedin.json" portion
	        	readablename = fullpath[71:-14]
	        	JSONdump[readablename] = workhistory
	        except ValueError:
	        	print fullpath, " has this error: ", ValueError
	        except TypeError:
	        	print fullpath, " has this error: ", TypeError
	with open("companyaffiliation.json", 'w') as results:
		json.dump(JSONdump, results)
