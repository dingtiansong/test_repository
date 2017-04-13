# -*- coding: utf-8 -*-
'''
@Time : 2017/4/12 15:57

@author: song
'''
import pickle
import sys
import chardet
import numpy as np
import pandas as pd
from numpy import mean
from tagFactor import TagFactor
from sklearn import metrics
# from sklearn.metrics import confusion_matrix
from numpy import mean
from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import GaussianNB
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from sumdata import MatchFactor

if __name__=='__main__':
    import xlrd

    fname = "D:\\work\\tags\\orig_data\\orig_comp_data.xls"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "no sheet in %s named Sheet1" % fname
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows, ncols)
    # 获取第一行第一列数据
    cell_value = sh.cell_value(1, 1)
    # print cell_value

    row_list = []
    # 获取各行数据
    for i in range(1, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    print row_data[1]
    newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'
    with open(newdatapath2, 'rb') as f:
        data = pickle.load(f)
    dictpath='D:\\work\\tags\\data\\worddict.pkl'
    with open(dictpath, 'rb') as f:
        word_dict = pickle.load(f)
    datafpath='D:\\work\\tags\\data\\datafpath.pkl'
    with open(datafpath, 'rb') as f:
        ff = pickle.load(f)
    dataf=ff[0]
    y=ff[1]
    mf=MatchFactor()
    tf=TagFactor()
    sentence_index, all_redo_data=mf.gether_data(data)
    dict=mf.sentence_order(data,sentence_index)
    total_dict=mf.create_total_Dict(data)
    allsentence=[]
    gnb = GaussianNB()
    gnbclf = gnb.fit(dataf, y)

    with open('D:\\work\\tags\\data\\tagtestdata.txt') as f:
        test_data=f.readlines()
    needtag=['D','P']
    for i in range(1, nrows):
        sen=sh.row_values(i)[0]
        row_data = sh.row_values(i)
        sentence1=sen.decode('utf-8')
        final_tag_sentence, orig_factor, factor_list, sortkey\
            =mf.generate_tag_sentence(total_dict,needtag,sentence1)
        print sentence1
        print final_tag_sentence
        print orig_factor
        print factor_list
        for z in range(len(sortkey)):
            word_start_index=sortkey[z][0]
            word_end_index=sortkey[z][1]
            adjust_index=0
            meta_word=tf.create_word_list(sentence1,word_start_index,word_end_index,adjust_index)
            vector = tf.bag_of_words_2_vec(word_dict, meta_word)
            # print z,meta_word
            print sortkey[z],sentence1[sortkey[z][0]:sortkey[z][1]], \
                 factor_list[z],gnbclf.predict(vector)
        print '----------------------------------------------------------------'

    print mf.tag_factor.__doc__