# domain to company by hand
import json
import string
import clearbit
from pprint import pprint

with open('companies.json') as company_dump:
	companies = json.load(company_dump)

# with open('baddata.txt') as baddata:
# 	dirtyComp = baddata.readlines()
# 	i =0
# 	for comp in dirtyComp:
# 		i=i+1
# 		if (i%3 ==0):
# 			print comp


commitCompany = {}
j=2
for key in companies:
	print("what is this company?")
	print key
	company = raw_input()
	# commitCompany[key] = dirtyComp[j]
	j=j+3

pprint(commitCompany)

with open('companies2.json', 'w') as company_dump:
	json.dump(commitCompany, company_dump)


# with open('companies2.json') as company_dump:
# 	check = json.load(company_dump)
# 	pprint(check)