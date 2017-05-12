# Company Affiliation
Finding what contributors are affiliated with what company.

### Code

* affiliation_calculation.py

Contains a variety of helper functions that help us determine the percentage of top committers are affiliated with the organization that hosts the repository. 

```
$ cd ~/github-research/company-affiliation
$ python affiliation_calculation.py
Out of top 100 percent of deeplearning4j's committers, at least 6.92307692308 percent of them are affiliated with Skymind.io
Out of top 100 percent of Theano's committers, at least 13.539192399 percent of them are affiliated with Univ. of Montreal
Out of top 100 percent of caffe's committers, at least 1.0752688172 percent of them are affiliated with Berkeley Vision and Learning Center
Out of top 100 percent of CNTK's committers, at least 15.9090909091 percent of them are affiliated with Microsoft
Out of top 100 percent of tensorflow's committers, at least 8.75576036866 percent of them are affiliated with Google
```

* companyaffiliation.json
A large JSON file that contains the work histories we have of the Stack and ML repositories. 

There's a small disclaimer: Most of the entries in this file is manually done, with some help from the getLinkedInInfo() function in affiliation_calculation.py. If you want to run this code on other repositories, you may have to add more entries

* geckodriver.log
File needed to use the function getLinkedInInfo() in affiliation_calculation.py