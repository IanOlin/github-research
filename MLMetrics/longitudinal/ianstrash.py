from datetime import date
from collections import defaultdict
import json
CURRENT_DATE = date(2016, 11, 1)
EARLIEST_DATE = date(2008, 1, 1) #Theano's first commit
pathToJSON = "/home/jwb/Documents/json/"
fileList = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json")
def calculateOverall():
    # herfindahlIndices = {}
    # for file in fileList:
    #     userCommitHist, commitCount = countCommits(file, date.min, date.max)
    #     index = 0
    #     commitCount = float(commitCount)
    #     for user, commits in userCommitHist.items():
    #         index += (commits/commitCount)**2
    #     repo = getRepoID(file)
    #     herfindahlIndices[repo] = index
    # return herfindahlIndices
    # avgDelay = {}
    # for file in fileList:
    #     userCommitHist, commitCount, userCommitDates = countCommits(file, date.min, date.max)
    #     index = 0
    #     avgSum = 0
    #     commitCount = float(commitCount)
    #     for user, dates in userCommitDates.items():
    #         if (max(dates) != min(dates)):
    #             # print user
    #             index = index + 1
    #             dateRange = max(dates)-min(dates)
    #             numberCommit = len(dates)
    #             avgSum = avgSum + numberCommit/dateRange.total_seconds()
    #     # print userCommitDates
    #     repo = getRepoID(file)
    #     avgDelay[repo] = avgSum/index
    # return avgDelay
    regularityMetric = {}
    for file in fileList:
        userCommitHist, commitCount, userCommitDates = countCommits(file, date.min, date.max)
        index = 0
        avgTerm = 0
        commitCount = float(commitCount)
        for user, dates in userCommitDates.items():
            if (max(dates) != min(dates)):
                index = index + 1
                dateRange = max(dates)-min(dates)
                avgTerm = dateRange.total_seconds() + avgTerm
                # numberCommit = len(dates)
                # avgSum = avgSum + numberCommit/dateRange.total_seconds()
        # print userCommitDates
        repo = getRepoID(file)
        regularityMetric[repo] = (avgTerm/index)/604800
    return regularityMetric
def calculateYear():
    herfindahlIndices = {}
    for file in fileList:
        repo = getRepoID(file)
        herfindahlIndices[repo] = {}
        year = CURRENT_DATE.year
        userCommitHist, commitCount = countCommitsByYear(file)
        while(year >= EARLIEST_DATE.year):
            index = 0
            commitHist = userCommitHist.get(year, {})
            commitNum = float(commitCount.get(year, 0))
            for user, commits in commitHist.items():
                index += (commits/commitNum)**2
            herfindahlIndices[repo][year] = index
            year-=1
    return herfindahlIndicesz
def calculateMonth():
    herfindahlIndices = {}
    for file in fileList:
        repo = getRepoID(file)
        herfindahlIndices[repo] = {}
        currentMonth = getMonthID(CURRENT_DATE)
        userCommitHist, commitCount = countCommitsByMonth(file)
        while(currentMonth >= getMonthID(EARLIEST_DATE)):
            index = 0
            commitHist = userCommitHist.get(currentMonth, {})
            commitNum = float(commitCount.get(currentMonth, 0))
            for user, commits in commitHist.items():
                index += (commits/commitNum)**2
            herfindahlIndices[repo][currentMonth] = index
            #decrement a month
            currentMonth -= 1
            if(currentMonth%100 == 0):
                currentMonth-=100
                currentMonth+=12
    return herfindahlIndices
def getRepoID(fname):
    filePieces = fname.split("-")
    repo = filePieces[0]+"-"+filePieces[1]
    return repo
def countCommits(rawFileName, startDate=date.min, endDate=date.max):
    raw = openJSON(pathToJSON + rawFileName)
    userCommitHist = {}
    userCommitDates = defaultdict(list)
    commitCount = 0
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        name = commit["commit"]["author"]["name"].encode("utf-8")
        if commitdate < endDate and commitdate >= startDate:
            userCommitHist[name] = userCommitHist.get(name, 0) + 1
            commitCount+=1
            userCommitDates[name].append(commitdate)
    return userCommitHist, commitCount, userCommitDates
def countCommitsByYear(rawFileName):
    raw = openJSON(pathToJSON + rawFileName)
    userCommitHist = {}
    commitCount = {}
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        name = commit["commit"]["author"]["name"].encode("utf-8")
        year = commitdate.year
        if year not in userCommitHist:
            userCommitHist[year] = {}
        userCommitHist[year][name] = userCommitHist[year].get(name, 0) + 1
        commitCount[year] = commitCount.get(year, 0) + 1
    return userCommitHist, commitCount
def countCommitsByMonth(rawFileName):
    raw = openJSON(pathToJSON + rawFileName)
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
def openJSON(fname):
    return json.load(open(fname, "r"))
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print 'Overall Average Time Delay'
    for item in sorted(calculateOverall().items()):
        print "{:<30}\t{}".format(item[0], item[1])
    # print '\nPer Year'
    # hiSortedByYear = sorted(calculateYear().items())
    # index = 0
    # sortedYears = sorted(hiSortedByYear[0][1].keys())
    # print "{:<12}".format("Year"),
    # for item in hiSortedByYear:
    #     print "{:<30}".format(item[0]),
    # while(index < len(sortedYears)):
    #     currYear = sortedYears[index]
    #     print "\n{:<12}".format(currYear),
    #     for item in hiSortedByYear:
    #         print "{:<30}".format(item[1][currYear]),
    #     index+=1
    # print ''
    #
    # print '\nPer Month'
    # hiSortedByMonth = sorted(calculateMonth().items())
    # index = 0
    # sortedMonths = sorted(hiSortedByMonth[0][1].keys())
    # print "{:<12}".format("Month"),
    # for item in hiSortedByMonth:
    #     print "{:<30}".format(item[0]),
    # while(index < len(sortedMonths)):
    #     currMonth = sortedMonths[index]
    #     print "\n{} {:<7}".format(currMonth/100, currMonth%100),
    #     for item in hiSortedByMonth:
    #         print "{:<30}".format(item[1][currMonth]),
    #     index+=1
