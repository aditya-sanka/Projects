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
	b.open('http://en.wikipedia.org/')

	b.select_form(nr=0)
	b['search'] = query
	fd = b.submit()

	s=fd.read()
	
	soup=BeautifulSoup(s)
	k = soup.findAll('p')
	
	html_tree=lh.fromstring(str(k[0]))
	html_text=html_tree.text_content()
	html_text=html_text.encode('ascii','ignore')
	html_text=html_text.lower()

	sentences= html_text.split('.')
#	print colored("\n############### Wikipedia #################\n",'red')
#	print sentences[0]
	queue.put(str(sentences[0]))
						
def main():
	artifact=raw_input("Please enter the artifact :")
	search(query=artifact)

if __name__ == "__main__":
	main()
