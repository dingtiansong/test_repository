#-*- coding:utf-8 -*-
'''
Created on 2016��8��22��

@author: Administrator
'''
import numpy as np
from pyasn1.compat.octets import null
from sklearn import svm
# import copy
from pandas import Series
from pandas import DataFrame
#from guidata.utils import pairs
# from sklearn.externals import joblib
# from sklearn import metrics
import random
import matplotlib.pyplot as plt  



class entityRelationExtractionModel(object):
    '''
    classdocs
    '''
    maxColumn = 5
    english = []
    list_rain = []
    clf_rbf = []
    dict = []
    maxFactor = 15
    
    def __init__(self, params = 5,maxFactor = 15,  list1 = ['D','P','T','R'], list2=['D1','T1','P1','R1','R2'], list3 = [['D1','P1','T1','R1'],['D1','P1','T1','R2']]):
        '''
        Constructor
        '''
        self.english = list1
        self.list_rain = [list2, list3]
        self.maxColumn = params
        self.dict = self.dictCre(list1,maxFactor)
    
    def getTrainEigenvector(self, tmp_train = [], english = [], column = []):
        if tmp_train == [] :
            tmp_train = self.list_rain
        if english == []:
            english = self.english
        else:
            self.english = english
        if column == []:
            column = self.maxColumn
        
        vector_feature = []
        relation = []
        bijection = []

        for [s1,s2] in tmp_train:
            #正例4元素对转正例2元素对
            relation2 = self.getTransFourTwo(s2)
            vector_feature1 = self.main_feature(english, column, s1, relation2)#д���������Ӹ���Ԫ��֮�������/��ϵ
            relation1 = [x[2][0] for x in vector_feature1]
            bijection1 = [x[0] for x in vector_feature1]
            vector_feature1 = [x[1] for x in vector_feature1]
            #vector_feature1 = np.matrix(vector_feature1)
            vector_feature = vector_feature + vector_feature1
            relation = relation + relation1
            bijection = bijection + bijection1
        
        vector_feature = np.matrix(vector_feature)
        
        return vector_feature,relation,bijection
    
    
    def getTestEigenvector1(self, sentence):
        factorMatrix=[]
        allrelation = self.getRelationSet(sentence)
        for pairs in allrelation:
            f1 = sentence.index(pairs[0])
            s1 = sentence.index(pairs[1])
            factorMatrix.append(self.structure_feature(self.english,sentence,f1,s1,self.maxColumn))
        return factorMatrix
    
    def getSVMModel(self, vector_feature, relation):
        #SVM训练
        return svm.SVC(kernel='rbf').fit(vector_feature, relation)
        
    def getSVMResult(self, clf_rbf, vector_feature):
        #SVM预测判断
        answer = []
        for iv in vector_feature:
            temp = np.array(iv).reshape((1, -1))
            answer.append(clf_rbf.predict(temp)[0])
        return answer
    
    def getExtraction(self, xList):
        xList = [x for x in xList if x[2] == 1]
        return self.getResult(xList)
    
    '''��������:��2����'''
    def feature(self, feature, base, base_value):
        if feature != null:
            base_value[base.index(feature)] = 1
            #print location
        
        return base_value
    
    def base_create(self, column,english):
        base=[]
        for i in range (len(english)):
            for j in range(1,column+1):
                word=str(english[i])+str(j)
                base.append(word)
        
        return base
    
    def structure_feature(self, english,a,f1,s1,column):
        #base=['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4','D1','D2','D3','D4']
        base = self.base_create(column,english)
        #print base
        bw = [0] * len(base)
        
        length = len(a)
        f,s = min(f1,s1),max(f1,s1)
        
        if f == 0:
            bwm1f = null
            bwm1l = null
        else:
            if f == 1:
                bwm1f = null
                bwm1l = a[f-1]
            else:
                bwm1f = a[f-2]
                bwm1l = a[f-1]
        
        mw1 = a[f]
        if (s-f) == 1:
            bwf = null
            bwl = null
            bwo = null
        else:
            bwf = a[f+1]
            bwl = a[s-1]
            if s-f == 2 or s-f == 3:
                bwo = null
            else:
                bwo = a[f+2:s-1]
        
        mw2 = a[s]
        if s == (length-1):
            bwm2f = null
            bwm2l = null
        else:
            if s == (length-2):
                bwm2f = a[s+1]
                bwm2l = null
            else:
                bwm2f = a[s+1]
                bwm2l = a[s+2]
        
        #print bwm1f,bwm1l,mw1,bwf,bwo,bwl,mw2,bwm2f,bwm2l
        bwm1f = self.feature(bwm1f, base, bw)
        bwm1l = self.feature(bwm1l, base, bw)
        mw1 = self.feature(mw1, base, bw)
        bwf = self.feature(bwf, base, bw)
        bwl = self.feature(bwl, base, bw)
        mw2 = self.feature(mw2, base, bw)
        bwm2f = self.feature(bwm2f, base, bw)
        bwm2l = self.feature(bwm2l, base, bw)
        bw = [0]*len(base)
        for word in bwo:
            bw = self.feature(word,base,bw)
        #     print bwm1f#ʵ��1ǰ�浹���ڶ�������
        #     print bwm1l#ʵ��1ǰ�浹����һ������
        #     print mw1#ʵ��1�Ĵ���
        #     print bwf#����ʵ��֮��ĵ�һ������
        #     print bw#����ʵ����ȥbwf��bwl֮��Ĵ���
        #     print bwl#����ʵ�������һ������
        #     print mw2#ʵ��2�Ĵ���
        #     print bwm2f#ʵ��2����ĵ�һ������
        #     print bwm2l#ʵ��2����ĵڶ�������
        feature_v = bwm1f+bwm1l+mw1+bwf+bw+bwl+mw2+bwm2f+bwm2l
        return feature_v
    
    def classification(self, a, b):
        if a in b:
            return 1
        elif [a[1],a[0]] in b:
            return 1
        else:
            return 0
    
    def main_feature(self, english, column, a, b=[]):
        vector_feature = []
        print len(b)
        if len(a) > 1:
            for i in range(len(a)-1):
                for j in range((i+1),len(a)):
                    tmp = self.structure_feature(english, a, i, j, column)
                    if len(b) > 0:
                        tmp.append([self.classification(tmp[0],b)])
                    vector_feature.append(tmp)
        return vector_feature
    
    
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
    
    def value_f1(self, index1, sentence):
        if(index1 == 0):
            value_f1 = 0           
        else:
            valuef1_index = index1-1
            value_f1=self.dict[sentence[valuef1_index]]
        return value_f1 
        
    def value_b1(self, index1,index2,sentence):
        if(index2-index1 == 1):
            value_b1 = 0 
        else :                
            valueb1_index = index1+1
            value_b1 = self.dict[sentence[valueb1_index]]
        return value_b1
        
    def value_f2(self, index2, index1, sentence):
        if(index2-index1 == 0):
            value_f2 = 0           
        else:
            valuef2_index=index2-1
            value_f2=self.dict[sentence[valuef2_index]]
        return value_f2
        
    def value_b2(self,index2,sentence):
        if(index2==len(sentence)-1):
            value_b2=0           
        else:
            valueb2_index=index2+1
            value_b2=self.dict[sentence[valueb2_index]]
        return value_b2
        
    def value_m(self,index1,index2,sentence):
        value_m=0
        if(index2-index1>2):
            for factor in sentence[index1+2:index2] :
                if (factor[0] in sentence[index1] or factor[0] in sentence[index2]):
                    value_m+=1
        return value_m
    
    ##Create feature vector 
    #构造特征向量
    #输入：2元素组，句子，构造规则
    #输出：特征向量            
    
    
    
    
    
    
    
    
    '''   ��������:��5����    '''
    def isGroup(self, xfind):
        tmp = ''.join(xfind)
        rt = True
        for e in self.english: 
            if e not in tmp:
                rt = False
                break
        return rt
    
    
    
    def realationset(self,factor):
        k=1
        realation_type=[]
        for i in range(0,len(factor)-1):
            for j in range(i+1,len(factor)):
                realation_type.append([factor[i],factor[j]])
                k+=1
        return realation_type
    
    def getFindResult0(self, xList, tmp):
        if [tmp[0], tmp[1]] in xList:
            return True
        elif [tmp[1], tmp[0]] in xList:
            return True
        else:
            return False
    
    def getFindResult(self, xList, xfind):
        if (self.getFindResult0(xList, [xfind[0],xfind[2]]) 
            and self.getFindResult0(xList, [xfind[0],xfind[3]])
            and self.getFindResult0(xList, [xfind[1],xfind[2]])
            and self.getFindResult0(xList, [xfind[1],xfind[3]])):
            return True
        else:
            return False
    
    def getResult(self, xList):
        n = len(xList)
        rt = []
        if n > 1:
            for i in range(n-1):
                for j in range(i+1,n):
                    xfind = xList[i][:2] + xList[j][:2]
                    if self.isGroup(xfind):
                        if self.getFindResult(xList, xfind):
                            xfind.sort()
                            if xfind not in rt:
                                rt.append(xfind)
        
        return rt
    
    #svmmodel = joblib.load("train_model.m")
    def getProduct(self,sentence,needfactor):
        factorMatrix=[]
        allrelation=self.getRelationSet(sentence)
        for pairs in allrelation:
            factorMatrix.append(self.fvactor(pairs[0], pairs[1], sentence))
