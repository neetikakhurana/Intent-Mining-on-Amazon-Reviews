import json
import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1', port='3306',
                              database='reviewshilling')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
  
def commit():
  cnx.commit()

def closeAll():
  cnx.commit()
  cnx.close()

categories = [
    {
      'id': '1',
      'name': u'Books'
      },
    {
      'id': '2',
      'name': u'Electronics'
      },
    {
      'id': '3',
      'name': u'Movies and TV'
      },
    {
      'id': '4',
      'name': u'CDs and Vinyl'
      },
    {
      'id': '5',
      'name': u'Clothing, Shoes and Jewelry'
      },
    {
      'id': '6',
      'name': u'Home and Kitchen'
      },
    {
      'id': '7',
      'name': u'Kindle Store'
      },
    {
      'id': '8',
      'name': u'Sports and Outdoors'
      },
    {
      'id': '9',
      'name': u'Cell Phones and Accessories'
      },
    {
      'id': '10',
      'name': u'Health and Personal Care'
      },
    {
      'id': '11',
      'name': u'Toys and Games'
      },
    {
      'id': '12',
      'name': u'Video Games'
      },
    {
      'id': '13',
      'name': u'Tools and Home Improvement'
      },
    {
      'id': '14',
      'name': u'Beauty'
      },
    {
      'id': '15',
      'name': u'Apps for Android'
      },
    {
      'id': '16',
      'name': u'Office Products'
      },
    {
      'id': '17',
      'name': u'Pet Supplies'
      },
    {
      'id': '18',
      'name': u'Automotive'
      },
    {
      'id': '19',
      'name': u'Grocery and Gourmet Food'
      },
    {
      'id': '20',
      'name': u'Patio, Lawn and Garden'
      },
    {
      'id': '21',
      'name': u'Baby'
      },
    {
      'id': '22',
      'name': u'Digital Music'
      },
    {
      'id': '23',
      'name': u'Musical Instruments'
      },
    {
      'id': '24',
      'name': u'Amazon Instant Video'
      }
    ]
  
def getAllCategories():
    return categories

def getCategory(id):
  return [cat for cat in categories if cat['id'] == id]

# needs to read hbase and get a list of products that belong to the category
# with an id of catid.  This will return json data containing the ids of
# category and product, product name and url of the image
def getAllProducts(catid):
  products = []
  cursor = cnx.cursor()
  query = ("SELECT pid, pname, imurl FROM product "
           "WHERE cid = %s AND pid IN (SELECT pid FROM review)")
  cursor.execute(query, (catid,))
  for (pid, pname, imurl) in cursor:
      products.append({'pid':pid, 'pname':pname, 'icon': imurl}) 
  cursor.close()
  return products

def existProduct(pid):
  cursor = cnx.cursor()
  query = ("SELECT count(*) as cnt FROM product "
           "WHERE pid = %s")
  cursor.execute(query, (pid,))
  reccnt = cursor.fetchone()[0]
  print("found" + str(reccnt))
  cursor.close()
  return 1 if reccnt > 0 else 0

def deleteProduct(pid):
  cursor = cnx.cursor()
  query = ("DELETE FROM product "
           "WHERE pid = %s")
  cursor.execute(query, (pid,))
  cursor.close()

def insertProduct(product):
  cursor = cnx.cursor()
  add_product = ("INSERT INTO product "
                 "(pid, pname, imurl, cid) VALUES "
                 "(%(pid)s, %(pname)s, %(imurl)s, %(cid)s)")
  cursor.execute(add_product, product)
  cursor.close()

def updateProduct(product):
  cursor = cnx.cursor()
  add_product = ("UPDATE product set pname = %(pname)s, "
                 "imurl = %(imurl)s, cid = %(cid)s"
                 "WHERE pid = %(pid)s")
  cursor.execute(add_product, product)
  cursor.close()

def insertReview(review):
  cursor = cnx.cursor()
              
  add_review = ("INSERT INTO review "
                "(pid, pprice, prank, rid, rname, fcount, hcount, score, "
                " utime, tlen, wlen, rtext, afinn, imx, inx, imwords, inwords) VALUES "
                "(%(pid)s, %(pprice)s, %(prank)s, %(rid)s, %(rname)s, "
                "%(fcount)s, %(hcount)s, %(score)s, %(utime)s, %(tlen)s, %(wlen)s, "
                "%(rtext)s, %(afinn)s, %(imx)s, %(inx)s, %(imwords)s, %(inwords)s)")
  cursor.execute(add_review, review)
  cursor.close()


