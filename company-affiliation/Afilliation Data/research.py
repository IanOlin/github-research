# Email extrator
import json
import string
import clearbit
from pprint import pprint

# clearbit.key = 'sk_81a531f454bb33d9868b872f29d45b4e'

with open("P:\+Research\GitWood\mlCommits\caffe-BVLC-commits.json") as data_file:    
    data = json.load(data_file)

commitCompanies = {}

for i in range(len(data)):
	email = data[i]['commit']['author']['email']
	try:
		domain = string.split(email, '@')[1]
		print('{0}, {1}'.format(email, domain))
		commitCompanies[domain] = 'domain'
	except:
		print "invalid email:" + email
		pass

with open('companies-caffe.json', 'w') as company_dump:
	json.dump(commitCompanies, company_dump)

# for i in range(len(data)):
# 	email = data[i]['commit']['author']['email']
# 	domain = string.split(email, '@')[1]
# 	print('{0}, {1}'.format(email, domain))
# 	try:
# 		company = clearbit.Company.find(domain=domain, stream=True)
# 	except:
# 		print "Lookup Error"
# 		commitCompanies[data[i]['sha']] = 'Lookup Error'
# 		pass
# 	if domain == 'review.openstack.org':
# 		botFlag = True
# 	try:
# 		if company['name'] != None:
# 			print i
# 			print "Name: " + company['name']
# 			commitCompanies[data[i]['sha']] = company['name']
# 			if botFlag:
# 				commitCompanies[data[i]['sha']] = 'review.openstack.org'
# 	except:
# 		print "Failed to find compay['name']"
# 		pass
# 	try:
# 		if company['name'] == None:
# 			print "No company found"
# 			commitCompanies[data[i]['sha']] = 'No company found'
# 	except:
# 		print "Failed to find compay['name']"
# 		with open('dump.json', 'w') as data_dump:
# 			json.dump(commitCompanies, data_dump)

# 		pass
# 	botFlag = False

pprint(commitCompanies)

# with open('dump.json', 'w') as data_dump:
# 	json.dump(commitCompanies, data_dump)
# with open('dump.json') as data_dump:
# 	data = json.load(data_dump)
# 	pprint(data)