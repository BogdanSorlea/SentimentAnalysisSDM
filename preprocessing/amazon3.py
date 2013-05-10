import urllib2, re, math, zlib, pprint, pickle
from BeautifulSoup import BeautifulSoup
import codecs
import time

def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""
			

opener = urllib2.build_opener()
opener.addheaders = [("Accept", "text/javascript, text/html, application/xml, text/xml, */*"),
					 ("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3"),
					 ("Accept-Encoding", "gzip,deflate,sdch"),
					 ("Accept-Language", "en-US,en;q=0.8"),
					 ("Connection", "keep-alive"),
					 ("Host", "www.amazon.com"),
					 ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"),
					 ("X-Prototype-Version", "1.7"),
					 ("X-Requested-With", "XMLHttpRequest")]


url = ["http://www.amazon.com/gp/bestsellers/","","/books/ref=zg_bsar_books_pg_1?ie=UTF8&pg=",""]
rurl = ["http://www.amazon.com/product-reviews/","","/ref=cm_cr_pr_top_link_2?ie=UTF8&filterBy=add","","&pageNumber=","","&showViewpoints=0"]
stars = ["OneStar","TwoStar","ThreeStar","FourStar","FiveStar"]
for h in (2012, 1995, -1):
	url[1]=str(h)
	top100links = list()
	# page = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
	# soup = BeautifulSoup(page);
	for i in range(1,6):
		url[3]=str(i)
		response = opener.open(url[0]+url[1]+url[2]+url[3])
		# toppage = urllib2.urlopen(url[0]+url[1]).read();
		page = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
		soup = BeautifulSoup(page);
		products = soup.findAll('div',attrs={'class':'zg_title'});
		for i in products:
			top100links.append(i.a["href"].strip(' \n\t'))
			print i.a["href"].strip(' \n\t')


	print "\n\n######## SCRAPING INITIALIZED #########\n\n"
			
	for i in top100links[13:]:
		ratingComments=[]
		movie_id = find_between(i, "dp/", "/ref=" )
		# print "Creating file " + str(h)+"/\amazon_"+str(movie_id)
		f=open( str(h) + '\\amazon_' + str(movie_id),'wb')
		rurl[1]=movie_id
		# print str(top100links[count])
	# -------------iterate over stars ------------#
		for j in range (5):
			rurl[3]=stars[j]
			total_pages = 0
			print rurl[0]+rurl[1]+rurl[2]+rurl[3]+rurl[4]+str(total_pages)+rurl[6]
			while True:
				try:
					response = opener.open(rurl[0]+rurl[1]+rurl[2]+rurl[3]+rurl[4]+str(total_pages)+rurl[6])
					page = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
					soup = BeautifulSoup(page);
					break
				except ValueError:
					time.sleep(3)
					print "error while loading page, waiting..."
					pass
			# -------------iterate over pages ------------#
			pnumber=0
			try:
				if soup.find('span',{'class':'paging'}) is not None:
					for x,nop in enumerate(soup.find('span',{'class':'paging'})):
						try:
							number = int(nop.string)
							if number > pnumber:
								pnumber = number
							if x >= 5:
								break
						except ValueError:
							continue
			except ValueError:
				continue
			print pnumber
			for k in range (1,pnumber+1):
				print str(k)
				rurl[5]=str(k)
				# print rurl[0]+rurl[1]+rurl[2]+rurl[3]+rurl[4]+rurl[5]+rurl[6]
				while True:
					try:
						response = opener.open(rurl[0]+rurl[1]+rurl[2]+rurl[3]+rurl[4]+rurl[5]+rurl[6])
						page = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
						soup = BeautifulSoup(page);
						break
					except ValueError:
						time.sleep(3)
						print "error while loading page, waiting..."
						pass
				products = soup.findAll("div", style = "margin-left:0.5em;")
				for i in products:
					if (i.findNext("div", style = "margin-bottom:0.5em;").string) is not None:
						currentUsefull = i.findNext("div", style = "margin-bottom:0.5em;").string.strip()
						usefull = re.findall('\d+', currentUsefull)[0]
						totall = re.findall('\d+', currentUsefull)[1]
					else:
						usefull = None
						totall = None
					if i.findNext('b') == None:
						currentTitle = None
					else:
						try:
							currentTitle = i.findNext('b').string.strip().encode('ascii', 'ignore')
						except AttributeError:
							currentTitle = None
					if i.findNext("div", "tiny") == None:
						currentString = None
					else:
						try:
							currentPart = i.findNext("div", "tiny").findNextSibling(text=True)
							currentString = currentPart.string.strip()
						except AttributeError:
							currentString = None
					while True:
						# print  currentPart.findNextSibling.name
						if not (currentPart.findNextSibling(text=True)):
							break
						else:
							currentPart = currentPart.findNextSibling(text=True)
							currentString += "\n" + currentPart.string.strip()
					if currentString == None:
						currentBody = None
					else:
						currentBody = currentString.encode('ascii', 'ignore')
					t=(currentBody,j,currentTitle,usefull,totall)	
					ratingComments.append(t)
		pickle.dump(ratingComments,f)
		f.close()	