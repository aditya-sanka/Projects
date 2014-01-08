import mechanize
import re
from BeautifulSoup import BeautifulSoup
import urllib2
import lxml.html as lh
from termcolor import colored
from multiprocessing import Process,JoinableQueue

def search(queue,query="default"):

	b = mechanize.Browser()
	b.set_handle_robots(False)
	b.addheaders = [('User-agent',' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0')]
	b.open('http://goodictionary.so8848.com/')

	b.select_form(name="SUYB")
	b['word'] = query
	fd = b.submit()

	s=fd.read()
	
	soup=BeautifulSoup(s)
	k = soup.findAll(attrs={"style":"list-style:decimal; margin-bottom:10px;"})
	
	html_tree=lh.fromstring(str(k[0]))
	html_text=html_tree.text_content()
	html_text=html_text.encode('ascii','ignore')
	html_text=html_text.lower()

	#print colored("\n############### Google Dictionary #################\n",'red')
	#print html_text

	sentences=html_text.split(';')
	#print sentences[0]
	queue.put(str(sentences))

def main():
	artifact=raw_input("Please enter the artifact :")
	search(query=artifact)

if __name__ == "__main__":
	main()
