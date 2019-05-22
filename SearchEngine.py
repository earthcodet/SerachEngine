import glob
import json
import pandas as pd
import re
import fnmatch
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
stem = SnowballStemmer('english')
stopwords = ENGLISH_STOP_WORDS
regex = re.compile(r"\b\w{3,}\b")


def open_file():
    file = list()
    for filename in glob.glob('.\\web\\*.txt'):
        with open(filename, 'r') as f:
            file.append(f.read())
    return file

data = open_file()
df = pd.DataFrame({'Token':data})
v = TfidfVectorizer(smooth_idf=False, sublinear_tf=True,)
x = v.fit_transform(df['Token'])
tfidf = pd.DataFrame(x.toarray(), columns=v.get_feature_names())



def search(keyword, df):
    result = pd.DataFrame()

    for i in keyword:
        if i in df:
            result[i] = pd.Series(df[i].values, index=df.index)

    result['Sum'] = pd.Series(result.sum(axis=1), index=df.index)
    result = result.sort_values(by=['Sum'], ascending=False)
    index = result.index[result['Sum'] > 0].tolist()

    return index

def check_word(w,df):
    tokens = df.columns
    words = list()
    wordss = list()

    words.extend(fnmatch.filter(tokens, w))

    if words == list():
        word = regex.findall(w)
        word = [token for token in word if token not in stopwords]
        word = [stem.stem(token) for token in word]
        le = len(word)
        #print(le)
        for i in word:
            words.extend(fnmatch.filter(tokens, i))

        #lew = (le - len(words))
        #print(lew)
        #if le != len(words):
            #for i in range(lew, le):
                #if i == le - 1:
                    #words.append("")

    #print(len(words))


    return words


def Search_pro(word):

    j=0
    s = set()
    arr = set()
    r = check_word(word,tfidf)
    #print(r)

    if len(r) == 1:
        s = set(search(r, tfidf))
    elif len(r) > 1:
        for i in r:
            #print(i)
            arr = set(search([i],tfidf))
            #print('a',arr)
            #print('b',s)
            s = set.intersection(s,arr)
            #print('resutl',s)
            if s ==set() and j==0:
                s=arr
                arr=set()
                j=1


    if s == set():
        return None
    else:
        return  s,r


#g = Search_pro('kill this java is internet')
#print(g)



