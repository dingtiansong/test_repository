# -*- coding: utf-8 -*-
'''
@Time : 2017/3/28 11:25

@author: song
'''
import chardet
import pickle
import numpy as np
import pandas as pd
from sklearn import metrics
# from sklearn.metrics import confusion_matrix
from numpy import mean
from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import GaussianNB
import re

class TagFactor():



    def create_word_list(self,sentence,word_start_index,word_end_index,adjust_index):

        if word_start_index==adjust_index:
            front_1_word='*'
            front_2_word='*'
        elif word_start_index==adjust_index+1 :
            front_1_word = '*'
            front_2_word=sentence[word_start_index-adjust_index-1]
        else:
            # print sentence
            front_1_word=sentence[word_start_index-adjust_index-2]
            front_2_word=sentence[word_start_index-adjust_index-1]
        if word_end_index==len(sentence)+adjust_index:
            back_1_word='*'
            back_2_word='*'
        elif word_end_index==len(sentence)+adjust_index-1:
            # print len(sentence),word_end_index,'^^^^'
            back_1_word = sentence[word_end_index-adjust_index-1]
            back_2_word='*'
        else:
            # print word_end_index,len(sentence),'-----'
            # print sentence
            back_1_word=sentence[word_end_index-adjust_index]
            back_2_word=sentence[word_end_index-adjust_index+1]

        tag_word=sentence[word_start_index-adjust_index:word_end_index-adjust_index]
        feature_word=[front_1_word,front_2_word,tag_word,back_1_word,back_2_word]
        return feature_word

    def create_data_set(self,data):
        data_set = []
        for meta_data in data:
            sentence, word_start_index, word_end_index=meta_data[2],meta_data[4],meta_data[5]
            meta_word_list=self.create_word_list(sentence,word_start_index,word_end_index,adjust_index=13)
            data_set.append(meta_word_list)
        return data_set

    def create_word_dict(self,data_set):
        word_set = set([])
        for document in data_set:
            word_set = word_set | set(document)
        return list(word_set)

    def bag_of_words_2_vec(self,word_dict,input_set):
        return_vec = [0]*len(word_dict)
        for word in input_set:
            if word in word_dict:
                return_vec[word_dict.index(word)] += 1
        return return_vec

    def create_data_matrix(self,data_set,word_dict):
        data_mt=[]
        for i in data_set:
            vector=self.bag_of_words_2_vec(word_dict,i)
            data_mt.append(vector)
        data_frame=pd.DataFrame(data_mt)
        return data_frame

    def print_result(self,data,y):
        gnb = GaussianNB()
        gnbclf = gnb.fit(dataf, y)
        # print 'naive_bayes confusion matrix ：'
        # print confusion_matrix(gnbclf.predict(dataf),y)
        cla_result = metrics.classification_report(y, gnbclf.predict(dataf))
        # print '准确率：', cla_result[179:183]
        # print '召回率：', cla_result[189:193]
        # print 'F1值：', cla_result[199:203]
        precision,recall,F1_score=cla_result[179:183],cla_result[189:193],cla_result[199:203]
        return [precision,recall,F1_score]


    # def predict_tags(self,sentence,tags):


if __name__=='__main__':
    path = 'D:\\work\\tags\\data\\learning_quote_origin_element2.pkl'
    newdatapath2 = 'D:\\work\\tags\\data\\newdata2.pkl'
    newdatapath3 = 'D:\\work\\tags\\data\\newdata3.pkl'
    dictpath='D:\\work\\tags\\data\\worddict.pkl'
    datafpath='D:\\work\\tags\\data\\datafpath.pkl'
    with open(newdatapath3, 'rb') as f:
        data = pickle.load(f)
    # newdata=[]
    # for i in range(len(data)):
    #     if i!=88:
    #         newdata.append(data[i])
    # f1 = file(newdatapath2, 'wb')
    # pickle.dump(newdata, f1, True)
    tf=TagFactor()
    data_set=tf.create_data_set(data)
    word_dict=tf.create_word_dict(data_set)
    # f1 = file(dictpath, 'wb')
    # pickle.dump(word_dict, f1, True)
    # print tf.bag_of_word_2_vec(word_dict,data_set[1])
    # print data_set[1]
    dataf=tf.create_data_matrix(data_set,word_dict)

    with open('C:\\Users\\John64pc\\Desktop\\work\\data.txt','rb') as f:
        textdata=f.readlines()
    tag_y=[]
    for i in textdata:
        if '-----' in i :
            tag_y.append(i[-3])
    y=[]
    for i in range(len(tag_y)):
        if tag_y[i] =='2' :
            y.append(0)
        else:
            y.append(int(tag_y[i]))
    ff=[dataf,y]
    # f2 = file(datafpath, 'wb')
    # pickle.dump(ff, f2, True)
 ######################################naive_bayes##############################

    # gnb = GaussianNB()
    # gnbclf = gnb.fit(dataf, y)
    # print 'naive_bayes confusion matrix ：'
    # # print confusion_matrix(gnbclf.predict(dataf),y)
    # cla_result = metrics.classification_report(y, gnbclf.predict(dataf))
    # # cross-validation
    # print cla_result
    # print '\n cross_validation scores:'
    # scores = cross_val_score(gnbclf,dataf, y, cv=4)
    # print scores ,mean(scores)
    # result=tf.print_result(dataf,y)
    # print result
########################################################################








