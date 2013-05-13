import re
import math
import pickle
import pprint

datapath = "../../data/"
labMTsource = "labMT"
labMTsourceExtension = ".txt"

#reviewDataSourceFile = "goodreads.13496"
reviewDataSourceFile = "goodreads.20130510"

def normalizeSentiment(sentiment):
    min = 1.0
    max = 9.0
    return (sentiment - min) / (max - min)

def normalizeRating(rating):
    min = 1.0
    max = 5.0
    return (rating - min) / (max - min)

def toSentiment(rating):
    A = 1
    B = 0
    #A = 0.025
    #B = 5.355
    return float(A * rating + B)

def getwords(doc):
    splitter = re.compile('\\W*')
    #split the words
    words = [s.lower() for s in splitter.split(doc)
                 if len(s) > 2 and len(s) < 20]
    return dict([(w, 1) for w in words])

input_ = open(datapath + "stopwords" + labMTsourceExtension, "rb")
stopData = dict([(w.replace("\r\n", ""), 1) for w in input_.readlines()])
#pprint.pprint(stopData)
input_.close();

input_ = open(datapath + labMTsource + ".picksplit" + labMTsourceExtension, "rb")
MTdata = pickle.load(input_)
#pprint.pprint(MTdata["validation"]["necessity"])
input_.close()

input_ = open(datapath + reviewDataSourceFile + labMTsourceExtension, "rb")
TXTdata = pickle.load(input_)
#pprint.pprint(TXTdata)
input_.close()

#stars,reviews
lim = 0
setLimit = False

newwords = {}

for i in range(len(TXTdata["reviews"])):

    if TXTdata["stars"][i] == 1:
        continue
    
    if setLimit and lim == 100:
        break
    else:
        lim += 1

    print "Review " + str(i) + " ========================="
        
    #print(TXTdata["reviews"][i].replace("...more", ""))
    words = getwords(TXTdata["reviews"][i].replace("...more", ""))
    countNew = 0
    totalRelevant = len(words)
    #rating = TXTdata["stars"][i] * len(words)
    rating = 1.0

    notfound = []
    
    for key in words.keys():
        if key in stopData:
            totalRelevant -= 1
            continue
        elif key in MTdata["training"].keys():
            rating *= normalizeSentiment(MTdata["training"][key])
            #print "F - " + str(MTdata["training"][key]) + " | " \
            #      + str(normalizeSentiment(MTdata["training"][key]))    \
            #      + " | " + key
        else:
            countNew += 1
            notfound.append(key)
            #print "N - " + key
    #print "----- " + str(TXTdata["stars"][i]) + " star(s)"
    #print "----- " + str(toSentiment(normalizeRating(TXTdata["stars"][i])))
    #print "----- " + str(pow(toSentiment(normalizeRating(TXTdata["stars"][i])), totalRelevant))
    if countNew == 0:
        continue
    tmp = rating
    #print "----- " + str(tmp)
    rating = pow(toSentiment(normalizeRating(TXTdata["stars"][i])), totalRelevant)
    rating /= tmp
    rating = math.pow(rating, 1/float(countNew))
    #print rating

    #some cases exist where the rating for each of the new words is not in range
    if rating > 1 or rating < 0:
        continue

    print "Rating for not found: " + str(rating)
    print "Total words | relevant | new :: " + str(len(words)) + " | " + \
          str(totalRelevant) + " | " + str(countNew)

    for j in range(len(notfound)):
        newwords.setdefault(notfound[j], {"sentiment" : 0, "hits" : 0})
        newwords[notfound[j]]["sentiment"] += rating
        newwords[notfound[j]]["hits"] += 1

print "NEWWORDS ========"
print "======== ========"
for key in newwords.keys():
    print key + "   ::   " + str(newwords[key]["sentiment"])

print " VERIFY  ========"
print "======== ========"
print "key :: hits :: computed_sentiment :: labMT sentiment"
print "======== ========"
newwords_sorted_keys = sorted(newwords.keys(), key=lambda y: (newwords[y]['hits']))
for key in newwords_sorted_keys:
    if key in MTdata["validation"].keys():
        print key + "  ::  " + str(newwords[key]["hits"]) + "  ::   "    \
            + str(newwords[key]["sentiment"] / newwords[key]["hits"]) \
            + "   ::   "    \
            + str(normalizeSentiment(MTdata["validation"][key]))
    
            
