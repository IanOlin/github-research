from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

# Go here to install dependencies for chrome webdriver: https://christopher.su/2015/selenium-chromedriver-ubuntu/
from datetime import datetime, time
from pattern.web import * 
from pattern.web import URL, extension, download
import json
import pickle
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from sets import Set
import os
import json
import sys 
from unidecode import unidecode 

PATH = "../resources/linkedin_info/"
DEBUG = True

indexToStart = 0
# START_AT_INDEX = False
signup = 0
stubbornpeople = []


def findlinkedininfo(name_list, START_AT_INDEX): #name is a tuple, StART_AT_INDEX is a boolean if we can implement it
	"""
	Takes in a list of names as a tuple and returns a file for each name if there is linkedin info for that name
	"""
	global signup
	global stubbornpeople
	allcompanies = []

	if START_AT_INDEX:
		with open("index.txt", 'r') as f:
			s = f.readline() #(indexToStart).strip()
			global indexToStart
			indexToStart = int(s)

	for j in range(indexToStart, len(name_list)):
		name = name_list[j]
		print "{}'s index: ".format(name.encode("utf-8")) + str(j)
		driver = webdriver.Firefox(capabilities=firefox_capabilities)
		if DEBUG:
			print driver
		#example: What to put in the open() URL area for Geetika Batra: https://www.google.com/#q=Geetika+Batra+linkedin
		driver.get('https://www.google.com/#q={}+linkedin'.format(name.encode("utf-8")))
		time.sleep(2)
		google_results = driver.find_elements_by_class_name("r") # should get the headlines/main title of each google result

		orgsAndCompanies = []
		for res in google_results:
			googleresult_headline = str(res.text.encode('ascii', 'ignore').decode('ascii')) #The headline you see in each google result
			if (str(res.text.encode('ascii', 'ignore').decode('ascii'))[-10:]) == "| LinkedIn": #slice the string from -10 to -1 to get  "| LinkedIn"
				#getting the index that fits the if statement's qualifications
				index = google_results.index(res)
				if DEBUG:
					print index;

				profile_url = driver.find_elements_by_class_name('_Rm')[index].text.encode('ascii', 'ignore').decode('ascii')
				
				# opening the Linkedin URL
				driver.get(profile_url)
				time.sleep(2)
				title = driver.title #driver.find_element_by_tag_name('title').text.encode('ascii', 'ignore').decode('ascii')
				if (title == "Sign Up | LinkedIn"):
					#Adding this name to the stubbornpeople list, incrementing the times we encounter this signup page
					signup = signup + 1
					#commenting out all the index related functions because I'm planning to remove
					# some problem people to a different file
					# indexToStart = j
					# print "last index: " + str(j)
					driver.quit()

					# with open("index.txt", 'w') as f:
					# 	f.write(str(j + 1))

					with open("stubbornpeoplefile.json", 'r') as f:						
						current_stubbornpeople_file = json.load(f)
						current_stubbornpeople_file["glance-openstack"].append(name)
						name_list.remove(name) #removing because we already added the name ot the stubborn people list

					with open("stubbornpeoplefile.json", 'w') as f:
						json.dump(current_stubbornpeople_file, f)

					# If we get this 1-2 times, then let's try again:
					if (signup < 4):
						time.sleep(60) #wait 1 minute and try again.
						return findlinkedininfo(name_list, False)
					else: #Stop this program
						sys.exit(0)


				#Messy lines that help find the text in the item-subtitle and date-range classes				
				orgs_worklife = driver.find_elements_by_class_name("item-subtitle")
				dateranges = driver.find_elements_by_class_name("date-range")

				for i in range(len(dateranges)):
					try:
						daterange = dateranges[i]
						one_daterange = daterange.text.encode('ascii', 'ignore').decode('ascii')
						print i
						one_org = orgs_worklife[i].text.encode('ascii', 'ignore').decode('ascii')
						orgsAndCompanies.append((one_org, one_daterange))
					except IndexError as e:
						break

				driver.close()
				time.sleep(2)
				break
		f = open(PATH+'{}_linkedin.json'.format(name.encode("utf-8")), 'w')
		json.dump(orgsAndCompanies, f)
		allcompanies.append(orgsAndCompanies)
		f.close()
		driver.quit()
	return allcompanies

