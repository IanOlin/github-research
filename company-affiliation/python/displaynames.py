# -*- coding: utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# This Python file uses the following encoding: utf-8
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
# from unidecode import unidecode 
from collections import defaultdict

PATH = "../resources/linkedin_info/"
DEBUG = True

indexToStart = 0
# START_AT_INDEX = False
signup = 0
stubbornpeople = []


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
	# print names
	return (dates, shas, names)

"""
Gets one of each name and stores the results into a list
"""
def getNameFrequencies(comprehensiveNameList):
	nameFrequencies = defaultdict(int)
	for name in comprehensiveNameList:
	    nameFrequencies[name] += 1
	return nameFrequencies

	# newNameSet = Set()
	# for name in comprehensiveNameList:
	# 	newNameSet.add(name)
	# return newNameSet

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

	#TODO:
	#call findlinkedininfo on list of names, save in companies
	#change all Nones to "no company" with a flag of 0, change all other companies to a flag of like 3.
	#for others, find the company that matches the date in date
	#zip shas and companies to a dict or something
	#save to file


def getFinalNameDict(filename):
	"""
	returns the final list of names to run
	"""
	# get the file name of the filename path variable here:

	(dates, shas, names) = obtainDatesShasNames(filename)
	#Getting one of each name
	finalNameFrequencies = getNameFrequencies(names)	
	return finalNameFrequencies
	
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
			print one_org
			orgsAndCompanies.append((one_org, one_daterange))
		except IndexError as e:
			break
	driver.quit()
	time.sleep(2)
	f = open(PATH+'{}_linkedin.json'.format(name.encode("utf-8")), 'w')
	json.dump(orgsAndCompanies, f)
	f.close()
	return name + str(orgsAndCompanies)


# getLinkedInInfo("kaisheny", "https://www.linkedin.com/in/kaishengyao")


