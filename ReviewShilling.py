#!flask/bin/python
from flask import Flask, jsonify, request, abort
from flask import make_response, url_for
from flask_httpauth import HTTPBasicAuth

import json
import requests
import data

app = Flask(__name__)
auth = HTTPBasicAuth()

ml_url = 'http://localhost:5001/ReviewShillingML/v1.0/predict'
sa_url = 'http://localhost:5002/ReviewShillingSA/v1.0/analyze'

users = {"sai": "vallurupalli", "nitika" : "khurana", "pranav": "chauthaiwale"}

@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/ReviewShilling/v1.0/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': data.getAllCategories()})


@app.route('/ReviewShilling/v1.0/categories/<string:cat_id>', methods=['GET'])
def get_category(cat_id):
    category = data.getCategory(cat_id)
    if len(category) == 0:
        abort(404)
    return jsonify({'category': category[0]})

@app.route('/ReviewShilling/v1.0/products', methods=['GET'])
@app.route('/ReviewShilling/v1.0/categories/<string:cat_id>/products', methods=['GET'])
def get_products(cat_id = 9):
    products = []
    for item in data.getAllProducts(cat_id):
      product = {}
      for field in item:
        if field == 'pid':
          product['uri'] = url_for('get_product', prod_id=item['pid'], _external = True)
          product[field] = item[field]
        else:
          product[field] = item[field]
      products.append(product)
    return jsonify({'products': products})

@app.route('/ReviewShilling/v1.0/products/<string:prod_id>', methods=['GET'])
def get_product(prod_id):
    print "here?"
    (uneval_reviews, names) = data.getUnevalReviews(prod_id)
    if uneval_reviews is not None:
      print('found some uneval reviews')
      print(json.dumps({'reviews': uneval_reviews, 'names': names}))
      r = requests.post(ml_url, data=json.dumps({'reviews': uneval_reviews, 'names': names}))
      result = json.loads(r.text)['result']
      data.updateResult(result)

    product = data.getProductInfo(prod_id)
    if len(product) == 0:
        abort(404)

    return jsonify({'product': product[0]})

@app.route('/ReviewShilling/v1.0/products/<string:prod_id>/reviews', methods=['GET'])
def get_productreviews(prod_id):
    reviews = []
    for item in data.getProdReviews(prod_id):
      review = {}
      for field in item:
        if field == 'rid':
          review['uri'] = url_for('get_reviewer', rev_id = item['rid'], _external = True)
          review[field] = item[field]
        else:
          review[field] = item[field]
      reviews.append(review)
    return jsonify({'reviews': reviews})

@app.route('/ReviewShilling/v1.0/reviewers/<string:rev_id>', methods=['GET'])
def get_reviewer(rev_id):
    reviewer = data.getReviewerInfo(rev_id)
    if len(reviewer) == 0:
        abort(404)
    return jsonify({'reviewer': reviewer[0]})

@app.route('/ReviewShilling/v1.0/reviewers/<string:rev_id>/reviews', methods=['GET'])
def get_reviewerreviews(rev_id):
    reviews = data.getReviewerReviews(rev_id)
    if len(reviews) == 0:
        abort(404)
    return jsonify({'reviews': reviews})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/ReviewShilling/v1.0/products', methods=['POST'])
@auth.login_required
def create_product():
    if not request.get_json(force=True) or not 'asin' in request.get_json(force=True):
        abort(400)
    prod_id = request.get_json(force=True)['asin']
    cat_id = request.get_json(force=True)['cid']
    pname = request.get_json(force=True)['title']
    url = request.get_json(force=True)['imurl']
    price = request.get_json(force=True)['price']
    rank = request.get_json(force=True)['rank']
    if len(prod_id) == 0:
        abort(404)
    # need to check if product is in the product table, if not create it, else throw error 
    if data.existProduct(prod_id):
        abort(405)
    product = {'pid': prod_id, 'cid': cat_id, 'pname': pname, 'imurl': url, 'price': price, 'rank': rank}
    data.insertProduct(product)
    reviews = request.get_json(force=True)['reviews']
    for r in reviews:
      ret = requests.post(sa_url, data=json.dumps({'review': r, 'product': product}))
      review = json.loads(ret.text)
      # review with that prod_id and reviewer_id should not exist, but if they
      # do throw error
      print(review)
      if data.existReview(prod_id, review['rid']):
        abort(405)
      else:
        data.insertReview(review)     
    data.commit()
    (uneval_reviews, names) = data.getUnevalReviews(prod_id)
    print('found some uneval reviews')
    if uneval_reviews is not None:
      print(json.dumps({'reviews': uneval_reviews, 'names': names}))
      r = requests.post(ml_url, data=json.dumps({'reviews': uneval_reviews, 'names': names}))
      result = json.loads(r.text)['result']
      data.updateResult(result)
    product = data.getProductInfo(prod_id)
    return jsonify({'product': product[0]})

@app.route('/ReviewShilling/v1.0/products/<string:product_id>', methods=['PUT'])
@auth.login_required
def update_product(product_id):
    if not request.get_json(force=True) or not 'asin' in request.get_json(force=True):
        abort(400)
    prod_id = request.get_json(force=True)['asin']
    cat_id = request.get_json(force=True)['cid']
    pname = request.get_json(force=True)['title']
    url = request.get_json(force=True)['imurl']
    price = request.get_json(force=True)['price']
    rank = request.get_json(force=True)['rank']
    if len(prod_id) == 0 or product_id != prod_id:
        abort(404)
    # need to check if product is in the product table, if not throw error 
    if not data.existProduct(prod_id):
        abort(405)
    product = {'pid': prod_id, 'cid': cat_id, 'pname': pname, 'imurl': url, 'price': price, 'rank': rank}
    data.updateProduct(product)
    reviews = request.get_json(force=True)['reviews']
    for r in reviews:
      print(r)
      ret = requests.post(sa_url, data=json.dumps({'review': r, 'product': product}))
      review = json.loads(ret.text)
      # review with this prod_id and reviewer_id may not exist, if it does
      # update the review, else insert.
      if data.existReview(prod_id, review['rid']):
        data.updateReview(review)
      else:
        data.insertReview(review)
    data.commit()
    (uneval_reviews, names) = data.getUnevalReviews(prod_id)
    print('found some uneval reviews')
    if uneval_reviews is not None:
      print(json.dumps({'reviews': uneval_reviews, 'names': names}))
      r = requests.post(ml_url, data=json.dumps({'reviews': uneval_reviews, 'names': names}))
      result = json.loads(r.text)['result']
      data.updateResult(result)
    product = data.getProductInfo(prod_id)
    return jsonify({'product': product[0]})

@app.route('/ReviewShilling/v1.0/products/<string:product_id>', methods=['DELETE'])
@auth.login_required
def delete_product(product_id):
    if not request.get_json(force=True) or not 'asin' in request.get_json(force=True):
        abort(400)
    prod_id = request.get_json(force=True)['asin']
    if not data.existProduct(prod_id):
        abort(405)
    data.deleteProduct(prod_id)
    data.deleteProductReviews(prod_id)
    return jsonify({'result': True})

@app.route('/ReviewShilling/v1.0/reviewers/<string:reviewer_id>', methods=['DELETE'])
@auth.login_required
def delete_reviewer(reviewer_id):
    if not request.get_json(force=True) or not 'rid' in request.get_json(force=True):
        abort(400)
    reviewer_id = request.get_json(force=True)['rid']
    data.deleteReviewerReviews(reviewer_id)
    return jsonify({'result': True})

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
