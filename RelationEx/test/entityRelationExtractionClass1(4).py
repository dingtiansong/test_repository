#-*- coding:utf-8 -*-
'''
Created on 2016��8��22��

@author: Administrator
'''
import numpy as np
from pyasn1.compat.octets import null
from sklearn import svm
import copy
from pandas import Series
from pandas import DataFrame
#from guidata.utils import pairs
from sklearn.externals import joblib
from sklearn import metrics
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
    
    #svmmodel = joblib.load("train_model.m")
    def getProduct(self,sentence,needfactor):
        factorMatrix=[]
        allrelation=self.getRelationSet(sentence)
        for pairs in allrelation:
            factorMatrix.append(self.fvactor(pairs[0], pairs[1], sentence))
        featureMatrix={}
        i=0
        rel_type=self.realationset(needfactor)
        x = self.getTestEigenvector2(sentence)
        #svmmodel = joblib.load("train_model.m")        
        print x
        y=range(len(x))
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
    
    def getSVMRelationRT(self, trainModel, dateSet, vType):
        predictValue = []
        predictRelation = []
        predictList = {}
        for [sentence,relation4] in dateSet:
            #句子构造测试2元素对
            testSet = self.getRelationSet(sentence)
            #构造测试特征向量和测试结果向量
            trainVector,trainValue = self.getTransEigenvector([[sentence,relation4]],vType)
            #模型预测结果
            testValue = self.getSVMResult(trainModel, trainVector)
            rtList = self.getResult2(testSet,trainValue,testValue)
            #根据预测结果和测试2元素对生成预测2元素对
            testRelation2 = self.getValueToRelation(testSet, testValue)
            #预测2元素对转4元素对
            testRelation4 = self.getTransTwoFour(testRelation2)
            #结果汇总
            predictValue = predictValue + (testValue)
            predictRelation.append(testRelation4)
            predictList[','.join(sentence)] = rtList
        return predictValue,predictRelation,predictList
    
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
    
     
if __name__=='__main__':  
     
