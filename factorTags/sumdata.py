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

newdatapath2 = 'D:\\work\\tags\\data\\newdata2.pkl'
with open(newdatapath2, 'rb') as f:
    data = pickle.load(f)

def create_dict(data,f_type):
    dict=[]
    for i in data:
        if i[3]==f_type:
            dict.append(i[1])
    return dict

T_Dict=create_dict(data,f_type=u'期限')
D_Dict=create_dict(data,f_type=u'方向')
P_Dict=create_dict(data,f_type=u'产品')

sentence=[]
for i in data:
    if i[2] not in sentence:
        sentence.append(i[2])

print len(sentence),len(data)
# for i in sentence:
#     for j in data:
#         if j[2]==i:
#             dict_sentence[]