#!/usr/bin/python

import time
import nltk
from nltk import stem
import sys
from nltk.stem.wordnet import WordNetLemmatizer
from termcolor import colored
from multiprocessing import Process,JoinableQueue
import search_engine

def pos_tag(queue,text) :
	tokens=nltk.word_tokenize(text)
	pos=nltk.pos_tag(tokens)

	result=''

	for x in pos :
		result=result+" "+x[0]+" "+x[1]
	queue.put(result)

def tagger(artifact):

	start_time=time.time()

	text=search_engine.search(artifact)
#	print colored('INFORMATION_EXTRACTION : ','red'),colored(' %.2f '% ( time.time()-start_time),'green'),'seconds'

	jobs=[]
	queue=JoinableQueue()

	for line in text :
		jobs.append(Process(target=pos_tag,args=(queue,line,)))

	for job in jobs : job.start()
	for job in jobs : job.join()
	
	result=[]

	while not queue.empty():
		result.append(queue.get())

#	print colored('POS_TAGGING : ','red'),colored(' %.2f '% ( time.time()-start_time),'green'),'seconds'
	
	return result

def main():
	artifact=str(sys.argv[1])
	result=tagger(artifact)

if __name__ == "__main__":
	main()
