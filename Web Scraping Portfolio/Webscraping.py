import pickle
from os import listdir

from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# Gets all the urls using a web crawler in the parameter that are related to arcane
def getURLfromWeb(_url):
    r = requests.get(_url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    counter = 0

    # Write urls in the urls.txt
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            # Check if the link is related to arcane
            if 'Arcane' in link_str or 'arcane' in link_str or 'legends' in link_str:
                if link_str.startswith('http') and 'google' not in link_str:
                    f.write(link_str + "\n")
                    counter = counter + 1
            if counter > 30:
                break


# Filter the hltm if it is text
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# Web Scrape all of the urls within the urls.txt text.
def addressToText():
    urls = []
    # Store the urls in a list for easier access
    with open('urls.txt', 'r') as f:
        for line in f.readlines():
            urls.append(line)

    # Visit each url and Receive all that text
    for url in urls:
        # Visit with a request to avoid a error
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # Catches the expection if the website blocks webscaping
        try:
            # Reads the raw html code
            html = urlopen(req).read()
            soup = BeautifulSoup(html)
            data = soup.findAll(text=True)
            result = filter(visible, data)
            temp_list = list(result)  # list from filter

            # Store the all of the words from the list
            temp_str = ' '.join(temp_list)

            # Write text in the textfile
            with open('WebPageText\\' + re.sub(r'\W+', '', url) + '.txt', 'w', encoding="utf-8") as f:
                f.write(temp_str)
        except:
            print("Website close the website")


# Cleans up the text, removing all new lines and tabs and split the text by the sentences
def cleanUpText():
    for address in listdir('WebPageText'):
        with open("WebPageText\\" + address, 'r', encoding="utf-8") as f:
            text = f.read()
        # Remove all newlines and tabs on the text
        text = text.replace("\n", "")
        text = text.replace("\t", "")

        # Split the text by sentences
        sents = sent_tokenize(text)
        with open("WebPageSentences\\" + address, 'w', encoding="utf-8") as f:
            for sen in sents:
                f.write(sen + "\n")


# Get the 30 most common words out of all of the website
def extractTerms():
    counts = {}
    for address in listdir('WebPageSentences'):
        with open("WebPageSentences\\" + address, 'r', encoding="utf-8") as f:
            text = f.read()
            # Tokenize each word and stores into list
            tokens = word_tokenize(text)
            # Remove all stopwords, number and lower cases them
            tokens = [t.lower() for t in tokens]
            tokens = [t for t in tokens if t.isalpha() and
                      t not in stopwords.words('english')]
            setToken = set(tokens)

            # Creates a dict of every word
            for t in setToken:
                if t in counts:
                    counts[t] = counts[t] + tokens.count(t)
                else:
                    counts[t] = tokens.count(t)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("\n50 most common words in all pages:")
    for i in range(50):
        print(sorted_counts[i])


# Create the pickle with the filter sentences
def makePickle():
    # Manunl list of all the word for filtering
    topList = ["arcane", "league", "animated", "riot", "vi", "jinx", "piltover", "jayce", "silco", "zaun"]
    # Initized the dict
    knowledgeBase = {i: list() for i in topList}
    for address in listdir('WebPageSentences'):
        with open("WebPageSentences\\" + address, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                # Check if the sentence contains one of the words.
                res = [ele for ele in topList if (ele in line.lower())]
                if bool(res):
                    knowledgeBase[str(res[0])].append(line)
    pickle.dump(knowledgeBase, open('knowledgeBase.p', 'wb'))



# getURLfromWeb("https://en.wikipedia.org/wiki/Arcane_(TV_series)")
# addressToText()
# cleanUpText()
# extractTerms()
makePickle()
# readPickle()
