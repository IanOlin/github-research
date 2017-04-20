from datetime import date, datetime
import json
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
from misc_info.constants import ML, STACK, return_constants, return_filename

constants_dict = {}

def calculateOverall():
    global constants_dict
    herfindahlIndices = {}

    for repo in constants_dict["repos"]:
        userCommitHist, commitCount = countCommits(repo, date.min, date.max)

        #actual calculation
        index = 0
        for user, commits in userCommitHist.items():
            index += herfRatio(user, commits, commitCount)

        # record HI
        repo_key = "{}-{}".format(repo["name"], repo["user"])
        herfindahlIndices[repo_key] = index

    return herfindahlIndices


def calculateYear():
    global constants_dict
    herfindahlIndices = {}

    for repo in constants_dict["repos"]:
        repo_key = "{}-{}".format(repo["name"], repo["user"])
        herfindahlIndices[repo_key] = {}

        userCommitHist, commitCount = countCommitsByYear(repo)

        # calculation by year
        data_ret_date = get_data_retrieval_date()
        year = data_ret_date.year
        while(year >= constants_dict["earliest-commit"].year):
            index = 0
            # data for this particular year
            commitHist = userCommitHist.get(year, {})
            commitNum = float(commitCount.get(year, 0))

            # adding it all up
            for user, commits in commitHist.items():
                index += herfRatio(user, commits, commitNum)

            # record HI
            herfindahlIndices[repo_key][year] = index
            year-=1

    return herfindahlIndices

def calculateMonth():
    global constants_dict
    herfindahlIndices = {}

    for repo in constants_dict["repos"]:
        repo_key = "{}-{}".format(repo["name"], repo["user"])
        herfindahlIndices[repo_key] = {}

        userCommitHist, commitCount = countCommitsByMonth(repo)

        # calculation by month
        data_ret_date = get_data_retrieval_date()
        currentMonth = getMonthID(data_ret_date)
        while(currentMonth >= getMonthID(constants_dict["earliest-commit"])):
            index = 0
            #data for this particular month
            commitHist = userCommitHist.get(currentMonth, {})
            commitNum = float(commitCount.get(currentMonth, 0))

            # adding it up
            for user, commits in commitHist.items():
                index += herfRatio(user, commits, commitNum)

            # record HI
            herfindahlIndices[repo_key][currentMonth] = index

            #decrement a months
            currentMonth -= 1
            if(currentMonth%100 == 0):
                currentMonth-=100
                currentMonth+=12

    return herfindahlIndices

def herfRatio(user, commits, totalCommitCount):
    global constants_dict

    if user not in constants_dict["jenkins"]:
        return (float(commits)/totalCommitCount)**2 # the ratio
    return 0

def countCommits(repo, startDate=date.min, endDate=date.max):
    raw = openJSON(repo)
    userCommitHist = {}
    commitCount = 0
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        name = commit["commit"]["author"]["name"].encode("utf-8")

        if commitdate < endDate and commitdate >= startDate:
            userCommitHist[name] = userCommitHist.get(name, 0) + 1
            commitCount+=1

    return userCommitHist, commitCount

def countCommitsByYear(repo):
    raw = openJSON(repo)
    userCommitHist = {}
    commitCount = {}
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        name = commit["commit"]["author"]["name"].encode("utf-8")

        # get the year
        year = commitdate.year
        if year not in userCommitHist:
            userCommitHist[year] = {}

        userCommitHist[year][name] = userCommitHist[year].get(name, 0) + 1
        commitCount[year] = commitCount.get(year, 0) + 1

    return userCommitHist, commitCount

def countCommitsByMonth(repo):
    raw = openJSON(repo)
    userCommitHist = {}
    commitCount = {}
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        name = commit["commit"]["author"]["name"].encode("utf-8")

        actualMonth = getMonthID(commitdate)
        if actualMonth not in userCommitHist:
            userCommitHist[actualMonth] = {}

        userCommitHist[actualMonth][name] = userCommitHist[actualMonth].get(name, 0) + 1
        commitCount[actualMonth] = commitCount.get(actualMonth, 0) + 1

    return userCommitHist, commitCount

def getMonthID(dateObj):
    return  dateObj.year*100 + dateObj.month

def parseTimeStamp(unixTime):
    """
    Grabs a unix time stamp (specifically the one that the Github API spits out) and returns a date object of that date
    Same code as found in company_affiliation.py

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

def openJSON(repo):
    global constants_dict
    path = os.path.join(constants_dict["commits-fpath"], return_filename(repo))
    return json.load(open(path, "r"))

def get_data_retrieval_date():
    global constants_dict
    path = os.path.join(constants_dict["commits-fpath"], "date.txt")
    datestr = open(path).read()
    datetimedate = datetime.strptime(datestr, "%b %d, %Y")
    data_ret_date = datetimedate.date()
    return data_ret_date


def herf(flag):
    constants_dict = return_constants(flag)

    import doctest
    doctest.testmod()

    print 'Overall Herfindahl Indices'
    for item in sorted(calculateOverall().items()):
        print "{:<30}\t{}".format(item[0], item[1])

    print '\nPer Year'
    hiSortedByYear = sorted(calculateYear().items())
    index = 0
    sortedYears = sorted(hiSortedByYear[0][1].keys())
    print "{:<12}".format("Year"),
    for item in hiSortedByYear:
        print "{:<30}".format(item[0]),
    while(index < len(sortedYears)):
        currYear = sortedYears[index]
        print "\n{:<12}".format(currYear),
        for item in hiSortedByYear:
            print "{:<30}".format(item[1][currYear]),
        index+=1
    print ''

    print '\nPer Month'
    hiSortedByMonth = sorted(calculateMonth().items())
    index = 0
    sortedMonths = sorted(hiSortedByMonth[0][1].keys())
    print "{:<12}".format("Month"),
    for item in hiSortedByMonth:
        print "{:<30}".format(item[0]),
    while(index < len(sortedMonths)):
        currMonth = sortedMonths[index]
        print "\n{} {:<7}".format(currMonth/100, currMonth%100),
        for item in hiSortedByMonth:
            print "{:<30}".format(item[1][currMonth]),
        index+=1
