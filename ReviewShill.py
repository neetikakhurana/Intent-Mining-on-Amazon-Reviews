#!flask/bin/python
from flask import Flask, jsonify, request, abort, redirect
from flask import make_response, url_for, render_template
from flask_httpauth import HTTPBasicAuth
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

import json
import requests
import data
rev=0
prod=0
app = Flask(__name__)
auth = HTTPBasicAuth()
menu_products={}
rs_url = 'http://localhost:5000/ReviewShilling/v1.0/'

users = {"sai": "vallurupalli", "nitika" : "khurana", "pranav": "chauthaiwale"}

@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/ReviewShill/v1.0/home', methods=['GET','POST'])
def home():
#-----------------
    # get a list of categories 
    category=dict()
    print "pro"
    rev=0
    prod=0
    response = requests.get(rs_url + 'categories')
    print "response",response
    for i in json.loads(response.text)['categories']:
        for k,v in i.items():
            if (k == 'name'): cname = v 
            if (k == 'id'): cid = v  
        category[cname] = cid
        
    # get a list of products
    products=dict()
    response = requests.get(rs_url + 'products')
    print "respprod",response
    product_list = json.loads(response.text)['products']
    for i in product_list:
        for k,v in i.items():
            if (k == 'pname'): pname = v 
            if (k == 'pid'): pid = v 
            if (k == 'uri'): uri = v  
        products[pname] = pid
#-------------------
    for k,v in products.items():
        menu_products[k]=v
        if len(menu_products)==20:
            break
    #menu_products = sorted(products, key=products.get,reverse=False)[:20]
    prod_id=request.form.get('prod_id')
    print prod_id
    """if prod_id!="":
        response = requests.get(rs_url + 'products/' + prod_id)
        info = json.loads(response.text)['product']
        print(info)"""
	
    # select the first product and its reviews
    item = product_list[0]
    print item
    print item['uri']
    response = requests.get(item['uri'])
    info = json.loads(response.text)['product']
    response = requests.get(item['uri'] + '/reviews')
    reviews= dict()
    for r in json.loads(response.text)['reviews']:
        reviews[r['rtext']]={r['rname']:url_for('get_reviewer', rev_id = r['rid'], _external=True)}

    fakeper=((float)(info['scount'])/(float)(info['rcount']))*100
    words = [(k, float(v)) for k, v in json.loads(info['inwords']).items()]
    words.extend([(k, float(v)) for k, v in json.loads(info['imwords']).items()])    
    
    wordcloud = WordCloud(stopwords=None, background_color='white',
                width=1200, height=1000).generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/'+item['pid']+'.png')
    plt.clf()
    return render_template('index.html',prod=prod,rev=rev,products=products,menuprod=menu_products,pid=item['pid'],product_name = item['pname'],brand_name = '',url = item['icon'],categories=category,reviews=reviews,length=len(reviews),fake=int(fakeper),shill=float(info['sindex']))   

@app.route('/ReviewShill/v1.0/reviewers/<string:rev_id>', methods=['GET','POST'])
def get_reviewer(rev_id):
#-----------------
    prod=0
    # get a list of categories 
    category=dict()
    rev=1
    response = requests.get(rs_url + 'categories')
    for i in json.loads(response.text)['categories']:
        for k,v in i.items():
            if (k == 'name'): cname = v 
            if (k == 'id'): cid = v  
        category[cname] = cid
        
    # get a list of products
    products=dict()
    product_names=dict()
    response = requests.get(rs_url + 'products')
    product_list = json.loads(response.text)['products']
    for i in product_list:
        for k,v in i.items():
            if (k == 'pname'): pname = v 
            if (k == 'pid'): pid = v 
            if (k == 'uri'): uri = v  
        products[pname] = pid
#-----------------
        product_names[pid] = pname
    for k,v in products.items():
        menu_products[k]=v
        if len(menu_products)==20:
            break
    #menu_products = sorted(products, key=products.get,reverse=False)[:20]

    # select the first product and its reviews
    response = requests.get(rs_url + 'reviewers/' + rev_id)
    info = json.loads(response.text)['reviewer']
    print(info)

    response = requests.get(rs_url + 'reviewers/' + rev_id+ '/reviews')
    reviews= dict()
    for r in json.loads(response.text)['reviews']:
        reviews[r['rtext']]={product_names[r['pid']]:url_for('get_product', prod_id = r['pid'], _external=True)}

    fakeper=((float)(info['scount'])/(float)(info['rcount']))*100
    words = [(k, float(v)) for k, v in json.loads(info['inwords']).items()]
    words.extend([(k, float(v)) for k, v in json.loads(info['imwords']).items()])    
    
    wordcloud = WordCloud(stopwords=None, background_color='white',
                width=1200, height=1000).generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/'+rev_id+'.png')
    plt.clf()
    return render_template('index.html',prod=prod,rev=rev,products=products,menuprod=menu_products,pid=rev_id,product_name = info['rname'],categories=category,reviews=reviews,length=len(reviews),fake=int(fakeper),shill=float(info['sindex']))   