def updateReview(review):
  cursor = cnx.cursor()
              
  add_review = ("UPDATE review SET pprice = %(pprice)s, prank = %(prank)s, rname = %(rname)s,"
                "fcount = %(fcount)s, hcount = %(hcount)s, score = %(score)s, utime = %s(utime)s, "
                "tlen = %(tlen)s, wlen = %(wlen)s, rtext = %(rtext)s, afinn = %(affin)s, "
                "imx = %(imx)s, inx = %(inx)s, imwords = %(imwords)%, inwords = %(inwords)s"
                "WHERE rid = %(rid)s and pid = %(pid)s")
  cursor.execute(add_review, review)
  cursor.close()


def deleteProductReviews(pid):
  cursor = cnx.cursor()
  query = ("DELETE FROM review "
           "WHERE pid = %s")
  cursor.execute(query, (pid,))
  cursor.close()


def deleteReviewerReviews(rid):
  cursor = cnx.cursor()
  query = ("DELETE FROM review "
           "WHERE rid = %s")
  cursor.execute(query, (rid,))
  cursor.close()


def existReview(pid, rid):
  cursor = cnx.cursor()
  query = ("SELECT count(*) as cnt FROM review "
           "WHERE pid = %s and rid = %s")
  cursor.execute(query, (pid, rid))
  reccnt = cursor.fetchone()[0]
  cursor.close()
  return 1 if reccnt > 0 else 0

def getShillIndex(rid):
  cursor = cnx.cursor()
  if (rid == 0):
    query = ("SELECT truth, count(truth) as cnt FROM review "
             "WHERE evaluate = '1' AND truth IS NOT NULL group by truth order by truth")
    cursor.execute(query)
  else:
    query = ("SELECT truth, count(truth) as cnt FROM review "
             "WHERE evaluate = '1' AND rid = %s AND truth IS NOT NULL group by truth order by truth")
    cursor.execute(query, (rid,))
  total_cnt = 0
  for (truth, cnt) in cursor:
    if (truth == 0):
      shill_cnt = cnt
      total_cnt += cnt
    else:
      total_cnt += cnt
  cursor.close()
  return (shill_cnt, total_cnt)
  
# needs to read hbase and get the product info with the given id.  This will
# return json data with all the product's information
def getProductInfo(pid):
  cursor = cnx.cursor()

  (total_scnt, total_cnt) = getShillIndex(0)
  total_idx = total_scnt/total_cnt
  cnt = 0
  query = ("SELECT rid, truth, inx, imx, afinn, imwords, inwords FROM review "
           "WHERE pid = %s and evaluate = '1'")
  cursor.execute(query, (pid,))
  eval_cnt = 0
  shill_cnt = 0
  shill_idx = 0.0
  inx_total = 0.0
  imx_total = 0.0
  afinn_total = 0.0
  im_words = dict()
  in_words = dict()
  rids = []  

  for (rid, truth, inx, imx, afinn, imwords, inwords) in cursor:
    rimw = json.loads(imwords)
    for w in rimw.keys():
      if w in im_words.keys():
        rimw[w] = float(im_words[w]) + float(rimw[w])
    im_words.update(rimw)
    
    rinw = json.loads(inwords)
    for w in rinw.keys():
      if w in in_words.keys():
        rinw[w] = float(in_words[w]) + float(rinw[w])
    in_words.update(rinw)

    inx_total += float(inx)
    imx_total += float(imx)
    afinn_total += float(afinn)
    eval_cnt += 1
    if truth == 0:
      rids.append(rid)
      shill_cnt += 1

  for rid in rids:  
    # if the review is a shill, it will contribute to the product's shill index
    # if it is true it does not contribute directly, but contributes by changing
    # the total index
      (r_scnt, r_cnt) = getShillIndex(rid)
      rev_idx = r_scnt/r_cnt 
      shill_idx +=  rev_idx 
      print(shill_idx)
 
  if (eval_cnt > 0):
    return [{'sindex': shill_idx/eval_cnt , 'rcount': eval_cnt,
             'scount': shill_cnt, 'senx': afinn_total/eval_cnt,
             'imx': imx/eval_cnt, 'inx': inx/eval_cnt,
             'imwords': json.dumps(im_words), 'inwords': json.dumps(in_words)}] 
  else:
    return [{'sindex':0, 'rcount':0, 'scount':0, 'senx':0, 'imx':0, 'inx':0,
             'imwords': json.dumps(im_words), 'inwords': json.dumps(in_words)}]
  cursor.close()
  return ret_val


