# -*- coding: utf-8 -*-
'''
Created on 2016年9月21日
@author: song
'''
from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from test.getProductRelation import getProductRelation
import numpy
    ### convert data type 

factor=['D','P','T','M','R']
needfactor=['D','P','T','M']
#dict = dictCre(factor,15)
# sentence=['D1','T1','M1','P1','M2','P2','P3']
# correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
sentence=['D1','P1','T1','R1','T2','R2']
correct_set=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])
maxFactor = 15
numsentence=30
tmp = getProductRelation(factor,maxFactor,sentence,correct_set)
data=tmp.Crexy(factor,numsentence)
data[['distence','length']]=data[['distence','length']].astype(int)
data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']]=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']].astype(int)
# x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]

x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
y = data['relation_state'].astype(int)
x1= numpy.array(x)
y1=numpy.array(y)
X_train, X_test, Y_train, Y_test = train_test_split(x1, y1,
                                                    test_size=0.2,
                                                    random_state=1)
# Models we will use
logistic = linear_model.LogisticRegression()
rbm = BernoulliRBM(random_state=0, verbose=True)

classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])

###############################################################################
# Training

# Hyper-parameters. These were set by cross-validation,
# using a GridSearchCV. Here we are not performing cross-validation to
# save time.
rbm.learning_rate = 0.06
rbm.n_iter = 20
# More components tend to give better prediction performance, but larger
# fitting time
rbm.n_components = 100
logistic.C = 6000.0

# Training RBM-Logistic Pipeline
classifier.fit(X_train, Y_train)

# Training Logistic regression
logistic_classifier = linear_model.LogisticRegression(C=100.0)
logistic_classifier.fit(X_train, Y_train)

###############################################################################
# Evaluation

print()
print("Logistic regression using RBM features:\n%s\n" % (
    metrics.classification_report(
        Y_test,
        classifier.predict(X_test))))

print("Logistic regression using raw pixel features:\n%s\n" % (
    metrics.classification_report(
        Y_test,
        logistic_classifier.predict(X_test))))

###############################################################################

