# -*- coding: utf-8 -*-
'''
@Time : 2017/3/31 14:55

@author: song
'''
import pickle
import numpy as np
import pandas as pd
from numpy import mean
import re

newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'

with open(newdatapath2, 'rb') as f:
    data = pickle.load(f)

def create_dict(data,f_type):
    dict=[]
    for i in data:
        if i[3]==f_type and i[1] not in dict:
            dict.append(i[1])
    return dict

def gether_data(data):
    sentence_index=[]
    for i in data:
        if i[7] not in sentence_index:
            sentence_index.append(i[7])
    all_redo_data=[]
    for i in sentence_index:
        redo_data=[]
        for j in data:
            if j[7]==i:
                redo_data.append([j[1],j[3],j[4],j[5],j[6]])
        all_redo_data.append([i,redo_data])
    return sentence_index, all_redo_data


def sentence_order(data,sentence_index):
    dict={}
    for i in sentence_index:
        for j in data:
            if j[7]==i:
                dict[str(i)]=j[2]
    return dict


T_Dict=create_dict(data,f_type=u'期限')
D_Dict=create_dict(data,f_type=u'方向')
P_Dict=create_dict(data,f_type=u'产品')

sentence_index, all_redo_data=gether_data(data)
dict=sentence_order(data,sentence_index)
for i in all_redo_data:
    for j in i[1]:
        print j[0],j[1],j[2],j[3]
    print '-------------------------------------------'
    print dict[str(i[0])]
    print '*******************************************'

