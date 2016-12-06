# Python version
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))

# Load libraries
import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import mysql.connector
from mysql.connector import errorcode
import data

# db timing out on this, so had to do this manually
#data.createTrainingData()

(reviews, names) = data.getTrainData()
dataset = pandas.DataFrame(data = reviews, columns=names)
print (dataset.shape)

# Split-out validation dataset

# first column of dataset contains ids
# the next 10 columns contain the feature vector
array=dataset.values
I = array[:,0]
# in a supervised model the 2nd column is the expected result, else,
# column where the result will be populated
R = array[:,1]
X = array[:,2:]
#validation_size = 0.20
#seed = 7
#X_train, X_validation, Y_train, Y_validation =  \
#           cross_validation.train_test_split(X, R, test_size=validation_size,
#                                      random_state=seed)
#num_folds = 10
#num_instances = len(X_train)
#scoring = 'accuracy'

kmeans = KMeans(n_clusters = 2, random_state = 1).fit(X)
data.updateResult(zip(I, kmeans.labels_))

(reviews, names) = data.getUnTrainData()
dataset = pandas.DataFrame(data = reviews, columns=names)
print (dataset.shape)


# first column of dataset contains ids
# the next 10 columns contain the feature vector
array=dataset.values
I = array[:,0]
X = array[:,2:]
data.updateResult(zip(I, kmeans.predict(X)))

(reviews, names) = data.getAllReviewFeatures()
dataset = pandas.DataFrame(data = reviews, columns=names)

print (dataset.shape)
#print (dataset.head(2))
#print (dataset.describe())
dataset.plot(kind='box', subplots=True, layout=(4,4), sharex=False, sharey=False)
plt.show()
dataset.hist()
plt.show()
scatter_matrix(dataset)
plt.show()

# Spot Check Algorithms
#models = []
#models.append(('LR', LogisticRegression()))
#models.append(('LDA', LinearDiscriminantAnalysis()))
#models.append(('KNN', KNeighborsClassifier()))
#models.append(('CART', DecisionTreeClassifier()))
#models.append(('NB', GaussianNB()))
#models.append(('SVM', SVC()))
# evaluate each model in turn
#results = []
#names = []
#for name, model in models:
#	kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
#	cv_results = cross_validation.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
#	results.append(cv_results)
#	names.append(name)
#	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#	print(msg)

# Compare Algorithms
#fig = plt.figure()
#fig.suptitle('Algorithm Comparison')
#ax = fig.add_subplot(111)
#plt.boxplot(results)
#ax.set_xticklabels(names)
#plt.show()

# Make predictions on validation dataset
#nb = GaussianNB()
#nb.fit(X_train, Y_train)
#names = ['id', 'pprice', 'prank', 'fcount', 'hcount', 'tlen', 'wlen', 'dtime',
#         'afinn', 'inx', 'imx']
#query = ("SELECT id, pprice, prank, fcount, hcount, tlen, wlen, utime - mtime,"
#         "afinn, inx, imx FROM review inner join (select pid, min(utime) as mtime"
#         " from review group by pid) as mintab where review.pid = mintab.pid "
#           " and evaluate is null order by id")
#uneval_reviews = []
#cursor.execute(query)
#for ( id, pprice, prank, fcount, hcount, tlen, wlen, dtime, afinn, inx, imx) in cursor:
#      uneval_reviews.append([id, pprice, prank, fcount, hcount, tlen, wlen, dtime, afinn, inx, imx])
#dataset = pandas.DataFrame(data = uneval_reviews, columns=names)
#print (dataset.shape)

# Split-out columns
#array=dataset.values
#I = array[:,0]
#X = array[:,1:10]

 
#predictions = nb.predict(X)
#upd_review = ("UPDATE review SET truth =  %s, evaluate = '1' WHERE id = %s")
#for i in list(zip(predictions, I)):
#  print(i[0], i[1])
#  cursor.execute(upd_review, (str(i[0]), str(i[1])))

#cnx.commit()
#cursor.close()
#cnx.close()

#print(predictions)
#print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
#print(classification_report(Y_validation, predictions))