#     #样本句子
#     a = ['D1','P1','T1','T2','R1','P2','T3','R2','T4','R3','P3','T5','R4']
#     #正例
#     b = [['D1','P1','T1','R1'],
#          ['D1','P1','T2','R1'],
#          ['D1','P2','T3','R2'],
#          ['D1','P2','T4','R3'],
#          ['D1','P3','T5','R4']]
    a1=['D1','T1','M1','P1','M2','P2']
    b1=[['D1','T1','M1','P1'],['D1','T2','M2','P2']]
    a2=['D1','T1','M1','M2','P1','P2']
    b2=[['D1','T1','M1','P1'],['D1','T2','M2','P2'],['D1','T1','M2','P1'],['D1','T2','M1','P2']]
    a3=['D1','T1','M1','P1']
    b3=[['D1','T1','M1','P1']]
     
    a4=['D1','M1','T1','P1','P2']
    b4=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
     
    a5=['D1','T1','M1','P1','M2','P2']
    b5=[['D1','T1','M1','P1'],['D1','T2','M2','P2']]
     
    a6=['D1','T1','P1','M1']
    b6=[['D1','T1','M1','P1']]
     
    a7=['D1','T1','M1','P1','P2']
    b7=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
     
    a8=['D1','T1','T2','T3','M1','P1']
    b8=[['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1']]
     
    a9=['D1','T1','T2','T3','T4','M1','P1','P2']
    b9=[['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'],['D1','T4','M1','P1'],['D1','T1','M1','P2'],['D1','T2','M1','P2'],['D1','T3','M1','P2'],['D1','T4','M1','P2']]
     
    a10=['D1','T1','M1','P1','M2','P2']
    b10=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
     
    a11=['D1','T1','M1','P1','P2']
    b11=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
     
    a12=['D1','T1','M1','P1','M2','P2']
    b12=[['D1','T1','M1','P1'],['D1','T2','M2','P2']]
     
    a13=['D1','T1','M1','P1','P2','P3']
    b13=[['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3']]
     
    a14=['D1','T1','M1','P1','M2','P2']
    b14=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
     
    a15=['D1','T1','M1','P1','P2']
    b15=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
     
    a16=['D1','T1','M1','T2','M2','P1']
    b16=[['D1','T1','M1','P1'],['D1','T2','M2','P1']]
     
    a17=['D1','T1','M1','P1','P2','P3']
    b17=[['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3']]
     
    a18=['D1','T1','M1','P1','M2','P2']
    b18=[['D1','T1','M1','P1'],['D1','T1','M2','P2']]
     
    a19=['D1', 'P1', 'M1', 'T1']
    b19=[['D1', 'P1', 'M1', 'T1']]
    a20=['D1', 'M1', 'T1', 'P1']
    b20=[['D1', 'M1', 'T1', 'P1']]
    a21=['D1', 'T1', 'P1', 'M1']
    b21=[['D1', 'T1', 'P1', 'M1']]
    a22=['D1', 'M1', 'P1', 'T1', 'T2']
    b22=[['D1','M1','P1','T1'],['D1','M1','P1','T2']]
    a23=['D1', 'T1', 'M1', 'P1', 'P2']
    b23=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    a24=['D1', 'M1', 'P1', 'P2', 'T1', 'M2', 'P3', 'P4', 'P5']
    b24=[['D1','T1','M1','P1'],['D1','T1','M1','P2']]
     
     
     
     
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
#     
#     #2元素根据正例2元素对构造特征值
#     trainValue = test.getTrainValue(trainSet, relation2)
#     
#     #特征向量叠加
#     
#     #特征值向量叠加
#     
#     
    #训练样本
    tmp_train = [[a2,b2]]
    #测试对照样本
    tmp_train0 = [[a2,b2]]
     
     
    column = 5#max（每个类别的个数）
    maxFactor = 15
    vType = 2
    english = ['D','P','T','M']
     
    allData = [[a5,b5],[a1,b1],[a2,b2],[a3,b3],[a4,b4],[a6,b6],[a7,b7],[a8,b8],[a9,b9],[a10,b10],[a11,b11],[a12,b12],[a13,b13],[a14,b14],[a15,b15],[a16,b16],[a17,b17],[a18,b18],[a19,b19],[a20,b20],[a21,b21],[a22,b22],[a23,b23],[a24,b24]]
     
    sList = range(len(allData)-5,10,-1)
    #定义取随机数子集的函数
    def getRandomSet(allData, numList = [1], repeated = False):
        rtData = []
        sList = range(len(allData))
        if len(allData) >= sum(numList):
            for i in numList:
                slice1 = random.sample(sList, i)
                #print [allData[x] for x in slice1]
                rtData.append([allData[x] for x in slice1])
                if repeated == False:
                    sList = list(set(sList).difference(set(slice1)))
        return rtData
    sss = getRandomSet(allData, [3,4])
     
     
    sentence02 = ['D1','T1','M1','M2','P1','P2']
    correct_set02 = [['D1','T1','M1','P1'],['D1','T2','M2','P2'],['D1','T1','M2','P1'],['D1','T2','M1','P2']]
    tmp_train = [[sentence02,correct_set02]]
    test = entityRelationExtractionModel(column,maxFactor, english)
    #生成模型训练集
    trainVector,trainValue = test.getTransEigenvector(tmp_train,vType)
    print trainValue
     
