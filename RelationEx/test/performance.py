# -*- coding: utf-8 -*-
'''
Created on 2016年8月23日

@author: song
'''
from test.getProductRelation import getProductRelation
from sklearn import svm
import numpy
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import cross_val_score
from numpy import mean
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn import metrics
import random
import numpy as np
# from test.mlmodel import svmmodel

    ### convert data type 

factor=['D','P','T','M','R']
needfactor=['D','P','T','M']
#dict = dictCre(factor,15)
# sentence=['D1','T1','M1','P1','M2','P2','P3']
# correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
sentence=['D1','P1','T1','R1','T2','R2']
correct_set=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])

maxFactor = 15
numsentence=130
modeltype='train_modelonline.m'
tmp = getProductRelation(factor,maxFactor,sentence,correct_set)
bb=tmp.getProduct(sentence,needfactor,modeltype)
print bb

# ##print tmp.Crexy(factor,numsentence)
#  
# ### svm model 
# data=tmp.Crexy(factor,numsentence)
# data[['distence','length']]=data[['distence','length']].astype(int)
# data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']]=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']].astype(int)
# # x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
# 
# x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
# y = data['relation_state'].astype(int)
# x1= numpy.array(x)
# y1=numpy.array(y)
# ###将序列混合均匀
# np.random.seed(0)
# indices = np.random.permutation(len(x))
# z=500
# train = x1[indices[:-z]]
# t_train = y1[indices[:-z]]
# test  = x1[indices[-z:]]
# t_test  = y1[indices[-z:]]
# # print data
# ##svm.SVC(kernel='poly', degree=3).fit(x, y)
# ##poly kernel
# # svmmodel = svm.SVC(kernel='poly').fit(x1, y1)
# ##linear kernel
# # svmmodel = svm.SVC(kernel='linear').fit(x1, y1)
# ##RBF kernel 
# svmmodel = svm.SVC(kernel='rbf',degree= 3).fit(x1, y1)
# ##print svmmodel.predict(x1)
# 
# ##save the onlinemodel
# # joblib.dump(svmmodel, "train_modelonline.m")
# 
# ##load the online model
# # svmmodel = joblib.load("train_modelonline.m")
# 
# 
# # ##save the offline model
# # joblib.dump(svmmodel, "train_modeloffline.m")
# # 
# # ##load the offline model 
# # svmmodel = joblib.load("train_modeloffline.m")
# ##########################################################################3
#  
# # train, test, t_train, t_test = cross_validation.train_test_split(x1, y1, test_size=0.3, random_state=2)
# 
# # svmmodel = svm.SVC(kernel='rbf',degree= 3).fit(train, t_train)
# ### model confusion matrix
# print 'confusion matrix ：' 
# print confusion_matrix(svmmodel.predict(test),t_test)
# print metrics.classification_report(t_test, svmmodel.predict(test))   
# ## cross-validation 
# print '\ncross_validation scores:'
# scores = cross_val_score(svmmodel, train, t_train, cv=5)
# print scores,mean(scores)
# 
# 
# ##输出判断特征矩阵
# # datajud=data
# # print type(data.values)
# # print type(data)
# # ypredict=svmmodel.predict(x1)
# # print len(ypredict)
# # datajud['predict']=ypredict
# # print datajud
# # datajud.to_csv('E:\outdata112.csv')
# 
# 
# # ###############################ANN############################
# # print 'ANN模型'
# # from scipy.ndimage import convolve
# # from sklearn import linear_model, datasets, metrics
# # from sklearn.cross_validation import train_test_split
# # from sklearn.neural_network import BernoulliRBM
# # from sklearn.pipeline import Pipeline
# #     ### convert data type 
# #   
# # factor=['D','P','T','M','R']
# # needfactor=['D','P','T','M']
# # #dict = dictCre(factor,15)
# # # sentence=['D1','T1','M1','P1','M2','P2','P3']
# # # correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
# # sentence=['D1','P1','T1','R1','T2','R2']
# # correct_set=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])
# # maxFactor = 15
# # numsentence=30
# # tmp = getProductRelation(factor,maxFactor,sentence,correct_set)
# # data=tmp.Crexy(factor,numsentence)
# # data[['distence','length']]=data[['distence','length']].astype(int)
# # data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']]=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']].astype(int)
# # # x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
# #   
# # x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
# # y = data['relation_state'].astype(int)
# # x1= numpy.array(x)
# # y1=numpy.array(y)
# # X_train, X_test, Y_train, Y_test = train_test_split(x1, y1,
# #                                                     test_size=0.5,
# #                                                     random_state=1)
# # # Models we will use
# # logistic = linear_model.LogisticRegression()
# # rbm = BernoulliRBM(random_state=0, verbose=True)
# #   
# # classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
# #  
# # ###############################################################################
# # # Training
# #  
# # # Hyper-parameters. These were set by cross-validation,
# # # using a GridSearchCV. Here we are not performing cross-validation to
# # # save time.
# # rbm.learning_rate = 0.06
# # rbm.n_iter = 20
# # # More components tend to give better prediction performance, but larger
# # # fitting time
# # rbm.n_components = 100
# # logistic.C = 6000.0
# #  
# # # Training RBM-Logistic Pipeline
# # classifier.fit(X_train, Y_train)
# #  
# # # Training Logistic regression
# # logistic_classifier = linear_model.LogisticRegression(C=100.0)
# # logistic_classifier.fit(X_train, Y_train)
# #  
# # ###############################################################################
# # # Evaluation
# #  
# # print()
# # print("Logistic regression using RBM features:\n%s\n" % (
# #     metrics.classification_report(
# #         Y_test,
# #         classifier.predict(X_test))))
# #  
# # print("Logistic regression using raw pixel features:\n%s\n" % (
# #     metrics.classification_report(
# #         Y_test,
# #         logistic_classifier.predict(X_test))))
# # # 
# # # ###############################################################################
# # print('Bagging meta-estimator :')
# # from sklearn.ensemble import BaggingClassifier
# # from sklearn.neighbors import KNeighborsClassifier
# # from sklearn import linear_model, datasets, metrics
# # from sklearn.cross_validation import train_test_split
# # X_train, X_test, Y_train, Y_test = train_test_split(x1, y1,
# #                                                     test_size=0.2,
# #                                                     random_state=1)
# # 
# # bagging = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5)
# # 
# # ##############################decision trees##################################
# from sklearn import tree
# import pydotplus 
# clftree = tree.DecisionTreeClassifier()
# clf = clftree.fit(train,t_train)
# print 'Decision tree confusion matrix ：' 
# print confusion_matrix(clf.predict(train),t_train)
# print metrics.classification_report(t_train, clf.predict(train))   
# ## cross-validation 
# print '\ncross_validation scores:'
# scores = cross_val_score(clf, train, t_train, cv=5)
# print scores,mean(scores)
# # dot_data = tree.export_graphviz(clf, out_file=None) 
# # graph = pydotplus.graph_from_dot_data(dot_data) 
# # graph.write_pdf("iris.pdf") 
# # ######################################naive_bayes##############################
# 
# from sklearn.naive_bayes import GaussianNB
# gnb = GaussianNB()
# gnbclf=gnb.fit(train,t_train)
# print 'naive_bayes confusion matrix ：' 
# print confusion_matrix(gnbclf.predict(test),t_test)
# print metrics.classification_report(t_test, gnbclf.predict(test))   
# ## cross-validation 
# print '\ncross_validation scores:'
# scores = cross_val_score(gnbclf,train, t_train, cv=5)
# print scores,mean(scores)