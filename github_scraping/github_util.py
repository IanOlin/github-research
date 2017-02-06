import json
import requests
import os

#grab api keys -- there are multiple, each key on a line
keyfile = open(os.path.join(os.path.dirname(__file__), 'keyfile.txt'))
KEY_LIST = keyfile.readlines()
for k in range(len(KEY_LIST)):
    KEY_LIST[k] = KEY_LIST[k].strip()
KEY = KEY_LIST[0]
print KEY
keyfile.close()
indexOfFirstKey = None #necessary for remembering whether or not we've already checked the number of calls for a key, later

#no idea if this is right, complete shot in the dark. the only one that should
#matter is 200
STATUS_CODES_SUCCESSFUL = set([200])

"""
accesses the api and gets the requested information as a Response object (requests module)
"""
def api_get(baseURL, parameters = {}, minAPICallsNeeded=1):
    global KEY, indexOfFirstKey
    indexOfFirstKey = None
    while True:
        try:
            #helper methods at the bottom of the page
            remaining = get_rate_limit()
            if remaining < minAPICallsNeeded:
                get_more_calls()
            else:
                parameters['access_token'] = KEY
                intendedResponse = requests.get(baseURL, params=parameters)
                return intendedResponse

        except requests.exceptions.ConnectionError:
            print 'ConnectionError, trying again'

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
        error_dump("{}\n{}\n{}".format(json.dumps(jsonObject), breakdown, keyTuple))
        raise e

def has_next_page(response):
    try:
        pageLinks = response.headers["link"]
        return pageLinks.find('rel="next"') > 0
    except KeyError:
        return False

def is_successful_response(response):
    if response.status_code in STATUS_CODES_SUCCESSFUL:
        return True
    else:
        return False

"""
throws the error message in a file called ERROR.txt
should be used in the event of a fatal error
"""
def error_dump(errorMessage):
    try:
        errorfile = open('ERROR.txt', 'w')
        errorfile.write(errorMessage)
        errorfile.close()
    except:
        print 'could not write to file'

def write_dl_file(fileName, rowLabels, columnLabels, matrix):
    f=open(fileName,'w')
    f.write("dl nr={} nc={} format=fullmatrix\n".format(len(matrix),len(matrix[0])))

    f.write("row labels:\n")
    for r in rowLabels:
        f.write(str(r)+' ')
    f.write('\n')

    f.write('column labels:\n')
    for c in columnLabels:
        f.write(str(c)+' ')
    f.write('\n')

    for row in matrix:
        for i in row:
            f.write(str(i)+' ')
        f.write('\n')
    f.close()

def get_rate_limit():
    URLstr = "https://api.github.com/rate_limit"
    response = requests.get(URLstr, params={'access_token':KEY})
    responseJSON = json.loads(response.text)
    try:
        remaining = int(JSON_access(responseJSON, ('resources', 'core', 'remaining')))
        return remaining
    except KeyError as e:
        error_dump(response.text)
        raise e

def get_more_calls():
    if indexOfFirstKey == None:
        indexOfFirstKey = KEY_LIST.index(KEY)
    else:
        nextIndex = (KEY_LIST.index(KEY)+1)%len(KEY_LIST)
        if nextIndex!=indexOfFirstKey:
            KEY = KEY_LIST[currIndex]
            print 'KEYSWITCH '+str(KEY)
        else:
            print 'waiting',
            sys.stdout.flush() #write to stdout immediately
            #sleep for the suggested amount of time
            time_sec = int(JSON_access(responseJSON, ('resources', 'core', 'reset')))
            time.sleep(abs(time_sec+5-int(time.time())))
            print 'done waiting',
            sys.stdout.flush()
