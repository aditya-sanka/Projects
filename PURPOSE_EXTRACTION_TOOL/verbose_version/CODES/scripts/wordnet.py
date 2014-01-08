import re
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import lxml.html as lh
import re
from termcolor import colored
from multiprocessing import Process,JoinableQueue

def search(queue,query="default"):
	
	Wordnet_base="http://wordnetweb.princeton.edu/perl/webwn?s="

	fd=urllib2.urlopen(Wordnet_base + urllib.quote(query))
	response=fd.read()
	soup=BeautifulSoup(response)
	
	k = soup.findAll('li')

	html_tree=lh.fromstring(str(k[0]))
	html_text=html_tree.text_content()
	html_text=html_text.encode('ascii','ignore')
	html_text=html_text.lower()
	
	match=re.findall(r'(?<=\()(.*?)(?=\))',str(html_text))
	#print colored("\n############### Wordnet #################\n",'red')
	#print match[1]
	queue.put(str(match[1]))
						
def main():
	artifact=raw_input("Please enter the artifact :")
	search(query=artifact)

if __name__ == "__main__":
	main()