#         featureMatrix={}
#         i=0
#         rel_type=self.realationset(needfactor)
        x = self.getTestEigenvector2(sentence)
        #svmmodel = joblib.load("train_model.m")        
        print x
#         y=range(len(x))
        #y=svmmodel.predict(x)        
        #for i in range(len(y)):
        #    factorMatrix.values()[i].append(y[i])  
        data_frame1=DataFrame(factorMatrix).T 
        #data_frame1.columns=['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length','relation_type','entity1R','entity2R','relation_est'] 
        return data_frame1
    def getTransEigenvector(self,dateSet,Type = 1):
        trainVector = []
        trainValue = []
        if Type == 1:
            for [sentence,relation4] in dateSet:
                trainVector = trainVector + test.getTestEigenvector1(sentence)
                relation2 = test.getTransFourTwo(relation4)
                trainValue = trainValue + test.getTrainValue(sentence, relation2)
        else:
            for [sentence,relation4] in dateSet:
                trainVector = trainVector + test.getTestEigenvector2(sentence)
                relation2 = test.getTransFourTwo(relation4)
                trainValue = trainValue + test.getTrainValue(sentence, relation2)
        return trainVector,trainValue
    ''' get test eigenvector'''
    def getTestEigenvector(self, sentence,Type = 1):
        if Type == 1:
            return self.getTestEigenvector1(sentence)
        else:
            return self.getTestEigenvector2(sentence)
    def getTestEigenvector2(self, sentence):
        factorMatrix=[]
        allrelation = self.getRelationSet(sentence)
        for pairs in allrelation:
            factorMatrix.append(self.fvactor(pairs[0], pairs[1], sentence))
        return factorMatrix
    def fvactor(self,entity1,entity2,sentence): 
        index1=min(sentence.index(entity1),sentence.index(entity2))
        index2=max(sentence.index(entity1),sentence.index(entity2))
        distence=index2-index1
        length=len(sentence)    
        factor1=self.value_f1(index1,sentence)
        factorself1=self.dict[entity1]
        factor2=self.value_b1(index1,index2,sentence)
        factor3=self.value_m(index1,index2,sentence)
        factor4=self.value_f2(index1,index2,sentence)
        factorself2=self.dict[entity2]
        factor5=self.value_b2(index2,sentence)
        fvactor=[factor1,factorself1,factor2,factor3,factor4,factorself2,factor5,distence,length]
        return fvactor
    '''get relation set from sentence'''
    def getRelationSet(self,sentence):
        all_set=[]
        for factor1 in sentence:
            for factor2 in sentence[sentence.index(factor1):len(sentence)]:
                if(factor1[0]!=factor2[0]):
                    all_set.append([factor1,factor2])
        return all_set
    '''get Train value from relation extraction'''
    def getTrainValue(self, sentence, relation2):
        trainValue = []
        allrelation = self.getRelationSet(sentence)
        for pairs in allrelation:
            trainValue.append(self.classification(pairs, relation2))
        return trainValue
    '''get test Value To Relation'''
    def getValueToRelation(self, testSet, testValue):
        relation2 = []
        for i in range(len(testValue)):
            if testValue[i] == 1:
                relation2.append(testSet[i])
        return relation2
    ''' relation number transformation: 2 to 4 or 4 to 2'''
    def getTransformation(self,extraction):
        rt = []
        if isinstance(extraction,list):
            if len(extraction) > 0:
                if isinstance(extraction[0],list):
                    if len(extraction[0]) == 4:
                        rt = self.getTransFourTwo(extraction)
                    elif len(extraction[0]) == 2:
                        rt = self.getTransTwoFour(extraction)
        return rt
    def getTransTwoFour(self, xList):
        n = len(xList)
        relation4 = []
        if n > 1:
            for i in range(n-1):
                for j in range(i+1,n):
                    xfind = xList[i][:2] + xList[j][:2]
                    if self.isGroup(xfind):
                        if self.getFindResult(xList, xfind):
                            xfind.sort()
                            if xfind not in relation4:
                                relation4.append(xfind)
        return relation4
    ''' get predict result from trainModel '''
    def getSVMRelation(self, trainModel, tmp_test, vType):
        predictValue = []
        predictRelation = []
        for sentence in tmp_test:
            #句子构造测试2元素对
            testSet = self.getRelationSet(sentence)
            #测试2元素对构造句子对应的特征向量
            testVector = self.getTestEigenvector(sentence,vType)
            #模型预测结果
            testValue = self.getSVMResult(trainModel, testVector)
            #根据预测结果和测试2元素对生成预测2元素对
            testRelation2 = self.getValueToRelation(testSet, testValue)
            #预测2元素对转4元素对
            testRelation4 = self.getTransTwoFour(testRelation2)
            #结果汇总
            predictValue = predictValue + (testValue)
            predictRelation.append(testRelation4)
        return predictValue,predictRelation
    def getTransFourTwo(self, extraction):
        relation2 = []
        for tmp in extraction:
            xList = self.getRelationSet(tmp)
            for pairs in xList:
                if self.classification(pairs, relation2) == 0:
                    relation2.append(pairs)
        return relation2
    def getRelationCompare(self,trainR4,predictR4):
        k = 0
        for tmp1 in trainR4:
            for tmp2 in predictR4:
                tmp1.sort() 
                tmp2.sort()
                if tmp1 == tmp2:
                    k = k + 1
                    #break
        return k
