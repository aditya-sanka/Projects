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
dict1['class1']=['as IN \w*? DT \w*? NN .\w*? POS \w*? NN','as IN \w*? NN .\w*? POS \w*? NN']
dict1['class2']=['\w*? VB\w*? \w*? TO \w*? VB\w*? \w*? NNS','\w*? NN\w*? \w*? IN \w*? VBG \w*? JJ \w*? NN',]
dict1['class3']=['\w*? TO \w*? VB\w*? \w*? DT \w*? NN\w*?']
dict1['class4']=['use\w*? VB. \w*? IN \w*? NN \w*? NNS',]
dict1['class5']=['used VB\w*? \w*? IN \w*? NN \w*? NN \w*? NN\w*?',
		 'used VB\w*? \w*? IN \w*? NN \w*? NN',
		 'used VB\w*? \w*? IN \w*? NN']
dict1['class6']=['a DT \w*? NN for IN \w*? NN \w*? NN','a DT \w*? NN for IN \w*? NN']
dict1['class7']=['\w*? NN \w*? IN \w*? WDT \w*? TO \w*? VB']
dict1['class8']=['\w*? VBZ \w*? DT \w*?ing NN \w*? NN']
dict1['class9']=['used VBN for IN \w* NNS']
dict1['class10']=['\w*? TO \w*? VB \w*? JJ \w*? JJ']
dict1['class11']=['\w*? IN \w*? VBG \w*? NN',
	 	 '\w*? TO \w*? VB \w*? NN\w*?']

def removepos(matched):
	length=len(matched)
	count=0;
	count2=0;
	string=''
	for count in range(0,length):
		if matched[count].isupper():
			do=0
		elif matched[count]==' ':
			do=0
			count2=count2+1
			if count2%2==0:
				do=0
			else:
				string=string+' '
		else:
			string=string+matched[count]
	return string 

def printmatch(artifact,matched,classname):
	file_name='cache/'+artifact
	f=open(file_name,'a')

	if classname=='class1' or classname=='class3' or classname=='class11' or classname=='class10':
		print artifact,'is used',
		f.write(artifact+" is used ")
		string=removepos(matched)
		print colored(string,'blue')
		f.write(colored(string,'blue')+'\n')
	elif classname=='class5' or classname=='class9' or classname=='class2' or classname=='class4' or classname=='class6' or classname=='class9':
		print artifact,'is',
		f.write(artifact+" is ")
		string=removepos(matched)
		print colored(string,'blue')
		f.write(colored(string,'blue')+'\n')
	elif classname=='class8':
		print artifact,
		f.write(artifact+" ")
		string=removepos(matched)
		print colored(string,'blue')
		f.write(colored(string,'blue')+'\n')

def extract_purpose(queue,artifact,text):
	string='class'

	for count in range(1,12):
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
	print artifact+" ~> "
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
