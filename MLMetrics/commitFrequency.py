from HerfindahlCalculator import * # Thanks, Serena! 
import json
import csv
import datetime
from quicksort import *
pathToJSON = "/home/anne/ResearchJSONs/"
mlfileList = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json", "incubator-systemml-apache-commits.json")
stackfileList = ("cloudstack-apache-commits.json", "cinder-openstack-commits.json", "glance-openstack-commits", "horizon-openstack-commits.json", "keystone-openstack-commits.json", "neutron-openstack-commits.json", "nova-openstack-commits.json", "swift-openstack-commits.json")
pathToUserJSONs = "/home/anne/github-research/MLMetrics/UserCommitHistories"

def getRepoCommitters(reponame):
	"""
	Given a repo name, return the list of users (their names on Github)
	"""
	userlist = []
	dates = []
	usercommithistoryPmonth, commitcountPmonth = countCommitsByMonth(getThisRepoFile(reponame))
	for date in usercommithistoryPmonth:
		dates.append(date)
		for user in usercommithistoryPmonth[date]:
			if user not in userlist:
				userlist.append(user)
	return userlist

def getRepoMonths(reponame):
	"""
	Given a repo name, return the months the repo was active
	"""
	userlist = []
	dates = []
	usercommithistoryPmonth, commitcountPmonth = countCommitsByMonth(getThisRepoFile(reponame))
	for date in usercommithistoryPmonth:
		dates.append(date)
	return dates

def getRepoYears(reponame):
	"""
	Given a repo name, return the months the repo was active
	"""
	userlist = []
	dates = []
	usercommithistoryPyear, commitcountPyear = countCommitsByYear(getThisRepoFile(reponame))
	for date in usercommithistoryPyear:
		dates.append(date)
	return dates

def getThisRepoFile(reponame):
	""" 
	Since typing file names is tiring, Annie made this inefficient method so we don't have to type a repo's entire file name.
	"""
	filename = ""
	if (reponame == "systemml"):
		filename = "incubator-systemml-apache-commits.json"
	elif (reponame == "caffe"):
		filename = "caffe-BVLC-commits.json"
	elif (reponame == "CNTK"):
		filename = "CNTK-Microsoft-commits.json"
	elif (reponame == "deeplearning4j"):
		filename = "deeplearning4j-deeplearning4j-commits.json"
	elif (reponame == "tensorflow"):
		filename = "tensorflow-tensorflow-commits.json"
	elif (reponame == "theano"):
		filename = "Theano-Theano-commits.json"
	elif (reponame == "torch7"):
		filename = "torch7-torch-commits.json"
    #Openstack & Cloudstack Committer Lists:
	elif (reponame == "cloudstack"):
		filename = "cloudstack-apache-commits.json"
	elif (reponame == "cinder.json"):
		filename = "cinder-openstack-commits.json"
	elif (reponame == "glance.json"):
		filename = "glance-openstack-commits.json"
	elif (reponame == "horizon.json"):
		filename = "horizon-openstack-commits.json"
	elif (reponame == "keystone.json"):
		filename = "keystone-openstack-commits.json"
	elif (reponame == "neutron.json"):
		filename = "neutron-openstack-commits.json"
	elif (reponame == "nova.json"):
		filename = "nova-openstack-commits.json"
	elif (reponame == "swift.json"):
		filename = "swift-openstack-commits.json"
	return filename

def getDatesPerCommitter(date1, date2):
	"""
	Method that, given a committer and a repo, returns the months that this particular user committed to this repo
	"""
	file = getThisRepoFile(reponame)
	returndates = []
	usercommithistoryPmonth, commitcountPmonth = countCommitsByMonth(file)
	for date in usercommithistoryPmonth:
		if user in usercommithistoryPmonth[date]:
			returndates.append(date)
	return returndates

