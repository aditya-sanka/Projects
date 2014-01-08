#!/bin/bash

# This is a script to install the required dependencies

#	These are the required python modules
#	We have been using python 2.7.4
#
#	mechanize
#	BeautifulSoup
#	urllib2
#	lxml
#	termcolor
#	multiprocessing

sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv

sudo apt-get install python-mechanize
sudo pip install BeautifulSoup
sudo apt-get install python-tk
sudo apt-get install libxml2-dev libxslt-dev
sudo pip install termcolor
