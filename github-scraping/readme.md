# GitHub Scraping
Scripts and modules to help with grabbing stuff from the GitHub API.

Proper usage requires a GitHub API key to be in a file called "keyfile.txt". Multiple keys can be used (put them on separate lines).

Fatal errors will have the error message printed to a file called "ERROR.txt".

### github_util.py
Outlines functions to make calls to the API and navigate JSONS. Here are some important ones:

* api_get
Accesses the API using the link and parameters provided (the function automatically adds the API key as a parameter). Will automatically detect when the GitHub API is being rate limited and will wait the proper amount of time. Returns a Response object (from the requests module).

* JSON_access
Given an object (intended to be a list or dict generated from a JSON file), and a list of keys, this function will return the object generated after following the set of keys provided.

* is_successful_response
Given a requests.Response object, this function returns whether it was a successful response (status code is 200).

* write_dl_file
Writes a matrix with given row names, column names, and a given matrix to a dl file of the given filename.

### repo_info.py
The next layer of abstraction. Has functions specific to GitHub repositories and the GitHub API. Also has the list of repository names and owners that we are analyzing.

* get_repos
returns the list of repositories for that all the given users own. Takes a list of usernames. Returns a dictionary that maps each user to the repositories the user owns.

* repo_people
Gets the list of all the users that have contributed to the repos given. Can also get all collaborators or forkers.

* parent_repo
Checks if the given repo is forked, and if so, returns the parent repo in a tuple (reponame, ownername). Otherwises, it returns None.

* get_all_commits
Returns all the commits of the given repo, as the API returns it.

### get_commits.py
Depending on the value of the "currentRepos" field, it grabs all the commits from the list of repos indicated, and writes the commits to separate files (one file per repo specified).

### snowballing.py
Currently specific to the machine learning repos. Grabs all the contributors of all the machine learning repos, then grabs all the repos that the contributors own and fork from, and creates a giant dl matrix of all the repos and users found, where a box in the matrix is marked if the user contributed to the repo.