# -*- coding: utf-8 -*-
'''
@Time : 2017/3/31 14:55

@author: song
'''
import pickle
import sys
import chardet
import numpy as np
import pandas as pd
from numpy import mean
import re
# print(sys.getdefaultencoding())

class MatchFactor():

    def len_sort(self,dictList):
        dictList.sort(lambda x,y :cmp(len(x),len(y)),reverse=True)
        return dictList


    def create_dict(self, data,f_type):
        dict=[]
        for i in data:
            if i[3]==f_type and i[1] not in dict:
                dict.append(i[1])
        dict=self.len_sort(dict)
        return dict

    def gether_data(self,data):
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



    def sentence_order(self,data,sentence_index):
        dict={}
        for i in sentence_index:
            for j in data:
                if j[7]==i:
                    dict[str(i)]=j[2]
        return dict

    def create_total_Dict(self,data):
        T_Dict=self.create_dict(data,f_type=u'期限')
        D_Dict=self.create_dict(data,f_type=u'方向')
        P_Dict=self.create_dict(data,f_type=u'产品')
        M_Dict=self.create_dict(data,f_type=u'金额')
        R_Dict=self.create_dict(data,f_type=u'利率')
        total_dict=[D_Dict,P_Dict,T_Dict,R_Dict,M_Dict]
        return total_dict

# def match_factor(sentence,total_dict):
#     for i in Dict:

if __name__=='__main__':
    newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'
    with open(newdatapath2, 'rb') as f:
        data = pickle.load(f)
    mf=MatchFactor()
    sentence_index, all_redo_data=mf.gether_data(data)
    dict=mf.sentence_order(data,sentence_index)
    total_dict=mf.create_total_Dict(data)
    allsentence=[]
    for i in all_redo_data:
        for j in i[1]:
            print j[0],j[1],j[2],j[3]
            print '匹配位置：', dict[str(i[0])].find(j[0])+13, dict[str(i[0])].find(j[0])+len(j[0])+13
            print dict[str(i[0])][j[2]-13:j[3]-13],'&&&&&&&&'
        print '-------------------------------------------'
        print dict[str(i[0])]
        allsentence.append(dict[str(i[0])])
        print '*******************************************'
    for i in total_dict:
        for j in i:
            print j