import sentiment
import json
import pickle

# sentiment.analyse expects a list of (review string, rating) tuples.
# This example uses academic dataset https://www.yelp.com/academic_dataset
# It's around 200 mb so I won't be uploading it to github.

labMTPath = "happiness.txt"
grPath = "../../data/goodreads.20130510.txt"

def loadYelpData(path):
    reviews = []
    with open(path, "r") as f:
        for line in f:
            dict = json.loads(line)
            reviews += [(dict["text"], float(dict["stars"]))]
    return reviews

def loadGoodreadsData(path):
    reviews = []
    input_ = open(path, "rb")
    data = pickle.load(input_)
    for i in range(len(data["stars"])):
        reviews += [(data["reviews"][i], data["stars"][i])]
    return reviews

data = loadGoodreadsData(grPath)

#print data

sentiment.analyse(data, labMTPath, "goodreadsSentiment.pkl")
sentiment.visualise('goodreadsSentiment.pkl')
