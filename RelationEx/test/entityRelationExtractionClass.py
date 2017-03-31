#-*- coding:utf-8 -*-
'''
Created on 2016��8��22��

@author: Administrator
'''
import numpy as np
from pyasn1.compat.octets import null
from sklearn import svm

class entityRelationExtractionModel(object):
    '''
    classdocs
    '''
    maxColumn = 5
    english = []
    list_rain = []
    clf_rbf = []
    
    def __init__(self, params = 5, list1 = ['D','P','T','R'], list2=['D1','T1','P1','R1','R2'], list3 = [['D1','P1','T1','R1'],['D1','P1','T1','R2']]):
        '''
        Constructor
        '''
        self.english = list1
        self.list_rain = [list2, list3]
        self.maxColumn = params
    
    def getEigenvector(self,tmp_train = [], english = [], column = []):
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
            vector_feature1,relation1,bijection1 = self.main_feature(s1, s2, english, column)#д���������Ӹ���Ԫ��֮�������/��ϵ
            #vector_feature1 = np.matrix(vector_feature1)
            vector_feature = vector_feature + vector_feature1
            relation = relation + relation1
            bijection.append(bijection1)
        
        vector_feature = np.matrix(vector_feature)
        
        return vector_feature,relation,bijection
    
    def getTestEigenvector(self, a, english, column):
        vector_feature = []
        bijection = []
        if len(a) > 1:
            for i in range(len(a)-1):
                for j in range((i+1),len(a)):
                    vector_feature.append(self.structure_feature(english, a, i, j, column))
                    bijection.append([a[i],a[j]])
        
        vector_feature = np.matrix(vector_feature)
        return vector_feature,bijection
    
    def getSVMModel(self, vector_feature, relation):
        #构建样本数据
        x = vector_feature
        y = relation
        #SVM训练
        clf_rbf = svm.SVC().fit(vector_feature, relation)
        return clf_rbf
        
    def getSVMResult(self, clf_rbf, vector_feature, bijection):
        #SVM预测判断
        answer = []
        for iv in vector_feature:
            answer.append(clf_rbf.predict(iv)[0])
        
        xList = bijection
        k = 0
        for i in range(len(xList)):
                xList[i].append(answer[k])
                k = k + 1
        
        return xList
    
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
    
    def classification(self, f1,s1,a,b):
        row = len(b)#b������
        relation = 0
        for i in range (row):
            #print b[i][:]
            if a[f1] in b[i][:]:
                if a[s1] in b[i][:]:
                    relation=1
                    break
        
        return relation
    
    def main_feature(self, a,b,english,column):
        vector_feature = []
        relation = []
        bijection = []
        
        if len(a) > 1:
            for i in range(len(a)-1):
                for j in range((i+1),len(a)):
                    vector_feature.append(self.structure_feature(english, a, i, j, column))
                    relation.append(self.classification(i,j,a,b))
                    bijection.append([a[i],a[j]])
        
        return vector_feature,relation,bijection
    
    '''   ��������:��5����    '''
    def isGroup(self, xfind):
        tmp = ''.join(xfind)
        rt = True
        for e in self.english: 
            if e not in tmp:
                rt = False
                break
        return rt
    
    def getFindResult0(self, xList, tmp):
        if [tmp[0], tmp[1], 1] in xList:
            return True
        elif [tmp[1], tmp[0], 1] in xList:
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
    
if __name__=='__main__':  
    
    #样本句子

    a = ['D1','P1','T1','T2','R1','P2','T3','R2','T4','R3','P3','T5','R4']
    #正例
    b = [['D1','P1','T1','R1'],
         ['D1','P1','T2','R1'],
         ['D1','P2','T3','R2'],
         ['D1','P2','T4','R3'],
         ['D1','P3','T5','R4']]
    a1 = ['D1','T1','P1','R1','R2']
    b1 = [['D1','P1','T1','R1'],['D1','P1','T1','R2']]
    a2 = ['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
    b2 = [['D1','P1','T1','R1'],
          ['D1','P1','T2','R2'],
          ['D1','P1','T3','R3'],
          ['D1','P1','T4','R4'],
          ['D1','P1','T5','R5']]
    
    tmp_train = [[a2,b2]]
    #元素
    english=['D','P','T','R']
    #每个特征中相同元素重复的次数
    column=5#max（每个类别的个数）
    
    #新建一个类
    test = entityRelationExtractionModel(column, english)
    #构造训练特征向量
    vector_feature,relation,bijection = test.getEigenvector(tmp_train, english, column)
    #训练SVM模型
    clf_rbf = test.getSVMModel(vector_feature, relation)
    #构造测试特征向量
    tmp_test = a2
    vector_feature1,bijection1 = test.getTestEigenvector(tmp_test, english, column)
    #预测测试结果
    xList = test.getSVMResult(clf_rbf, vector_feature1, bijection1)
    
    #生成预测的实体关系
    result = test.getExtraction(xList)
    print result
    xList = bijection[0]
    k = 0
    for i in range(len(xList)):
            xList[i].append(relation[k])
            k = k + 1
    print xList
    print bijection1
        
    

        
        
        
        
        
        