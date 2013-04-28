import sentiment
import json

# sentiment.analyse expects a list of (review string, rating) tuples.
# This example uses academic dataset https://www.yelp.com/academic_dataset
# It's around 200 mb so I won't be uploading it to github.

labMTPath = "happiness.txt"
yelp = "..\Yelp\yelp_phoenix_academic_dataset\yelp_academic_dataset_review.json"

def loadYelpData(path):
    reviews = []
    with open(path, "r") as f:
        for line in f:
            dict = json.loads(line)
            reviews += [(dict["text"], float(dict["stars"]))]
    return reviews

sentiment.analyse(loadYelpData(yelp), labMTPath, "yelpSentiment.pkl")
sentiment.visualise('yelpSentiment.pkl')