"""
Takes all commits, maps shas to name, date, flag, and company (according to linkedin)
"""
from datetime import date
import re
import json

# linkedin flags
NO_COMPANY = 0
PARSING_ERROR = 1
MULTI_COMPANY = 2 
SINGLE_COMPANY = 3

# company flags
MANUAL_CERTAIN = 6
LIKELY_EMAIL = 4
LIKELY_LINKEDIN = 3
UNLIKELY = 1
NO_DATA = 0

# date constants
CURRENT_DATE = date(2016, 11, 1)
CURRENT_DATE_STR = "Present"
MONTHS = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}

# file pathing
pathToJSON = "/home/anne/MLCommits/"
pathToLinkedIn = "../resources/linkedin_info/"
pathToOutput = "../resources/linkedin-csvs/"

rawFileNames = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json")#("glance-openstack-commits.json", "cinder-openstack-commits.json", "cloudstack-apache-commits.json", "glance-openstack-commits.json",
    #"horizon-openstack-commits.json", "keystone-openstack-commits.json", "neutron-openstack-commits.json", "nova-openstack-commits.json",
    #"swift-openstack-commits.json") #jsons here


pathToEmailList = "../../Ian's Trash/Research/companies2.json"
domainToCompany = json.load(open(pathToEmailList))

# rawFileNames = ("glance-openstack-commits.json",)
 # "cinder-openstack-commits.json", "cloudstack-apache-commits.json", "glance-openstack-commits.json",
 #    "horizon-openstack-commits.json", "keystone-openstack-commits.json", "neutron-openstack-commits.json", "nova-openstack-commits.json",
 #    "swift-openstack-commits.json") #jsons here


#memoization to cut down on the number of date objects we have to make
memoizedPeople = {}

# OUTLINE
# read in commit json
# for each commit
    # get name
    # get company list
    # grab all companies for that person
    # find relevant companies
    # put in commitInfo dict

def mapCommits():
    """
    Reads in a bunch of raw commits from the GitHub API, and uses the name provided to search through the given linkedin data (see get_linkedin_info.py)
    Finds all companies & organizations the committer was a part of at the time of commit, according to their linkedin (or the linkedin of someone of the same name)
    Writes to a JSON
    """
    # counters
    numSingle = 0
    numMulti = 0
    numNone = 0
    numError = 0

    for filename in rawFileNames:
        raw = openJSON(pathToJSON + filename)
        commitInfo = {}
        for commit in raw:
            # simple fields
            unixDate = commit["commit"]["author"]["date"].encode("utf-8")
            commitdate = parseTimeStamp(unixDate)
            url = commit["commit"]["url"]
            sha = url.split("/")[-1].encode("utf-8")
            email = commit["commit"]["author"]["email"].encode("utf-8")
            name = commit["commit"]["author"]["name"].encode("utf-8")

            # grab company according to linkedin
            linkedinFlag, linkedinCompanyList = linkedinCompanies(name, commitdate)
            if linkedinFlag == SINGLE_COMPANY:
                numSingle+=1
            elif linkedinFlag == MULTI_COMPANY:
                numMulti+=1
            elif linkedinFlag == PARSING_ERROR:
                numError+=1
            elif linkedinFlag == NO_COMPANY:
                numNone+=1

            # grab company according to email
            emailFlag, emailCompany = emailCompanies(email)

            # find best match company, with flag for likelihood
            overallFlag = -1
            overallCompany = ""
            if emailFlag == 1:
                overallFlag = LIKELY_EMAIL
                overallCompany = emailCompany
            elif linkedinFlag == SINGLE_COMPANY:
                overallFlag = LIKELY_LINKEDIN
                overallCompany = linkedinCompanyList[0]
            elif linkedinFlag == MULTI_COMPANY:
                overallFlag = UNLIKELY
                overallCompany = linkedinCompanyList[0]
            else:
                overallFlag = NO_DATA

            # write to dictionary
            commitInfo[sha] = (name, email, unixDate, {"LINKEDIN":(linkedinFlag, linkedinCompanyList), "EMAIL":(emailFlag, emailCompany), "OVERALL":(overallFlag, overallCompany)})

        # write to file
        writeJSON(pathToOutput+"linkedin-"+filename, commitInfo)
    print "Single: {} Multi: {} None: {} Error: {}".format(numSingle, numMulti, numNone, numError)


