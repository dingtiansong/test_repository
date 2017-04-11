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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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

    def find_factor_index(self,factor,type,sentence):
        '''
        找出所有句中所有factor的位置
        '''
        startindex=0
        numlist=[]
        while True:
            index=sentence.find(factor, startindex)
            # index2=index+len(factor)
            if index == -1:
                break
            numlist.append([index,type])
            # print numlist,'numlist$$$$$$$$$$'
            startindex=index+1
        return numlist

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
        temp_org_dict={}
        factor_index=[]
        factor_list=u''
        orig_factor = []
        for i in data_dict:
            for j in i[1]:
                # print j[0],'@@@@'
                temp_dict[str(j[0])] = j[1]
                temp_org_dict[str(j[0])] = i[0]

        # print temp_dict,'####）））））））'
        sortkey = sorted([int(i) for i in temp_dict.keys()])
        # print sortkey
        # print sortkey, len(sortkey), len(data_dict)
        for key in sortkey:
            orig_factor.append(temp_org_dict[str(key)])
            factor_list=factor_list+temp_dict[str(key)]
            factor_index.append((key,key+len(temp_org_dict[str(key)])))
            # print factor_list
        return orig_factor,factor_list,factor_index

    # def get_period(self,sentence):
    #     pattern=re.compile(r"(\\d{1,}(\\.\\d{1,})?)")
    #     factor=pattern.search(sentence)

    def get_price(self,sentence,pre_tag_factor_sentence,pre_data_dict):
        p_percent = re.compile(r'[0-9]{0,2}\.[0-9]{0,3}%?')
        # p_bp=re.compile(r'\+[0-9]*bp',re.I)
        p_num=re.compile(r'[0-9]{0,2}\.[0-9]{0,3}')
        result=p_percent.findall(sentence)
        # print result,'price@@@@@@@@@@@@@@@@@@@@@'
        if result:
            for i in result:
                word_index = self.find_factor_index(i,'R', sentence)
                pre_tag_factor_sentence.append(('R',word_index))
                pre_data_dict.append((i,word_index))
        # print pre_data_dict
        return pre_tag_factor_sentence,pre_data_dict

    def get_amount(self,sentence,pre_tag_factor_sentence,pre_data_dict):
        temp_dict=pre_data_dict
        temp_tag_sentence=pre_tag_factor_sentence
        # p_amount=re.compile(r'[0-9]\.?[0-9]*[个千]?[ewEW万亿]')
        p_amount=re.compile(ur'[0-9]\.?[0-9]*[个千]?[ewEW万亿]')
        # p_amount2=re.compile(r'[一二三四五六七八九两]')
        result=p_amount.findall(sentence)
        # print result, 'amount**********************'
        if result:
            for i in result:
                word_index = self.find_factor_index(i,'A', sentence)
                temp_tag_sentence.append(('A',word_index))
                temp_dict.append((i,word_index))
        # print temp_dict
        return temp_tag_sentence,temp_dict

    def generate_tag_sentence(self, total_dict, needtag, sentence):
        '''
        根据字典将原文转化为标注序列
        '''
        pre_data_dict = []
        tag_sentence = sentence
        right_orig_sentence = []
        pre_tag_factor_sentence=[]
        for i in needtag:
            for j in total_dict[i]:
                # jn = j.replace('\n', '')
                if j in tag_sentence and j != '':
                    #                     print jn,m
                    right_orig_sentence.append(j)
                    tag_sentence = tag_sentence.replace(j, i)
                    word_index = self.find_factor_index(j, i, sentence)
                    pre_tag_factor_sentence.append((i,word_index))
                    # print word_index,'************'
                    pre_data_dict.append((j, word_index))
        # print pre_tag_factor_sentence
        r1,r2=self.get_amount(sentence, pre_tag_factor_sentence, pre_data_dict)
        # print sentence
        # print r1,'金额'
        r3,r4=self.get_price(sentence,r1,r2)
        # print r3,'利率'
        # print r4,'dict###'
        # clear_tag_sentence = re.sub('[^DPTRM]', '', tag_sentence)##替换查找
        # print [sentence]
        #         print aaa
        # print clear_tag_sentence
        # tag_sentence2 = self.tag_factor(clear_tag_sentence)##del
        orig_factor, factor_list, sortkey=self.reverse_dict(r4)

        final_tag_sentence=self.tag_factor(factor_list)
        # print final_tag_sentence,'``````'
        # print orig_factor
        # print sortkey
        # for i in sortkey:
        #     print i,
        #     print sentence[i[0]:i[1]],
        #         dat=self.reverseDict(datadict)
        #                     print tagsentence
        return final_tag_sentence, orig_factor, factor_list, sortkey



if __name__=='__main__':
    newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'
    with open(newdatapath2, 'rb') as f:
        data = pickle.load(f)
    mf=MatchFactor()
    sentence_index, all_redo_data=mf.gether_data(data)
    dict=mf.sentence_order(data,sentence_index)
    total_dict=mf.create_total_Dict(data)
    allsentence=[]

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

    test_sentence2='''玫瑰诚借 1-7天  2亿，求小窗玫瑰玫瑰'''

    test_sentence3='''【经理】陈立广（唐山银行）(94696767)  14:32:17
 唐山银行（1900亿+城商行）近期业务：
1.【收】收资金，收资金，收资金，任意期限，价格美丽。欢迎各位领导同事小窗。
2.【出】各期限高高高价理财（4.6%-4.8%）,4.6%-4.8%,3w,7.2个亿,4千万,5亿,1亿
联系人：陈立广，电话：15176574515（微信同号）
            柳清：15130574269'''
    test_sentence4=' 3.24借7天1.2亿，押利率'
    needtag=['D','P','T']


    for i in all_redo_data:
        sentence3= dict[str(i[0])]
        sentence1= '\n'.join(sentence3.split('\n')[1:])
        sentence2 = sentence3.split('\n')[0]
        print sentence2 ,'^^^^^^^^^^^^^^^^^^'
        print sentence1
        final_tag_sentence, orig_factor, factor_list, sortkey\
            =mf.generate_tag_sentence(total_dict,needtag,sentence1)
        print final_tag_sentence
        print orig_factor
        print factor_list
        print  sortkey
        print '-------------------------------------------------------------------------------------'

    # for i in all_redo_data:
    #     test_sentence= dict[str(i[0])]
    #     price_regx = re.compile(r'[0-9]{0,2}\.[0-9]{0,3}%')
    #     period_regx = re.compile(r'[0-9]\.?[0-9]*[个千]?[ewEW万亿]')
    #     print 'price match:', price_regx.findall(test_sentence)
    #     print 'period match:', period_regx.findall(test_sentence)
    #     print test_sentence

    # price_regx = re.compile(r'[0-9]{0,2}\.[0-9]{0,3}%')
    # amount_regx=re.compile(r'[0-9]\.?[0-9]*[千个]?[weWE万亿]')
    # temp_regx=re.compile(r'亿')
    # print temp_regx.findall(test_sentence3)
    # zz= amount_regx.findall(test_sentence3)
    # print price_regx.findall(test_sentence3)
    # print zz
    # print mt.endpos
    # import sys
    # print sys.getdefaultencoding()
    # for i in zz:
    #     print test_sentence3.find(i),test_sentence3.find(i)+len(i)
    #     print test_sentence3[test_sentence3.find(i):test_sentence3.find(i)+len(i)]
