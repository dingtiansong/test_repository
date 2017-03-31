# -*- coding: utf-8 -*-
'''
Created on 2016年10月12日

@author: song
'''
from pandas import Series

class Cutsent(object):
    '''
    classdocs
    '''
    factor=['D','P','T','R','M','Z','Y','X','U']

    dict = []
    maxFactor = 15
    def __init__(self, factor,maxFactor):
        '''
        Constructor
        '''
        if factor != '':
            self.factor = factor
        if maxFactor != '':
            self.maxFactor = maxFactor
        if sentence != '':
            self.sentence = sentence
            
        self.dict = self.dictCre(factor,maxFactor)
    
    ##生成元素对照字典
    def dictCre(self, factor, value_max):
        length = len(factor)+1    
        base = []    
        for i in range (length - 1):
            for j in range(1, value_max + 1):
                word = str(factor[i]) + str(j)
                base.append(word)
        aa = []
        for i in range(1, length):
            aa+=([i] * value_max)
        fdict=Series(aa, index = base)
        return fdict

    ##目标元素前面第一个元素
    def cutfactor_f1(self,index,sentence):
        if (index==0):
            value_f1=0
        else:
            value_f1_index=index-1
            value_f1=self.dict[sentence[value_f1_index]]
        return value_f1
    
    ##目标元素前面第二个元素    
    def cutfactor_f2(self,index,sentence):
        if (index<2):
            value_f2=0
        else:
            value_f2_index=index-2
            value_f2=self.dict[sentence[value_f2_index]]
        return value_f2
    ##目标元素前面第三个元素       
    def cutfactor_f3(self,index,sentence):
        if (index<3):
            value_f3=0
        else:
            value_f3_index=index-3
            value_f3=self.dict[sentence[value_f3_index]]
        return value_f3

    ##目标元素后面第一个元素       
    def cutfactor_b1(self,index,sentence):
        if (index==len(sentence)-1):
            value_b1=0
        else:
            value_b1_index=index+1
            value_b1=self.dict[sentence[value_b1_index]]
        return value_b1

    ##目标元素后面第二个元素    
    def cutfactor_b2(self,index,sentence):
        if (index>len(sentence)-3):
            value_b2=0
        else:
            value_b2_index=index+2
            value_b2=self.dict[sentence[value_b2_index]]
        return value_b2

    ##目标元素后面第三个元素    
    def cutfactor_b3(self,index,sentence):
        if (index>len(sentence)-4):
            value_b3=0
        else:
            value_b3_index=index+3
            value_b3=self.dict[sentence[value_b3_index]]
        return value_b3
    
    # def factorset(index,sentence,needfactor):
    #     num=0
    #     for factor in sentence[:index]:
    #         if factor in needfactor:
    #             num+=1
    #     return num
    
            
    ##目标元素与前面第一个相同元素之间的距离        
    def cutfactor_len(self,sentence,index):
        if (index!=0): 
            for i in range(1,index+1):
                lengthcut=i-1
                indexb=index-i
    #             print i
                if sentence[indexb][0]==sentence[index][0] :
                    break
    #         lengthcut=lengthcut0
    #         if lengthcut0<(index-1):
    #                 lengthcut=lengthcut0
    #         else :
    #                 lengthcut=0                   
        else :
            lengthcut=0        
        return lengthcut
    def punctans(self,sentence):
        for e in sentence:
            if e == '，' or e ==',':
                sentence[sentence.index(e)]='Z1'
            elif e=='。' or e == '.':
                sentence[sentence.index(e)]='Y1'
            elif e==';' or e=='；':
                sentence[sentence.index(e)]='X1'
            elif e == '/n' :
                sentence[sentence.index(e)]='U1'
        return sentence        


    ##生成特征向量
    def fvector(self,sentence,factor0):
        index=sentence.index(factor0)
        sentence1=self.punctans(sentence)
        aa1=self.cutfactor_len(sentence1,index)  
        aa2=self.cutfactor_f1(index,sentence1)
        aa3=self.cutfactor_f2(index,sentence1)
        aa4=self.cutfactor_f3(index,sentence1)
        aa5=self.cutfactor_b1(index,sentence1)
        aa6=self.cutfactor_b2(index,sentence1)
        aa7=self.cutfactor_b3(index,sentence1)
        vector=[ aa2,aa3,aa4,aa5,aa6,aa7,aa1]
        return vector

##demo
if __name__=='__main__': 
        factor=['D','P','T','R','A','M','Z','Y','X','U']#,'。','；']
        sentence=['D1','P1','D2','R1','T2','R2','T3',',','D3','.','。',';','/n','T4','R4','D4','T5','R5']
        factor0=sentence[0]
        maxFactor=30
        cutvector=Cutsent( factor,maxFactor)
#         print cutvector.dictCre(factor, maxFactor)
#         print cutvector.punctans(sentence)
#         print cutvector.cutfactor_b1(1, sentence)
        for factor in sentence:
            aa=cutvector.fvector(sentence, factor)
            print aa
#         print Cutsent.punctans(sentence)  
#         print sentence
        # print dict
        # def cutfactor_cab(index,sentence):
