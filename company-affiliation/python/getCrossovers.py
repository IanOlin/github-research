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
import json

from get_linkedin_info import changeDirectory, obtainDatesShasNames, simplifyNameList, filterLists, commitsToCompanies, JSON_access, findlinkedininfo

PATH = "../resources/linkedin_info/"
DEBUG = True

indexToStart = 0
# START_AT_INDEX = False

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
	return (dates, shas, finalnamelist)


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
	print "hello!"

	#Getting the crossovers:
	#remember! The 3rd index of the (reponame)_results are the names

	# Machine Learning Repo results:
	deeplearning4j_deeplearning4j = pathtojsons+"deeplearning4j-deeplearning4j-commits.json" # + "filename"
	(deeplearning4j_dates, deeplearning4j_shas, deeplearning4j_names) = commitsToCompanies(deeplearning4j_deeplearning4j)

	caffe_BVLC = pathtojsons+"caffe-BVLC-commits.json" # + "filename"
	(caffe_dates, caffe_shas, caffe_names) = commitsToCompanies(caffe_BVLC)

	tensorflow_tensorflow = pathtojsons+"tensorflow-tensorflow-commits.json" # + "filename"
	(tensorflow_dates, tensorflow_shas, tensorflow_names) = commitsToCompanies(tensorflow_tensorflow)

	Theano_Theano = pathtojsons+"Theano-Theano-commits.json" # + "filename"
	(Theano_dates, Theano_shas, Theano_names) = commitsToCompanies(Theano_Theano)

	torch7_torch = pathtojsons+"torch7-torch-commits.json" # + "filename"
	(torch7_dates, torch7_shas, torch7_names) = commitsToCompanies(torch7_torch)

	#Openstack results:
	glance_openstack = pathtojsons+"glance-openstack-commits.json" # + "filename"
	(glance_openstack_dates, glance_openstack_shas, glance_openstack_names) = commitsToCompanies(glance_openstack)

	cinder_openstack = pathtojsons+"cinder-openstack-commits.json" # + "filename"
	(cinder_openstack_dates, cinder_openstack_shas, cinder_openstack_names) = commitsToCompanies(cinder_openstack)

	horizon_openstack = pathtojsons+"horizon-openstack-commits.json" # + "filename"
	(horizon_openstack_dates, horizon_openstack_shas, horizon_openstack_names) = commitsToCompanies(horizon_openstack)

	keystone_openstack = pathtojsons+"keystone-openstack-commits.json" # + "filename"
	(keystone_openstack_dates, keystone_openstack_shas, keystone_openstack_names) = commitsToCompanies(keystone_openstack)

	neutron_openstack = pathtojsons+"neutron-openstack-commits.json" # + "filename"
	(neutron_openstack_dates, neutron_openstack_shas, neutron_openstack_names) = commitsToCompanies(neutron_openstack)

	nova_openstack = pathtojsons+"nova-openstack-commits.json" # + "filename"
	(nova_openstack_dates, nova_openstack_shas, nova_openstack_names) = commitsToCompanies(nova_openstack)

	swift_openstack = pathtojsons+"swift-openstack-commits.json" # + "filename"
	(swift_openstack_dates, swift_openstack_shas, swift_openstack_names) = commitsToCompanies(swift_openstack)

	#cloudstack results:
	cloudstack_apache = pathtojsons+"cloudstack-apache-commits.json" # + "filename"
	(cloudstack_apache_dates, cloudstack_apache_shas, cloudstack_apache_names) = commitsToCompanies(cloudstack_apache)

	all_contributor_names = deeplearning4j_names + caffe_names + tensorflow_names + Theano_names + torch7_names + glance_openstack_names + cinder_openstack_names + horizon_openstack_names + keystone_openstack_names + neutron_openstack_names + nova_openstack_names + swift_openstack_names + cloudstack_apache_names
	
	name_frequencies = {}
	# list_of_zeroes = [0] * (len(all_contributor_names))
	# for name in all_contributor_names:
	# 	name_frequencies[name] = 0 #for now

	for i in range(len(all_contributor_names) - 1):
		name = all_contributor_names[i]
		if name in name_frequencies:
			name_frequencies[name] += 1
		else:
			name_frequencies[name] = 1

	# print name_frequencies

	crossovers = []

	for name in name_frequencies:
		frequency = name_frequencies[name]
		if frequency > 1:
			crossovers.append(name)

	findlinkedininfo(crossovers, True)