"""
Changing the directory so that the headline files are stored in a convenient place
"""
def changeDirectory():
	# Check current working directory.
	retval = os.getcwd()
	if DEBUG:
		print "Current working directory %s" % retval

	# Now change the directory
	os.chdir( PATH )

	# Check current working directory.
	retval = os.getcwd()

	if DEBUG:
		print "Directory changed successfully %s" % retval


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
eliminate Jenkins, OpenStack Proposal Bot, and Openstack Jenkins
Also replaces the email with the person's actual name
"""
def filterLists(dates, shas, names):
	for i in range(len(names) - 1, -1, -1):
		n = names[i]
		if (n == 'OpenStack Proposal Bot') or (n == 'Jenkins') or (n == 'OpenStack Jenkins'):
			index_location = names.index(n)
			del names[index_location]
			del shas[index_location]
			del dates[index_location]

	#TODO:
	#call findlinkedininfo on list of names, save in companies
	#change all Nones to "no company" with a flag of 0, change all other companies to a flag of like 3.
	#for others, find the company that matches the date in date
	#zip shas and companies to a dict or something
	#save to file


def getFinalNameList(filename):
	"""
	returns the final list of names to run
	"""
	# get the file name of the filename path variable here:


	(dates, shas, names) = obtainDatesShasNames(filename)
	#Getting one of each name
	finalcompletenamelist = list(simplifyNameList(names))
	# get the ones without linkedin profiles so far:
	finalnamelist = []
	for i in range(len(finalcompletenamelist)):
		name = finalcompletenamelist[i]
		with open(PATH+'{}_linkedin.json'.format(name.encode("utf-8"))) as data_file:
			data = json.load(data_file)
			if len(data) == 0: #if we don't have data on this person, append him/her to the new list
				finalnamelist.append(name)

	#remove any names that appear in the stubbornpeoplefile file:
	with open("stubbornpeoplefile.json", 'r') as f:						
		current_stubbornpeople_file = json.load(f)

	#get right versions of names in finalnamelist in here:
	stubbornpeoplelist = current_stubbornpeople_file["glance-openstack"]
	for i in range(len(stubbornpeoplelist)):
		stubbornperson = stubbornpeoplelist[i]
		rightversion = unidecode(stubbornperson)
		stubbornpeoplelist.remove(stubbornperson)
		stubbornpeoplelist.append(rightversion)

		current_stubbornpeople_file["glance-openstack"] = stubbornpeoplelist
		# print current_stubbornpeople_file["glance-openstack"]


	for i in range(len(finalnamelist) - 1):
		print i
		name = finalnamelist[i]
			
		if name in current_stubbornpeople_file["glance-openstack"]:
			finalnamelist.remove(name)
	return finalnamelist
	
def runLinkedinProcess(filename):
	"""
	runs everything
	"""
	finalnamelist = getFinalNameList(filename) #Change True to False if you want to start at the beginning
	findlinkedininfo(finalnamelist, False)


def JSON_access(jsonObject, keyTuple):
    try:
        breakdown = jsonObject
        #following the keys through the json structure
        for key in keyTuple:
            breakdown = breakdown[key]
        return breakdown
    except (KeyError, TypeError) as e:
        print "{}\n{}\n{}".format(json.dumps(jsonObject), breakdown, keyTuple)
        raise e


if __name__ == '__main__':
	pathtojsons = "/home/jwb/research/"
	companyfile = pathtojsons+"glance-openstack-commits.json" # + "filename"
	print "hello!"
	runLinkedinProcess(companyfile)
