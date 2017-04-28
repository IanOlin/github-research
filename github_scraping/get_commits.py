from repo_info import *
import json
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join('..')))
from misc_info.constants import ML, STACK, return_constants, return_filename, CURRENT_DATE

def get_commits(projects=ML):
    constants = return_constants(projects) #change this if necessary

    #directory
    dirName = constants["commits-fpath"]

    #getting correct repos
    repo_list = constants['repos']

    # record the date of data retrieval
    date_file = open(os.path.join(dirName, "date.txt"), 'w')
    date_file.write(CURRENT_DATE.strftime("%b %d, %Y"))
    date_file.close()

    #getting commits
    for repo_data in repo_list:
        commits = get_all_commits(repo_data)

        print "writing data..."
        output_file = open(os.path.join(dirName, return_filename(repo_data)), 'w')
        json.dump(commits, output_file)
        output_file.close()
        print "done writing data."

if __name__ == '__main__':
    get_commits(STACK)