# needs to read hbase and get the reveiwer info with the given id.  This will
# return json data with all the reviewer's information...need to decide what
# that is.  Also, need to calculate the reveiwer's Shill Index and word cloud...
def getReviewerInfo(rid):
  cursor = cnx.cursor()
  query = ("SELECT rname, truth, inx, imx, afinn, imwords, inwords FROM review "
           "WHERE rid = %s and evaluate = '1'")
  cursor.execute(query, (rid,))
  eval_cnt = 0
  shill_cnt = 0
  inx_total = 0.0
  imx_total = 0.0
  afinn_total = 0.0
  im_words = dict()
  in_words = dict()
  for (rname, truth, inx, imx, afinn, imwords, inwords) in cursor:
    rimw = json.loads(imwords)
    for w in rimw.keys():
      if w in im_words.keys():
        rimw[w] = float(im_words[w]) + float(rimw[w])
    im_words.update(rimw)
    
    rinw = json.loads(inwords)
    for w in rinw.keys():
      if w in in_words.keys():
        rinw[w] = float(in_words[w]) + float(rinw[w])
    in_words.update(rinw)

    inx_total += float(inx)
    imx_total += float(imx)
    afinn_total += float(afinn)
    eval_cnt += 1
    if truth == 0:
      shill_cnt += 1  
     
  if (eval_cnt > 0):
    return [{'sindex': shill_cnt/eval_cnt, 'rcount': eval_cnt,
             'scount': shill_cnt, 'senx': afinn_total/eval_cnt,
             'imx': imx/eval_cnt, 'inx': inx/eval_cnt, 'rname': rname,
             'imwords': json.dumps(im_words), 'inwords': json.dumps(in_words)}] 
    
  else:
    return [{'sindex':0, 'rcount':0, 'scount':0, 'senx':0, 'imx':0, 'inx':0, 'rname': rname,
             'imwords': json.dumps(im_words), 'inwords': json.dumps(in_words)}]
  cursor.close()
  return ret_val    
                 

# needs to read hbase and get a list of reviews that belong to the product
# with an id of pid.  This will return json data containing several fields ...
# which ones? ...
def getProdReviews(pid):
  product_reviews = []  
  cursor = cnx.cursor()
  query = ("SELECT rtext, score, evaluate, truth, rname, rid FROM review "
           "WHERE pid = %s order by utime")
  cursor.execute(query, (pid,))
  for (rtext, score, evaluate, truth, rname, rid) in cursor:
     product_reviews.append({'rtext': str(rtext), 'score': score,
                             'eval': evaluate, 'truth': truth,
                             'rname': rname, 'rid': rid})

  cursor.close()
  return product_reviews

# needs to read hbase and get the reveiwer's reviews with the given reviewer id.
# This will return json data with all the reveiws...need to decide what
# fields to return
def getReviewerReviews(rid):
  reviewer_reviews = []  
  cursor = cnx.cursor()
  query = ("SELECT rtext, score, evaluate, truth, pid FROM review "
           "WHERE rid = %s order by utime")
  cursor.execute(query, (rid,))
  for (rtext, score, evaluate, truth, pid) in cursor:
     reviewer_reviews.append({'rtext': str(rtext), 'score': score,
                              'eval':evaluate, 'truth': truth, 'pid': pid})
  cursor.close()
  return reviewer_reviews

# This will return 12 + 2 fields from a review to be used for training
def getTrainData():
  cursor = cnx.cursor()
  reviews = []
  names = ['id', 'truth', 'pprice', 'prank', 'fcount', 'hcount', 'score', 'tlen', 'wlen', 'utime', 'dtime',
           'afinn', 'inx', 'imx']
  query = ("SELECT id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, utime - mtime, "
           "afinn, inx, imx FROM review INNER JOIN "
           "(SELECT pid, min(utime) as mtime FROM review GROUP BY pid) AS mintab "
           "WHERE review.pid = mintab.pid AND train = 1 ORDER BY id")
  cursor.execute(query)
  for ( id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, dtime, afinn, inx, imx) in cursor:
    reviews.append([id, truth, pprice, prank, fcount, hcount, score, tlen, wlen,
                    utime, dtime, afinn, inx, imx])
  cursor.close()
  return (reviews, names)

