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
	b.open('http://www.collinsdictionary.com/')


	b.select_form(nr=0)
	b['q'] = query
	fd = b.submit()

	s=fd.read()
	soup=BeautifulSoup(s)
	k = soup.findAll(attrs={"class":"def"})
	
	html_tree=lh.fromstring(str(k[0]))
	html_text=html_tree.text_content()
	html_text=html_text.encode('ascii','ignore')
	html_text=html_text.lower()

	#print colored("\n############### Collins Dictionary #################\n",'red')
	#print html_text

	queue.put(str(html_text))

def main():
	artifact=raw_input("Please enter the artifact :")
	search(query=artifact)

if __name__ == "__main__":
	main()
