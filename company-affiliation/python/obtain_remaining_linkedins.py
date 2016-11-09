# Script for people we didn't get linkedin with
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

# Go here to install dependencies for chrome webdriver: https://christopher.su/2015/selenium-chromedriver-ubuntu/
from datetime import datetime, time
from pattern.web import * 
from pattern.web import URL, extension, download
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from sets import Set
import os
from pprint import pprint

PATH = "../resources/linkedin_info/"
DEBUG = True

#Getting functions from get_linkedin_info.py
from get_linkedin_info import changeDirectory, obtainDatesShasNames, simplifyNameList, filterLists, commitsToCompanies, JSON_access
indexToStart = 0

#TODO:
#1. Get all the names (literallly all of them) in a list I can run through- Check!
#2. Open the JSON files iteratively. If the JSON is empty, add the name to the list. If it isn't empty, close it/don't modify it. - check!
#3. Run a modified get_linkedin_info.py script to get more linkedin info

def getnames(filename):
	"""
	returns the element or json object from the tuple of keys
	"""
	(dates, shas, names) = obtainDatesShasNames(filename)
	#Getting one of each name
	finalnamelist = list(simplifyNameList(names))
	needslinkedIn_list = [] 
	for i in range(len(finalnamelist)):
		name = finalnamelist[i]
		with open(PATH+'{}_linkedin.json'.format(name)) as data_file:
			data = json.load(data_file)
			if len(data) ==0:
				needslinkedIn_list.append(name)
	return needslinkedIn_list

def findlinkedininfo(name_list, START_AT_INDEX): #name is a tuple, StART_AT_INDEX is a boolean if we can implement it
	"""
	Takes in a list of names as a tuple and returns a file for each name if there is linkedin info for that name
	"""
	allcompanies = []

	if START_AT_INDEX:
		with open("index.txt", 'r') as f:
			s = f.readline() 
			global indexToStart
			indexToStart = int(s)

	print "starting index: ",  indexToStart


	for j in range(indexToStart, len(name_list)): 
		name = name_list[j]
		print "{}'s index: ".format(name) + str(j)
		print name
		driver = webdriver.Firefox(capabilities=firefox_capabilities)
		if DEBUG:
			print driver
		#What to put in the open() URL area for Geetika Batra: https://www.google.com/#q=Geetika+Batra+linkedin
		driver.get('https://www.google.com/#q={}+linkedin'.format(name))
		time.sleep(2)
		google_results = driver.find_elements_by_class_name("r") # should get the headlines/main title of each google result

		orgsAndCompanies = []
		for res in google_results:
			googleresult_headline = str(res.text.encode('ascii', 'ignore').decode('ascii')) #The headline you see in each google result
			if (googleresult_headline[-10:]) == "| LinkedIn": #Takes the first linkedin profile it sees.
				#getting the index that fits the if statement's qualifications
				index = google_results.index(res)
				if DEBUG:
					print index;

				profile_url = driver.find_elements_by_class_name('_Rm')[index].text.encode('ascii', 'ignore').decode('ascii')
				
				# opening the Linkedin URL
				driver.get(profile_url)
				time.sleep(2)
				title =  driver.title #driver.find_element_by_tag_name('title').text.encode('ascii', 'ignore').decode('ascii')
				if (title == "Sign Up | LinkedIn"):
					indexToStart = j
					print "last index: " + str(j)
					driver.quit()

					with open("index.txt", 'w') as f:
						j += 1
						f.write(str(j)) #this way we can skip over the stubborn ones

					driver.close()
					break
					return name_list #Supposed to break out of everything
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
		f = open(PATH+'{}_linkedin.json'.format(name), 'w')
		json.dump(orgsAndCompanies, f)
		allcompanies.append(orgsAndCompanies)
		f.close()
		driver.quit()
	return allcompanies


if __name__ == '__main__':
	pathtojsons = "/home/anne/"
	companyfile = pathtojsons+"glance-openstack-commits.json" # + "filename"
	print "hello!"
	namelist = getnames(companyfile)
	print len(namelist)
	findlinkedininfo(namelist, True)