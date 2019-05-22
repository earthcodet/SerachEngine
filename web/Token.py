import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import pandas
import json
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()
regex = re.compile(r"\b[a-zA-Z]{3,}\b")

#nltk.download('punkt')
#nltk.download('stopwords')
upload = pandas.read_csv("linked.csv", encoding='utf-8')
stop_words = set(stopwords.words('english'))
punctuations = '''!()-, "''[]{};:"'\,<>./?@ "''"=#$``%^&*""_~"""/""""—`'''
stop_words.update(punctuations)
dic = defaultdict(list)
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
stem = SnowballStemmer('english')
stopwords = ENGLISH_STOP_WORDS

class Doc:

    def __init__(self, name, doc):
        self.name = name
        self.doc = doc

    def myfunc(self):
        print("{} is in {} ".format(self.name, self.doc))


def getlink(web):
    resp = requests.get(web)
    soup = BeautifulSoup(resp.content, 'html.parser')
    content = soup.find("body").get_text()
    tokens = nltk.word_tokenize(content.lower())
    token1 = list()
    for tokenq in tokens:
        try:
            token = regex.fullmatch(tokenq)
            if len(token.string)<10:
                token1.append(token.string)
        except:
            pass
    #print(token1)
    token = [token for token in token1 if token not in stopwords]
    token = [stem.stem(token) for token in token]
    token = sorted(token)
    print(token)
    return token


def gen_doc(token, index):
    doc = []
    for e in token:
        doc.append(Doc(e, index))
    return doc

def cles(word):
  word =  [w for w in word if not w in stop_words]
  return word

def tokenSave():
    for i in range(len(upload)):
        web = upload['url'][i]
        tk = getlink(web)
        # doc = gen_doc(tk, i + 1)

        # for j in doc:
        #     if dic.get(j.name) is None:
        #         dic[j.name].append(j.doc)
        #     else:
        #         dic[j.name].append(j.doc)

        s = '{}.txt'.format(i)
        with open(s, 'w')as f:
           json.dump(tk, f)


    return dic

a=tokenSave()

