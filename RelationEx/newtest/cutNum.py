# -*- coding: utf-8 -*-

'''
Created on 2016年10月19日

@author: song
'''
import pickle
from pandas.core.frame import DataFrame
import numpy as np
import copy
from entityRelationExtractionClass7 import initializeModel


class cutNum(object):
    '''
    1.处理标注长句清洗及分段
    2.对分段后的短句进行识别
    '''
    print(__doc__)
    
    needfactor=['C', 'D', 'P', 'T', 'A','M']
    cutfactor=['C']
    tModel = initializeModel()
    datapath = u'E:/work/infoEx/data/modelsentences3.pickle'   
     
    def __init__(self,needfactor=[],datapath=''):
        '''
        Constructor
        ''' 
#         if 

    def getData(self,datapath):
        with open(datapath, 'rb') as f:
            allData = pickle.load(f)
        return allData
        
#     allData=getData(datapath)
    
    # print allData[2]
    
    ##可用的数据（含分段数据）   
    def getAvdata(self,allData):
        avData=[]
        for i in allData.keys():
                tDict = allData[i]['trainData']
                if len(tDict['feature']) > 0:
                    if len([x for x in tDict['result'] if x > 0]) > 0:
        #                 print i,len(tDict['feature']),len(tDict['result']),len(tDict['feature'])-len(tDict['result'])==0
        #                 print tDict['result']
                        avData.append(allData[i])
        return avData
    
    
#     avData=getAvdata(allData)
    # print avData[1].decode('utf-8')
#     demosentence=avData[1]['trainData']['sentence']
#     print demosentence[1][0] in ['C', 'D', 'P', 'T', 'A','M']

    #清除不需要的标注
    def cleanSent(self,sentence,needfactor):
        sentence0 = copy.copy(sentence)
        sentence1=list(sentence0)
        for e in sentence :
    #         print e
            if e[0] not in needfactor:
                sentence1.remove(e)
    #     print sentence
        return sentence1
#     needfactor=['C', 'D', 'P', 'T', 'A','M']
#     dosentence=cleanSent(demosentence, needfactor)   
#     print dosentence

    #以cutfactor为分割点，对标注语句进行分割
    def cutsentence(self,csentence,cutfactor):
        cutindex=[]
        donesentence=[]
        for i in range(len(csentence)):
            if csentence[i][0] in cutfactor:
                cutindex.append(i)
#             else :
#                 print 'Do not exist the cut-factor'
#         print cutindex
        if cutindex != '':
            for j in range(len(cutindex)):
                if cutindex[j] !=0 and j==0 :
                    tempcut1=csentence[:cutindex[j]]
#                     donesentence.append('tempcut1')
                    donesentence.append(tempcut1)
                elif cutindex[j]!=0 and j==len(cutindex)-1 and j !=0:
                    tempcut3=csentence[cutindex[j]:]
                    tempcut2=csentence[cutindex[j-1]:cutindex[j]]                    
#                     donesentence.append('tempcut2')
#                     donesentence.append('tempcut3')
                    donesentence.append(tempcut2)
                    donesentence.append(tempcut3)
                elif j !=0 and j != len(cutindex) :
#                     print j
                    tempcut4 = csentence[cutindex[j-1]:cutindex[j]]
#                     donesentence.append('tempcut4')
                    donesentence.append(tempcut4)

        return donesentence
    ##清除列表中的空值
    def removeBlack(self,sentence):
        for data in sentence:
            for e in data:
                if e=='':                
                    data.remove(e)
        return sentence
    # 批量处理数据   
    def batchData(self,avData,needfactor,cutfactor):
        ##可调整所需数据
        vdata = []
        for data in avData:
            rightresult = self.removeBlack(data['QUOTEextraction'])
            
            sentence=data['trainData']['sentence']
            dosentence=self.cleanSent(sentence, needfactor)
            cuttedsen=self.cutsentence(dosentence, cutfactor)
            combdata=[cuttedsen,rightresult]#data['sentence']
            if cuttedsen!=[]:
                vdata.append(combdata)
            
        return vdata
    
    ##利用模型预测得到比较数据
    def calculateAcc(self,vdata,needfactor):
#         i=0
        for oridata in vdata:
            finalresult=[]
#             i+=1
#             print '\n','%s%s%s'%('第',i+1,'段数据：'),'\n'
#             print oridata[0]
            for data in oridata[0]:
                if data!=[] :
    # print '原始分段数据：'
    #                 print data
                    testdata=self.cleanSent(data, needfactor)
    #                 print '清洗过的数据：'
    #                 print testdata
                    csentence="|".join(testdata)
    #                 print '|分隔的数据 ：'
    #                 print csentence
                    result = tModel.getEntityRelationResult(csentence)

    #                 print spresult
    # #                 sortresult=[x.sort() for x in spresult]
    # #                 print sortresult                
    #                 print '模型预测结果 ：'
    #                 print result
                    if result !=[]:
                        spresult=[x.split('|') for x in result]                        
                        finalresult.append(spresult)
#                        finalresult.append(spresult)
            oridata.append(finalresult)
#         print oridata
        return vdata
            
    def delemt(self,vdata):
        for data1 in vdata:
            for data2 in data1:
                if [] in data2:
                    data2.remove([])
        return vdata
    
    ##切分表现
    def getPerformance(self,vdata):
        allnum=0##所有正确的报价
        rightnum=0##预测正确的报价
        pridictnum=0##所有预测报价
        self.delemt(vdata)
        for data in vdata:
#             print data
            for x in data[1]:
                x.sort()
#                 print x
            for x in data[2]:
                x.sort()
#                 print x 
        for data in vdata:
#             print data
            for e in data[2]:
#                 print data[2]
                for d in e :
                    pridictnum+=1
                    if d in data[1]:
                        rightnum+=1
            for zz in data[1] :
                print zz
                allnum+=1
            print data[1]      
        return allnum,rightnum,pridictnum
                 
               
        
            
        
##demo
if __name__=='__main__': 
    vType='Offline'
    needfactor=['C', 'D', 'P', 'T', 'A','R']###清除不需要标注时所需要素
    needfactor2=['D', 'P', 'T', 'A','R']##进行短句解析时所需要素
    cutfactor=['C']##切分点
    datapath = u'E:/work/infoEx/data/modelsentences3.pickle'
    ccut=cutNum(needfactor,datapath)    
    allData=ccut.getData(datapath)   
    avData=ccut.getAvdata(allData)
    demosentence=avData[3]['trainData']['sentence']
    dosentence=ccut.cleanSent(demosentence, needfactor)
#     print demosentence  
#     print dosentence
#     print ccut.cutsentence(dosentence,cutfactor)   
    daa=ccut.batchData(avData, needfactor, cutfactor)
#     for ss in daa:
#         print ss
#     print dosentence
#     sen=[u'C1', u'P1', u'P2', u'D2', u'T1', u'R1', u'T2', u'R2', u'T3', u'R3', u'T4', u'R4', u'T5', u'R5', u'T6', u'R6', u'T7', u'R7']
#     spsentence = "|".join(sen)
#     print spsentence
    tModel = initializeModel()
#     print tModel.getEntityRelationResult(spsentence)
    #print initializeModel.getEntityRelationResult(spsentence)
    
    res=ccut.calculateAcc(daa,needfactor2)
    print res
    ss= ccut.getPerformance(res)
    print ss
        