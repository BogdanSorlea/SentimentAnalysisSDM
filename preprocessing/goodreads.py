import urllib2
import math
from bs4 import BeautifulSoup
import zlib
import pprint
import pickle
from datetime import datetime

path = "../data/"
sourcename = "goodreads"

domain = "https://www.goodreads.com"
#book_url = "/book/show/1049153.History_of_Religious_Ideas_Volume_1"

# if you add more books, look on Goodreads for Epic Fantasy, past page 12 of the listing
book_url = ["/book/show/1215032.The_Wise_Man_s_Fear",
            "/book/show/15241.The_Two_Towers",
            "/book/show/5907.The_Hobbit",
            "/book/show/34.The_Fellowship_of_the_Ring",
            "/book/show/228665.The_Eye_of_the_World",
            "/book/show/186074.The_Name_of_the_Wind",
            "/book/show/233649.The_Great_Hunt",
            "/book/show/13496.A_Game_of_Thrones",
            "/book/show/10572.A_Clash_of_Kings",
            "/book/show/62291.A_Storm_of_Swords",
            "/book/show/768889.A_Storm_of_Swords",
            "/book/show/13497.A_Feast_for_Crows",
            "/book/show/9539.The_Shadow_Rising",
            "/book/show/34897.The_Dragon_Reborn",
            "/book/show/18512.The_Return_of_the_King",
            "/book/show/761732.Soul_of_the_Fire",
            "/book/show/2248573.Brisingr",
            "/book/show/153008.Kushiel_s_Dart",
            "/book/show/45112.Assassin_s_Quest",
            "/book/show/44659.Pawn_of_Prophecy",
            "/book/show/91981.The_Dragonbone_Chair",
            "/book/show/29396.Furies_of_Calderon",
            "/book/show/7332.The_Silmarillion",
            "/book/show/253058.Temple_of_the_Winds",
            "/book/show/55399.Gardens_of_the_Moon",
            "/book/show/68429.The_Well_of_Ascension",
            "/book/show/1166599.The_Gathering_Storm",
            "/book/show/43889.Wizard_s_First_Rule",
            "/book/show/47959.Queen_of_the_Darkness",
            "/book/show/13927.Son_of_the_Shadows",
            "/book/show/13994.Winds_of_Fury",
            "/book/show/28187.The_Lightning_Thief",
            "/book/show/249633.Medalon",
            "/book/show/34897.The_Dragon_Reborn",
            "/book/show/242793.The_World_of_Robert_Jordan_s_The_Wheel_of_Time",
            "/book/show/448873.The_Thief",
            "/book/show/185292.The_Ruins_of_Ambrai",
            "/book/show/29137.The_Baker_s_Boy",
            "/book/show/36157.Feast_of_Souls",
            "/book/show/176797.The_Oathbound",
            "/book/show/28247.Voice_of_the_Gods",
            "/book/show/28246.Last_of_the_Wilds",
            "/book/show/2408602.The_Red_Wolf_Conspiracy",
            "/book/show/400924.Chronicles_of_the_Black_Company",
            "/book/show/2120932.The_Battle_of_the_Labyrinth",
            "/book/show/147842.The_High_King_s_Tomb",
            "/book/show/15550.Straken",
            "/book/show/74274.Hidden_Warrior",
            "/book/show/13925.Child_of_the_Prophecy",
            "/book/show/13836.Wild_Magic",
            "/book/show/13834.The_Realms_of_the_Gods",
            "/book/show/77366.The_Hero_and_the_Crown",
            "/book/show/28514.Dragons_of_a_Vanished_Moon",
            "/book/show/537124.Deryni_Rising",
            "/book/show/153785.Page",
            "/book/show/7347.The_Book_of_Lost_Tales_Part_One",
            "/book/show/2015492.Empress",
            "/book/show/47953.The_Black_Jewels_Trilogy",
            "/book/show/19821.Riddle_Master",
            "/book/show/111023.Passage_to_Dawn",
            "/book/show/1170158.The_Earthsea_Trilogy",
            "/book/show/780866.Requiem_for_the_Sun",
            "/book/show/68041.The_Earthsea_Quartet",
            "/book/show/104085.A_Song_for_Arbonne",
            "/book/show/13814.Into_a_Dark_Realm",
            "/book/show/4407.American_Gods",
            "/book/show/60154.The_Sailor_on_the_Seas_of_Fate",
            "/book/show/44689.The_Rivan_Codex",
            "/book/show/28541.Dragonsong"
            ]

stars = []
reviews = []
likes = []
ratingConcatString = " of 5 stars"
likeConcatStringSingular = " like"
likeConcatStringPlural = " likes"
noOfItemsDelimiter = "of";
itemsPerPage = 30.0;

debugPrint = False
debugShowOutput = False

totalcount = 0
totalRating = 0
totalLikes = 0

for i_url in range(0, len(book_url)):

   url = domain + book_url[i_url]
   id_ = book_url[i_url].replace("/book/show/", "")
   id_ = int(id_[ : id_.find(".")])

   initPage = urllib2.urlopen(url)
   soup = BeautifulSoup(initPage)

   #noOfPages = soup.select("#reviews > div")# > div > a");
   #noOfPages = noOfPages[0].select("span")[0].getText().replace(")", "").replace(",", "")
   #noOfPages = noOfPages[noOfPages.find(noOfItemsDelimiter) + 3 : len(noOfPages) - 1]
   #noOfPages = int(noOfPages)
   #print "Total reviews count: " + str(noOfPages)
   #print "Page count: " + str(int(math.ceil(noOfPages / itemsPerPage)))

   #pageCount = int(math.ceil(noOfPages / itemsPerPage))

   try:
      asynchURL = soup.select("#reviews > div")[3].select("div a")[0].get("onclick")
      #print asynchURL
      securityToken = asynchURL
      asynchURL = asynchURL.replace("new Ajax.Request('", "")
      asynchURL = asynchURL[ : asynchURL.find("{asynchronous:true") - 4]
      securityToken = securityToken[securityToken.find("encodeURIComponent('") + len("encodeURIComponent('") : ]
      securityToken = securityToken[ : len(securityToken) - len("')}); return false;")]
      #print securityToken
      #exit()
   except:
      continue

   #if pageCount > 100:
   #   pageCount = 100      # limit to 100 as to avoing creating files that are too big

   #pageCount = 2       # just for testing purposes

   pageCount = 1

   for i in range(1, 100):
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

       if count == 0:
         break
       else:
         pageCount += 1

       print "\t\t" + str(count)
       totalcount = totalcount + count

#datetime = datetime.now()

output = open(path + sourcename + "." + "20130511" + ".txt", "wb")
pickle.dump({"stars" : stars, "reviews": reviews, "likes": likes, "totalLikes": totalLikes, "totalRating": totalRating, "totalCount": totalcount}, output)
output.close()

input_ = open(path + sourcename + "." + "20130511" + ".txt", "rb")
data = pickle.load(input_)
if debugShowOutput :
   pprint.pprint(data)

print str(len(data["stars"])) + " :: " + str(len(data["reviews"])) + " :: " + str(len(data["likes"]))
input_.close()

print "Total count: " + str(totalcount)
print "Total rating: " + str(totalRating)
print "Total likes: " + str(totalLikes)
print "Avg. rating: " + str(totalRating * 1.0 / totalcount)
print "Avg. likes: " + str(totalLikes * 1.0 / totalcount)