if __name__=='__main__':  
    
#     #样本句子
#     a = ['D1','P1','T1','T2','R1','P2','T3','R2','T4','R3','P3','T5','R4']
#     #正例
#     b = [['D1','P1','T1','R1'],
#          ['D1','P1','T2','R1'],
#          ['D1','P2','T3','R2'],
#          ['D1','P2','T4','R3'],
#          ['D1','P3','T5','R4']]
#     a1=['D1','P1','T1','R1','T2','R2']
#     b1=[['D1','P1','T1','R1'],['D1','P1','T2','R2']]
#      
#     a2=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
#     b2=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
#      
#     a3=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
#     b3=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
#      
#     a4=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
#     b4=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
#      
#     a5=['D1','P1','T1','R1','T2','R2','T3','R3']
#     b5=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3']]
#      
#     a6=['D1','P1','T1','R1','T2','R2','T3','R3']
#     b6=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3']]
#      
#     a7=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
#     b7=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
#      
#     a8=['D1','P1','T1','R1']
#     b8=[['D1','P1','T1','R1']]
#      
#     a9=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
#     b9=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
#      
#     a11=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
#     b11=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6']]
#      
#     a12=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
#     b12=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
#      
#     a13=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4']
#     b13=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4']]
#      
#     a14=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
#     b14=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
#      
#     a15=['D1','P1','T1','R1']
#     b15=[['D1','P1','T1','R1']]
#      
#     a16=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9','T10','R10']
#     b16=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9'],['D1','P1','T10','R10']]
#      
#     a17=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
#     b17=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
#      
#     a18=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
#     b18=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
#      
#     a19=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7']
#     b19=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7']]
#      
#     a20=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9']
#     b20=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9']]
#      
#     a10=['D1','P1','P2','T1','R1','T2','R2','T3','R3','T4','R4']
#     b10=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P2','T1','R1'],['D1','P2','T2','R2'],['D1','P2','T3','R3'],['D1','P2','T4','R4']]
#     
#     sentence19=['D1','P1','P2','P3','P4','P5','T1','R1']
#     correct_set19=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P3','T1','R1'],['D1','P4','T1','R1'],['D1','P5','T1','R1']]
#      
#     sentence20=['D1','T1','R1','P1','P2']
#     correct_set20=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence21=['D1','T1','R1','P1','P2']
#     correct_set21=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence22=['D1','T1','R1','P1','P2','P3']
#     correct_set22=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P3','T1','R1']]
#      
#     sentence23=['D1','T1','R1','P1','P2','P3']
#     correct_set23=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P3','T1','R1']]
#      
#     sentence24=['D1','R1','T1','P1','P2','P3']
#     correct_set24=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P3','T1','R1']]
#      
#     sentence25=['D1','T1','R1','P1','P2']
#     correct_set25=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence26=['D1','T1','R1','P1','P2']
#     correct_set26=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence27=['D1','R1','T1','P1']
#     correct_set27=[['D1','P1','T1','R1']]
#      
#     sentence28=['D1','T1','R1','P1']
#     correct_set28=[['D1','P1','T1','R1']]
#      
#     sentence29=['D1','T1','R1','R2','P1']
#     correct_set29=[['D1','P1','T1','R1'],['D1','P1','T1','R2']]
#      
#     sentence30=['D1','T1','R1','P1']
#     correct_set30=[['D1','P1','T1','R1']]
#      
#     sentence31=['D1','T1','R1','P1']
#     correct_set31=[['D1','P1','T1','R1']]
#      
#     sentence32=['D1','T1','R1','R2','P1']
#     correct_set32=[['D1','P1','T1','R1'],['D1','P1','T1','R2']]
#      
#     sentence33=['D1','T1','T2','R1','P1']
#     correct_set33=[['D1','P1','T1','R1'],['D1','P1','T2','R1']]
#      
#     sentence34=['D1','T1','T2','T3','R1','P1']
#     correct_set34=[['D1','P1','T1','R1'],['D1','P1','T2','R1'],['D1','P1','T3','R1']]
#      
#     sentence35=['D1','T1','R1','P1','P2']
#     correct_set35=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence36=['D1','T1','R1','R2','P1','P2']
#     correct_set36=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P1','T1','R2'],['D1','P2','T1','R2']]
#      
#     sentence37=['D1','T1','R1','P1','P2']
#     correct_set37=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence38=['D1','T1','T2','T3','R1','P1','P2']
#     correct_set38=[['D1','P1','T1','R1'],['D1','P1','T2','R1'],['D1','P1','T3','R1'],['D1','P2','T1','R1'],['D1','P2','T2','R1'],['D1','P2','T3','R1']]
#      
#     sentence39=['D1','T1','P1','P2','R1']
#     correct_set39=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence40=['D1','T1','P1','R1','T2','P2','R2']
#     correct_set40=[['D1','P1','T1','R1'],['D1','P2','T2','R2']]
#      
#     sentence41=['D1','R1','T1','P1']
#     correct_set41=[['D1','P1','T1','R1']]
#      
#     sentence42=['D1','P1','T1','R1']
#     correct_set42=[['D1','P1','T1','R1']]
#      
#     sentence43=['D1','P1','T1','R1']
#     correct_set43=[['D1','P1','T1','R1']]
#      
#     sentence44=['D1','T1','T2','R1','P1']
#     correct_set44=[['D1','P1','T1','R1'],['D1','P1','T2','R1']]
#      
#     sentence45=['D1','T1','R1','P1','P2']
#     correct_set45=[['D1','P1','T1','R1'],['D1','P2','T1','R1']]
#      
#     sentence46=['D1','T1','T2','R1','P1']
#     correct_set46=[['D1','P1','T1','R1'],['D1','P1','T2','R1']]
#      
#     sentence47=['D1','T1','R1','P1']
#     correct_set47=[['D1','P1','T1','R1']]
#      
#     sentence48=['D1','R1','P1','R2','P2','T1']
#     correct_set48=[['D1','P1','T1','R1'],['D1','P2','T1','R2']]
#      
#     sentence49=['D1','T1','R1','P1','P2','P3']
#     correct_set49=[['D1','P1','T1','R1'],['D1','P2','T1','R1'],['D1','P3','T1','R1']]
#      
#     sentence50=['D1','T1','R1','P1']
#     correct_set50=[['D1','P1','T1','R1']]




    
    
    
#     a20=['D3', 'T1', 'R1', 'T2', 'R2', 'T3', 'R3', 'T4', 'R4', 'T5', 'R5', 'T6', 'R6', 'T7', 'R7', 'P5', 'M1']
#     b20=[[ 'D3','P4','T1', 'R1'],['D3','P4','T2','R2'],['D3', 'P4','T3', 'R3'],['D3','P4', 'T4', 'R4'],['D3','P4', 'T5', 'R5'],['D3', 'P4','T6', 'R6'],['D3','P4', 'T7', 'R7']]
#      
#     a21=['T1', 'P1', 'D1', 'R1', 'M1']
#     b21=[['T1', 'P1', 'D1', 'R1']]
#     
#      
#     a24=['D1', 'P1', 'P2', 'T1', 'R1', 'M1']
#     b24=[['D1', 'P1', 'T1', 'R1'] ,['D1', 'P2', 'T1', 'R1']]
#     
#     a26=['P1', 'T1', 'P2', 'R1', 'D1', 'T2', 'P3', 'R2', 'M1', 'D2', 'D3', 'P4', 'D4', 'P5', 'P6']
#     b26=[['D1', 'T2', 'P3', 'R2']]
#     
#     a27=['D1', 'P1', 'P2', 'T1', 'R1']
#     b27=[['D1','T1','R1','P1'],['D1','T1','R1','P2']]
#      
#     a28=['D1', 'M1', 'P1', 'T1', 'R1', 'T2', 'R2']
#     b28=[['D1','T1','R1','P1'],['D1','T2','R2','P1']]
#     
#     a31=['D1', 'P1', 'M1', 'T1', 'R1']
#     b31=[['D1','T1','R1','P1']]

    
#     tmp_train = [[a2,b2]]
#     #元素
#     english=['D','P','T','R']
#     #每个特征中相同元素重复的次数
#     column=5#max（每个类别的个数）
#     maxFactor = 15
#     vType = 2
#     
#     
#     sentence = a2
#     relation4 = b2
#     
#     test = entityRelationExtractionModel(column,15, english)
#     
#     #句子构造训练2元素对
#     trainSet = test.getRelationSet(sentence)
#     
#     #训练2元素对构造句子对应的特征向量
#     trainVector = test.getTestEigenvector1(sentence)
#     print trainVector
#     #正例4元素对转正例2元素对
#     relation2 = test.getTransFourTwo(relation4)  
#     #2元素根据正例2元素对构造特征值
#     trainValue = test.getTrainValue(trainSet, relation2)
#     #特征向量叠加
#     #特征值向量叠加
    #训练样本