def formatDatesandCommits(user, reponame, timediv):
	"""
	given a user, a repo name, and a string that either says "month" or "year", 
	return a list of tuples as (month or year, # of commits)
	"""
	date_numcommits_list = []
	if timediv == "month":
		usercommithistoryPmonth, commitcountPmonth = countCommitsByMonth(getThisRepoFile(reponame))
		for month in usercommithistoryPmonth:
			if user in usercommithistoryPmonth[month]:
				numCommits = usercommithistoryPmonth[month][user]
				date_numcommits_list.append((month, numCommits))
	elif timediv == "year":
		usercommithistoryPyear, commitcountPyear = countCommitsByYear(getThisRepoFile(reponame))
		for year in usercommithistoryPyear:
			if user in usercommithistoryPyear[year]:
				numCommits = usercommithistoryPyear[year][user] #
				date_numcommits_list.append((year, numCommits))
	return date_numcommits_list

def avgcommitpermonth(reponame):
	avg = 0
	commitcountPmonth = countCommitsByMonth(getThisRepoFile(reponame))[1]
	for date in commitcountPmonth:
		avg += commitcountPmonth[date]
	avg = avg/len(commitcountPmonth)
	return avg

def avgcommitperyear(reponame):
	avg = 0
	commitcountPyear = countCommitsByYear(getThisRepoFile(reponame))[1]
	for date in commitcountPyear:
		avg += commitcountPyear[date]
	avg = avg/len(commitcountPyear)
	return avg

def totalNumCommitsofUser(user, reponame):
	date_numcommits = formatDatesandCommits(user, reponame, "year")
	numcommits = 0
	for item in date_numcommits:
		numcommits = item[1]
	return (user, numcommits)

def findTop10Contributors(reponame):
	""" 
	Runs through all the users in the repo & returns the ones with the most contributions
	"""
	unsortedlist = []
	committers = getRepoCommitters(reponame)
	for committer in committers:
		unsortedlist.append(totalNumCommitsofUser(committer, reponame))
	sortedlist = quicksort(unsortedlist, 0, len(unsortedlist) - 1)
	return sortedlist[-25:]

# def deltaDates(month1, month2):
# 	date1 = datetime.datetime.strptime(month1, '%Y%m')
# 	date2 = datetime.datetime.strptime(month2, '%Y%m')
# 	difference_days = date2 - date1
# 	return abs(difference_days.days/28)

if __name__ == "__main__":
	import doctest
	doctest.testmod()
	print "Average commits/month"
	print "CNTK-Microsoft: ", avgcommitpermonth('CNTK')
	print "Theano-Theano: ", avgcommitpermonth('theano')
	print "caffe-BLVC: ", avgcommitpermonth('caffe')
	print "deeplearning4j-deeplearning4j: ", avgcommitpermonth('deeplearning4j')
	print "incubator-systemml: ", avgcommitpermonth('systemml')
	print "tensorflow-tensorflow: ", avgcommitpermonth('tensorflow')
	print "torch7-torch7: ", avgcommitpermonth('torch7')
	print ""
	print "Average commits/year"
	print "CNTK-Microsoft: ", avgcommitperyear('CNTK')
	print "Theano-Theano: ", avgcommitperyear('theano')
	print "caffe-BLVC: ", avgcommitperyear('caffe')
	print "deeplearning4j-deeplearning4j: ", avgcommitperyear('deeplearning4j')
	print "incubator-systemml: ", avgcommitperyear('systemml')
	print "tensorflow-tensorflow: ", avgcommitperyear('tensorflow')
	print "torch7-torch7: ", avgcommitperyear('torch7')
	print ""
	print "Top 25 contributors for each repo"
	print "CNTK-Microsoft: ", findTop10Contributors('CNTK')
	print "Theano-Theano: ", findTop10Contributors('theano')
	print "caffe-BLVC: ", findTop10Contributors('caffe')
	print "deeplearning4j-deeplearning4j: ", findTop10Contributors('deeplearning4j')
	print "incubator-systemml: ", findTop10Contributors('systemml')
	print "tensorflow-tensorflow: ", findTop10Contributors('tensorflow')
	print "torch7-torch7: ", findTop10Contributors('torch7')
	print ""