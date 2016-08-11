import json
import requests

#grab api keys -- there are multiple, each key on a line
keyfile = open('keyfile.txt')
KEY_LIST = keyfile.readlines()
for k in range(len(KEY_LIST)):
    KEY_LIST[k] = KEY_LIST[k].strip()
KEY = KEY_LIST[0]
print KEY
keyfile.close()

#no idea if this is right, complete shot in the dark. the only one that should 
#matter is 200
STATUS_CODES_SUCCESSFUL = set([200, 201, 203, 204, 206, 207, 208, 226])
STATUS_CODES_RETRY = set([202, 205])

def api_get(baseURL, parameters = {}, minAPICallsNeeded=1):
    """
    accesses the api and gets the requested information as a Response object (requests module), 
    returns None if the response returns with an error code (beta)
    """
    ### TODO: implement error code reading and error handling
    indexOfFirstKey = None
    global KEY
    while True:
        try:
            remaining = get_rate_limit()
            if remaining < minAPICallsNeeded:
                get_more_calls()
            else:
                parameters['access_token'] = KEY
                intendedResponse = requests.get(baseURL, params=parameters)

                if intendedResponse.status_code in STATUS_CODES_SUCCESSFUL:
                    return intendedResponse
                elif intendedResponse in STATUS_CODES_RETRY:
                    continue
                else:
                    return None

        except requests.exceptions.ConnectionError:
            print 'ConnectionError, trying again'

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

def JSON_access(jsonObject, keyTuple):
    """
    returns the element or json object from the tuple of keys
    returns None if repo is blocked
    """
    try:
        breakdown = jsonObject
        #following the keys through the json structure
        for key in keyTuple:
            breakdown = breakdown[key]
        return breakdown
    except (KeyError, TypeError) as e:
        #following commented code should be obsolete due to status codes
        #if repository is blocked, return nothing
        # try:
        #     if "blocked" in jsonString['message']:
        #         return None
        # except:
        #     pass
        # print 'not blocked' 
        #key errors
        error_dump(json.dumps(jsonString))
        raise e

def has_next_page(response):
    try:
        pageLinks = response.headers["link"]
        return pageLinks.find('rel="next"') > 0
    except KeyError:
        return False


def error_dump(errorMessage):
    try:
        errorfile = open('ERROR.txt', 'w')
        errorfile.write(errorMessage)
        errorfile.close()
    except:
        print 'could not write to file'