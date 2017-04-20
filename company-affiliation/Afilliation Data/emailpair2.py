import json
import string
from pprint import pprint

with open('companies-caffe.json') as company_dump:
	companies = json.load(company_dump)

with open('companies2.json') as company_dump:
	commitCompany = json.load(company_dump)

pprint(commitCompany)
j=2
for key in companies:
	if key not in commitCompany:	
		print("what is this company?")
		print key
		company = raw_input()
		# commitCompany[key] = dirtyComp[j]
		commitCompany[key] = company
		j=j+3

with open('companies2.json', 'w') as company_dump:
	json.dump(commitCompany, company_dump)

pprint(commitCompany)