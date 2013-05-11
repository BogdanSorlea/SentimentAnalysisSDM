import urllib2
import math
from bs4 import BeautifulSoup
import zlib
import pprint
import pickle

path = "../data/"
sourcename = "goodreads"

domain = "https://www.goodreads.com"
#book_url = "/book/show/1049153.History_of_Religious_Ideas_Volume_1"
book_url = "/book/show/13496.A_Game_of_Thrones"

url = domain + book_url
id_ = book_url.replace("/book/show/", "")
id_ = int(id_[ : id_.find(".")])

ratingConcatString = " of 5 stars"
likeConcatStringSingular = " like"
likeConcatStringPlural = " likes"
noOfItemsDelimiter = "of";
itemsPerPage = 30.0;

debugPrint = False
debugShowOutput = False

stars = []
reviews = []
likes = []

initPage = urllib2.urlopen(url)
soup = BeautifulSoup(initPage)

noOfPages = soup.select("#reviews > div")# > div > a");
noOfPages = noOfPages[0].select("span")[0].getText().replace(")", "").replace(",", "")
noOfPages = noOfPages[noOfPages.find(noOfItemsDelimiter) + 3 : len(noOfPages) - 1]
noOfPages = int(noOfPages)
print "Total reviews count: " + str(noOfPages)
print "Page count: " + str(int(math.ceil(noOfPages / itemsPerPage)))

pageCount = int(math.ceil(noOfPages / itemsPerPage))

asynchURL = soup.select("#reviews > div")[3].select("div a")[0].get("onclick")
#print asynchURL
securityToken = asynchURL
asynchURL = asynchURL.replace("new Ajax.Request('", "")
asynchURL = asynchURL[ : asynchURL.find("{asynchronous:true") - 4]
securityToken = securityToken[securityToken.find("encodeURIComponent('") + len("encodeURIComponent('") : ]
securityToken = securityToken[ : len(securityToken) - len("')}); return false;")]
#print securityToken
#exit()

totalcount = 0

if pageCount > 100:
   pageCount = 100      # limit to 100 as to avoing creating files that are too big

#pageCount = 2       # just for testing purposes

totalRating = 0
totalLikes = 0