#     for pltkkk in range(6):
#         scoreList = []
#         for i in sList:
#             tmp_train = []  #训练集
#             tmp_train0 = [] #测试集
#             [tmp_train,tmp_train0] = getRandomSet(allData, [i,4])
#             
#             #print tmp_train
#             #带入模型的样本
#             tmp_test = [x[0] for x in tmp_train0]
#             
#             test = entityRelationExtractionModel(column,maxFactor, english)
#             #生成模型训练集
#             trainVector,trainValue = test.getTransEigenvector(tmp_train,vType)
#             #训练模型
#             trainModel = test.getSVMModel(np.matrix(trainVector), trainValue)
#             #生成预测结果的参照集
#             trainVector0,trainValue0 = test.getTransEigenvector(tmp_train0,vType)
#             #生成预测结果
#             predictValue,predictRelation = test.getSVMRelation(trainModel, tmp_test, vType)
#             #预测结果对比参照集
#             #print metrics.accuracy_score(trainValue0, predictValue)
#             #print metrics.classification_report(trainValue0, predictValue)
#             tp = 0
#             fp = 0
#             fn = 0
#             tn = 0
#             for i in  range(len(trainValue0)):
#                 if trainValue0[i] == 0 :
#                     if predictValue[i] == 0:
#                         tn = tn + 1
#                     else:
#                         fn = fn + 1
#                 else:
#                     if predictValue[i] == 0:
#                         fp = fp + 1
#                     else:
#                         tp = tp + 1
#             Ap = 0
#             if tn+fp > 0:
#                 Ap = Ap + tn*1.0/(tn+fp)*(fn+tn)
#             if fn+tp > 0:
#                 Ap = Ap + tp*1.0/(fn+tp)*(fp+tp)
#             Ap = Ap * 1.0 / (fp+tp+fn+tn)
#             Ar = (tp+tn)*1.0/(fp+tp+fn+tn)     
#             #print [Ap,Ar,2*Ap*Ar/(Ap+Ar)]
#             
#             
#             #预测关系对比参照集
#             xList = []
#             Aprecision = 0
#             Arecall = 0
#             AtrainR4 = 0
#             for i in range(len(tmp_train0)):
#                 trainR4 = tmp_train0[i][1]
#                 predictR4 = predictRelation[i]
#                 recall = test.getRelationCompare(trainR4,predictR4) *1.0 / len(trainR4) 
#                 if len(predictR4) > 0:
#                     precision = test.getRelationCompare(trainR4,predictR4) *1.0 / len(predictR4)
#                 else:
#                     precision = 0.0
#                 #f1score = 2.0*precision*recall/(recall + precision)
#                 Aprecision = Aprecision + precision*len(trainR4) 
#                 Arecall = Arecall + recall*len(trainR4)
#                 AtrainR4 = AtrainR4 + len(trainR4)
#                 #xList.append([precision,recall,f1score,len(trainR4),len(predictR4)])
#             #print xList
#             Aprecision = Aprecision/AtrainR4
#             Arecall = Arecall/AtrainR4
#             
#             #print [Aprecision,Arecall,2*Aprecision*Arecall/(Arecall + Aprecision)]
#             scoreList.append([len(tmp_train),Ap,Ar,2*Ap*Ar/(Ap+Ar),Aprecision,Arecall,2*Aprecision*Arecall/(Arecall + Aprecision)])
#         
#         
#         #输出
#         print np.matrix(scoreList)
#         np.savetxt("filenamep%s.txt"%pltkkk,scoreList)
#     
#     
#     
#     for i in range(6):
#         plt.subplot(3, 2, i+1)  
#         scoreList =  np.loadtxt("filenamep%s.txt" %i)
#         
#         xlabel = ['p','r','f1','r4p','r4r','r4f1']
#         for i in range(1,len(scoreList[0])):
#             plt.plot([x[0] for x in scoreList],[x[i] for x in scoreList],label=xlabel[i-1])
#             
#     plt.legend(loc='lower left')
#     plt.show() 
#     #绘图
# #     plt.plot([x[0] for x in scoreList],[x[1] for x in scoreList],label = '0-1')
# #     plt.plot([x[0] for x in scoreList],[x[4] for x in scoreList],label = 'r4')
# #     plt.legend(loc='upper left')
# #     xlabel = ['p','r','f1','r4p','r4r','r4f1']
# #     for i in range(1,len(scoreList[0])):
# #         plt.plot([x[0] for x in scoreList],[x[i] for x in scoreList],label=xlabel[i-1])
# #         
# #     plt.legend(loc='lower left')
# #     plt.show()


    
    
    
    
    