resultingdict = {"kaisheny": "https://www.linkedin.com/in/kaishengyao", "UnderdogGeek": "https://uk.linkedin.com/in/bhaskarmitra" , "Eldar Akchurin": "https://de.linkedin.com/in/eldar-akchurin-b5a5a833", "Philipp Kranen": "https://de.linkedin.com/in/philipp-kranen-08525747", "Cha Zhang": "https://www.linkedin.com/in/cha-zhang-24bb86" , "Yongqiang Wang": "https://www.linkedin.com/in/yongqiang-wang-a57ba622", "frankseide": "https://cn.linkedin.com/in/frank-seide-36ab258", "pkranen": "https://de.linkedin.com/in/philipp-kranen-08525747/en", 'Wayne Xiong': "https://www.linkedin.com/in/waxiong", 'Chris Basoglu': "https://www.linkedin.com/in/chris-basoglu-779b761", "Frank Seide": "https://cn.linkedin.com/in/frank-seide-36ab258", "Nikos Karampatziakis": "https://www.linkedin.com/in/nikos-karampatziakis-a11236123", "Gaizka Navarro": "https://www.linkedin.com/in/gaizka-navarro-97347090", "Yu Zhang": "https://www.linkedin.com/in/yu-zhang-8544aaa", "Marko Radmilac": "https://www.linkedin.com/in/marko-radmilac-17a27329", "Vladimir Ivanov": "https://www.linkedin.com/in/444442", "Amit Agarwal": "https://www.linkedin.com/in/amit-agarwal-09ba984",  "Vadim Mazalov": "https://www.linkedin.com/in/mazalov",  "Alexey Orlov": "https://www.linkedin.com/in/alorlov", "xiaohuliu": "https://www.linkedin.com/in/xiaohuliu", "Yinggong ZHAO": "https://cn.linkedin.com/in/zhao-yinggong-a8350918", "Alexey Kamenev": "https://www.linkedin.com/in/alexeykamenev", "Malcolm Slaney": "https://www.linkedin.com/in/malcolm-slaney-31650821", "anthonyaue": "https://www.linkedin.com/in/anthony-aue-71648b", "chenguoguo": "https://www.linkedin.com/in/guoguo-chen-788a7124", "yzhang87": "https://www.linkedin.com/in/yuzhangcmu" , "Jasha Droppo": "https://www.linkedin.com/in/jasha-droppo-a52a353", "Scott Cyphers": "https://www.linkedin.com/in/scott-cyphers-a53467", "Qiwei Ye": "https://www.linkedin.com/in/qiwei-ye-66867222", "Clemens Marschner": "https://de.linkedin.com/in/clemens-marschner-116847", "William Darling": "https://de.linkedin.com/in/williamdarling", "Thilo Will": "https://de.linkedin.com/in/thilo-will-04592a4a", "jeanfad": "https://de.linkedin.com/in/jbfaddoul", "Willi Richert": "https://de.linkedin.com/in/willirichert/en", "Zhou Wang": "https://de.linkedin.com/in/zhou-wang-9bb24952", "Mark Hillebrand": "https://de.linkedin.com/in/mark-hillebrand-075ba71a", "Mike Seltzer": "https://www.linkedin.com/in/michael-seltzer-a3815382", "agibsonccc": "https://www.linkedin.com/in/agibsonccc", "Adam Gibson": "https://www.linkedin.com/in/agibsonccc", "nyghtowl": "https://www.linkedin.com/in/melaniewarrick", "eraly": "https://www.linkedin.com/in/susan-eraly-8a2b2839", "Melanie Warrick": "https://www.linkedin.com/in/melaniewarrick", "Kevin James Matzen": "https://www.linkedin.com/in/kevin-matzen-b3714414" , "sguada": "https://www.linkedin.com/in/sergio-guadarrama-1724379", "Jason Yosinski": "https://www.linkedin.com/in/jasonyosinski", "Kai Li": "https://www.linkedin.com/in/kai-li-1b272952", "Jeff Donahue": "https://www.linkedin.com/in/jeff-donahue-94a5507", "Cyprien Noel": "https://www.linkedin.com/in/cypriennoel", "qipeng": "https://www.linkedin.com/in/peng-qi-39580090", "Maciek Chociej": "https://www.linkedin.com/in/maciejchociej", "Alexey Surkov": "https://www.linkedin.com/in/aleksey-surkov-b4881585/en", "Justine Tunney": "https://www.linkedin.com/in/jtunney", "Charles Nicholson": "https://www.linkedin.com/in/charles-nicholson-403a7b", "caisq": "https://www.linkedin.com/in/shanqingcai", "Illia Polosukhin": "https://www.linkedin.com/in/illia-polosukhin-77b6538", "Manjunath Kudlur": "https://www.linkedin.com/in/keveman", "Cassandra Xia": "https://www.linkedin.com/in/cassandraxia", "Jan Prach": "https://www.linkedin.com/in/janprach", "Yoshua Bengio": "https://ca.linkedin.com/in/yoshuabengio", "Vincent Dumoulin": "https://ca.linkedin.com/in/vdumoulin", "Rami Al-Rfou": "https://www.linkedin.com/in/ramieid", "Christof Angermueller": "https://uk.linkedin.com/in/cangermueller", "Dustin Webb": "https://www.linkedin.com/in/daemonmaker", "gdesjardins": "https://uk.linkedin.com/in/guillaume-desjardins-4a318289", "Vincent Michalski": "https://ca.linkedin.com/in/vincent-michalski-87930a12b/de", "Sigurd Spieckermann": "https://de.linkedin.com/in/sspieckermann/en", "Guillaume Desjardins": "https://uk.linkedin.com/in/guillaume-desjardins-4a318289", "Chinnadhurai Sankar": "https://ca.linkedin.com/in/chinnadhuraisankar", "goodfeli": "https://www.linkedin.com/in/ian-goodfellow-b7187213", "Nouiz": "https://ca.linkedin.com/in/fbastien", "Robert McGibbon": "https://www.linkedin.com/in/robert-t-mcgibbon-64285398", "Samira Shabanian": "https://ca.linkedin.com/in/samirashabanian", "Georg Ostrovski": "https://uk.linkedin.com/in/georg-ostrovski-5690a538", "Clement Farabet": "https://www.linkedin.com/in/clementfarabet", "nicholas-leonard": "https://ca.linkedin.com/in/nicholas-léonard-a838225a", "Nicholas Leonard": "https://ca.linkedin.com/in/nicholas-léonard-a838225a", "koray kavukcuoglu": "https://uk.linkedin.com/in/koray-kavukcuoglu-0439a720", "Hugh Perkins": "https://uk.linkedin.com/in/hughperkins", "Sam Gross": "https://www.linkedin.com/in/samgross", "Ronan Collobert": "https://www.linkedin.com/in/ronan-collobert-b110aa8"}

needslinkedIn_list = [] 
for name in resultingdict:
	with open(PATH+'{}_linkedin.json'.format(name)) as data_file:
		data = json.load(data_file)
		if len(data) == 0:
			needslinkedIn_list.append(name)
print needslinkedIn_list


for key in needslinkedIn_list:
	print key
	getLinkedInInfo(key, resultingdict[key])

# if __name__ == '__main__':
# 	pathtojsons = "/home/jwb/research/"
# 	companyfile = pathtojsons+"torch7-torch-commits.json" # + "filename"
# 	# print "hello!"
# 	unsortedDict = getFinalNameDict(companyfile)
# 	resultingnames = []
# 	for name in unsortedDict:
# 		if unsortedDict[name] >= 10:
# 			resultingnames.append(name)

