#!/usr/bin/python

from multiprocessing import Process,JoinableQueue
import time
import nltk
from nltk import stem
import sys
from nltk.stem.wordnet import WordNetLemmatizer

import os
import re
from termcolor import colored

import CODES.pos_tagger as pos_tagger

common_verbs=[]
rex=[]
lmtzr = WordNetLemmatizer()

dict1={}
dict1['class1']=['\w*? VB\w*? \w*? TO \w*? VB\w*? \w*? NNS','\w*? NN\w*? \w*? IN \w*? VBG \w*? JJ \w*? NN',]
dict1['class2']=['\w*? TO \w*? VB\w*? \w*? DT \w*? NN\w*?']
dict1['class3']=['use\w*? VB. \w*? IN \w*? NN \w*? NNS',]
dict1['class4']=['used VB\w*? \w*? IN \w*? NN \w*? NN \w*? NN\w*?',
		 'used VB\w*? \w*? IN \w*? NN \w*? NN',
		 'used VB\w*? \w*? IN \w*? NN']
dict1['class5']=['a DT \w*? NN for IN \w*? NN \w*? NN','a DT \w*? NN for IN \w*? NN']
dict1['class6']=['\w*? VBZ \w*? DT \w*?ing NN \w*? NN']
dict1['class7']=['used VBN for IN \w* NNS']
dict1['class8']=['\w*? TO \w*? VB \w*? JJ \w*? JJ']
dict1['class9']=['\w*? IN \w*? VBG \w*? NN']

def getpurpose(matched,classname):
	lmtzr = WordNetLemmatizer()
	if classname=='class4' or classname=='class6' or classname=='class3':
		exp='\w*?ing NN\w*?'
		match=re.search(exp,matched)
		purpose_text=match.group().split()
		purpose=lmtzr.lemmatize(purpose_text[0],'v')
		return purpose
	if classname=='class2':
		exp='\w*? VB\w*?'
		match=re.search(exp,matched)
		purpose_text=match.group().split()
		purpose=lmtzr.lemmatize(purpose_text[0],'v')
		return purpose
	if classname=='class5' or classname=='class7':
		exp='for IN \w*? NN\w*?';
		match=re.search(exp,matched)
		purpose_text=match.group().split()
		purpose=lmtzr.lemmatize(purpose_text[2],'v')
		return purpose
	if classname=='class1' or 'class9':
		exp='\w*? IN \w*? VBG'
		match=re.search(exp,matched)
		if match:
			purpose_text=match.group().split()
			purpose=lmtzr.lemmatize(purpose_text[2],'v')
			return purpose
	if classname=='class1':
		exp='\w*? TO \w*? VB\w*? \w*? NN\w*?'
		match=re.search(exp,matched)
		if match:
			purpose_text=match.group().split()
			purpose=lmtzr.lemmatize(purpose_text[2],'v')
			return purpose
	return None

def printmatch(artifact,matched,classname):
	file_name='cache/'+artifact
	string=getpurpose(matched,classname)
	purpose_list=[]
	if string==None:
		return 
	if os.path.exists(file_name):
		f=open(file_name,'rt')
		line=f.read()
		purpose_list=line.split('\n')
	if string not in purpose_list:
		f2=open(file_name,'a')
		print string
		f2.write(string+'\n')
		f2.close()

def extract_purpose(queue,artifact,text):
	string='class'

	for count in range(1,9):
		classa=string+str(count)
		for exp in dict1[classa]:
			match=re.search(exp,text)
			if match :
				classname='class'+str(count)
				printmatch(artifact,match.group(),classname);
				break
def check_cache(artifact):
	file_name='cache/'+artifact

	if os.path.exists(file_name):
		f=open(file_name,'r')
		print f.read()
		return True
	else :
		return False


def purpose_extraction(artifact):

	folder='cache/'

	if not os.path.exists(folder):
		os.makedirs(folder)
	
	start_time=time.time()
	print (artifact+" ~> "),
	if check_cache(artifact):
		sys.exit(1)

	text=pos_tagger.tagger(artifact)

	jobs=[]
	queue=JoinableQueue()

	for line in text : 
		jobs.append(Process(target=extract_purpose,args=(queue,artifact,line)))	
	

	for job in jobs : job.start()
	for job in jobs : job.join()

	print colored('Execution time : ','red'),colored(' %.2f '% ( time.time()-start_time),'green'),'seconds'

def main():
	
	err=open(os.devnull,'w')
	sys.stderr=err
	
	if len(sys.argv) == 3 and sys.argv[1] == "-f":
		list_of_artifacts=open(sys.argv[2],'r')
		for line in  list_of_artifacts:
			purpose_extraction(line.replace('\n',''))
		return
	
	artifact=sys.argv[1].replace('\n','')
	purpose_extraction(artifact)

if __name__ == "__main__":
	main()
