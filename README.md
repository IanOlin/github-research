# Open Source Software and Strategy
[Jared Briskman](https://github.com/jaredbriskman), [Serena Chen](https://github.com/poosomooso), [Anne Ku](https://github.com/kuannie1), [Ian Paul](https://github.com/IanOlin) (Olin College)

Under the direction of Jason Woodard (Olin College) and Jonathan Sims (Babson College).

This repo houses two separate, but related research projects:

* Analyzing a list of machine learning projects (CNTK, TensorFlow, Theano, Caffe, Torch7, Deeplearning4j)
* Analyzing the differences between Cloudstack and Openstack

This repository is mostly used for data extraction and manipulation. We get our data from the GitHub API.

Tooling is written in Python 2.7, with a little bit of Mathematica 11.

Tooling is tested stable on Ubuntu 14.04 and 16.04, if running on windows, YMMV.

### Dependencies

Dependencies include Requests, an HTTP library for python. Installation is as simple as:

```
$ pip install requests
```

### Quick (ish) Use Instructions

#### Step 1: Clone this repository
Navigate to the desired local location for the repository and clone via:
HTTP - 
```
$ git clone https://github.com/IanOlin/github-research.git 
```

SSH - 
```
$ git clone git@github.com:IanOlin/github-research.git 
```


#### Step 2: Add the keyfile
Use of the software requires a keyfile, `keyfile.txt`, in the `github_scraping/` directory. 
This should be a plain text document, with at least one github OAuth token in it. More tokens may be added, separated by newlines.

Create a keyfile in an editor of your choice, and generate github oauth tokens with the following instructions:
<https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>

#### Step 3: Acquire Data
Skip this step if you already have a dataset.

From the top level, run:
```
$ python run_scraping.py
```
to generate a dataset for the ML repositories studied in the research project.

#### Step 4: Run metrics
From the top level, run:
```
$ python run_metrics.py
``` 
in order to print all calculated metrics to STDOUT. 
Redirecting to a text file may be useful, and can be accomplished via:
```
$ python run_metrics.py > yourpath/yourfile.txt
```

### Usage notes
If one desires to add other repositories for analysis, extend `misc_info/constants.py`, adding another flag for the set of repositories, then running scraping and analysis with that flag.



