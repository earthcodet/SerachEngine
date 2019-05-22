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


def Check_w_wild(w,df):
    tokens = df.columns
    w = w.split()
    words = list()

    for i in w:
        words.extend(fnmatch.filter(tokens, i))

    return words

def Search_wild(word,df):
    result = pd.DataFrame()

    for i in word:
        if i in df:
            result[i] = pd.Series(df[i].values, index=df.index)

    result['Sum'] = pd.Series(result.sum(axis=1), index=df.index)
    result = result.sort_values(by=['Sum'], ascending=False)
    index = result.index[result['Sum'] > 0].tolist()

    return index

def Search_pro_wild(word):
    r = Check_w_wild(word, tfidf)
    s = list()
    if r == list():
        return None
    else:
        s = set(Search_wild(r, tfidf))
        return s


#g2 = Search_pro_wild('man*')
#print(g2)