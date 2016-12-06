import json
import requests

import data
import datautil
import safunc

sa_url = 'http://localhost:5002/ReviewShillingSA/v1.0/analyze'

product_file = 'meta_Cell_Phones_and_Accessories.json.gz'
review_file = 'reviews_Cell_Phones_and_Accessories_5.json.gz'
review_feature_file = 'review_features.txt'

# extracts product features such as id, title, url, price and sales rank.
def extractProductFields(product):
  # if the JSON data is valid there has to be a product_id
  product_id = product['asin']

  # some of the JSON objects do not have a title attribute
  # set them to "NO TITLE"
  try:
    product_title = product['title']
  except KeyError:
    product_title = "NO TITLE"

  # some of the JSON objects do not have an image url attribute 
  # so no image can be displayed for these products
  try:
    product_url = product['imUrl']
  except KeyError:
    product_url = "IMAGE UNAVAILABLE"

  # some of the JSON objects do not have a price attribute
  # assume the price is 0.0 in that case
  try:
    product_price = product['price']
  except KeyError:
    product_price = 0.0;

  # some of the JSON objects are listed with the wrong category.
  # in these cases the salesRank category does not match the product
  # category.  In this situation it might be better to abandon this
  # object because it does not belong in this category. 
  try:
    if (product['salesRank']['Cell Phones & Accessories']) :
      product_rank = str(product['salesRank']['Cell Phones & Accessories'])

    return {'cid': '9', 'pid': product_id, 'pname': product_title,
            'imurl': product_url, 'price': product_price, 'rank': product_rank}

  except KeyError:
    return None

#----- create product table          
cnt = 0
products = []
for line in datautil.parse(product_file):
  line = datautil.dataCleanup(line)
  pdata = datautil.dataInJson(line)
  if pdata is not None:
    product = extractProductFields(pdata)
    if product is not None:
      cnt += 1
      products.append(product)
      data.insertProductFeatures(product)
data.commit()

#----- create review table          
cnt = 0
bad_cnt = 0
reviews = []
rff = open(review_feature_file, 'wt')      
for line in datautil.parse(review_file):
  print(line)
  rdata = datautil.dataInJson(line)
  json.dump(rdata, open('post.txt', 'wt'))
  if rdata is not None:
    cnt += 1
    pdata = [product for product in products if product['pid'] == rdata['asin']]
    try:
#      ret = requests.post(sa_url, data=json.dumps({'review': rdata, 'product': pdata[0]}))
#      review = json.loads(ret.text)
      review = safunc.extractReviewFeatures(rdata, pdata[0])
      data.insertReviewFeatures(review)
      print(cnt)
      if cnt % 10000 == 0:
        data.commit()
    except IndexError:
      bad_cnt += 1
print('Reviews that did not have a matching product ' + str(bad_cnt))
data.closeAll()
