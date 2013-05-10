import re
import math
import pickle
import pprint

def getparts(doc):
    splitter = re.compile('[ \t]*')
    #split the words
    words = [s.lower() for s in splitter.split(doc)]
    #return dictionary
    return words

datapath = "../data/"
labMTsource = "labMT"
labMTsourceExtension = ".txt"
limit = 100

debugMode = False
debugResult = False

input_ = open(datapath + labMTsource + ".original" + labMTsourceExtension, "rb")

count = 0
MTdata = []

for line in input_:
    count += 1
    if count == limit and debugMode:
        break
    if count % 100 == 0:
        print count
    parts = getparts(line)
    MTdata.append((parts[0], float(parts[2])))
    #dict([(w, 1) for w in words])

input_.close()

MTdata = dict([elem for elem in MTdata])
    
output = open(datapath + labMTsource + ".pickled" + labMTsourceExtension, "wb")
pickle.dump(MTdata, output)
output.close()

if debugResult:
    input_ = open(datapath + labMTsource + ".pickled" + labMTsourceExtension, "rb")
    data = pickle.load(input_)
    pprint.pprint(data)
    input_.close()

i = 0
MTtrain = []
MTvalidation = []

for key in MTdata.keys():
    if i == 9:
        MTvalidation.append((key, MTdata[key]))
    else:
        MTtrain.append((key, MTdata[key]))
    i = (i+1) % 10

MTvalidation = dict([elem for elem in MTvalidation])
MTtrain = dict([elem for elem in MTtrain])
MTdata = {"training" : MTtrain, "validation" : MTvalidation}


output = open(datapath + labMTsource + ".picksplit" + labMTsourceExtension, "wb")
pickle.dump(MTdata, output)
output.close()

if debugResult:
    input_ = open(datapath + labMTsource + ".picksplit" + labMTsourceExtension, "rb")
    data = pickle.load(input_)
    pprint.pprint(data)
    input_.close()
