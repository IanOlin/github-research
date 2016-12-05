# Company Affiliation
Finding what contributors are affiliated with what company.

### Code

* get_linkedin_info.py
Grabs each of the commits from the API output (stored in files), and takes the commit author and scrapes the author's linkedin profile. Writes the results of the scraping to a file in "company-affiliation/resources/linkedin_info" that is specific to that commit author. Requires Selenium Webdriver and Firefox.

* company_affiliation.py
Goes through each commit from the API output and, using the commit author and the linkedin data generated from get_linkedin_info.py, finds the company or organization(s) the user was involved in at the time of the commit. Also generates a company that the user is affiliated with using the email domain. Writes a json for each repo, with the commit's sha mapped to the commit's author, email, timestamp, and list of companies/organizations, along with a flag that denotes how likely that company is to be the actual company the user is affiliated with.

* getCrossovers.py

* obtain_remaining_linkedins.py

* python_findtitle.py