#-*- coding:utf-8 -*-
'''
Created on 20160923

@author: Administrator
'''
import numpy as np
#from pyasn1.compat.octets import null
from sklearn import svm
import copy
from pandas import Series
from pandas import DataFrame
import os
import pickle
import sys

#from guidata.utils import pairs
from sklearn.externals import joblib
# from sklearn import metrics
# import random
# import matplotlib.pyplot as plt  



class entityRelationExtractionModel(object):
    '''
    classdocs
    '''
    maxColumn = 5
    english = []
    list_rain = []
    clf_rbf = []
    dict = []
    maxFactor = 30
    
    def __init__(self, params = 5,maxFactor = 30,  list1 = ['D','P','T','R'], list2=['D1','T1','P1','R1','R2'], list3 = [['D1','P1','T1','R1'],['D1','P1','T1','R2']]):
        '''
        Constructor
        '''
        self.english = list1
        self.list_rain = [list2, list3]
        self.maxColumn = params
        self.dict = self.dictCre(list1,maxFactor)
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
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
        #print vector_feature
        #rbf  linear  poly  sigmoid
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
        if not feature:
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
            bwm1f = ''
            bwm1l = ''
        else:
            if f == 1:
                bwm1f = ''
                bwm1l = a[f-1]
            else:
                bwm1f = a[f-2]
                bwm1l = a[f-1]
        
        mw1 = a[f]
        if (s-f) == 1:
            bwf = ''
            bwl = ''
            bwo = ''
        else:
            bwf = a[f+1]
            bwl = a[s-1]
            if s-f == 2 or s-f == 3:
                bwo = ''
            else:
                bwo = a[f+2:s-1]
        
        mw2 = a[s]
        if s == (length-1):
            bwm2f = ''
            bwm2l = ''
        else:
            if s == (length-2):
                bwm2f = a[s+1]
                bwm2l = ''
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
        #print len(b)
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
    
    def getTransEigenvector(self,dateSet,Type = 1):
        trainVector = []
        trainValue = []
        if Type == 1:
            for [sentence,relation4] in dateSet:
                trainVector = trainVector + self.getTestEigenvector1(sentence)
                relation2 = self.getTransFourTwo(relation4)
                trainValue = trainValue + self.getTrainValue(sentence, relation2)
                
        else:
            k=0
            for [sentence,relation4] in dateSet:
                relation2 = self.getTransFourTwo(relation4)
                k=k+1
                tmp = self.getTrainValue(sentence, relation2)
                trainVector = trainVector + self.getTestEigenvector2(sentence)
                relation2 = self.getTransFourTwo(relation4)
                trainValue = trainValue + self.getTrainValue(sentence, relation2)
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
        factor4=self.value_f2(index2,index1,sentence)
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
    
    '''数据字典初始化
    sentence:list真实句子,relation4:list真实四元组,
    unitNum:dist各种元素出现的数量
    isTrain:value是否训练样本,isTest:value是否测试样本,
    relation2:list句子分解的二元组,
    vector:list二元组构造的特征向量,trueValue:list二元组关系真实结果
    predictValue:list预测二元组关系结果,isError:list预测结果是否错误
    predictRelation2:list预测结果构造的二元组,predictRelation4:list预测二元组构造的四元组,
    precision,recall,f1Score:value分别是预测结果的准确率，召回率，f1值
    precision2,recall2,f1Score2:value分别是预测结果构造的二元组准确率，召回率，f1值
    precision4,recall4,f1Score4:value分别是预测结果构造的四元组准确率，召回率，f1值
    '''
    def getSampleDist(self,sentence,correct_set):
        tmpDist={'sentence':sentence,'relation4':correct_set,'isTrain':0,'isTest':0}
        tmpDist['relation2'] = self.getRelationSet(sentence)
        #         #生成模型训练集
        #         trainVector,trainValue = test.getTransEigenvector([[sentence,correct_set]],1)
        #         tmpDist['vector1'] = trainVector
        #         trainVector,trainValue = test.getTransEigenvector([[sentence,correct_set]],2)
        #         tmpDist['vector2'] = trainValue
        #         tmpDist['value'] = trainValue
        tmpDist['unitNum'] = {}
        for i in sentence:
            if i[0] not in tmpDist['unitNum'].keys():
                tmpDist['unitNum'][i[0]] = 1
            else:
                tmpDist['unitNum'][i[0]] += 1
        #计算是否4个唯一元素，或3个唯一元素加1个可重复元素
        k1,k2 = 1,0
        for i in tmpDist['unitNum'].keys():
            k1 = k1 * tmpDist['unitNum'][i]
            k2 = max(k2 , tmpDist['unitNum'][i])
        if k1 == k2 and k2 == len(correct_set):
            tmpDist['isTrain'] = -1
            tmpDist['isTest'] = -1
        return tmpDist
    
    #
    
    def getDistTransEigenvector(self,xDist,vType):
        for i in xDist.keys():
            sentence = xDist[i]['sentence']
            correct_set = xDist[i]['relation4']
            trainVector,trainValue = self.getTransEigenvector([[sentence,correct_set]],vType)
            xDist[i]['vector'] = trainVector
            xDist[i]['trueValue'] = trainValue
        return xDist
    
    def getDistSVMModel(self,xDist):
        trainVector = []
        trainValue = []
        for i in xDist.keys():
            if xDist[i]['isTrain'] == 1:
                trainVector += xDist[i]['vector']
                trainValue += xDist[i]['trueValue']
        trainModel = self.getSVMModel(np.matrix(trainVector), trainValue)
        return trainModel
    
    def getDistSVMResult(self,trainModel, xDist):
        for i in xDist.keys():
            if xDist[i]['isTest'] == 1:
                trainVector = np.matrix(xDist[i]['vector'])
                testValue = self.getSVMResult(trainModel, trainVector)
                
                xDist[i]['predictValue'] = testValue
                xDist[i]['isError'] = [abs(testValue[j] - xDist[i]['trueValue'][j]) for j in range(len(testValue))]
                xDist[i]['predictRelation2'] = self.getValueToRelation(xDist[i]['relation2'], testValue)
                xDist[i]['predictRelation4'] = self.getTransTwoFour(xDist[i]['predictRelation2'])
                
                rtList=self.getResult2(xDist[i]['relation2'],xDist[i]['trueValue'],testValue)
                xDist[i]['precision'] = rtList['Ap']
                xDist[i]['recall'] = rtList['Ar']
                xDist[i]['f1Score'] = rtList['Af1']
                
                rtList=self.getResult4(self.getValueToRelation(xDist[i]['relation2'], xDist[i]['trueValue']),xDist[i]['predictRelation2'])
                xDist[i]['precision2'] = rtList['r4p']
                xDist[i]['recall2'] = rtList['r4r']
                xDist[i]['f1Score2'] = rtList['r4f1']
                
                rtList=self.getResult4(xDist[i]['relation4'],xDist[i]['predictRelation4'])
                xDist[i]['precision4'] = rtList['r4p']
                xDist[i]['recall4'] = rtList['r4r']
                xDist[i]['f1Score4'] = rtList['r4f1']
        return xDist
    
    #按句子进行评判
    def getResult2(self,Relation2,trainValue0,predictValue):
        rtList={'tp':0,'fp':0,'fn':0,'tn':0}
        for i in range(len(Relation2)):
            if trainValue0[i] == 0 :
                if predictValue[i] == 0:
                    rtList['tn'] += 1
                else:
                    rtList['fn'] += 1
            else:
                if predictValue[i] == 0:
                    rtList['fp'] += 1
                else:
                    rtList['tp'] += 1
        rtList['Ap'] = 0
        if rtList['tn']+rtList['fp'] > 0:
            rtList['Ap'] += rtList['tn']*1.0/(rtList['tn']+rtList['fp'])*(rtList['fn']+rtList['tn'])
        if rtList['fn']+rtList['tp'] > 0:
            rtList['Ap'] += rtList['tp']*1.0/(rtList['fn']+rtList['tp'])*(rtList['fp']+rtList['tp'])
        rtList['Ap'] = rtList['Ap']*1.0/(rtList['fp']+rtList['tp']+rtList['fn']+rtList['tn'])
        rtList['Ar'] = (rtList['tp']+rtList['tn'])*1.0/(rtList['fp']+rtList['tp']+rtList['fn']+rtList['tn'])
        if rtList['Ap']+rtList['Ar'] > 0:
            rtList['Af1'] = 2*rtList['Ap']*rtList['Ar']*1.0/(rtList['Ap']+rtList['Ar'])
        else:
            rtList['Af1'] = 0
        return rtList
    
    def getResult4(self,trainR4,predictR4):
        predictR0 = copy.deepcopy(predictR4)
        trainR0 = copy.deepcopy(trainR4)
        for i in range(len(trainR0)):
            trainR0[i].sort()
        for i in range(len(predictR0)):
            predictR0[i].sort() 
        
        recall = self.getRelationCompare(trainR0,predictR0) *1.0 / len(trainR0) 
        if len(predictR4) > 0:
            precision = self.getRelationCompare(trainR0,predictR0) *1.0 / len(predictR0)
        else:
            precision = 0.0
        if recall + precision > 0:
            f1score = 2*precision*recall * 1.0/(recall + precision)
        else:
            f1score = 0
        rtList={'r4p':precision,'r4r':recall,'r4f1':f1score,'r4tLen':len(trainR0),'r4pLen':len(predictR0)}
        return rtList
    
    #输出结果
    def getResult62(self,allDist):
        for i in allDist.keys():
            tmpDist = allDist[i]
            tDist = {}
            if 'isError' in tmpDist.keys():
                for j in range(len(tmpDist['isError'])):
                    if tmpDist['isError'][j] == 1:
                        xlist = sorted(tmpDist['relation2'][j])
                        xkeys = xlist[0][0] + xlist[1][0]
                        if xkeys in tDist.keys():
                            tDist[xkeys] += 1
                        else:
                            tDist[xkeys] = 1
                        xkeys = str(tmpDist['trueValue'][j])
                        if xkeys in tDist.keys():
                            tDist[xkeys] += 1
                        else:
                            tDist[xkeys] = 1
                        xkeys = xlist[0][0] + xlist[1][0] + str(tmpDist['trueValue'][j])
                        if xkeys in tDist.keys():
                            tDist[xkeys] += 1
                        else:
                            tDist[xkeys] = 1
            allDist[i]['totalError'] = tDist
        return allDist
     
    def getResultSave(self,allDist,vType=2,trainModel = ''):
        #构造数据特征向量
        allDist1 = self.getDistTransEigenvector(allDist,vType)
        #构造svm模型
        if trainModel == '':
            trainModel = self.getDistSVMModel(allDist1)
        #根据模型生成预测结果和评价指标
        allDist = self.getDistSVMResult(trainModel, allDist)
        return self.getResult62(allDist)
    
    
    #get the svm model from trainList=[[sentence01, correct_set01],...]
    def getListSVMModel(self,trainList,vType = 2):
        #过滤数据后的训练样本集合
        trainList1 = self.getSVMModelData(trainList)
        #构造特征向量组和01分类向量
        trainVector = []
        trainValue = []
        for [sentence,correct_set] in trainList1:
            vector,trueValue = self.getTransEigenvector([[sentence,correct_set]],vType)
            trainVector += vector
            trainValue += trueValue
        #构造svm模型
        trainModel = self.getSVMModel(np.matrix(trainVector), trainValue)
        return trainModel
    
    #del 4个唯一元素，或3个唯一元素加1个可重复元素的这种全连接形式的句子
    def getSVMModelData(self,trainData):
        resultData = []
        for [sentence,correct_set] in trainData:
            tmpDist = {}
            for element in sentence:
                if element[0] not in tmpDist.keys():
                    tmpDist[element[0]] = [element]
                else:
                    tmpDist[element[0]].append(element)
            #计算是否4个唯一元素，或3个唯一元素加1个可重复元素
            k1,k2 = 1,0
            for element in tmpDist.keys():
                k1 = k1 * len(tmpDist[element])
                k2 = max(k2 , len(tmpDist[element]))
            if k1 == k2 and len(tmpDist) == 4 and k2 == len(correct_set):
                pass
            else:
                resultData.append([sentence,correct_set])
        return resultData
    
    #返回4元组
    def getModelResult(self,testSentence,trainModel,vType = 2):
        #测试简单模型
        rt = self.getSimpleModel(testSentence)
        if rt == []:
            return self.getSVMModelResult(testSentence,trainModel,vType)
        else:
            return rt
    
    def getSVMModelResult(self,sentence,trainModel,vType = 2):
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
        return testRelation4
    def getSimpleModel(self,sentence):
        tmpDist = {}
        for element in sentence:
            if element[0] not in tmpDist.keys():
                tmpDist[element[0]] = [element]
            else:
                tmpDist[element[0]].append(element)
        #计算是否4个唯一元素，或3个唯一元素加1个可重复元素
        k1,k2 = 1,0
        for element in tmpDist.keys():
            k1 = k1 * len(tmpDist[element])
            k2 = max(k2 , len(tmpDist[element]))
        
        relation4 = []
        if k1 == k2 and len(tmpDist) == 4:
            for i in range(k1):
                tmp = []
                for element in tmpDist.keys():
                    if len(tmpDist[element]) == 1:
                        tmp.append(tmpDist[element][0])
                    else:
                        tmp.append(tmpDist[element][i])
                relation4.append(tmp)
        return relation4
    
