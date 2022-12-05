import csv
import allennlp
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import pickle
import progressbar
import re

def jokeData():
    jData = {}
    predictor = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")
    jData['NA'] = []
    with open("shortjokes.csv", encoding='utf8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        print("Start ")

        for row in csv_reader:
            if line_count % 8 == 1:
                index = -1
                first = True
                a = predictor.predict(sentence=row[1])
                while True:
                    try:
                        index = a['pos'].index('PROPN',index+1)
                        word = re.sub(r'[^\w\s]','',a['words'][index]).lower()
                        first = False
                        if jData.get(word) == None:
                            jData[word] = [row[1]]
                        else:
                            jData[word].append(row[1])
                    except ValueError:
                        break
                    except IndexError:
                        break

                if first:
                    try:
                        index = 0
                        index = a['pos'].index('NOUN', index)
                        word = re.sub(r'[^\w\s]','',a['words'][index]).lower()
                        if jData.get(word) == None:
                            jData[word] = [row[1]]
                        else:
                            jData[word].append(row[1])
                    except ValueError:
                        jData['NA'].append(row[1])
            line_count += 1
            print("\r"+str(line_count/250000), end='', flush=True)


    f.close()

    pickle.dump(jData, open('jokeData.p', 'wb'))

#jokeData()
a=  pickle.load(open('jokeData.p', 'rb'))
print(a)
