# This is a sample Python script.
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sys
import os
import itertools
from random import seed
from random import randint


# Method to open txt file, process the data within, and return the 50 most common words in the txt
def readFile(fp):
    alist = []

    # Opens according to filepath and type of os
    with open(os.path.join(os.getcwd(), fp), 'r') as f:
        # Store every token into list
        wordList = [word for line in f for word in line.split()]
        wordSet = set(wordList)
        print("\nLexical diversity: %.2f" % (len(wordSet) / len(wordList)))
        # Process the wordList according the requirements
        wordList, nounList = rawFile(wordList)
        wordSet = set(wordList)
        print("\nLexical diversity after data processing: %.2f\n" % (len(wordSet) / len(wordList)))
        dictList = {}
        # Creates a dict for every noun in nounlist and stores the count of the noun as the value
        for word in nounList:
            dictList[word] = wordList.count(word)
        # Sorts the dict from descending value
        dictList = {k: v for k, v in sorted(dictList.items(), key=lambda item: item[1], reverse=True)}
        # Prep to print top 50 in dict
        out = dict(itertools.islice(dictList.items(), 50))
        print("50 most common words in file")
        alist = []
        for key in out.keys():
            alist.append(key)
            print(key + " " + str(out.get(key)))
        print("\n")
    f.close()
    return alist


def rawFile(wordList):
    wnl = WordNetLemmatizer()
    # Add to lowercase words to the list if the word is a word, not a stopword and haves a length > 5
    wordList = [t.lower() for t in wordList if t.isalpha() and
                t not in stopwords.words('english') and len(t) > 5]
    # Lemmatize the words in the list
    tempWordList = [wnl.lemmatize(t) for t in wordList]
    wordSet = set(tempWordList)
    # Creates tag list from Lemmaitzed list
    tags = nltk.pos_tag(nltk.word_tokenize(' '.join(tempWordList)))
    [print(i, end='\n') for i in tags[:20]]
    # Creates a list with the tags NN
    nounList = [token for token, tag in tags if tag == 'NN']
    print("Number of words:" + str(len(wordList)) + "\nNumber of Nouns: " + str(len(nounList)))
    return wordList, nounList


def guessingGame(wordList):
    seed(1234)
    # Variable Sets for score, word to guess, a list to of guessed letters, and the list of foamed word
    currentScore = 5
    guessWord = wordList[randint(0, 50)]
    guessList = []
    listGuess = ['_'] * len(guessWord)
    print("Let\'s play a word guessing game!")
    # Output the list of foamed word
    [print(i, end=' ') for i in listGuess]
    print()
    # Loop till break requirements are meant, score < 0 or currGuess == !
    while True:
        currGuess = input("Guess a letter: ")
        # check if users wants to quit game
        if currGuess == '!':
            print("You Quit the Game with a score of " + str(currentScore))
            break
        # check if guess is a valid guess
        if currGuess == "" or not currGuess.isalpha() or len(currGuess) > 1:
            print(currGuess + " is not a valid answer")
            continue
        # check if guess was already guess before
        if currGuess in guessList:
            print("You have already guess this letter, try again.")
            continue

        guessList.append(currGuess)
        # If letter is in the word
        if currGuess in guessWord:
            index = -1
            # Loop to get all letters in the words and adds score accordingly
            while currGuess in guessWord[index + 1:]:
                index = guessWord.index(currGuess, index + 1)
                listGuess[index] = currGuess
                currentScore = currentScore + 1
            print("Right! Score is " + str(currentScore))
            [print(i, end=' ') for i in listGuess]
            print()
        # If letter is not in the word
        else:
            currentScore = currentScore - 1
            # Check if score is negative to quit game
            if currentScore < 0:
                print("You have a negative score, therefore you failed to guess the word. The word was " + str(
                    guessWord) + "\nQuiting Game.")
                break

            print("Sorry, guess again. Score is " + str(currentScore))
            [print(i, end=' ') for i in listGuess]
            print()
        # Check if word has been guessed
        if not '_' in listGuess:
            guessList = []
            print("You solved it!")
            print("\nCurrent score: " + str(currentScore))
            print("\nGuess another word")
            # Creates new word
            guessWord = wordList[randint(0, 50)]
            listGuess = ['_'] * len(guessWord)
            [print(i, end=' ') for i in listGuess]


def main():
    # Check if arguments exist
    if len(sys.argv) < 2:
        print("No arguments in command, quiting program...")
    else:
        fp = sys.argv[1]
        # Check if file exist
        if os.path.isfile(fp):
            commonWordList = readFile(fp)
            guessingGame(commonWordList)
        else:
            print("File doesnt exist")


main()
