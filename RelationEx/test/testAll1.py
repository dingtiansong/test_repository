#-*- coding:utf-8 -*-
'''
Created on 20160831

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
from entityRelationExtractionClass12 import entityRelationExtractionModel
import pickle

if __name__ == '__main__':
    
    
    
    column = 8#max（每个类别的个数）
    maxFactor = 15
    vType = 2
    english = ['D','P','T','M']
    
    sentence01 = ['D1','T1','M1','P1','M2','P2']
    correct_set01 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
    sentence02 = ['D1','T1','M1','M2','P1','P2']
    correct_set02 = [['D1','T1','M1','P1'],['D1','T1','M2','P2'],['D1','T1','M2','P1'],['D1','T1','M1','P2']]
    sentence03 = ['D1','T1','M1','P1']
    correct_set03 = [['D1','T1','M1','P1']]
    sentence04 = ['D1','M1','T1','P1','P2']
    correct_set04 = [['D1','T1','M1','P1'],['D1','T1','M1','P2']]
    sentence05 = ['D1','T1','M1','P1','M2','P2']
    correct_set05 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
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
    correct_set12 = [['D1','T1','M1','P1'],['D1','T1','M2','P2']]
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
    correct_set51=[['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3']]
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
    correct_set67=[['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3']]
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
    correct_set83=[['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3']]
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
    

    print '---Test Error Start---'
    allData = [[sentence01, correct_set01], [sentence02, correct_set02], [sentence03, correct_set03], [sentence04, correct_set04], [sentence05, correct_set05], [sentence06, correct_set06], [sentence07, correct_set07], [sentence08, correct_set08], [sentence09, correct_set09], [sentence10, correct_set10], [sentence11, correct_set11], [sentence12, correct_set12], [sentence13, correct_set13], [sentence14, correct_set14], [sentence15, correct_set15], [sentence16, correct_set16], [sentence17, correct_set17], [sentence18, correct_set18], [sentence19, correct_set19], [sentence20, correct_set20], [sentence21, correct_set21], [sentence22, correct_set22], [sentence23, correct_set23], [sentence24, correct_set24], [sentence25, correct_set25], [sentence26, correct_set26], [sentence27, correct_set27], [sentence28, correct_set28], [sentence29, correct_set29], [sentence30, correct_set30], [sentence31, correct_set31], [sentence32, correct_set32], [sentence33, correct_set33], [sentence34, correct_set34], [sentence35, correct_set35], [sentence36, correct_set36], [sentence37, correct_set37], [sentence38, correct_set38], [sentence39, correct_set39], [sentence40, correct_set40], [sentence41, correct_set41], [sentence42, correct_set42], [sentence43, correct_set43], [sentence44, correct_set44], [sentence45, correct_set45], [sentence46, correct_set46], [sentence47, correct_set47], [sentence48, correct_set48], [sentence49, correct_set49], [sentence50, correct_set50], [sentence51, correct_set51], [sentence52, correct_set52], [sentence53, correct_set53], [sentence54, correct_set54], [sentence55, correct_set55], [sentence56, correct_set56], [sentence57, correct_set57], [sentence58, correct_set58], [sentence59, correct_set59], [sentence60, correct_set60], [sentence61, correct_set61], [sentence62, correct_set62], [sentence63, correct_set63], [sentence64, correct_set64], [sentence65, correct_set65], [sentence66, correct_set66], [sentence67, correct_set67], [sentence68, correct_set68], [sentence69, correct_set69], [sentence70, correct_set70], [sentence71, correct_set71], [sentence72, correct_set72], [sentence73, correct_set73], [sentence74, correct_set74], [sentence75, correct_set75], [sentence76, correct_set76], [sentence77, correct_set77], [sentence78, correct_set78], [sentence79, correct_set79], [sentence80, correct_set80], [sentence81, correct_set81], [sentence82, correct_set82], [sentence83, correct_set83], [sentence84, correct_set84], [sentence85, correct_set85], [sentence86, correct_set86], [sentence87, correct_set87], [sentence88, correct_set88], [sentence89, correct_set89], [sentence90, correct_set90], [sentence91, correct_set91], [sentence92, correct_set92], [sentence93, correct_set93], [sentence94, correct_set94], [sentence95, correct_set95], [sentence96, correct_set96], [sentence97, correct_set97], [sentence98, correct_set98]]
    k=1
    for i in range(len(allData)):
        s1,c1 = allData[i][0],allData[i][1]
        for c2 in c1:
            for c3 in c2:
                if c3 not in s1:
                    print i
    print '---Test Error End---'
                    
        

      
    test = entityRelationExtractionModel(column,maxFactor, english)
    #构造数据集
    allDist = {}
    for i in range(len(allData)):
        allDist[i] = test.getSampleDist(allData[i][0],allData[i][1])
     
    with open('allDist.pickle', 'wb') as f:
        pickle.dump(allDist, f)
     
    sList = [x for x in allDist.keys() if allDist[x]['isTrain'] == 0]
      
       
    #构造样本的测试集和训练集标记
    testNum = len(sList) / 4
    trainSet = {}
    for i in range(10):
        testKey = random.sample(sList, testNum)
        trainSet[i] = {'test':testKey}
        tList = list(set(sList).difference(set(testKey)))
        k = 1
        for j in range(2,len(tList)+1,len(tList)/15):
            trainKey = random.sample(tList, j)
            trainSet[i]['train%s'%k] = trainKey
            k = k + 1
    with open('trainSet.pickle', 'wb') as f:
        pickle.dump(trainSet, f)
       
      
    #输出结果
    def getResult62(allDist):
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
    def getResultSave(allDist,vType=2):
        print vType
        #构造数据特征向量
        allDist1 = test.getDistTransEigenvector(allDist,vType)
        #构造svm模型
        trainModel = test.getDistSVMModel(allDist1)
        #根据模型生成预测结果和评价指标
        allDist = test.getDistSVMResult(trainModel, allDist)
        return getResult62(allDist)
          
          
    with open('trainSet.pickle', 'rb') as f:
        trainSet = pickle.load(f)
      
    for j in trainSet.keys():
        with open('allDist.pickle', 'rb') as f:
            allDist = pickle.load(f)
        testKey = trainSet[j]['test']
        for k in range(1,len(trainSet[j])):
            trainKey = trainSet[j]['train%s'%k]
            for i in range(len(allDist)):
                allDist[i]['isTrain'] = 0
                allDist[i]['isTest'] = 0
            for i in trainKey:
                allDist[i]['isTrain'] = 1
            for i in testKey:
                allDist[i]['isTest'] = 1
            rtDist = getResultSave(allDist,vType)
            with open('rtDist.%s.%s.pickle'%(j,k), 'wb') as f:
                pickle.dump(allDist, f)
    
#     for i in allDist.keys():
#         tmp = allDist[i]
#         if 'isError' in tmp.keys():
#             if tmp['totalError'] != {}:
#                 print tmp['sentence']
#                 print tmp['precision'],tmp['recall'],tmp['f1Score']
#                 print tmp['precision2'],tmp['recall2'],tmp['f1Score2']
#                 print tmp['precision4'],tmp['recall4'],tmp['f1Score4']
#                 print sum(tmp['predictValue'])*1.0/len(tmp['predictValue'])
#                 print tmp['totalError']
    
    def getReprot(allDist):
        xlist = [0,0,0,0,0,0,0,0]
        for i in allDist.keys():
            tmp = allDist[i]
            xlist[7] += tmp['isTest']
            if 'isError' in tmp.keys():
                xlist[1] += len([x for x in range(len(tmp['isError'])) if tmp['isError'][x] == 1 and tmp['trueValue'][x] == 1])
                xlist[2] += len([x for x in range(len(tmp['isError'])) if tmp['isError'][x] == 1 and tmp['trueValue'][x] == 0])
                xlist[3] += tmp['f1Score']
                xlist[4] += tmp['f1Score2']
                xlist[5] += tmp['f1Score4']
                xlist[6] += 1
                if tmp['f1Score4'] < 1:
                    xlist[0] += 1 
        xlist[3] = xlist[3] * 1.0 / xlist[6]
        xlist[4] = xlist[4] * 1.0 / xlist[6]
        xlist[5] = xlist[5] * 1.0 / xlist[6]
        return xlist
    
    with open('trainSet.pickle', 'rb') as f:
        trainSet = pickle.load(f)
    
    for j in trainSet.keys():
        xlist = []
        for k in range(1,len(trainSet[j])):
            with open('rtDist.%s.%s.pickle'%(j,k), 'rb') as f:
                tDist = pickle.load(f)
            print '---%s---%s---------'%(j,k)
            print getReprot(tDist)  
            xlist.append(getReprot(tDist))
        plt.subplot(4, 3, j+1) 
        plt.plot(list(range(1,len(trainSet[j]))),[1-x[0]*1.0/x[7] for x in xlist],label = ['p'])
        plt.plot(list(range(1,len(trainSet[j]))),[x[3] for x in xlist],label = ['f1'])
        plt.plot(list(range(1,len(trainSet[j]))),[x[4] for x in xlist],label = ['f2'])
        plt.plot(list(range(1,len(trainSet[j]))),[x[5] for x in xlist],label = ['f4'])
    plt.subplot(4, 3, j+2)
    plt.plot(list(range(1,len(trainSet[j]))),[1-x[0]*1.0/x[7] for x in xlist],label = ['p'])
    plt.plot(list(range(1,len(trainSet[j]))),[x[3] for x in xlist],label = ['f1'])
    plt.plot(list(range(1,len(trainSet[j]))),[x[4] for x in xlist],label = ['f2'])
    plt.plot(list(range(1,len(trainSet[j]))),[x[5] for x in xlist],label = ['f4'])
    plt.legend(loc='lower left')
    plt.show() 
            
              
                            
    
    
    
    
    
