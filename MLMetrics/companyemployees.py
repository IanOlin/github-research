# So... I already got the names of all the committers
# Next, find out if they work in that company
	# If they currently do, then flag that person as a 2
	# If they used to but currently don't, then flag him/her as a 1
	# If they haven't worked there at all, then flag him/her as a 0
# Tally up all the 2s, 1s, and 0s and print them out

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
	return newNameSet
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
		if (n == 'OpenStack Proposal Bot') or (n == 'Jenkins') or (n == 'OpenStack Jenkins'):
			index_location = names.index(n)
			del names[index_location]
			del shas[index_location]
			del dates[index_location]

def findHistory(name):
	global pending
	personalHistory = []
	readablename = name.split(" ")
	# print readablename
	try:
		fileOpener = ""
		if len(readablename) == 3:
			fileOpener += PATHtoLinkedInJSONs+'{}{}{}_linkedin.json'.format(readablename[0], readablename[1], readablename[2])
		elif len(readablename) == 2:
			fileOpener += PATHtoLinkedInJSONs+'{}{}_linkedin.json'.format(readablename[0], readablename[1])
		with open(fileOpener) as data_file:
			data = json.load(data_file)
			if len(data) == 0: #if we don't have data on this person
				pending.append(name)
			else:
				for line in data:
					personalHistory.append(line)
	except IOError, Argument:
		pending.append(name)
		# print "this person's file doesn't exist yet", Argument
	except UnicodeEncodeError, Argument:
		pending.append(name)
		# print "we can't decode this name", Argument
	return personalHistory

"""
Helper function: get the people with 3+ commits for this company
"""
def frequentcommitters(companyfile):
	(dates, shas, names) = obtainDatesShasNames(companyfile)
	uniquenames = simplifyNameList(names)
	frequentcommitters = []
	# print "the committers:"
	for name in uniquenames:
		# print name
		if (findNumCommits(name, companyfile) > 2):
			frequentcommitters.append(name)
	return frequentcommitters

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
	if (len(readablename) == 1):
		f = open(PATHtoLinkedInJSONs + '{}_linkedin.json'.format(readablename[0]), 'w')
	if (len(readablename) == 2):
		f = open(PATHtoLinkedInJSONs + '{}{}_linkedin.json'.format(readablename[0], readablename[1]), 'w')
	if (len(readablename) == 3):
		f = open(PATHtoLinkedInJSONs + '{}{}{}_linkedin.json'.format(readablename[0], readablename[1], readablename[2]), 'w')
	json.dump(orgsAndCompanies, f)
	f.close()
	return name + str(orgsAndCompanies)

#Given company & work history, look for the word "Tensorflow", or "Google" for the tensorflow project
#Look for "CNTK" or "Microsoft" for the CNTK project
def findNumEmployees(project):
	numEmployees = 0
	committers = frequentcommitters(project)
	company = ""
	if (project == "/home/anne/ResearchJSONs/tensorflow-tensorflow-commits.json"):
		company += "Google"
	elif (project == "/home/anne/ResearchJSONs/CNTK-Microsoft-commits.json"):
		company += "Microsoft"
	elif (project == "/home/anne/ResearchJSONs/deeplearning4j-deeplearning4j-commits.json"):
		company += "Skymind"
	elif (project == "/home/anne/ResearchJSONs/Theano-Theano-commits.json"):
		company += "Montreal"
	elif (project == "/home/anne/ResearchJSONs/caffe-BVLC-commits.json"):
		company += "Berkeley"
	
	#looping through frequentcommitters to see if this person has worked at the company
	for name in committers:
		try:
			personalHistory = findHistory(name) #pulls up the personal work history of this person
			for alist_index in range(len(personalHistory)):
				currentCompany = personalHistory[alist_index] #a list in the form of [company, dates]
				if (company in currentCompany[0]):
					numEmployees += 1
					alist_index += 1
		except IOError, Argument:
			pending.append(name)
			# print "this person's file doesn't exist yet", Argument
		except UnicodeEncodeError, Argument:
			pending.append(name)
			# print "we can't decode this name", Argument
	return numEmployees

if __name__ == '__main__':
	companyfile = "/home/anne/ResearchJSONs/" + "caffe-BVLC-commits.json" # + "filename"
	print "Caffe, Berkeley: ", findNumEmployees("/home/anne/ResearchJSONs/" + "caffe-BVLC-commits.json")
	print "Tensorflow, Google: ", findNumEmployees("/home/anne/ResearchJSONs/" + "tensorflow-tensorflow-commits.json")
	print "CNTK-Microsoft: ", findNumEmployees("/home/anne/ResearchJSONs/" + "CNTK-Microsoft-commits.json")
	print "Theano, Montreal: ", findNumEmployees("/home/anne/ResearchJSONs/" + "Theano-Theano-commits.json")
	print "deeplearning4j, Skymind: ", findNumEmployees("/home/anne/ResearchJSONs/" + "deeplearning4j-deeplearning4j-commits.json")
	# pendinglist = {u'Lukasz Kaiser': "https://www.linkedin.com/in/lukaszkaiser", u'A. Rosenberg Johansen': "https://www.linkedin.com/in/alexander-rosenberg-johansen/en", u'SeongJae Park': "https://kr.linkedin.com/in/seongjae-park-1a5b9954", u'Manjunath Kudlur': "https://www.linkedin.com/in/keveman", u'Sung Kim': "https://hk.linkedin.com/in/hunkim", u'Di Zeng': "https://www.linkedin.com/in/dizeng", u'Zakaria Haque': "https://www.linkedin.com/in/zakariahaque", u'Igor Babuschkin': "https://uk.linkedin.com/in/igor-babuschkin-9bb5bab6", u'Noah Fiedel': "https://www.linkedin.com/in/noahfiedel", u'Alexander Rosenberg Johansen': "https://www.linkedin.com/in/alexander-rosenberg-johansen/en", u'Yuan (Terry) Tang': "https://www.linkedin.com/in/yuan-terry-tang-117ba962", u'Andrew Selle': "https://www.linkedin.com/in/andrew-selle-849a6b3", u'Craig Citro': "https://www.linkedin.com/in/craig-citro-54822651", u'luke iwanski': "https://uk.linkedin.com/in/lukeiwanski", u'Vinu Rajashekhar': "https://www.linkedin.com/in/vinu-rajashekhar-61377341", u'Ali Elqursh': "https://www.linkedin.com/in/ali-elqursh-57909324", u'Sergio Guadarrama': "https://www.linkedin.com/in/sergio-guadarrama-1724379", u'Martin Wicke': "https://www.linkedin.com/in/martin-wicke-a7b70514", u'Robert DiPietro': "https://www.linkedin.com/in/robert-dipietro-6910565a", u'Liangliang He': "https://www.linkedin.com/in/lianglianghe", u'Sukriti Ramesh': "https://www.linkedin.com/in/sukritiramesh", u'Vijay Vasudevan': "https://www.linkedin.com/in/vijay-vasudevan-a5062434", u'Martin Englund': "https://www.linkedin.com/in/pmenglund", u'Nikhil Thorat': "https://www.linkedin.com/in/nikhil-thorat-58a18232", u'Shanqing Cai': "https://www.linkedin.com/in/shanqingcai"}
	# for name in pendinglist:
	# 	print name
	# 	url = pendinglist[name]
	# 	getLinkedInInfo(name, url)
	# for name in frequentcommitterslist:
	# 	print findHistory(name)
	# print pending