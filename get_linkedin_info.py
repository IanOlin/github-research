from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

# Go here to install dependencies for chrome webdriver: https://christopher.su/2015/selenium-chromedriver-ubuntu/
from datetime import datetime, time
from pattern.web import * 
from pattern.web import URL, extension, download
import pickle
from selenium import webdriver
from pyvirtualdisplay import Display

#Changing the directory so that the headline files are stored in a convenient place
import os

path = "linkedin_info/"

# Check current working directory.
retval = os.getcwd()
print "Current working directory %s" % retval

# Now change the directory
os.chdir( path )

# Check current working directory.
retval = os.getcwd()

print "Directory changed successfully %s" % retval

print "hello!"
names = [("Geetika", "Batra") , ("Chmouel", "Boudjnah")]

name_history = [] 

def findlinkedininfo(name_list): #name is a tuple, predefinedlinkedin is a boolean
	for name in name_list:
		driver = webdriver.Firefox(capabilities=firefox_capabilities)
		print driver
		#What to put in the open() URL area for Geetika Batra: https://www.google.com/#q=Geetika+Batra+linkedin
		driver.get('https://www.google.com/#q={}+{}+linkedin'.format(name[0], name[1]))
		time.sleep(2)
		google_results = driver.find_elements_by_class_name("r") # should get the headlines/main title of each google result
		for res in google_results:
			if (str(res.text.encode('ascii', 'ignore').decode('ascii'))) == "{} {} | LinkedIn".format(name[0], name[1]):
				#getting the index that fits the if statement's qualifications
				index = google_results.index(res)
				print index;
				f = open('{}_{}_linkedin.pickle'.format(name[0], name[1]), 'w')
				# getting the url of the result:
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
					pickle.dump(one_org, f)
					pickle.dump(one_daterange, f)
				f.close()
				driver.close()
				time.sleep(2)
				break

		driver.quit()

findlinkedininfo(names)

	# # Block of code to get the contents from the linkedin profile
	# driver.get(profile_url)
	# 			time.sleep(2)
	# 			orgs_worklife = driver.find_elements_by_class_name("item-subtitle")
	# 			dateranges = driver.find_elements_by_class_name("date-range")
	# 			for daterange in dateranges:
	# 				one_daterange = daterange.text.encode('ascii', 'ignore').decode('ascii')
	# 				org_index = dateranges.index(daterange)
	# 				one_org = orgs_worklife[org_index].text.encode('ascii', 'ignore').decode('ascii')
	# 				pickle.dump(one_org, f)
	# 				pickle.dump(one_daterange, f)
	# 			f.close()
	# 			driver.close()
	# 			time.sleep(2)
	# 			break