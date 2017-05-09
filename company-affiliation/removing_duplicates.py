# This Python file uses the following encoding: utf-8

# import os, sys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime, time
from pattern.web import *
from pattern.web import URL, extension, download
from sets import Set
import json
import re
DUP_DICT = {u"Frederic" : u"Frédéric Bastien", u"Frederic Bastien" : u"Frédéric Bastien", u"nouiz" : u"Frédéric Bastien",
        u"lamblin" : u"Pascal Lamblin", 
        u"abergeron" : u"Arnaud Bergeron",
        u"carriepl" : u"Pierre Luc Carrier",
        u"Jon Long" : u"Jonathan L Long", u"longjon" : u"Jonathan L Long",
        u"Sergio" : u"Sergio Guadarrama",
        u"frankseide" : u"Frank Seide",
        u"terrytangyuan" : u"Yuan (Terry) Tang",
        u"caisq" : u"Shanqing Cai",
        u"yifeif" : u"Yifei Feng",
        u"Daniel W Mane" : u"Dan Mané",
        u"soumith" : u"Soumith Chintala",
        u"Nicholas Léonard" : u"Nicholas Leonard", u"nicholas-leonard" : u"Nicholas Leonard",
        u"GeorgOstrovski" : u"Georg Ostrovski",
        u"agibsonccc" : u"Adam Gibson",
        u"raver" : u"raver119", u"raver119@gmail.com" : u"raver119",
        u"nyghtowl" : u"Melanie Warrick", 
        u"jyt109" : u"Jeffrey Tang",
        u"bergstrj@iro.umontreal.ca" :u"James Bergstra", u"bergstra@ip05.m" : u"James Bergstra" }
 
PATHtoLinkedInJSONs = "/home/anne/github-research/company-affiliation/resources/linkedin_info/"
DEBUG = True
pending = []
repos = ["CNTK", "Theano", "caffe", "deeplearning4j", "tensorflow"]

for repo in repos:
	print repo
	json_file = "{}_frequentcommitters.json".format(repo)
	with open(json_file, 'r') as data_file:
		json_dict = json.load(data_file)
		affiliated = json_dict["affiliated"]
		overall = json_dict["overall"]
	# Get keys of DUP_DICT
	extra_names = DUP_DICT.keys()
	for i in range(len(affiliated)):
		name = affiliated[i]
		if name in extra_names:
			affiliated[i] = DUP_DICT[name]
	for i in range(len(overall)):
		name = overall[i]
		if name in extra_names:
			overall[i] = DUP_DICT[name]
	new_affiliated = Set(affiliated)
	new_overall = Set(overall)
	final_json= {}
	final_json["affiliated"] = list(new_affiliated)
	final_json["overall"] = list(new_overall)
	print "\nAt least {} people out of the top {} committers are affilaited with {}".format(len(final_json["affiliated"]), len(final_json["overall"]), repo)