def linkedinCompanies(name, dateobject):
     # company list
    companyList = []
    if name in memoizedPeople:
        companyList = memoizedPeople[name]
    else:
        try:
            companies = openJSON(pathToLinkedIn + "{}_linkedin.json".format(name))
            companyList = [(co[0], convertToDates(co[1])) for co in companies]
            memoizedPeople[name] = companyList
        except IOError:
            pass

    # pick out the ones that match the date
    badDataSomewhere = False
    timeFrameCompanies = []
    for co in companyList:
        if co[1] == None:
            badDataSomewhere = True
        else:
            dateStart = co[1][0]
            dateEnd = co[1][1]

            if dateobject < dateEnd and dateobject > dateStart:
                timeFrameCompanies.append(co[0])

    # flag
    flag = -1

    if badDataSomewhere:
        flag = PARSING_ERROR
    elif len(timeFrameCompanies) == 1:
        flag = SINGLE_COMPANY
    elif len(timeFrameCompanies) > 1:
        flag = MULTI_COMPANY
    elif len(timeFrameCompanies) == 0:
        flag = NO_COMPANY
    else:
        raise AttributeError("nonexistent list length? " + str(len(timeFrameCompanies)))

    return flag, timeFrameCompanies

def emailCompanies(email):
    try:
        domain = email.split("@")[-1] #get domain--last half of email
    except IndexError:
        return 0, ""
    flag = 0
    company = ""
    try:
        company = domainToCompany[domain]
        if company != "personal\n":
            flag = 1
    except KeyError:
        pass
    return flag, company


def parseTimeStamp(unixTime):
    """
    Grabs a unix time stamp (specifically the one that the Github API spits out) and returns a date object of that date

    >>> parseTimeStamp("2010-08-06T03:06:42Z")
    datetime.date(2010, 8, 6)

    >>> parseTimeStamp("2011-01-23T16:16:27Z")
    datetime.date(2011, 1, 23)

    >>> parseTimeStamp("2011-02-02T18:41:28Z")
    datetime.date(2011, 2, 2)
    """
    datePart = unixTime.split("T")[0]
    parts = datePart.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    return date(year, month, day)

def convertToDates(datesStr):
    """
    Takes a date in the format 'earlierMonth earlierYear laterMonth laterYear' and returns a tuple of date objects
    if the later date is "Present", use the value stored in CURRENT_DATE

    >>> convertToDates("October 2016  Present (1 month)")
    (datetime.date(2016, 10, 1), datetime.date(2016, 11, 1))

    >>> convertToDates("2007  2009")
    (datetime.date(2007, 1, 1), datetime.date(2009, 1, 1))

    >>> convertToDates("July 2001  July 2004 (3 years 1 month)")
    (datetime.date(2001, 7, 1), datetime.date(2004, 7, 1))

    >>> convertToDates("September 2011  March 2012 (7 months)")
    (datetime.date(2011, 9, 1), datetime.date(2012, 3, 1))

    >>> convertToDates("May 2008  August 2008 (4 months)")
    (datetime.date(2008, 5, 1), datetime.date(2008, 8, 1))

    >>> convertToDates("November 2008")
    (datetime.date(2008, 11, 1), datetime.date(2016, 11, 1))

    >>> convertToDates("dezembro de 2012  janeiro de 2013 (2 meses)")
    ['dezembro', 'de', '2012', 'janeiro', 'de', '2013']

    >>> convertToDates("Starting November 2013")
    (datetime.date(2016, 11, 1), datetime.date(2016, 11, 1))
    """
    splitDateAndLength = datesStr.split("(") # string has a (n months) portion to it
    words = splitDateAndLength[0].split()
    if(len(words) == 0):
        return None
    date1 = None
    date2 = None
    try:
        #starting
        if len(words) > 0 and (words[0]=="Starting" or words[0]=="Issued"):
            date1 = date2 = CURRENT_DATE
        else:
            #date2
            if words[-1] == CURRENT_DATE_STR or (len(words) == 2 and isAlpha(words[0])) or len(words) == 1:
                date2 = CURRENT_DATE
            else:
                year = int(words[-1])
                month = words[-2]
                if isAlpha(month):
                    date2 = date(year, MONTHS[month], 1)
                else:
                    date2 = date(year, 1, 1)
            #date1
            if words[0] == CURRENT_DATE_STR:
                date1 = CURRENT_DATE
            else:
                if isAlpha(words[0]) and len(words)>1 and isNum(words[1]): # is a month, year
                    date1 = date(int(words[1]), MONTHS[words[0]], 1)
                else:
                    date1 = date(int(words[0]),1,1)
    except (KeyError, ValueError):
        print words
        return None
    return (date1, date2)

def isAlpha(possibleStr):
    return re.match("[A-Za-z]+$", possibleStr)
def isNum(possibleStr):
    return re.match("[0-9]+$", possibleStr)

def openJSON(fname):
    return json.load(open(fname, "r"))
def writeJSON(fname, thing):
    f = open(fname, "w")
    json.dump(thing, f)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    mapCommits()
