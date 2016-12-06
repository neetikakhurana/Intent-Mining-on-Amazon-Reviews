import textutil
import re
import json
import nltk
from nltk.corpus import stopwords
from afinn import Afinn
afinn = Afinn()
df = json.load(open('review_text.txt', 'rt'))  

def extractReviewFeatures(review, product):
  product_id = review['asin']
  product_price = 0.0
  product_rank = 0
  product_price = product['price']
  product_rank = product['rank']  
  reviewer_id = review['reviewerID']
  review_score = review['overall']
  review_num_feedbacks = review['helpful'][0]
  review_pos_feedbacks = review['helpful'][0]
  # would be good to store how many positive ahead, and negative ahead 
  review_time = review['unixReviewTime'] # will give us position
    
  try:
    reviewer_name = review['reviewerName']
  except KeyError:
    reviewer_name = "NONAME"

  review_text = review['summary'] + ' ' + review['reviewText']
  clean_text = re.sub('[^0-9]+.[^0-9]+', lambda w: w.group(0).replace('.',' '), review_text.lower())
  review_afinn_index = afinn.score(clean_text)
  review_tokens = nltk.Text(nltk.word_tokenize(clean_text))
  review_pos = nltk.pos_tag(review_tokens)
  review_len = len(review_tokens)
  imwords = textutil.getImaginativeWords(review_pos, df)
  inwords = textutil.getInformativeWords(review_pos, df)
  
  return {'pid': product_id, 'pprice': product_price,
          'prank': product_rank, 'rid': reviewer_id, 'rname': reviewer_name, 
          'fcount': str(review_num_feedbacks), 'hcount': str(review_pos_feedbacks),
          'score': str(review_score), 'utime': str(review_time),
          'tlen': str(len(review_text)), 'wlen': review_len,
          'rtext': review_text,
          'afinn': review_afinn_index/review_len,
          # count adverbs, verbs, pronouns & pre-determiners
          'imx': textutil.getIndex(imwords)/review_len,
          # count nouns, adjectives, prepositions, determiners and conjunctions
          'inx': textutil.getIndex(inwords)/review_len,
          'imwords': textutil.getTopN(imwords, 25),
          'inwords': textutil.getTopN(inwords, 25)}
