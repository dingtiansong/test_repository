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
        '''
        param : data 
        return: 要素字典
        '''
        T_Dict=self.create_dict(data,f_type=u'期限')
        D_Dict=self.create_dict(data,f_type=u'方向')
        P_Dict=self.create_dict(data,f_type=u'产品')
        M_Dict=self.create_dict(data,f_type=u'金额')
        R_Dict=self.create_dict(data,f_type=u'利率')
        total_dict=pd.Series([D_Dict,P_Dict,T_Dict,R_Dict,M_Dict],index=['D','P','T','R','M'])
        return total_dict

    def find_factor_index(self,factor,sentence):
        '''
        找出所有句中所有factor的位置
        '''
        startindex=0
        numlist=[]
        while True:
            index=sentence.find(factor, startindex)
            index2=index+len(factor)
            if index == -1:
                break
            numlist.append([index,index2])
            startindex=index+1
        return numlist

    def generate_tag_sentence(self, total_dict, needtag, sentence):
        '''
        根据字典将原文转化为标注序列
        '''
        data_dict = []
        tag_sentence = sentence
        right_orig_sentence = []
        for i in needtag:
            for j in total_dict[i]:
                # jn = j.replace('\n', '')
                if j in tag_sentence and j != '':
                    #                     print jn,m
                    right_orig_sentence.append(j)
                    tag_sentence = tag_sentence.replace(j, i)
                    word_start = self.find_factor_index(j, sentence)
                    print word_start
                    data_dict.append((j, word_start))
        clear_tag_sentence = re.sub('[^DPTRA]', '', tag_sentence)
        #         print aaa
        tag_sentence2 = self.tag_factor(clear_tag_sentence)
        #         dat=self.reverseDict(datadict)
        #                     print tagsentence
        return tag_sentence2, tag_sentence, data_dict

    def tag_factor(self, tag_sentence):
        '''
        对标注后序列进行编号
        '''
        replace_sentence = []
        slen = len(tag_sentence)
        for i in range(slen):
            if i == 0:
                temp_factor = tag_sentence[0] + str(1)
                #                 print tempfactor
            else:
                m = 0
                for j in tag_sentence[:i]:
                    if tag_sentence[i] == j:
                        m += 1
                temp_factor = tag_sentence[i] + str(m + 1)
                #                 print tempfactor
            replace_sentence.append(temp_factor)
        return replace_sentence

    def reverse_dict(self, data_dict):
        temp_dict = {}
        orig_factor = []
        for i in data_dict:
            if len(i[1]) == 1:
                temp_dict[str(i[1][0])] = i[0]
                #                 print i[0],i[1]
            else:
                for j in i[1]:
                    temp_dict[str(j)] = i[0]
        sortkey = sorted([int(i) for i in temp_dict.keys()])
        for key in sortkey:
            orig_factor.append(temp_dict[str(key)])
        return orig_factor



if __name__=='__main__':
    newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'
    with open(newdatapath2, 'rb') as f:
        data = pickle.load(f)
    mf=MatchFactor()
    sentence_index, all_redo_data=mf.gether_data(data)
    dict=mf.sentence_order(data,sentence_index)
    total_dict=mf.create_total_Dict(data)
    # allsentence=[]
    #
    # for i in all_redo_data:
    #     for j in i[1]:
    #         print j[0],j[1],j[2],j[3]
    #         print '匹配位置：', dict[str(i[0])].find(j[0])+13, dict[str(i[0])].find(j[0])+len(j[0])+13
    #         print dict[str(i[0])][j[2]-13:j[3]-13],'&&&&&&&&'
    #     print '-------------------------------------------'
    #     print dict[str(i[0])]
    #     allsentence.append(dict[str(i[0])])
    #     print '*******************************************'


    test_sentence=u'''湖滨农商行赵磊(1307956997)  14:53:08
 3.24借七天1亿，押利率'''
    test_sentence1=u'''
出  AA存单  3M4.95  ！
出  AA存单  3M4.95  ！
出  AA存单  3M4.95  ！'''
    test_sentence2=u'''玫瑰诚借 1-7天  2亿，求小窗玫瑰玫瑰'''
    needtag=['D','P','T','R','M']
    r1,r2,r3=mf.generate_tag_sentence(total_dict,needtag,test_sentence1)