"""@app.route('/ReviewShill/v1.0/categories/<string:cat_id>', methods=['GET','POST'])
def get_products(cat_id):
#-----------------
    prod=0
    # get a list of categories 
    category=dict()
    rev=0
    print "here"
    print cat_id
    response = requests.get(rs_url + 'categories')
    for i in json.loads(response.text)['categories']:
        for k,v in i.items():
            if (k == 'name'): cname = v 
            if (k == 'id'): cid = v
        category[cname] = cid
    for k,v in category.items():
        if v==cat_id:
       
    # get a list of products
    products=dict()
    product_names=dict()
    response = requests.get(rs_url + 'products')
    print rs_url + 'products'+prod_id
    product_list = json.loads(response.text)['products']
    for i in product_list:
        for k,v in i.items():
            if (k == 'pname'): pname = v 
            if (k == 'pid'): pid = v 
            if (k == 'uri'): uri = v  
        products[pname] = pid
#-----------------
    menu_products = sorted(products, key=products.get,reverse=False)[:20]
    # select the given product and its reviews
    item = [p for p in product_list if (p['pid'] == prod_id)]
    print "item",item,item[0]['pname']
    print item[0]['uri']
    response = requests.get(item[0]['uri'])
    info = json.loads(response.text)['product']
    response = requests.get(item[0]['uri'] + '/reviews')
    reviews= dict()
    for r in json.loads(response.text)['reviews']:
        reviews[r['rtext']]={r['rname']:url_for('get_reviewer', rev_id = r['rid'], _external=True)}

    fakeper=((float)(info['scount'])/(float)(info['rcount']))*100
    words = [(k, float(v)) for k, v in json.loads(info['inwords']).items()]
    words.extend([(k, float(v)) for k, v in json.loads(info['imwords']).items()])    
    
    wordcloud = WordCloud(stopwords=None, background_color='white',
                width=1200, height=1000).generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/'+item[0]['pid']+'.png')
    plt.clf()
    return render_template('index.html',products=products,rev=rev,menuprod=menu_products,pid=item[0]['pid'],product_name = item[0]['pname'],brand_name = '',url = item[0]['icon'],categories=category,reviews=reviews,length=len(reviews),fake=int(fakeper),shill=float(info['sindex']))   
"""

    
@app.route('/ReviewShill/v1.0/products/<string:prod_id>', methods=['GET','POST'])
def get_product(prod_id):
#-----------------
    # get a list of categories 
    category=dict()
    rev=0
    print "here"
    print prod_id
    response = requests.get(rs_url + 'categories')
    for i in json.loads(response.text)['categories']:
        for k,v in i.items():
            if (k == 'name'): cname = v 
            if (k == 'id'): cid = v  
        category[cname] = cid
        
    # get a list of products
    products=dict()
    product_names=dict()
    response = requests.get(rs_url + 'products')
    print rs_url + 'products'+prod_id
    product_list = json.loads(response.text)['products']
    for i in product_list:
        for k,v in i.items():
            if (k == 'pname'): pname = v 
            if (k == 'pid'): pid = v 
            if (k == 'uri'): uri = v  
        products[pname] = pid
#-----------------
    for k,v in products.items():
        menu_products[k]=v
        if len(menu_products)==20:
            break
    #menu_products = sorted(products, key=products.get,reverse=False)[:20]
    # select the given product and its reviews
    item = [p for p in product_list if (p['pid'] == prod_id)]
    print "item",item,item[0]['pname']
    print item[0]['uri']
    response = requests.get(item[0]['uri'])
    info = json.loads(response.text)['product']
    response = requests.get(item[0]['uri'] + '/reviews')
    reviews= dict()
    for r in json.loads(response.text)['reviews']:
        reviews[r['rtext']]={r['rname']:url_for('get_reviewer', rev_id = r['rid'], _external=True)}

    fakeper=((float)(info['scount'])/(float)(info['rcount']))*100
    words = [(k, float(v)) for k, v in json.loads(info['inwords']).items()]
    words.extend([(k, float(v)) for k, v in json.loads(info['imwords']).items()])    
    
    wordcloud = WordCloud(stopwords=None, background_color='white',
                width=1200, height=1000).generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/'+item[0]['pid']+'.png')
    plt.clf()
    return render_template('index.html',products=products,rev=rev,menuprod=menu_products,pid=item[0]['pid'],product_name = item[0]['pname'],brand_name = '',url = item[0]['icon'],categories=category,reviews=reviews,length=len(reviews),fake=int(fakeper),shill=float(info['sindex']))   


    
