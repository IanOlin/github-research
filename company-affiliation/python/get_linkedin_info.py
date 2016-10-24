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

import os
import json

PATH = "../resources/linkedin_info/"
DEBUG = True

def findlinkedininfo(name_list): #name is a tuple, predefinedlinkedin is a boolean
	"""
	Takes in a list of names as a tuple, and a boolean
	"""
	allcompanies = []
	for name in name_list:
		driver = webdriver.Firefox(capabilities=firefox_capabilities)
		if DEBUG:
			print driver
		#What to put in the open() URL area for Geetika Batra: https://www.google.com/#q=Geetika+Batra+linkedin
		driver.get('https://www.google.com/#q={}+{}+linkedin'.format(name[0], name[1]))
		time.sleep(2)
		google_results = driver.find_elements_by_class_name("r") # should get the headlines/main title of each google result
		orgsAndCompanies = []
		for res in google_results:
			if (str(res.text.encode('ascii', 'ignore').decode('ascii'))) == "{} {} | LinkedIn".format(name[0], name[1]):
				#getting the index that fits the if statement's qualifications
				index = google_results.index(res)
				if DEBUG:
					print index;

				profile_url = driver.find_elements_by_class_name('_Rm')[index].text.encode('ascii', 'ignore').decode('ascii')
				
				# opening the Linkedin URL
				driver.get(profile_url)
				time.sleep(2)
				orgs_worklife = driver.find_elements_by_class_name("item-subtitle")
				dateranges = driver.find_elements_by_class_name("date-range")


				for daterange in dateranges:
					one_daterange = daterange.text.encode('ascii', 'ignore').decode('ascii')
					org_index = dateranges.index(daterange)
					one_org = orgs_worklife[org_index].text.encode('ascii', 'ignore').decode('ascii')
					orgsAndCompanies.append((one_org, one_daterange))

				driver.close()
				time.sleep(2)
				break
		f = open(PATH+'{}_{}_linkedin.json'.format(name[0], name[1]), 'w')
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

def commitsToCompanies(filename):
	#TODO: actually make this method

	commits = json.load(open(filename, 'r'))
	shas = []
	names = []
	dates = []
	companies = []
	for c in commits: 
		#TODO:
		#store dates in dates
		dates.append(c["commit"]["author"]["date"])
		#store sha in shas
		#store name in names
		pass
	#TODO:
	#call findlinkedininfo on list of names, save in companies
	#change all Nones to "no company" with a flag of 0, change all other companies to a flag of like 3.
	#for others, find the company that matches the date in date
	#zip shas and companies to a dict or something
	#save to file

"""
returns the element or json object from the tuple of keys
"""
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
	companyfile = [pathtojsons+"glance-openstack-commits.json"] # + "filename"
	print "hello!"
	# names = [("Christina", "Tipps") , ("Chmouel", "Boudjnah"), ("Geetika", "Batra")]
	# name_history = [] 
	# print findlinkedininfo(names)
	commitsToCompanies(companyfile[0])



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