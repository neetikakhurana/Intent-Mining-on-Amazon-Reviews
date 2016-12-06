#
#  Contains functions used by ReviewShilling Semanic Analysis service
#
import re
import json
import nltk
from nltk.corpus import stopwords

# removes stop words in the stopwords corpus
def removeStopWords(text):
  english_stopwords = stopwords.words('english')
  return [(w, t) for (w, t) in text if w.lower() not in english_stopwords]

# reports words not in the words corpus (usually used to find misspelled words)
def unusualWords(text):
 text_vocab = set(w.lower() for w in text if w.isalpha())
 english_vocab = set(w.lower() for w in nltk.corpus.words.words())
 unusual = text_vocab.difference(english_vocab)
 return sorted(unusual)

# lemmatize words (this instead of stemming) 
def lemmatize(text):
  wnl = nltk.WordNetLemmatizer()
  return [(wnl.lemmatize(w), t) for (w, t) in text]

# get tfidfs for words that indicate motion (verbs, adverbs etc) and
# words that distance from self (pronouns, modifiers etc) etc.
def getImaginativeWords(text, df):
  words = dict()
  cfd = nltk.ConditionalFreqDist((t, w) for (w, t) in text)
  for k in cfd.keys():
    if re.match('^(V|PRO|ADV|EX|MOD).*$', k):
      for w in cfd[k].keys():
        words[w] = cfd[k][w]/df[w]
  return words

# get tfidfs for words that indicate self, and self experience (nouns, adjectives etc)
def getInformativeWords(text, df):
  words = dict()
  cfd = nltk.ConditionalFreqDist((t, w) for (w, t) in text)
  for k in cfd.keys():
    if re.match('^((N|ADJ|DET|CNJ|TO).*|P)$', k):
      for w in cfd[k].keys():
        words[w] = cfd[k][w]/df[w]
  return words

# compute a single index for a list of given words
def getIndex(words):
  cnt = 0.0
  for k in words.keys():
    cnt += words[k]
  return cnt

# return the top N words based on tfidf values
def getTopN(words, N):
  df = dict()
  retstr = ""
  for w in sorted(words, key=words.get, reverse=True)[:N]:
    df[w] = "%.7f" % words[w]
  retstr = json.dumps(df)
  return retstr

