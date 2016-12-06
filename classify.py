# Python version
import sys
# scipy
import scipy
# numpy
import numpy
# pandas
import pandas
# scikit-learn
import sklearn
import data
from sklearn.cluster import KMeans
model = ()

def trainModel(mtype, dataset):
  # first column of dataset contains ids
  # the next 10 columns contain the feature vector
  array=dataset.values
  I = array[:,0]
  # if it is a supervised model the 2nd column is the expected result
  if (mtype > 3):
    R = array[:,1]
    X = array[:2:]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation =  \
    cross_validation.train_test_split(X, Y, test_size=validation_size,
                                      random_state=seed)
    num_folds = 10
    num_instances = len(X_train)
    scoring = 'accuracy'
  else:
    X = array[:,1:]

  
  if (mtype == 1): # do unsupervised Kmeans
    kmeans = KMeans(n_clusters = 2, random_state = 0).fit(X)
    data.updateResult(list(zip(kmeans.labels_, I)))
    model = kmeans
  elif (mtype == 3): # supervised NB
    nb = GaussianNB()
    nb.fit(X_train, Y_train)
    model = nb
    

def predictData(dataset):
  array = dataset.values()
  I = array[:,0]
  X = array[:,1:]
  P = model.predict(X)
  return list(zip(I, P))
