from datetime import date
import json

CURRENT_DATE = date(2016, 11, 1)

pathToJSON = "/home/serena/GithubResearch/mlCommits-new/"
fileList = ("caffe-BVLC-commits.json", "CNTK-Microsoft-commits.json", "deeplearning4j-deeplearning4j-commits.json", "tensorflow-tensorflow-commits.json", "Theano-Theano-commits.json", "torch7-torch-commits.json", "incubator-systemml-apache-commits.json")

def calculateOverall():
    herfindahlIndices = {}
    for file in fileList:
        userCommitHist, commitCount = countCommits(file, date.min, date.max)
        index = 0
        commitCount = float(commitCount)
        for user, commits in userCommitHist.items():
            index += (commits/commitCount)**2
        repo = getRepoID(file)
        herfindahlIndices[repo] = index
    return herfindahlIndices

def calculateYear():
    herfindahlIndices = {}
    for file in fileList:
        repo = getRepoID(file)
        herfindahlIndices[repo] = {}
        year = CURRENT_DATE.year
        userCommitHist, commitCount = countCommitsByYear(file)

        while(year >= 2008):
            index = 0
            commitHist = userCommitHist.get(year, {})
            commitNum = float(commitCount.get(year, 0))

            for user, commits in commitHist.items():
                index += (commits/commitNum)**2
            herfindahlIndices[repo][year] = index
            year-=1
    return herfindahlIndices

def getRepoID(fname):
    filePieces = fname.split("-")
    repo = filePieces[0]+"-"+filePieces[1]
    return repo

def countCommits(rawFileName, startUnix, endUnix):
    raw = openJSON(pathToJSON + rawFileName)
    userCommitHist = {}
    commitCount = 0
    for commit in raw:
        # simple fields
        unixDate = commit["commit"]["author"]["date"].encode("utf-8")
        commitdate = parseTimeStamp(unixDate)
        # url = commit["commit"]["url"]
        # sha = url.split("/")[-1].encode("utf-8")
        # email = commit["commit"]["author"]["email"].encode("utf-8")
        name = commit["commit"]["author"]["name"].encode("utf-8")

        if commitdate < endUnix and commitdate >= startUnix:
            userCommitHist[name] = userCommitHist.get(name, 0) + 1
            commitCount+=1

    return userCommitHist, commitCount

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
    print 'Overall Herfindahl Indices'
    print calculateOverall()
    print 'Per Year'
    print calculateYear()