class initializeModel(object):
    '''
    classdocs
    '''
    #模型初始化
    #1、没有模型时，优先建立模型
    #查找建模数据，若没找到，则用脚本数据存储为数据集
    modelPath = 'OnlineModel.pkl'
    dataPath = 'OnlineData.pickle'
    maxColumn = 5
    english = []
    list_rain = []
    clf_rbf = []
    dict = []
    maxFactor = 30
    
    def __init__(self, params = ''):
        '''
        Constructor
        '''
        if params.find('.pkl') > -1:
            self.modelPath = params
        elif params.find('.pickle') > -1:
            self.dataPath = params
    
    #加载线上数据
    def getDataList(self,dataPath,dataList = [],dataList0 = []):
        if os.path.exists(dataPath) and os.path.isfile(dataPath):
            with open(dataPath, 'rb') as f:
                allData = pickle.load(f)
        else:    
            allData = dataList0
        if isinstance(dataList, list) and len(dataList) == 2:
            if isinstance(dataList[0], list) and isinstance(dataList[1], list):
                allData.append(dataList)
                with open(dataPath, 'wb') as f:
                    pickle.dump(allData, f)
        return allData
    
    #生成模型并存储
    def getModel(self,modelPath,column,maxFactor, english,vType,dataList = [],isNew = True):
        if os.path.exists(modelPath) and os.path.isfile(modelPath) and isNew:
            #load model to trainModel
            test = entityRelationExtractionModel(column,maxFactor, english)
            trainModel = joblib.load(modelPath)
        else:
            allData = dataList
            test = entityRelationExtractionModel(column,maxFactor, english)
            trainModel = test.getListSVMModel(copy.deepcopy(allData),vType)
            #save model  
            joblib.dump(trainModel, modelPath, compress=3)
        return test,trainModel
    
    #加载并使用模型
    def getModelResult(self, test, trainModel, testSentence):
        if isinstance(testSentence,list) and len(testSentence) > 0:
            testRelation4 = test.getModelResult(testSentence,trainModel)
        else:
            testRelation4 = []
        return testRelation4
    
    #模型调用函数
    def getEntityRelationResult(self, sentence = ''):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        typeList = ['Online','Offline']
        testRelation4 = []
        for vType in typeList:
            tmp = self._getEntityRelationResult(sentence, vType)
            if tmp != ['ERROR'] and tmp:
                testRelation4 = testRelation4 + tmp
        return testRelation4
    
    def _getEntityRelationResult(self, sentence = '', vType='Online'):
        typeList = ['Online','Offline']
        testRelation4 = ['ERROR']
        if isinstance(sentence,basestring) and len(sentence) > 0 and isinstance(vType,basestring) and vType in typeList:
            if vType == 'Online':
                column = 30#max（每个类别的个数）
                maxFactor = 30
                modelType = 2
                english = ['D','P','T','A']
                modelPath = 'OnlineModel.pkl'
                dataPath = 'OnlineData.pickle'
                dataList0 = self.getOnlineData()
            elif vType == 'Offline':
                column = 30#max（每个类别的个数）
                maxFactor = 30
                modelType = 2
                english = ['D','P','T','R']
                modelPath = 'OfflineModel.pkl'
                dataPath = 'OfflineData.pickle'
                dataList0 = self.getOfflineData()
            sentence0 = self.getDataToList(sentence,english)
            if len(sentence0) > 0:
                #读取数据
                allData = self.getDataList(dataPath,[],dataList0)
                #读取模型
                test, trainModel = self.getModel(modelPath,column,maxFactor, english,modelType,allData)
                #运行模型，获得结果
                relation4 = self.getModelResult(test, trainModel, sentence0)
                if len(relation4) > 0:
                    testRelation4 = ["|".join(x) for x in relation4]
        return testRelation4
    
    #更新数据及模型
    def updateDataList(self, sentence = '',correct_set = [], vType = 'Online'):
        typeList = ['Online','Offline']
        tmp = 0
        if isinstance(sentence,basestring) and isinstance(correct_set,list) and isinstance(vType,basestring) and vType in typeList:
            #数据初始化
            if vType == 'Online':
                column = 30 #max（每个类别的个数）
                maxFactor = 30
                modelType = 2
                english = ['D','P','T','A']
                modelPath = 'OnlineModel.pkl'
                dataPath = 'OnlineData.pickle'
                dataList0 = self.getOnlineData()
            elif vType == 'Offline':
                column = 30#max（每个类别的个数）
                maxFactor = 30
                modelType = 2
                english = ['D','P','T','R']
                modelPath = 'OfflineModel.pkl'
                dataPath = 'OfflineData.pickle'
                dataList0 = self.getOfflineData()
            #句子转元素list
            sentence0 = self.getDataToList(sentence,english)
            correct_set0 = []
            #人工校对的元素关系组合转list
            for tmp_set in correct_set:
                tmpList = self.getDataToList(tmp_set,english)
                if tmpList != []:
                    correct_set0.append(tmpList)
            
            if len(sentence0) > 0 and len(correct_set0) > 0:
                dataList = [sentence0, correct_set0]
            else:
                dataList = []
            
            if isinstance(dataList, list) and len(dataList) > 0:
                for x in dataList:
                    if x and x[0] in english:
                        tmp = 1
                        break
            if tmp == 0:
                #更新数据
                allData = self.getDataList(dataPath,dataList,dataList0)
                #更新模型
                test, trainModel = self.getModel(modelPath,column,maxFactor, english,modelType,allData,False)
        else:
            tmp = 1
        return tmp
    
    def getDataToList(self,sentence,english):
        rtList = []
        tmpEn = []
        if isinstance(sentence, basestring) and sentence.find('|')> -1:
            xList = sentence.split('|')
            for x in xList:
                if x and x[0] in english:
                    rtList.append(x)
                    tmpEn.append(x[0])
            if len([x for x in english if x in tmpEn]) != 4:
                rtList = []
        return rtList
    
    def getOnlineData(self):
        sentence01 = ['D1','T1','A1','P1','A2','P2']
        correct_set01 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence02 = ['D1','T1','A1','A2','P1','P2']
        correct_set02 = [['D1','T1','A1','P1'],['D1','T1','A2','P2'],['D1','T1','A2','P1'],['D1','T1','A1','P2']]
        sentence03 = ['D1','T1','A1','P1']
        correct_set03 = [['D1','T1','A1','P1']]
        sentence04 = ['D1','A1','T1','P1','P2']
        correct_set04 = [['D1','T1','A1','P1'],['D1','T1','A1','P2']]
        sentence05 = ['D1','T1','A1','P1','A2','P2']
        correct_set05 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence06 = ['D1','T1','P1','A1']
        correct_set06 = [['D1','T1','A1','P1']]
        sentence07 = ['D1','T1','A1','P1','P2']
        correct_set07 = [['D1','T1','A1','P1'],['D1','T1','A1','P2']]
        sentence08 = ['D1','T1','T2','T3','A1','P1']
        correct_set08 = [['D1','T1','A1','P1'],['D1','T2','A1','P1'],['D1','T3','A1','P1']]
        sentence09 = ['D1','T1','T2','T3','T4','A1','P1','P2']
        correct_set09 = [['D1','T1','A1','P1'],['D1','T2','A1','P1'],['D1','T3','A1','P1'],['D1','T4','A1','P1'],['D1','T1','A1','P2'],['D1','T2','A1','P2'],['D1','T3','A1','P2'],['D1','T4','A1','P2']]
        sentence10 = ['D1','T1','A1','P1','A2','P2']
        correct_set10 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence11 = ['D1','T1','A1','P1','P2']
        correct_set11 = [['D1','T1','A1','P1'],['D1','T1','A1','P2']]
        sentence12 = ['D1','T1','A1','P1','A2','P2']
        correct_set12 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence13 = ['D1','T1','A1','P1','P2','P3']
        correct_set13 = [['D1','T1','A1','P1'],['D1','T1','A1','P2'],['D1','T1','A1','P3']]
        sentence14 = ['D1','T1','A1','P1','A2','P2']
        correct_set14 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence15 = ['D1','T1','A1','P1','P2']
        correct_set15 = [['D1','T1','A1','P1'],['D1','T1','A1','P2']]
        sentence16 = ['D1','T1','A1','T2','A2','P1']
        correct_set16 = [['D1','T1','A1','P1'],['D1','T2','A2','P1']]
        sentence17 = ['D1','T1','A1','P1','P2','P3']
        correct_set17 = [['D1','T1','A1','P1'],['D1','T1','A1','P2'],['D1','T1','A1','P3']]
        sentence18 = ['D1','T1','A1','P1','A2','P2']
        correct_set18 = [['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence19 = ['D1','P1','P2','P3','P4','P5','T1','A1']
        correct_set19 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P3','T1','A1'],['D1','P4','T1','A1'],['D1','P5','T1','A1']]
        sentence20 = ['D1','T1','A1','P1','P2']
        correct_set20 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence21 = ['D1','T1','A1','P1','P2']
        correct_set21 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence22 = ['D1','T1','A1','P1','P2','P3']
        correct_set22 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P3','T1','A1']]
        sentence23 = ['D1','T1','A1','P1','P2','P3']
        correct_set23 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P3','T1','A1']]
        sentence24 = ['D1','A1','T1','P1','P2','P3']
        correct_set24 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P3','T1','A1']]
        sentence25 = ['D1','T1','A1','P1','P2']
        correct_set25 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence26 = ['D1','T1','A1','P1','P2']
        correct_set26 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence27 = ['D1','A1','T1','P1']
        correct_set27 = [['D1','P1','T1','A1']]
        sentence28 = ['D1','T1','A1','P1']
        correct_set28 = [['D1','P1','T1','A1']]
        sentence29 = ['D1','T1','A1','A2','P1']
        correct_set29 = [['D1','P1','T1','A1'],['D1','P1','T1','A2']]
        sentence30 = ['D1','T1','A1','P1']
        correct_set30 = [['D1','P1','T1','A1']]
        sentence31 = ['D1','T1','A1','P1']
        correct_set31 = [['D1','P1','T1','A1']]
        sentence32 = ['D1','T1','A1','A2','P1']
        correct_set32 = [['D1','P1','T1','A1'],['D1','P1','T1','A2']]
        sentence33 = ['D1','T1','T2','A1','P1']
        correct_set33 = [['D1','P1','T1','A1'],['D1','P1','T2','A1']]
        sentence34 = ['D1','T1','T2','T3','A1','P1']
        correct_set34 = [['D1','P1','T1','A1'],['D1','P1','T2','A1'],['D1','P1','T3','A1']]
        sentence35 = ['D1','T1','A1','P1','P2']
        correct_set35 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence36 = ['D1','T1','A1','A2','P1','P2']
        correct_set36 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P1','T1','A2'],['D1','P2','T1','A2']]
        sentence37 = ['D1','T1','A1','P1','P2']
        correct_set37 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence38 = ['D1','T1','T2','T3','A1','P1','P2']
        correct_set38 = [['D1','P1','T1','A1'],['D1','P1','T2','A1'],['D1','P1','T3','A1'],['D1','P2','T1','A1'],['D1','P2','T2','A1'],['D1','P2','T3','A1']]
        sentence39 = ['D1','T1','P1','P2','A1']
        correct_set39 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence40 = ['D1','T1','P1','A1','T2','P2','A2']
        correct_set40 = [['D1','P1','T1','A1'],['D1','P2','T2','A2']]
        sentence41 = ['D1','A1','T1','P1']
        correct_set41 = [['D1','P1','T1','A1']]
        sentence42 = ['D1','P1','T1','A1']
        correct_set42 = [['D1','P1','T1','A1']]
        sentence43 = ['D1','P1','T1','A1']
        correct_set43 = [['D1','P1','T1','A1']]
        sentence44 = ['D1','T1','T2','A1','P1']
        correct_set44 = [['D1','P1','T1','A1'],['D1','P1','T2','A1']]
        sentence45 = ['D1','T1','A1','P1','P2']
        correct_set45 = [['D1','P1','T1','A1'],['D1','P2','T1','A1']]
        sentence46 = ['D1','T1','T2','A1','P1']
        correct_set46 = [['D1','P1','T1','A1'],['D1','P1','T2','A1']]
        sentence47 = ['D1','T1','A1','P1']
        correct_set47 = [['D1','P1','T1','A1']]
        sentence48 = ['D1','A1','P1','A2','P2','T1']
        correct_set48 = [['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence49 = ['D1','T1','A1','P1','P2','P3']
        correct_set49 = [['D1','P1','T1','A1'],['D1','P2','T1','A1'],['D1','P3','T1','A1']]
        sentence50 = ['D1','T1','A1','P1']
        correct_set50 = [['D1','P1','T1','A1']]
        
        sentence51=['D1','T1','A1','P1','A2','P2','A3','P3']
        correct_set51=[['D1','P1','T1','A1'],['D1','P2','T1','A2'],['D1','P3','T1','A3']]
        sentence52=['D1','T1','A1','T2','A2','P1']
        correct_set52=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence53=['D1','P1','T1','A1','P2','T2','A2','A3']
        correct_set53=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P2','T2','A3']]
        sentence54=['D1','P1','T1','A1','P2','T2','A2','P3','T3','A3','A4']
        correct_set54=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P3','T3','A3'],['D1','P3','T3','A4']]
        sentence55=['D1','T1','A1','P1','P2','T2','A2','P3','P4']
        correct_set55=[['D1','P1','T1','A1'],['D1','P2','T2','A1'],['D1','P3','T2','A2'],['D1','P4','T2','A2']]
        sentence56=['D1','T1','A1','P1','A2','P2']
        correct_set56=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence57=['D1','P1','T1','A1','T2','A2']
        correct_set57=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence58=['D1','T1','A1','P1','A2','P2']
        correct_set58=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence59=['D1','T1','A1','P1','A2','P2']
        correct_set59=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence60=['D1','T1','A1','P1','A2','P2']
        correct_set60=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence61=['D1','T1','A1','P1','A2','P2']
        correct_set61=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence62=['D1','T1','A1','P1','A2','P2']
        correct_set62=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence63=['D1','T1','A1','T2','A2','P1']
        correct_set63=[['D1','T1','A1','P1'],['D1','T2','A2','P1']]
        sentence64=['D1','T1','A1','P1','A2','P2']
        correct_set64=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence65=['D1','T1','P1','A1','T2','P2','A2']
        correct_set65=[['D1','P1','T1','A1'],['D1','P2','T2','A2']]
        sentence66=['D1','A1','P1','A2','P2','T1']
        correct_set66=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence67=['D1','T1','A1','P1','A2','P2','A3','P3']
        correct_set67=[['D1','P1','T1','A1'],['D1','P2','T1','A2'],['D1','P3','T1','A3']]
        sentence68=['D1','T1','A1','T2','A2','P1']
        correct_set68=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence69=['D1','P1','T1','A1','P2','T2','A2','A3']
        correct_set69=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P2','T2','A3']]
        sentence70=['D1','P1','T1','A1','P2','T2','A2','P3','T3','A3','A4']
        correct_set70=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P3','T3','A3'],['D1','P3','T3','A4']]
        sentence71=['D1','T1','A1','P1','P2','T2','A2','P3','P4']
        correct_set71=[['D1','P1','T1','A1'],['D1','P2','T2','A1'],['D1','P3','T2','A2'],['D1','P4','T2','A2']]
        sentence72=['D1','T1','A1','P1','A2','P2']
        correct_set72=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence73=['D1','P1','T1','A1','T2','A2']
        correct_set73=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence74=['D1','T1','A1','P1','A2','P2']
        correct_set74=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence75=['D1','T1','A1','P1','A2','P2']
        correct_set75=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence76=['D1','T1','A1','P1','A2','P2']
        correct_set76=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence77=['D1','T1','A1','P1','A2','P2']
        correct_set77=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence78=['D1','T1','A1','P1','A2','P2']
        correct_set78=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence79=['D1','T1','A1','T2','A2','P1']
        correct_set79=[['D1','T1','A1','P1'],['D1','T2','A2','P1']]
        sentence80=['D1','T1','A1','P1','A2','P2']
        correct_set80=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence81=['D1','T1','P1','A1','T2','P2','A2']
        correct_set81=[['D1','P1','T1','A1'],['D1','P2','T2','A2']]
        sentence82=['D1','A1','P1','A2','P2','T1']
        correct_set82=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence83=['D1','T1','A1','P1','A2','P2','A3','P3']
        correct_set83=[['D1','P1','T1','A1'],['D1','P2','T1','A2'],['D1','P3','T1','A3']]
        sentence84=['D1','T1','A1','T2','A2','P1']
        correct_set84=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence85=['D1','P1','T1','A1','P2','T2','A2','A3']
        correct_set85=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P2','T2','A3']]
        sentence86=['D1','P1','T1','A1','P2','T2','A2','P3','T3','A3','A4']
        correct_set86=[['D1','P1','T1','A1'],['D1','P2','T2','A2'],['D1','P3','T3','A3'],['D1','P3','T3','A4']]
        sentence87=['D1','T1','A1','P1','P2','T2','A2','P3','P4']
        correct_set87=[['D1','P1','T1','A1'],['D1','P2','T2','A1'],['D1','P3','T2','A2'],['D1','P4','T2','A2']]
        sentence88=['D1','T1','A1','P1','A2','P2']
        correct_set88=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        sentence89=['D1','P1','T1','A1','T2','A2']
        correct_set89=[['D1','P1','T1','A1'],['D1','P1','T2','A2']]
        sentence90=['D1','T1','A1','P1','A2','P2']
        correct_set90=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence91=['D1','T1','A1','P1','A2','P2']
        correct_set91=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence92=['D1','T1','A1','P1','A2','P2']
        correct_set92=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence93=['D1','T1','A1','P1','A2','P2']
        correct_set93=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence94=['D1','T1','A1','P1','A2','P2']
        correct_set94=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence95=['D1','T1','A1','T2','A2','P1']
        correct_set95=[['D1','T1','A1','P1'],['D1','T2','A2','P1']]
        sentence96=['D1','T1','A1','P1','A2','P2']
        correct_set96=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        sentence97=['D1','T1','P1','A1','T2','P2','A2']
        correct_set97=[['D1','P1','T1','A1'],['D1','P2','T2','A2']]
        sentence98=['D1','A1','P1','A2','P2','T1']
        correct_set98=[['D1','P1','T1','A1'],['D1','P2','T1','A2']]
        
        #构造样本集合
        allData = [[sentence01, correct_set01], [sentence02, correct_set02], [sentence03, correct_set03], [sentence04, correct_set04], [sentence05, correct_set05], [sentence06, correct_set06], [sentence07, correct_set07], [sentence08, correct_set08], [sentence09, correct_set09], [sentence10, correct_set10], [sentence11, correct_set11], [sentence12, correct_set12], [sentence13, correct_set13], [sentence14, correct_set14], [sentence15, correct_set15], [sentence16, correct_set16], [sentence17, correct_set17], [sentence18, correct_set18], [sentence19, correct_set19], [sentence20, correct_set20], [sentence21, correct_set21], [sentence22, correct_set22], [sentence23, correct_set23], [sentence24, correct_set24], [sentence25, correct_set25], [sentence26, correct_set26], [sentence27, correct_set27], [sentence28, correct_set28], [sentence29, correct_set29], [sentence30, correct_set30], [sentence31, correct_set31], [sentence32, correct_set32], [sentence33, correct_set33], [sentence34, correct_set34], [sentence35, correct_set35], [sentence36, correct_set36], [sentence37, correct_set37], [sentence38, correct_set38], [sentence39, correct_set39], [sentence40, correct_set40], [sentence41, correct_set41], [sentence42, correct_set42], [sentence43, correct_set43], [sentence44, correct_set44], [sentence45, correct_set45], [sentence46, correct_set46], [sentence47, correct_set47], [sentence48, correct_set48], [sentence49, correct_set49], [sentence50, correct_set50], [sentence51, correct_set51], [sentence52, correct_set52], [sentence53, correct_set53], [sentence54, correct_set54], [sentence55, correct_set55], [sentence56, correct_set56], [sentence57, correct_set57], [sentence58, correct_set58], [sentence59, correct_set59], [sentence60, correct_set60], [sentence61, correct_set61], [sentence62, correct_set62], [sentence63, correct_set63], [sentence64, correct_set64], [sentence65, correct_set65], [sentence66, correct_set66], [sentence67, correct_set67], [sentence68, correct_set68], [sentence69, correct_set69], [sentence70, correct_set70], [sentence71, correct_set71], [sentence72, correct_set72], [sentence73, correct_set73], [sentence74, correct_set74], [sentence75, correct_set75], [sentence76, correct_set76], [sentence77, correct_set77], [sentence78, correct_set78], [sentence79, correct_set79], [sentence80, correct_set80], [sentence81, correct_set81], [sentence82, correct_set82], [sentence83, correct_set83], [sentence84, correct_set84], [sentence85, correct_set85], [sentence86, correct_set86], [sentence87, correct_set87], [sentence88, correct_set88], [sentence89, correct_set89], [sentence90, correct_set90], [sentence91, correct_set91], [sentence92, correct_set92], [sentence93, correct_set93], [sentence94, correct_set94], [sentence95, correct_set95], [sentence96, correct_set96], [sentence97, correct_set97], [sentence98, correct_set98]]
        return allData
    
    def getOfflineData(self):
        ####  offlinedata
        sentence01=['D1','P1','T1','R1','T2','R2']
        correct_set01=[['D1','P1','T1','R1'],['D1','P1','T2','R2']]
                
        sentence02=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
        correct_set02=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
                
        sentence03=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
        correct_set03=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
                
        sentence04=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
        correct_set04=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
                
        sentence05=['D1','P1','T1','R1','T2','R2','T3','R3']
        correct_set05=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3']]
                
        sentence06=['D1','P1','T1','R1','T2','R2','T3','R3']
        correct_set06=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3']]
                
        sentence07=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
        correct_set07=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
                
        sentence08=['D1','P1','T1','R1']
        correct_set08=[['D1','P1','T1','R1']]
                
        sentence09=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
        correct_set09=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
                
        sentence11=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
        correct_set11=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6']]
                
        sentence12=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
        correct_set12=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
                
        sentence13=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4']
        correct_set13=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4']]
                
        sentence14=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
        correct_set14=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5']]
                
        sentence15=['D1','P1','T1','R1']
        correct_set15=[['D1','P1','T1','R1']]
                
        sentence16=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9','T10','R10']
        correct_set16=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9'],['D1','P1','T10','R10']]
                
        sentence17=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
        correct_set17=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
                
        sentence18=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
        correct_set18=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8']]
                
        sentence19=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7']
        correct_set19=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7']]
                
        sentence20=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9']
        correct_set20=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9']]
                
        sentence10=['D1','P1','P2','T1','R1','T2','R2','T3','R3','T4','R4']
        correct_set10=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P2','T1','R1'],['D1','P2','T2','R2'],['D1','P2','T3','R3'],['D1','P2','T4','R4']]
 
        #构造样本集合
        allData = [[sentence01, correct_set01], [sentence02, correct_set02], [sentence03, correct_set03], [sentence04, correct_set04], [sentence05, correct_set05], [sentence06, correct_set06], [sentence07, correct_set07], [sentence08, correct_set08], [sentence09, correct_set09], [sentence10, correct_set10], [sentence11, correct_set11], [sentence12, correct_set12], [sentence13, correct_set13], [sentence14, correct_set14], [sentence15, correct_set15], [sentence16, correct_set16], [sentence17, correct_set17], [sentence18, correct_set18], [sentence19, correct_set19], [sentence20, correct_set20]]
        return allData
    
if __name__=='__main__': 
    
    
    tModel = initializeModel()
    vType = 'Offline'
    dataList = []
    sentence10 = ['D1','P1','P2','T1','R1','T2','R2','T3','R3','T4','R4']
    correct_set10=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P2','T1','R1'],['D1','P2','T2','R2'],['D1','P2','T3','R3'],['D1','P2','T4','R4']]
    sentence0 = "|".join(sentence10) 
    print sentence0
    print vType
    print tModel.getEntityRelationResult(sentence0)
    
    sentence90=['D1','T1','A1','P1','A2','P2']
    correct_set90=[['D1','T1','A1','P1'],['D1','T1','A2','P2']]
        
    dataList = [sentence90,correct_set90]
    sentence78=['D1','M1','T1','A1','P1','A2','P2']
    
    sentence0 = "|".join(sentence78)    
    sentence = "|".join(sentence90)
    
    vType = 'Online'
    correct_set = ["|".join(x) for x in correct_set90]
    print sentence
    
    print correct_set
    print tModel.updateDataList(sentence,correct_set, vType)
    print tModel.getEntityRelationResult(sentence0)
#     
#     sentence05=['D1','P1','T1','R1','T2','R2','T3','R3']
#     correct_set05=[['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3']]
#     correct_set = ["|".join(x) for x in correct_set05]
#     print correct_set
#     print "|".join(sentence05)
        

    
    
    
    