# This will return 12 + 2 fields from a review to be used for predicting
def getUnTrainData():
  cursor = cnx.cursor()
  reviews = []
  names = ['id', 'truth', 'pprice', 'prank', 'fcount', 'hcount', 'score', 'tlen', 'wlen', 'utime', 'dtime',
           'afinn', 'inx', 'imx']
  query = ("SELECT id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, utime - mtime, "
           "afinn, inx, imx FROM review INNER JOIN "
           "(SELECT pid, min(utime) as mtime FROM review GROUP BY pid) AS mintab "
           "WHERE review.pid = mintab.pid AND train = 0 ORDER BY id")
  cursor.execute(query)
  for ( id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, dtime, afinn, inx, imx) in cursor:
    reviews.append([id, truth, pprice, prank, fcount, hcount, score, tlen, wlen,
                    utime, dtime, afinn, inx, imx])
  cursor.close()
  return (reviews, names)

# useful for plotting data features.
def getAllReviewFeatures():
  cursor = cnx.cursor()
  reviews = []
  names = ['truth', 'pprice', 'prank', 'fcount', 'hcount', 'score', 'tlen', 'wlen', 'utime', 'dtime',
           'afinn', 'inx', 'imx']
  query = ("SELECT truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, utime - mtime, "
           "afinn, inx, imx FROM review INNER JOIN "
           "(SELECT pid, min(utime) as mtime FROM review GROUP BY pid) AS mintab "
           "WHERE review.pid = mintab.pid ORDER BY id")
  cursor.execute(query)
  for ( truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, dtime, afinn, inx, imx) in cursor:
    reviews.append([truth, pprice, prank, fcount, hcount, score, tlen, wlen,
                    utime, dtime, afinn, inx, imx])
  cursor.close()
  return (reviews, names)

# predict using the 
def updateResult(tdata):
  cursor = cnx.cursor()
  upd_query = ("UPDATE review SET truth =  %s, evaluate = '1' WHERE id = %s")
  for item in tdata:
    print("updating data" + str(item[0]) + "  " + str(item[1]))
    cursor.execute(upd_query, (str(abs(item[1] - 1)), str(item[0])))
  cnx.commit()
  cursor.close() 

# evaluate any unevaluated reviews
def getUnevalReviews(pid):
  cnt = 0
  cursor = cnx.cursor()
  uneval_reviews = []
  names = ['id', 'truth', 'pprice', 'prank', 'fcount', 'hcount', 'score', 'tlen', 'wlen', 'utime', 'dtime',
           'afinn', 'inx', 'imx']
  query = ("SELECT id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, utime - mtime, "
           "afinn, inx, imx FROM review INNER JOIN "
           "(SELECT pid, min(utime) as mtime FROM review GROUP BY pid) AS mintab "
           "WHERE review.pid = mintab.pid AND review.pid = %s "
           "AND evaluate = 0 ORDER BY id")
  cursor.execute(query, (pid, ))
  for ( id, truth, pprice, prank, fcount, hcount, score, tlen, wlen, utime, dtime, afinn, inx, imx) in cursor:
    cnt += 1
    uneval_reviews.append([id, truth, pprice, prank, fcount, hcount, score, tlen, wlen,
                    utime, dtime, afinn, inx, imx])
  cursor.close()
  if (cnt > 0):
    return (uneval_reviews, names)
  else:
    return (None, None)


def getLastInsertID():
  cursor = cnx.cursor()
  cursor.execute("SELECT count(*) as cnt from review");
  for (cnt, ) in cursor:
    count = cnt
  cursor.close()
  return count

def createTrainingData():
  cursor = cnx.cursor()
  cursor.execute("UPDATE review SET train = 1 WHERE score = 1 OR score = 3 OR score = 5");
  for (cnt, ) in cursor:
    count = cnt
  cursor.close()
  return count
  
