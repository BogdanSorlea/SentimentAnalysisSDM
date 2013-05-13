# Import python 3.0 behaviour so division does not truncate reminder when dividing integers.
from __future__ import division
import matplotlib.pyplot as plt
import csv
import pickle
from pylab import polyfit, poly1d

def loadLabMT(path):
    """ Load labMT file into a dictionary.
    """
    happiness = {}
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        # Skip first lines that contain only column names and such.
        for _ in range(4):
            reader.next()
        for row in reader:
            happiness[row[0]] = float(row[2])
    return happiness

def getSentiment(text, labMT):
    """ Return sentiment of the text by calculating average happiness. Words are split on whitespace which
    might not work in some cases.

    text = string containing the text
    labMT = dictionary mapping words(lowercase) to happiness rating
    """
    score, matches = 0, 0
    for word in text.lower().split():
        if word in labMT:
            score = score + labMT[word]
            matches += 1
    return score / matches if matches > 0 else None


def sentimentRankingComparison(reviews, labMT):
    """ Return a tuple: ((ratings), (sentiment)) computed for over all reviews. Just plug into pyplot.
    reviews = a list of tuples: (review string, rating)
    labMT = dictionary mapping words(lowercase) to happiness rating
    """
    sentimentSum = {}
    matches = {}
    for entry in reviews:
        sentiment = getSentiment(entry[0], labMT)
        if sentiment is None:
            continue
        rating = entry[1]
        matches[rating] = matches.get(rating, 0) + 1
        sentimentSum[rating] = sentimentSum.get(rating, 0) + sentiment
    ratingAndSentiment = [(rating, sentSum / matches[rating]) for rating, sentSum in sentimentSum.iteritems()]
    # Keys might have been unsorted.
    sortedByRating = sorted(ratingAndSentiment, key= lambda (t): t[0])
    # We have a list of (rating, sentiment) but for pyplot we want two lists - of ratings and of sentiment.
    return zip(*sortedByRating)


def analyse(reviews, labMTPath, saveResultToPath):
    """ Analyse the sentiment vs ranking and save the result into fileName path.
    reviews = list of (review, ranking) tuples
    labMTPath = path to labMT file
    saveResultToPath = save the result to this file
    """
    result = sentimentRankingComparison(reviews, loadLabMT(labMTPath))
    with open(saveResultToPath, "wb") as f:
        pickle.dump(result, f)


def visualise(fileName, title="", linearFit=False):
    """ Draw graph representing the result. A bit verbose as that seem to be the only way to make borders gray.
    fileName = path and name of the pickled results
    """
    with open(fileName, "rb") as f:
        data = pickle.load(f)
        fig = plt.figure()
        p = fig.add_subplot(111)
        if not linearFit:
            p.plot(data[0], data[1], 'bo-', label="sentiment")
            p.plot([data[0][0], data[0][-1]], [data[1][0], data[1][-1]],
                   'g', label="straight line through first and last point")
        else:
            fit = polyfit(data[0], data[1], 1)
            fitFunc = poly1d(fit)
            p.plot(data[0], data[1], 'ro', label='sentiment')
            p.plot(data[0], fitFunc(data[0]), "--k", label="linear fit")
        p.legend(prop={'size': 10}, frameon=False)
        plt.ylabel("Average happiness")
        plt.xlabel("Rating")
        for e in ['bottom', 'top', 'left', 'right']:
            p.spines[e].set_color('gray')
        if title:
            plt.title(title)
        plt.show()




