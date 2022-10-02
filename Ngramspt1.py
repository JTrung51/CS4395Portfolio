import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle


def inputData(file):
    print("Processing data file: ", file)
    with open(file, encoding='utf8') as f:
        raw_text = f.readlines()
        f.close()

    # convert raw_text from [str] to str, grab unigrams and bigrams from raw_string
    raw_string = " ".join(raw_text)

    print("Creating Ngrams")
    unigrams = word_tokenize(raw_string)
    bigrams = list(ngrams(unigrams, 2))

    # take the uni and bigrams and count each unique unigram and bigram and for mat it as a dict
    print("Creating Dictionaries")
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict


def pickleDicts(dictTuple, file):
    print("Pickling Dicts for ", file)

    uni_dict = dictTuple[0]
    bi_dict = dictTuple[1]

    fileName = file[file.rfind("/") + 1:]
    uniLabel = 'unigrams-' + fileName
    biLabel = 'bigrams-' + fileName

    pickle.dump(uni_dict, open(uniLabel, 'wb'))
    pickle.dump(bi_dict, open(biLabel, 'wb'))


if __name__ == '__main__':
    for x in range(3):
        file = input("Please Input a File Name: ")
        data = inputData(file)
        pickleDicts(data, file)
    print("DONE!")
