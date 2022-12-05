import pickle
import random
import re
from nltk.corpus import wordnet as wn
import logging
from allennlp.predictors.predictor import Predictor
import time
from termcolor import colored


class ChatBot:
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "stop")
    anything_commands = ("anything", "whatever", "care", "surprise", "random", "any")

    userName = ""
    userKnowledgeDict = {}
    userKnowledge = []

    altJQuestion = []
    JQuestion = []
    JsecondQuestion = []
    jokeDatabase = {}
    endPharse = {}
    predictor = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")

    # Open up text and store every line in a list
    def openTxt(self, file):
        list = []
        with open(file, encoding='utf8') as f:
            for line in f:
                list.append(line.replace("\n", ""))
        return list

    # Setup for chatbot, loading all the databases
    def setUp(self):
        self.JsecondQuestion = self.openTxt("JsecondQuestion.txt")
        self.altJQuestion = self.openTxt("altJQuestion.txt")
        self.JQuestion = self.openTxt("JQuestion.txt")
        self.jokeDatabase = pickle.load(open('jokeData.p', 'rb'))
        self.endPharse = self.openTxt(" endPharse.txt")

    def start(self):
        self.setUp()
        # opening up user knowledgebase
        userKnowledgeDict = pickle.load(open('knowledgeBase.p', 'rb'))
        # Chat bot greetings
        user_response = input(
            colored('Jokebot',
                    'red') + ": Hello there! I'm a humor chatbot trained on a Kaggle dataset, first off, what is your name?\n")
        if user_response in self.exit_commands:
            print(colored('Jokebot', 'red') + ": Ok, have a great day!")
            return
        self.userName = user_response
        # Check if user is new or old
        if user_response not in userKnowledgeDict:
            userKnowledgeDict[user_response] = []
        self.userKnowledge = userKnowledgeDict[user_response]

        self.chat()

    # Output random joke from word using the jokeDatabase
    def jokeKeyword(self, word):
        print(colored('Jokebot', 'red') + ": " + self.jokeDatabase[word][
            random.randint(0, len(self.jokeDatabase[word]) - 1)])
        self.userKnowledge.append(word)

    # Output random joke from user history
    def jokeAlt(self):
        if len(self.userKnowledge) > 2:
            txt = "\n" + colored('Jokebot', 'red') + ": " + self.altJQuestion[
                random.randint(0, len(self.altJQuestion) - 1)] + "\n" + colored(self.userName, 'blue') + ": "
            jokeBase = self.userKnowledge[random.randint(0, len(self.userKnowledge) - 1)]
            userResponse = input(txt.format(jokeBase))  # ask if they want to hear a joke base on knowledge
            if userResponse not in self.negative_responses and userResponse not in self.exit_commands:
                self.jokeKeyword(jokeBase)

                return userResponse
            else:
                if userResponse in self.exit_commands:
                    return -1
                return userResponse
        return "userData not built"

    # Loop cycle of chating till user exits
    def chat(self):
        print(colored('Jokebot', 'red') + ": Greetings!")
        userResponse = ""
        while userResponse != -1:
            userResponse = self.jokeOpener()
            if userResponse != -1:
                time.sleep(3)
                print(colored('Jokebot', 'red') + ": " + self.endPharse[random.randint(0, len(self.endPharse) - 1)])

        # Save userknowledge base
        self.userKnowledgeDict[self.userName] = self.userKnowledge
        pickle.dump(self.userKnowledgeDict, open('knowledgeBase.p', 'wb'))
        print(colored('Jokebot', 'red') + ": It was great talking to you, good bye")

    # Get random joke from NA
    def jokeRandom(self):
        randomIndex = random.randint(0, len(self.jokeDatabase))
        # key = self.jokeDatabase.keys()[randomIndex]
        txt = colored('Jokebot', 'red') + ":" + self.jokeDatabase['NA'][
            random.randint(0, len(self.jokeDatabase['NA']) - 1)]
        self.userKnowledge.append('NA')
        print(txt)

    # Check for synonym and if they are in database
    def getSyn(self, word):
        synonyms = []
        for syn in wn.synsets(word):
            for i in syn.lemmas():
                if i.name().lower() in self.jokeDatabase:
                    return i.name().lower()
        return -1
    # Ask user what type of joke they want to hear
    def askJokeType(self):
        userResponse = input(colored('Jokebot', 'red') + ": " + self.JsecondQuestion[random.randint(0,
                                                                                                    len(self.JsecondQuestion) - 1)] + "\n" + colored(
            self.userName, 'blue') + ": ").lower()  # asking what kind of joke they want
        if userResponse in self.exit_commands:
            return -1
        if userResponse in self.negative_responses or userResponse in self.anything_commands:  # Random joke
            self.jokeRandom()
        else:
            userResponse = userResponse.replace("joke", "")
            # Tag user response
            tag = self.predictor.predict(userResponse)
            try:
                # check for proper nouns
                index = tag['pos'].index('PROPN')
                word = re.sub(r'[^\w\s]', '', tag['words'][index]).lower()
            except ValueError:
                try:
                    # check for nouns
                    index = tag['pos'].index('NOUN')
                    word = re.sub(r'[^\w\s]', '', tag['words'][index]).lower()
                except ValueError:
                    if userResponse.count(" ") == 0:
                        word = userResponse
                    else:
                        word = "-1"
            if word not in self.jokeDatabase:
                word = self.getSyn(word)

            if word != -1:
                self.jokeKeyword(word)
            else:
                print(colored('Jokebot', 'red') + ": I did not find a joke about that but here's a different joke")
                self.jokeRandom()
            return 0
    # Ask if user wants to hear a check
    def jokeOpener(self):
        txt = colored('Jokebot', 'red') + ": " + self.JQuestion[
            random.randint(0, len(self.JQuestion) - 1)] + "\n" + colored(self.userName, 'blue') + ": "
        userResponse = input(txt.format(self.userName)).lower()  # asking if they want to hear a joke
        if userResponse not in self.negative_responses and userResponse not in self.exit_commands:
            number = random.randint(1, 50)
            # randomy ask if the want get a joke from history
            if number % 2 == 0 and len(
                    self.userKnowledge) > 2:  # random ask if they want to hear a joke based on knowledge
                userResponse = self.jokeAlt()
                if userResponse in self.exit_commands:
                    return -1
                if userResponse in self.negative_responses:
                    self.askJokeType()
            else:
                self.askJokeType()
        else:
            if userResponse in self.exit_commands:
                return -1
            userResponse = input(
                colored('Jokebot', 'red') + ": Well let me know if you want to hear one!\n" + colored(self.userName,
                                                                                                      'blue') + ": ")
            if userResponse not in self.exit_commands:
                userResponse = self.askJokeType()

        return 0


A = ChatBot()
A.start()
