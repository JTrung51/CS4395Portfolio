import math
import pickle
import nltk
from nltk import word_tokenize, ngrams


def NgramProbModel(fileName, outFile):
    # Open all the pickled dicts
    bigramE = pickle.load(open('bigrams-English.txt', 'rb'))
    unigramE = pickle.load(open('unigrams-English.txt', 'rb'))
    bigramF = pickle.load(open('bigrams-French.txt', 'rb'))
    unigramF = pickle.load(open('unigrams-French.txt', 'rb'))
    bigramI = pickle.load(open('bigrams-Italian.txt', 'rb'))
    unigramI = pickle.load(open('unigrams-French.txt', 'rb'))

    # Gets the len of all the unigram and adds it for calcuataion
    VE = len(unigramE)
    VF = len(unigramF)
    VI = len(unigramI)
    V = VE + VF + VI
    i = 1
    list = []

    # Compute the most accuracy language for each line in filename
    with open(fileName, encoding='utf8') as f:
        for line in f:
            print("Line " + str(i), end=' ')

            # Computes probabilities
            GE, LE = compute_prob(line, unigramE, bigramE, V)
            GF, LF = compute_prob(line, bigramF, bigramF, V)
            GI, LI = compute_prob(line, unigramI, bigramI, V)

            # Output logic for most accurate Language for the line
            if LE > LF and LE > LI:
                list.append("English")
                print("English")
                print("Laplace Smoothing = %.100f" % LE)
            elif LF > LE and LF > LI:
                list.append("French")
                print("French")
                print("Laplace Smoothing = %.100f" % LE)
            elif LI > LF and LI > LE:
                list.append("Italian")
                print("Italian")
                print("Laplace Smoothing = %.100f" % LE)
            else:
                list.append("None")
                print("Results are ambiguoius")
            print()
            i = i + 1
    # Output the total accuracy and incorrect lines
    with open(outFile, encoding='utf8') as f:
        total = 0
        incorrect = []
        for line in f:
            if not list[total] in line:
                incorrect.append(total + 1)
            total = total + 1

        print("Accuracy: %.3f" % ((total - len(incorrect)) / total))
        print("Incorrect Lines")
        for line in incorrect:
            print("Line " + str(line))

# Computing the probabilities using Good-Turning and Laplace Smoothing
def compute_prob(text, unigram_dict, bigram_dict, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)
    N = 0
    for i in unigram_dict:
        N = N + unigram_dict[i]

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_gt = 1  # calculate p using a variation of Good-Turing smoothing
    p_laplace = 1  # calculate p using Laplace smoothing

    # Loop bigram by bigram calcuating the probability
    for bigram in bigrams_test:
        n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1 / N
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        if d != 0:
            p_gt = p_gt * (n_gt / d)
        else:
            p_gt = p_gt * (1 / N)
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_gt, p_laplace


if __name__ == '__main__':
    NgramProbModel("LangId.test", "LangId.sol")
    print("DONE!")
