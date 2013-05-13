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


def wholeTextSentiment(fileNames, years, labMTPath, outPath):
    """
    Calculate sentiment in a given year.
    fileNames = a list of fileNames containing pickled reviews
    years = a sorted ascending list of years with len equal to that of fileNames
    outPath = path where pickled result will be saved
    """
    print years
    sentiment = []
    labMT = loadLabMT(labMTPath)
    for i in range(len(fileNames)):
        with open(fileNames[i], "rb") as f:
            reviews = pickle.load(f)
            wholeText = " ".join([entry[0] for entry in reviews])
            sentiment += [getSentiment(wholeText, labMT)]
    with open(outPath, "wb") as f:
        pickle.dump((years, sentiment), f)


def ratingFrequency(reviews, outPath):
    """
    Calculate the total number of reviews for a given rating.
    reviews = list of review tuples
    outPath = path where pickled result will be saved.
    """
    freq = {}
    for r in reviews:
        rating = r[1]
        freq[rating] = freq.get(rating, 0) + 1
    data = zip(*freq.iteritems())
    with open(outPath, "wb") as f:
        pickle.dump(data, f)


def visualiseFrequency(picklePath, title= ""):
    """
    Visualise the result of ratingFrequency function.
    """
    with open(picklePath, "rb") as f:
        data = pickle.load(f)
        fig = plt.figure()
        p = fig.add_subplot(111)
        p.bar(data[0], data[1], align='center', color='red')
        plt.xlim([min(data[0])-1, max(data[0])+1])
        plt.ylabel("Number of reviews")
        plt.xlabel("Rating")
        for e in ['bottom', 'top', 'left', 'right']:
            p.spines[e].set_color('gray')
        if title:
            plt.title(title)
        plt.show()


def visualiseYears(picklePath, title=""):
    """
    Visualise the result of wholeTextSentiment function.
    """
    with open(picklePath, "rb") as f:
        data = pickle.load(f)
        fig = plt.figure()
        p = fig.add_subplot(111)
        p.plot(data[0], data[1], 'bo-', label="sentiment")
        p.legend(prop={'size': 10}, frameon=False)
        plt.ylabel("Average happiness")
        plt.xlabel("Year")
        for e in ['bottom', 'top', 'left', 'right']:
            p.spines[e].set_color('gray')
        if title:
            plt.title(title)
        plt.show()


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


def visualise(fileName, title="", linearFit=False, polyFit=True):
    """ Draw graph representing the result. A bit verbose as that seem to be the only way to make borders gray.
    fileName = path and name of the pickled results
    """
    with open(fileName, "rb") as f:
        data = pickle.load(f)
        fig = plt.figure()
        p = fig.add_subplot(111)
        if not linearFit and not polyfit:
            p.plot(data[0], data[1], 'bo-', label="sentiment")
            p.plot([data[0][0], data[0][-1]], [data[1][0], data[1][-1]],
                   'g', label="straight line through first and last point")
        elif linearFit:
            fit = polyfit(data[0], data[1], 1)
            fitFunc = poly1d(fit)
            p.plot(data[0], data[1], '-ro', label='sentiment')
            p.plot(data[0], fitFunc(data[0]), "--k", label="linear fit")
        elif polyFit:
            fit = polyfit(data[0], data[1], 2)
            f = [d*d*fit[0] + d*fit[1] + fit[2] for d in data[0]]
            p.plot(data[0], data[1], '-ro', label='sentiment')
            p.plot(data[0], f, "--k", label="polynomial fit")
        p.legend(prop={'size': 10}, frameon=False)
        plt.ylabel("Average happiness")
        plt.xlabel("Rating")
        for e in ['bottom', 'top', 'left', 'right']:
            p.spines[e].set_color('gray')
        if title:
            plt.title(title)
        plt.show()


def visualiseCombined(fileNames, labels, title=""):
    """ Draw graph representing combined results.
    fileNames = list of paths to pickled results
    """
    fig = plt.figure()
    p = fig.add_subplot(111)
    for i in range(len(fileNames)):
        data = normalizeDataFrom(fileNames[i])
        p.plot(data[0], data[1], label=labels[i])
    p.legend(prop={'size': 10}, frameon=False)
    plt.ylabel("Average happiness")
    plt.xlabel("Rating")
    for e in ['bottom', 'top', 'left', 'right']:
        p.spines[e].set_color('gray')
    if title:
        plt.title(title)
    plt.show()


def normalizeDataFrom(fileName):
    with open(fileName, "rb") as f:
        data = pickle.load(f)
        newData = []
        print data
        if len(data[0]) > 5:
            averages = [(data[1][i*2]+data[1][i*2+1])/2 for i in range(5)]
            newData = [range(1,6), averages]
            print newData
        else:
            newData = data
        return newData

