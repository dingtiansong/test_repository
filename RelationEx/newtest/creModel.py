# -*- coding: utf-8 -*-
'''
Created on 2016年10月18日

@author: song
'''
import pickle
from pandas.core.frame import DataFrame
import numpy as np

datapath = u'E:/work/infoEx/data/modelsentences3.pickle'
def getData(datapath):
    with open(datapath, 'rb') as f:
        allData = pickle.load(f)
    return allData
    
allData=getData(datapath)


##可用的数据（含分段数据）   
def getAvdata(allData):
    avData=[]
    for i in allData.keys():
            tDict = allData[i]['trainData']
            if len(tDict['feature']) > 0:
                if len([x for x in tDict['result'] if x > 0]) > 0:
    #                 print i,len(tDict['feature']),len(tDict['result']),len(tDict['feature'])-len(tDict['result'])==0
    #                 print tDict['result']
                    avData.append(allData[i])
    return avData


avData=getAvdata(allData)

# print len(avData)
##trainData index    ['sentence', 'result', 'feature']
# print avData[1]['trainData']
def dataMatrix(avData,needfactors):
    modelData=[]
    xdata=[]
    ydata=[]
    for i in range(len(avData)):
        sentence=avData[i]['trainData']['sentence']
        result=avData[i]['trainData']['result']
        feature=avData[i]['trainData']['feature']
        lensen=len(sentence)
#         print lensen
        for j in range(lensen):
            if sentence[j][0] in needfactors :
#                 print sentence[j],sentence             
#                 print j,result
                comdata=[result[j-1],sentence[j],feature[j]]

#                 print feature[j]
#                 allModeldata=[feature[j]+result[j]+sentence[j]
                xdata.append(feature[j])
                ydata.append(result[j-1])
                modelData.append(comdata)
                framedata=DataFrame(modelData)
                framex=DataFrame(xdata)
                framey=DataFrame(ydata)                
    return framedata,framex,framey

needfactors=['C','D']
# needfactors=['']
data1,xdata,ydata=dataMatrix(avData,needfactors)
print xdata,ydata
# print np.var(xdata)
# print data1[2].values.append('D')

                