#     tmp_train = [[a2,b2]]
#     #测试对照样本
#     tmp_train0 = [[a2,b2]]
    sentence01 = ['D1','T1','M1','P1','M2','P2']
    correct_set01 = [['D1','T1','M1','P1'],['D1','T2','M2','P2']]
    sentence02 = ['D1','T1','M1','M2','P1','P2']
    correct_set02 = [['D1','T1','M1','P1'],['D1','T2','M2','P2'],['D1','T1','M2','P1'],['D1','T2','M1','P2']]
    sentence03 = ['D1','T1','M1','P1']
    correct_set03 = [['D1','T1','M1','P1']]
    sentence04 = ['D1','M1','T1','P1','P2']
    correct_set04 = [['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    sentence05 = ['D1','T1','M1','P1','M2','P2']
    correct_set05 = [['D1','T1','M1','P1'],['D1','T2','M2','P2']]
    sentence06 = ['D1','T1','P1','M1']
    correct_set06 = [['D1','T1','M1','P1']]
    sentence07 = ['D1','T1','M1','P1','P2']
    correct_set07 = [['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    sentence08 = ['D1','T1','T2','T3','M1','P1']
    correct_set08 = [['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1']]
    sentence09 = ['D1','T1','T2','T3','T4','M1','P1','P2']
    correct_set09 = [['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'],['D1','T4','M1','P1'],['D1','T1','M1','P2'],['D1','T2','M1','P2'],['D1','T3','M1','P2'],['D1','T4','M1','P2']]
    sentence10 = ['D1','T1','M1','P1','M2','P2']
    correct_set10 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    sentence11 = ['D1','T1','M1','P1','P2']
    correct_set11 = [['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    sentence12 = ['D1','T1','M1','P1','M2','P2']
    correct_set12 = [['D1','T1','M1','P1'],['D1','T2','M2','P2']]
    sentence13 = ['D1','T1','M1','P1','P2','P3']
    correct_set13 = [['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3']]
    sentence14 = ['D1','T1','M1','P1','M2','P2']
    correct_set14 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    sentence15 = ['D1','T1','M1','P1','P2']
    correct_set15 = [['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    sentence16 = ['D1','T1','M1','T2','M2','P1']
    correct_set16 = [['D1','T1','M1','P1'],['D1','T2','M2','P1']]
    sentence17 = ['D1','T1','M1','P1','P2','P3']
    correct_set17 = [['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3']]
    sentence18 = ['D1','T1','M1','P1','M2','P2']
    correct_set18 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    sentence19 = ['D1','P1','P2','P3','P4','P5','T1','M1']
    correct_set19 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'],['D1','P4','T1','M1'],['D1','P5','T1','M1']]
    sentence20 = ['D1','T1','M1','P1','P2']
    correct_set20 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence21 = ['D1','T1','M1','P1','P2']
    correct_set21 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence22 = ['D1','T1','M1','P1','P2','P3']
    correct_set22 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1']]
    sentence23 = ['D1','T1','M1','P1','P2','P3']
    correct_set23 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1']]
    sentence24 = ['D1','M1','T1','P1','P2','P3']
    correct_set24 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1']]
    sentence25 = ['D1','T1','M1','P1','P2']
    correct_set25 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence26 = ['D1','T1','M1','P1','P2']
    correct_set26 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence27 = ['D1','M1','T1','P1']
    correct_set27 = [['D1','P1','T1','M1']]
    sentence28 = ['D1','T1','M1','P1']
    correct_set28 = [['D1','P1','T1','M1']]
    sentence29 = ['D1','T1','M1','M2','P1']
    correct_set29 = [['D1','P1','T1','M1'],['D1','P1','T1','M2']]
    sentence30 = ['D1','T1','M1','P1']
    correct_set30 = [['D1','P1','T1','M1']]
    sentence31 = ['D1','T1','M1','P1']
    correct_set31 = [['D1','P1','T1','M1']]
    sentence32 = ['D1','T1','M1','M2','P1']
    correct_set32 = [['D1','P1','T1','M1'],['D1','P1','T1','M2']]
    sentence33 = ['D1','T1','T2','M1','P1']
    correct_set33 = [['D1','P1','T1','M1'],['D1','P1','T2','M1']]
    sentence34 = ['D1','T1','T2','T3','M1','P1']
    correct_set34 = [['D1','P1','T1','M1'],['D1','P1','T2','M1'],['D1','P1','T3','M1']]
    sentence35 = ['D1','T1','M1','P1','P2']
    correct_set35 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence36 = ['D1','T1','M1','M2','P1','P2']
    correct_set36 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2']]
    sentence37 = ['D1','T1','M1','P1','P2']
    correct_set37 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence38 = ['D1','T1','T2','T3','M1','P1','P2']
    correct_set38 = [['D1','P1','T1','M1'],['D1','P1','T2','M1'],['D1','P1','T3','M1'],['D1','P2','T1','M1'],['D1','P2','T2','M1'],['D1','P2','T3','M1']]
    sentence39 = ['D1','T1','P1','P2','M1']
    correct_set39 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence40 = ['D1','T1','P1','M1','T2','P2','M2']
    correct_set40 = [['D1','P1','T1','M1'],['D1','P2','T2','M2']]
    sentence41 = ['D1','M1','T1','P1']
    correct_set41 = [['D1','P1','T1','M1']]
    sentence42 = ['D1','P1','T1','M1']
    correct_set42 = [['D1','P1','T1','M1']]
    sentence43 = ['D1','P1','T1','M1']
    correct_set43 = [['D1','P1','T1','M1']]
    sentence44 = ['D1','T1','T2','M1','P1']
    correct_set44 = [['D1','P1','T1','M1'],['D1','P1','T2','M1']]
    sentence45 = ['D1','T1','M1','P1','P2']
    correct_set45 = [['D1','P1','T1','M1'],['D1','P2','T1','M1']]
    sentence46 = ['D1','T1','T2','M1','P1']
    correct_set46 = [['D1','P1','T1','M1'],['D1','P1','T2','M1']]
    sentence47 = ['D1','T1','M1','P1']
    correct_set47 = [['D1','P1','T1','M1']]
    sentence48 = ['D1','M1','P1','M2','P2','T1']
    correct_set48 = [['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    sentence49 = ['D1','T1','M1','P1','P2','P3']
    correct_set49 = [['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1']]
    sentence50 = ['D1','T1','M1','P1']
    correct_set50 = [['D1','P1','T1','M1']]
    
    sentence51=['D1','T1','M1','P1','M2','P2','M3','P3']
    correct_set51=[['D1','P1','T1','M1'],['D1','P1','T2','M2'],['D1','P1','T3','M3']]
    
    
    sentence52=['D1','T1','M1','T2','M2','P1']
    correct_set52=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence53=['D1','P1','T1','M1','P2','T2','M2','M3']
    correct_set53=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3']]
    
    
    sentence54=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
    correct_set54=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4']]
    
    
    sentence55=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
    correct_set55=[['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2']]
    
    
    sentence56=['D1','T1','M1','P1','M2','P2']
    correct_set56=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    
    
    sentence57=['D1','P1','T1','M1','T2','M2']
    correct_set57=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence58=['D1','T1','M1','P1','M2','P2']
    correct_set58=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence59=['D1','T1','M1','P1','M2','P2']
    correct_set59=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence60=['D1','T1','M1','P1','M2','P2']
    correct_set60=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence61=['D1','T1','M1','P1','M2','P2']
    correct_set61=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence62=['D1','T1','M1','P1','M2','P2']
    correct_set62=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence63=['D1','T1','M1','T2','M2','P1']
    correct_set63=[['D1','T1','M1','P1'],['D1','T2','M2','P1']]
    
    sentence64=['D1','T1','M1','P1','M2','P2']
    correct_set64=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence65=['D1','T1','P1','M1','T2','P2','M2']
    correct_set65=[['D1','P1','T1','M1'],['D1','P2','T2','M2']]
    
    sentence66=['D1','M1','P1','M2','P2','T1']
    correct_set66=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    
    
    sentence67=['D1','T1','M1','P1','M2','P2','M3','P3']
    correct_set67=[['D1','P1','T1','M1'],['D1','P1','T2','M2'],['D1','P1','T3','M3']]
    
    
    sentence68=['D1','T1','M1','T2','M2','P1']
    correct_set68=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence69=['D1','P1','T1','M1','P2','T2','M2','M3']
    correct_set69=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3']]
    
    
    sentence70=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
    correct_set70=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4']]
    
    
    sentence71=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
    correct_set71=[['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2']]
    
    
    sentence72=['D1','T1','M1','P1','M2','P2']
    correct_set72=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    
    
    sentence73=['D1','P1','T1','M1','T2','M2']
    correct_set73=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence74=['D1','T1','M1','P1','M2','P2']
    correct_set74=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence75=['D1','T1','M1','P1','M2','P2']
    correct_set75=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence76=['D1','T1','M1','P1','M2','P2']
    correct_set76=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence77=['D1','T1','M1','P1','M2','P2']
    correct_set77=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence78=['D1','T1','M1','P1','M2','P2']
    correct_set78=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence79=['D1','T1','M1','T2','M2','P1']
    correct_set79=[['D1','T1','M1','P1'],['D1','T2','M2','P1']]
    
    sentence80=['D1','T1','M1','P1','M2','P2']
    correct_set80=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence81=['D1','T1','P1','M1','T2','P2','M2']
    correct_set81=[['D1','P1','T1','M1'],['D1','P2','T2','M2']]
    
    sentence82=['D1','M1','P1','M2','P2','T1']
    correct_set82=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    
    
    sentence83=['D1','T1','M1','P1','M2','P2','M3','P3']
    correct_set83=[['D1','P1','T1','M1'],['D1','P1','T2','M2'],['D1','P1','T3','M3']]
    
    
    sentence84=['D1','T1','M1','T2','M2','P1']
    correct_set84=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence85=['D1','P1','T1','M1','P2','T2','M2','M3']
    correct_set85=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3']]
    
    
    sentence86=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
    correct_set86=[['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4']]
    
    
    sentence87=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
    correct_set87=[['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2']]
    
    
    sentence88=['D1','T1','M1','P1','M2','P2']
    correct_set88=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    
    
    sentence89=['D1','P1','T1','M1','T2','M2']
    correct_set89=[['D1','P1','T1','M1'],['D1','P1','T2','M2']]
    
    sentence90=['D1','T1','M1','P1','M2','P2']
    correct_set90=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence91=['D1','T1','M1','P1','M2','P2']
    correct_set91=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence92=['D1','T1','M1','P1','M2','P2']
    correct_set92=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence93=['D1','T1','M1','P1','M2','P2']
    correct_set93=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence94=['D1','T1','M1','P1','M2','P2']
    correct_set94=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence95=['D1','T1','M1','T2','M2','P1']
    correct_set95=[['D1','T1','M1','P1'],['D1','T2','M2','P1']]
    
    sentence96=['D1','T1','M1','P1','M2','P2']
    correct_set96=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    
    sentence97=['D1','T1','P1','M1','T2','P2','M2']
    correct_set97=[['D1','P1','T1','M1'],['D1','P2','T2','M2']]
    
    sentence98=['D1','M1','P1','M2','P2','T1']
    correct_set98=[['D1','P1','T1','M1'],['D1','P2','T1','M2']]
    column = 10#max（每个类别的个数）
    maxFactor = 15
    vType = 2
    english = ['D','P','T','M']
    allData = [[sentence01, correct_set01], [sentence02, correct_set02], [sentence03, correct_set03], [sentence04, correct_set04], [sentence05, correct_set05], [sentence06, correct_set06], [sentence07, correct_set07], [sentence08, correct_set08], [sentence09, correct_set09], [sentence10, correct_set10], [sentence11, correct_set11], [sentence12, correct_set12], [sentence13, correct_set13], [sentence14, correct_set14], [sentence15, correct_set15], [sentence16, correct_set16], [sentence17, correct_set17], [sentence18, correct_set18], [sentence19, correct_set19], [sentence20, correct_set20],
                [sentence21, correct_set21], [sentence22, correct_set22], [sentence23, correct_set23], [sentence24, correct_set24],[sentence25, correct_set25], [sentence26, correct_set26], [sentence27, correct_set27], [sentence28, correct_set28], [sentence29, correct_set29], [sentence30, correct_set30], [sentence31, correct_set31], [sentence32, correct_set32], [sentence33, correct_set33], [sentence34, correct_set34], [sentence35, correct_set35], [sentence36, correct_set36], [sentence37, correct_set37], [sentence38, correct_set38], [sentence39, correct_set39], [sentence40, correct_set40],
                 [sentence41, correct_set41], [sentence42, correct_set42], [sentence43, correct_set43], [sentence44, correct_set44], [sentence45, correct_set45], [sentence46, correct_set46], [sentence47, correct_set47], [sentence48, correct_set48], [sentence49, correct_set49], [sentence50, correct_set50], [sentence51, correct_set51], [sentence52, correct_set52], [sentence53, correct_set53], [sentence54, correct_set54], [sentence55, correct_set55], [sentence56, correct_set56], [sentence57, correct_set57], [sentence58, correct_set58], [sentence59, correct_set59], [sentence60, correct_set60],
                 [sentence61, correct_set61], [sentence62, correct_set62], [sentence63, correct_set63], [sentence64, correct_set64], [sentence65, correct_set65], [sentence66, correct_set66], [sentence67, correct_set67], [sentence68, correct_set68], [sentence69, correct_set69], [sentence70, correct_set70],[sentence71, correct_set71], [sentence72, correct_set72], [sentence73, correct_set73], [sentence74, correct_set74], [sentence75, correct_set75], [sentence76, correct_set76], [sentence77, correct_set77], [sentence78, correct_set78], [sentence79, correct_set79], [sentence80, correct_set80],
                 [sentence81, correct_set81], [sentence82, correct_set82], [sentence83, correct_set83], [sentence84, correct_set84], [sentence85, correct_set85], [sentence86, correct_set86], [sentence87, correct_set87], [sentence88, correct_set88], [sentence89, correct_set89], [sentence90, correct_set90],[sentence91, correct_set91], [sentence92, correct_set92], [sentence93, correct_set93], [sentence94, correct_set94], [sentence95, correct_set95], [sentence96, correct_set96], [sentence97, correct_set97], [sentence98, correct_set98]]
#     allData=[[sentence19,correct_set19],[sentence20,correct_set20],[sentence21,correct_set21],[sentence22,correct_set22],[sentence23,correct_set23],[sentence24,correct_set24],[sentence25,correct_set25],[sentence26,correct_set26],[sentence27,correct_set27],[sentence28,correct_set28],[sentence29,correct_set29],[sentence30,correct_set30],[sentence31,correct_set31],[sentence32,correct_set32],[sentence33,correct_set33],[sentence34,correct_set34],[sentence35,correct_set35],[sentence36,correct_set36],[sentence37,correct_set37],[sentence38,correct_set38],[sentence39,correct_set39],[sentence40,correct_set40],[sentence41,correct_set41],[sentence42,correct_set42],[sentence43,correct_set43],[sentence44,correct_set44],[sentence45,correct_set45],[sentence46,correct_set46],[sentence47,correct_set47],[sentence48,correct_set48],[sentence49,correct_set49],[sentence50,correct_set50]]
#     slist2=range(len(allData)-1,0,-1)
#     allData = [[a5,b5],[a1,b1],[a2,b2],[a3,b3],[a4,b4],[a6,b6],[a7,b7],[a8,b8],[a9,b9],[a10,b10],[a11,b11],[a12,b12],[a13,b13],[a14,b14],[a15,b15],[a16,b16],[a17,b17],[a18,b18],[a19,b19],[a20,b20],[sentence19,correct_set19],[sentence20,correct_set20],[sentence21,correct_set21],[sentence22,correct_set22],[sentence23,correct_set23],[sentence24,correct_set24],[sentence25,correct_set25],[sentence26,correct_set26],[sentence27,correct_set27],[sentence28,correct_set28],[sentence29,correct_set29],[sentence30,correct_set30],[sentence31,correct_set31],[sentence32,correct_set32],[sentence33,correct_set33],[sentence34,correct_set34],[sentence35,correct_set35],[sentence36,correct_set36],[sentence37,correct_set37],[sentence38,correct_set38],[sentence39,correct_set39],[sentence40,correct_set40],[sentence41,correct_set41],[sentence42,correct_set42],[sentence43,correct_set43],[sentence44,correct_set44],[sentence45,correct_set45],[sentence46,correct_set46],[sentence47,correct_set47],[sentence48,correct_set48],[sentence49,correct_set49],[sentence50,correct_set50]]#,[a21,b21],[a22,b22],[a23,b23],[a24,b24]]
    sList = range(len(allData)-1,0,-1)
#     print sList
#     print len(sList)
    
#     print slist2

    test_num=10
    slice2=random.sample(sList,test_num)
    print slice2#测试数据集
#     print '320323'
#     print len(alldata2)
#     slist2=range(len(alldata2)-1,0,-1)
#     print slist2
#     slice2=random.sample(slist2,30)
#     print slice2
#     for i in slice2:
#         print alldata2[i]
#     print '3333333333333333333333333333333333'
    i_range=[]
#     print allData[0]
    for i in range(test_num+1,len(sList)):
        i_range.append(i)
    sList11=[]
#     print i_range
    for i in sList:
        if i in slice2:
            pass
        else:
            sList11.append(i)
    for circle in range(1,9):
        scoreList = []
        for i in range(20,len(sList11)):
            tmp_train = []
            tmp_train0 = []
            slice1 = random.sample(sList11, i)
#             print '333333333333333333'
            print slice1
            print 'slice1,slice2'
            print slice2
                #slice2 = random.sample(sList, i)
            for j in sList:
                if j in slice1:
                    tmp_train.append(allData[j-1])
                if j in slice2:
                    tmp_train0.append(allData[j-1])
            #print tmp_train
            #带入模型的样本
            tmp_test = [x[0] for x in tmp_train0]
#             print tmp_train
#             print tmp_train0
            test = entityRelationExtractionModel(column,maxFactor, english)
            #生成模型训练集
            trainVector,trainValue = test.getTransEigenvector(tmp_train,vType)
            #训练模型
            trainModel = test.getSVMModel(np.matrix(trainVector), trainValue)
            #生成预测结果的参照集
            trainVector0,trainValue0 = test.getTransEigenvector(tmp_train0,vType)
            #生成预测结果
            predictValue,predictRelation = test.getSVMRelation(trainModel, tmp_test, vType)
#             print predictValue
#             print '222222222'
#             print predictRelation#预测的组合结果
           
            #预测结果对比参照集
            #print metrics.accuracy_score(trainValue0, predictValue)
            #print metrics.classification_report(trainValue0, predictValue)
            tp = 0
            fp = 0
            fn = 0
            tn = 0
            for i in  range(len(trainValue0)):
                if trainValue0[i] == 0 :
                    if predictValue[i] == 0:
                        tn = tn + 1
                    else:
                        fn = fn + 1
                else:
                    if predictValue[i] == 0:
                        fp = fp + 1
                    else:
                        tp = tp + 1
            Ap = 0
            if tn+fp > 0:
                Ap = Ap + tn*1.0/(tn+fp)*(fn+tn)
            if fn+tp > 0:
                Ap = Ap + tp*1.0/(fn+tp)*(fp+tp)
            Ap = Ap * 1.0 / (fp+tp+fn+tn)
            Ar = (tp+tn)*1.0/(fp+tp+fn+tn)     
            #print [Ap,Ar,2*Ap*Ar/(Ap+Ar)]
            #预测关系对比参照集
            xList = []
            Aprecision = 0
            Arecall = 0
            AtrainR4 = 0
            for i in range(len(tmp_train0)):
                trainR4 = tmp_train0[i][1]
                predictR4 = predictRelation[i]
                recall = test.getRelationCompare(trainR4,predictR4) *1.0 / len(trainR4) 
                if len(predictR4) > 0:
                    precision = test.getRelationCompare(trainR4,predictR4) *1.0 / len(predictR4)
                else:
                    precision = 0.0
                #f1score = 2.0*precision*recall/(recall + precision)
                Aprecision = Aprecision + precision*len(trainR4) 
                Arecall = Arecall + recall*len(trainR4)
                AtrainR4 = AtrainR4 + len(trainR4)
                #xList.append([precision,recall,f1score,len(trainR4),len(predictR4)])
            #print xList
            Aprecision = Aprecision/AtrainR4
            Arecall = Arecall/AtrainR4
            #print [Aprecision,Arecall,2*Aprecision*Arecall/(Arecall + Aprecision)]
#             print Arecall
#             print Aprecision
            scoreList.append([len(tmp_train),Ap,Ar,2*Ap*Ar/(Ap+Ar),Aprecision,Arecall,2*Aprecision*Arecall/(Arecall + Aprecision)])
        #输出
#         print np.matrix(scoreList)
#         print '333333222222222222'
        np.savetxt("filename"+str(circle)+".txt",scoreList)
    
     
    for i in range(1,9):
        plt.subplot(4, 2, i)  
        scoreList =  np.loadtxt("filename%s.txt" %i)
        xlabel = ['p','r','f1','r4p','r4r','r4f1']
        for i in range(1,len(scoreList[0])):
            plt.plot([x[0] for x in scoreList],[x[i] for x in scoreList],label=xlabel[i-1])
    plt.legend(loc='lower left')
    plt.show()    
    #绘图
     
#     plt.plot([x[0] for x in scoreList],[x[1] for x in scoreList],label = '0-1')
#     plt.plot([x[0] for x in scoreList],[x[4] for x in scoreList],label = 'r4')
#     plt.legend(loc='upper left')
#     xlabel = ['p','r','f1','r4p','r4r','r4f1']
#     for i in range(1,len(scoreList[0])):
#         plt.plot([x[0] for x in scoreList],[x[i] for x in scoreList],label=xlabel[i-1])
#          
#     plt.legend(loc='lower left')
#     plt.show()   