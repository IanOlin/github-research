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
from pyvirtualdisplay import Display
from sets import Set
import os
import json

PATH = "../resources/linkedin_info/"
DEBUG = True

# shas = []
# names = []
# dates = []
# companies = []

problemPeople = []
indexToStart = 0
START_AT_INDEX = False
def findlinkedininfo(name_list): #name is a tuple, predefinedlinkedin is a boolean if we can implement it
	"""
	Takes in a list of names as a tuple and returns a file for each name if there is linkedin info for that name
	"""
	allcompanies = []

	if START_AT_INDEX:
		with open("index.txt", 'r') as f:
			s = f.read(indexToStart).strip();
			global indexToStart
			indexToStart = int(s)

	for j in range(indexToStart, len(name_list)):
		name = name_list[j]
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
			if (str(res.text.encode('ascii', 'ignore').decode('ascii'))) == "{} | LinkedIn".format(name):
				#getting the index that fits the if statement's qualifications
				index = google_results.index(res)
				if DEBUG:
					print index;

				profile_url = driver.find_elements_by_class_name('_Rm')[index].text.encode('ascii', 'ignore').decode('ascii')
				
				# opening the Linkedin URL
				driver.get(profile_url)
				time.sleep(2)
				title = driver.find_element_by_tag_name('title').text.encode('ascii', 'ignore').decode('ascii')
				if (title == "Sign Up | LinkedIn"):
					indexToStart = j
					print j
					driver.quit()
					print problemPeople
					return allcompanies
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
						problemPeople.append("{}, {}, {}".format(name, i, orgsAndCompanies))
						break

				driver.close()
				time.sleep(2)
				break
		f = open(PATH+'{}_linkedin.json'.format(name), 'w')
		json.dump(orgsAndCompanies, f)
		allcompanies.append(orgsAndCompanies)
		f.close()
		driver.quit()
	print problemPeople
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
		names.append(c["commit"]["author"]["name"].encode("utf-8"))
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


def commitsToCompanies(filename):
	"""
	returns the element or json object from the tuple of keys
	"""
	(dates, shas, names) = obtainDatesShasNames(filename)
	#Getting one of each name
	finalnamelist = list(simplifyNameList(names))
	findlinkedininfo(finalnamelist)


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
	pathtojsons = "/home/anne/"
	companyfile = pathtojsons+"glance-openstack-commits.json" # + "filename"
	print "hello!"
	# names = [("Christina", "Tipps") , ("Chmouel", "Boudjnah"), ("Geetika", "Batra")]
	# name_history = [] 
	# print findlinkedininfo(names)
	# (dates, shas, names) = obtainDatesShasNames(companyfile)
	commitsToCompanies(companyfile)
	with open("index.txt", 'w') as f:
		f.write(str(indexToStart))
	with open("problempeople.txt", 'w') as f:
		f.write(str(problemPeople))


	# # Block of code to get the contents from the linkedin profile
	# driver.get(profile_url)
	# 			time.sleep(2)
	# 			orgs_worklife = driver.find_elements_by_class_name("item-subtitle")
	# 			dateranges = driver.find_elements_by_class_name("date-range")
	# 			for daterange in dateranges:
	# 				one_daterange = daterange.text.encode('ascii', 'ignore').decode('ascii')
	# 				org_index = dateranges.index(daterange)
	# 				one_org = orgs_worklife[org_index].text.encode('ascii', 'ignore').decode('ascii')
	# 				json.dump(one_org, f)
	# 				json.dump(one_daterange, f)
	# 			f.close()
	# 			driver.close()
	# 			time.sleep(2)
	# 			break