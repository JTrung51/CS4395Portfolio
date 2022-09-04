from nltk import word_tokenize
from nltk import sent_tokenize

a = word_tokenize("Humpty Dumpty sat on the wall. Humpty Dumpty had a great fall. All the king's horses and all the king's men. Couldn't put Humpty together again.")
print(a)
b = sent_tokenize("Humpty Dumpty sat on the wall. Humpty Dumpty had a great fall. All the king's horses and all the king's men. Couldn't put Humpty together again.")
print(b)