for i in range(1, pageCount + 1):
    print domain + asynchURL + str(i)
    opener = urllib2.build_opener()
    opener.addheaders = [("Accept", "text/javascript, text/html, application/xml, text/xml, */*"),
                         ("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3"),
                         ("Accept-Encoding", "gzip,deflate,sdch"),
                         ("Accept-Language", "en-US,en;q=0.8"),
                         ("Connection", "keep-alive"),
                         ("Cookie", "__qca=P0-966782338-1366576573930; fbm_2415071772=base_domain=.goodreads.com; p=MTk5NDYwMjg%3D-2091f0959bf93a02d396382e92fcb765edc43c88; u=; __utma=250562704.990698196.1366576574.1367415275.1367421625.4; __utmb=250562704.7.10.1367421625; __utmc=250562704; __utmz=250562704.1367412376.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); fbsr_2415071772=5_BAMtr-qHHVZl8ITkKNVSKa8j7Nu1wbT1mISUaOMws.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJHVFcxRE44VkdxYlRYTDVHUG5wUXdiUTdMOURRckY3OVoyVmxsVVNNUkl1OTdBdlRfMEM3NWl0eTRjSW1rbWE1QTRpYk9Cbm00R2g1ZlZFS2RZZDNORGJ6RjNpdWwyOFZtUXJtWVREVTViTTRYOUpNS0JuYVFjU29mS2lCay1ZY19SaWpjejNkNlVUUVI2Zzdqb2tFYzlQbWxJeVdEZ3pjTmxJZlpZdGpFZ3FJRU54TXVDWGd3R2ZHNFc1cDdBbENBZTRHR0Y4RHJpbDhRTGpKam50SXc3UmRKbUdKb19ZRkQtSV93dkFpUmhmWEdONm9rM0tZVWs5WXh1MlJqbHdRbHlhWWZEc2JsVkVKNnMzYjI5WjBsakx0dFBsV0lmZUZiUGZibExZOEwwRHNTNUFBMmhXc05BV2tnbUtqeXpiR2pTUThoNFdMS0tqOWg2NjJsWUpfciIsImlzc3VlZF9hdCI6MTM2NzQyNDk2OSwidXNlcl9pZCI6IjEwMDAwMDAyMjY4MjI5NCJ9; _session_id2=887ac266c08f8df375249aa69d1ec659"),
                         ("Host", "www.goodreads.com"),
                         ("Referer", url),
                         ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"),
                         ("X-CSRF-Token", securityToken),
                         ("X-Prototype-Version", "1.7"),
                         ("X-Requested-With", "XMLHttpRequest")]
    response = opener.open(domain + asynchURL + str(i))
    page = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
    page = page[len('Element.update("reviews", "<div class=\"right bookMeta darkGreyText\">\n    <span class=\"smallText\">\n(showing\n91-120\nof\n597)\n</span>\n</div>\n\n<div id=\"bookReviewControls\">\n  <a class=\"uitext\" href=\"#\" id=\"span_class_actionlink_filter_span_tip_9\" onclick=\"return false\" style=\"cursor: pointer; \"><span class=\"actionLink\">filter</span></a><script type=\"text/javascript\">\n//<![CDATA[\n      var newTip = new Tip($("span_class_actionlink_filter_span_tip_9"), \"\\n      ') :]
    page = page[page.find("<div class") :]
    page = page.replace('");', "")
    page = page.replace(r"\n", "")
    page = page.replace(r'\\\"', '"')
    page = page.replace(r'\"', '"')
    page = page.replace(r"\\/", "/")
    page = page.replace(r"\\", "")
    page = page.replace(r"\ ", "")
    #print "\t\t" + page[:10]

    soup = BeautifulSoup(page)
    reviewBlocks = soup.select("div.friendReviews");

    count = 0

    for i in range(len(reviewBlocks)):
        starNode = reviewBlocks[i].select("a.staticStars")
        reviewNode = reviewBlocks[i].select("div.reviewText > span > span")
        likeNode = reviewBlocks[i].select("div.reviewFooter > div > div > span > a")
        if len(reviewNode) > 0 and len(starNode) > 0:# and len(likeNode) > 1:
            count = count + 1
            star = int(starNode[0].getText().replace(ratingConcatString, ""))
            stars.append(star)
            if (len(reviewNode) > 1):
               reviews.append(reviewNode[1].getText().replace("(less)", ""))
            else:
               reviews.append(reviewNode[0].getText().replace("...more", ""))
               #print reviewNode[0].getText().replace("...more", "")
            
            if len(likeNode) > 1:
               like = likeNode[1].getText().replace(likeConcatStringPlural, "")  \
                         .replace(likeConcatStringSingular, "")
            else:
               like = "0"
            like = int(like)
            totalLikes += like
            likes.append(like)
            totalRating += star

    if debugPrint:
        print "Found " + str(count) + " reviews."
        print "  Only " + str(len(stars)) + " = " + str(len(reviews)) + " = "   \
            + str(len(likes)) + " selected."

        for i in range(len(stars)):
            print str(stars[i]) + " | " + reviews[i][0:10] + "... | " + str(likes[i])

    print "\t\t" + str(count)
    totalcount = totalcount + count

output = open(path + sourcename + "." + str(id_) + ".txt", "wb")
pickle.dump({"stars" : stars, "reviews": reviews, "likes": likes, "totalLikes": totalLikes, "totalRating": totalRating, "totalCount": totalcount}, output)
output.close()

if debugShowOutput :
    input_ = open(path + sourcename + "." + str(id_) + ".txt", "rb")
    data = pickle.load(input_)
    pprint.pprint(data)
    input_.close()

print "Total count: " + str(totalcount)
print "Total rating: " + str(totalRating)
print "Total likes: " + str(totalLikes)
print "Avg. rating: " + str(totalRating * 1.0 / totalcount)
print "Avg. likes: " + str(totalLikes * 1.0 / totalcount)
