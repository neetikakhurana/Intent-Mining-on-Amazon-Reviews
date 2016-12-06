#!flask/bin/python
from flask import Flask, jsonify, request, abort
from flask import make_response, current_app, url_for 
app = Flask(__name__)

import re
import json
import nltk
from nltk.corpus import stopwords
from afinn import Afinn

import textutil

afinn = Afinn()
df = json.load(open('review_text.txt', 'rt'))  

@app.route('/ReviewShillingSA/v1.0/analyze', methods=['POST'])
def extractReviewFeatures():
  review = request.get_json(force=True)['review']
  product = request.get_json(force=True)['product']
  print(product)
  print(review)
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
  
  return jsonify({'pid': product_id, 'pprice': product_price,
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
          'inwords': textutil.getTopN(inwords, 25)})

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5002'))
    except ValueError:
        PORT = 5002
    app.run(HOST, PORT)
