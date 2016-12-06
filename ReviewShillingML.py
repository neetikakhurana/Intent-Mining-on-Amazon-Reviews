#!flask/bin/python
from flask import Flask, jsonify, request, abort
from flask import make_response, current_app, url_for 

import sys
import scipy
import numpy
import pandas
import sklearn
import json
import data
from sklearn.cluster import KMeans
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# Supported models at this time
models = [{'name':'K-means Clustering', 'id':'1'},
          {'name': 'Gaussion NB', 'id':'2'}]

model = ()
def setTModel(mtype):
  (reviews, names) = data.getTrainData()
  dataset = pandas.DataFrame(data = reviews, columns=names)
  print ("num train samples " + str(dataset.shape))

  # first column of dataset contains ids
  # the next 10 columns contain the feature vector
  array=dataset.values
  I = array[:,0]
  # in a supervised model the 2nd column is the expected result, else,
  # column where the result will be populated
  R = array[:,1]
  X = array[:,2:]
  validation_size = 0.20
  seed = 7
  X_train, X_validation, Y_train, Y_validation =  \
           cross_validation.train_test_split(X, R, test_size=validation_size,
                                      random_state=seed)
  num_folds = 10
  num_instances = len(X_train)
  scoring = 'accuracy'
  
  if (mtype == 1): # do unsupervised Kmeans
    tmodel = KMeans(n_clusters = 2, random_state = 0).fit(X)
    data.updateResult(list(zip(tmodel.labels_, I)))
    data.commit()
  elif (mtype == 3): # supervised NB
    tmodel = GaussianNB()
    tmodel.fit(X_train, Y_train)

  else:
    tmodel = ()
    
  return tmodel


app = Flask(__name__)
with app.app_context():
    # within this block, current_app points to app.
  model = setTModel(1)
# still trying to learn the difference between using the above vs below lines 
#from werkzeug.local import LocalProxy
#LocalProxy(setTModel(1))


@app.route('/ReviewShillingML/v1.0/train', methods=['GET'])
def getModels():
  return jsonify({'models': models})


@app.route('/ReviewShillingML/v1.0/train/<int:mtype>', methods=['GET'])
def trainTModel(mtype):
  try:
    model = setTModel(mtype)
    return jsonify({'Model': [m['name'] for m in models if int(m['id']) == mtype][0],
                    'Ready': '1'})
  except:
    return jsonify({'Model': 'None', 'Ready': '0'})


@app.route('/ReviewShillingML/v1.0/predict', methods=['POST'])
def predictData():
  reviews = request.get_json(force=True)['reviews']
  names = request.get_json(force=True)['names']
  dataset = pandas.DataFrame(data = reviews, columns=names)
  print ("num uneval samples " + str(dataset.shape))

  array = dataset.values  
  I = array[:,0]
  X = array[:,2:]
  P = model.predict(X)  
  return jsonify({'result': list(zip(I.tolist(), P.tolist()))})


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5001'))
    except ValueError:
        PORT = 5001
    app.run(HOST, PORT)