@app.route('/ReviewShill/v1.0/products/', methods=['GET','POST'])
def get_search_product():
    #prod_id = request.form.get("postprod")
#-----------------
    # get a list of categories 
    category=dict()
    rev=0
    prod=1
    response = requests.get(rs_url + 'categories')
    for i in json.loads(response.text)['categories']:
        for k,v in i.items():
            if (k == 'name'): cname = v 
            if (k == 'id'): cid = v  
        category[cname] = cid
        
    # get a list of products
    products=dict()
    product_names=dict()
    response = requests.get(rs_url + 'products')
    product_list = json.loads(response.text)['products']
    for i in product_list:
        for k,v in i.items():
            if (k == 'pname'): pname = v 
            if (k == 'pid'): pid = v 
            if (k == 'uri'): uri = v  
        products[pname] = pid
#-----------------
    for k,v in products.items():
        menu_products[k]=v
        if len(menu_products)==20:
            break
    #menu_products = sorted(products, key=products.get,reverse=False)[:20]

    # select the first product and its reviews
    item = product_list[0]
    print item
    print item['uri']
    response = requests.get(item['uri'])
    info = json.loads(response.text)['product']
    response = requests.get(item['uri'] + '/reviews')
    reviews= dict()
    for r in json.loads(response.text)['reviews']:
        reviews[r['rtext']]={r['rname']:url_for('get_reviewer', rev_id = r['rid'], _external=True)}

    fakeper=((float)(info['scount'])/(float)(info['rcount']))*100
    words = [(k, float(v)) for k, v in json.loads(info['inwords']).items()]
    words.extend([(k, float(v)) for k, v in json.loads(info['imwords']).items()])    
    
    wordcloud = WordCloud(stopwords=None, background_color='white',
                width=1200, height=1000).generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/'+item['pid']+'.png')
    plt.clf()
    return render_template('index.html',prod=prod,products=products,rev=rev,menuprod=menu_products,pid=item['pid'],product_name = item['pname'],brand_name = '',url = item['icon'],categories=category,reviews=reviews,length=len(reviews),fake=int(fakeper),shill=float(info['sindex']))   
    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/ReviewShill/v1.0/products', methods=['POST'])
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
    data.insertProductFeatures(product)
    reviews = request.get_json(force=True)['reviews']
    for r in reviews:
      ret = requests.post(sa_url, data=json.dumps({'review': r, 'product': product}))
      review = json.loads(ret.text)
      if data.existReview(prod_id, review['rid']):
          abort(405)
      # review with that prod_id and reviewer_id should not exist, but if they
      # do throw error
      print(review)    
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

@app.route('/ReviewShill/v1.0/products/<string:product_id>', methods=['PUT'])
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
    data.updateProductFeatures(product)
    reviews = request.get_json(force=True)['reviews']
    for r in reviews:
      print(r)
      ret = requests.post(sa_url, data=json.dumps({'review': r, 'product': product}))
      review = json.loads(ret.text)
      # review with this prod_id and reviewer_id may not exist, if it does
      # update the review, else insert.
      if data.existReview(prod_id, review['rid']):
        data.updateReviewFeatures(review)
      else:
        data.insertReviewFeatures(review)
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

@app.route('/ReviewShill/v1.0/products/<string:product_id>', methods=['DELETE'])
@auth.login_required
def delete_product(product_id):
    if not request.get_json(force=True) or not 'asin' in request.get_json(force=True):
        abort(400)
    prod_id = request.get_json(force=True)['asin']
    if not data.existProduct(prod_id):
        abort(405)
    data.deleteProduct(prod_id)
    data.deleteReviews(prod_id)
    return jsonify({'result': True})

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5005'))
    except ValueError:
        PORT = 5005
    app.run(HOST, PORT)
