import json

import readdata
import util

product_file = 'meta_Cell_Phones_and_Accessories.json.gz'
product_feature_file = 'product_features.txt'

# extracts product features such as id, title, url, price and sales rank.
def extractProductFeatures(product):
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

      result = product_id + ', ' + product_title + ', ' + \
               str(product_price) + ', ' + product_url + ', ' + product_rank + '\n';
    return result

  except KeyError:
    return None

pf = open(product_feature_file, 'wt')
for line in readdata.parse(product_file):
  line = util.dataCleanup(line)
  product = readdata.dataInJson(line)
  if product is not None:
    product_features = extractProductFeatures(product)
    if product_features is not None:
      pf.write(product_features)
        
