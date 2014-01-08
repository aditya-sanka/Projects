#!/usr/bin/python

from multiprocessing import Process,JoinableQueue
import time
from termcolor import colored
import os
import sys
import datetime

import scripts.wikipedia as wikipedia
import scripts.oxford as oxford
import scripts.cambridge as cambridge
import scripts.macmillan as macmillan
import scripts.wordnet as wordnet
import scripts.webster as webster
import scripts.dictionary_reference as dictionary_reference
import scripts.collins as collins
import scripts.longman as longman
import scripts.google_dictionary as google_dictionary
import scripts.wordreference as wordreference
import scripts.wordnik as wordnik

def search(artifact):

	start_time=time.time()
	jobs=[]
	queue=JoinableQueue()

	jobs.append(Process(target=wikipedia.search,args=(queue,artifact,)))
	jobs.append(Process(target=oxford.search,args=(queue,artifact,)))
	jobs.append(Process(target=cambridge.search,args=(queue,artifact,)))
	jobs.append(Process(target=macmillan.search,args=(queue,artifact,)))
	jobs.append(Process(target=wordnet.search,args=(queue,artifact,)))
	jobs.append(Process(target=webster.search,args=(queue,artifact,)))
	jobs.append(Process(target=dictionary_reference.search,args=(queue,artifact,)))
	jobs.append(Process(target=collins.search,args=(queue,artifact,)))
	jobs.append(Process(target=longman.search,args=(queue,artifact,)))
	jobs.append(Process(target=google_dictionary.search,args=(queue,artifact,)))
	jobs.append(Process(target=wordreference.search,args=(queue,artifact,)))
	jobs.append(Process(target=wordnik.search,args=(queue,artifact,)))

	for job in jobs : job.start()
	for job in jobs : job.join()

	text=[]	

	while not queue.empty():
		string=str(queue.get()).replace('\n',' ')
		text.append(string)
	return text

def main():		
	
	artifact=sys.argv[1]

	if artifact == "-f":	
		f=open(sys.argv[2],'r');
		for line in f:
			line=line.replace('\n','')
			line=line.replace('_',' ')
			search(line)
	else:	
		text=search(artifact)
if __name__ == "__main__":
	main()
