import re
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import lxml.html as lh
import re
from termcolor import colored
from multiprocessing import Process,JoinableQueue

def search(queue,query="default"):
	
	url_base="http://www.ldoceonline.com/dictionary/"
	
	query=query.replace(' ','-')

	fd=urllib2.urlopen(url_base + urllib.quote(query))
	response=fd.read()
	soup=BeautifulSoup(response)

	k = soup.findAll(attrs={'class':'DEF'})

	html_tree=lh.fromstring(str(k[0]))
	html_text=html_tree.text_content()
	html_text=html_text.encode('ascii','ignore')
	html_text=html_text.lower()
	
#	print colored("\n############### Longman English Dictionary #################\n",'red')
#	print html_text

	queue.put(str(html_text))
						
def main():
	artifact=raw_input("Please enter the artifact :")
	search(query=artifact)

if __name__ == "__main__":
	main()
