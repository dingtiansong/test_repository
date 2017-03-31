# -*- coding: utf-8 -*-
'''
Created on 2016年11月22日

@author: song

'''
import cPickle as pickle
# from test import matchData2
from matchData2 import dataMatch
class compareSet():
    def readText(self,filePath):
        textd=[]
        f = open(filePath,"r") 
        lines = f.readlines()#读取全部内容
        dataline=[]
        tmp=[]
        for line in lines:
            if '###' in line:
                dataline.append(tmp)
                tmp = []
            else:
                tmp.append(line)
#         print dataline
        for i in dataline:
#             if i !=[] :
                textd.append(i)                
        return textd
    def createDict(self,dodata,origdata):
        dict={}
        for i in range(len(dodata)):
            dict[origdata[i]]=dodata[i]
        return dict
    def getAllDictData(self,dictData):
        finalDictdata={}
        for keys in dictData.keys():
            productDictData=[]
            for i in dictData[keys]:
                z=i.split('|')
                pdict={}
                
                for j in z:
#                     print j       
                    K=j.split('(')
#                     print K[0]
                    if '\n' not in K:
#                         print K,'@@@@@@@@@@'
                        pdict[K[1][0]]=K[0]
                productDictData.append(pdict)
            finalDictdata[keys]=productDictData
        return finalDictdata
    def getDMDictData(self,offlinefilePath,finaldict):
        DMdata=[]
        cldata2 = dd.readText(offlinefilePath)
        dictionary2=dd.creOfflineDict(cldata2)
        
#         print len(dictionary2)
        allsentence=[]
        for i in dictionary2:
            if i['sentence'] not in allsentence:
#                 print i['sentence']
                allsentence.append(i['sentence'])
        za=sorted(allsentence)
        zs=sorted(finaldict.keys())
        
        for j in za:
#             print j
            alldata=[]
            for da in dictionary2:
                if da['sentence']==j:
#                     print da['sentence']
                    alldata.append(da)
            DMdata.append(alldata)
        return DMdata,allsentence
    def getWMDictData(self,origWMpath,finalWMDictData):
        DMdata=[]
        origWMdata=dd.readText(origWMpath)
        WMDict=dd.creWMDict(origWMdata)
#         print WMDict
        allsentence=[]
        for i in WMDict:
            if i['sentence'] not in allsentence:
#                 print i['sentence']
                allsentence.append(i['sentence'])
        za=sorted(allsentence)
        zs=sorted(finalWMDictData.keys())
        
        for j in za:
#             print j
            alldata=[]
            for da in WMDict:
                if da['sentence']==j:
#                     print da['sentence']
                    alldata.append(da)
            DMdata.append(alldata)
        return DMdata,allsentence
if __name__=='__main__':  
    dd=dataMatch()
    dpath='D:/data/DToffline.txt'
    dpath2='D:/data/offlinedata2.txt'
    spath='D:/data/offline.plk'
    DTWMspath='D:/data/DTWM.plk'
    offlinefilePath='D:/data/offline.txt'
    origWMpath='D:/data/origWM.txt'
    predictWMpath='D:/data/DTWMpredict.txt'
    origWMSentencepath='D:/data/WMsentence.txt'
#     with open(dpath2) as f:
#         origdata=f.readlines()
    datapath111='D:/data/WMsentence.txt'
    with open(datapath111) as f:
        data1=f.readlines()
    listsentence=''
    z=0
    for i in data1:
        z+=1
        listsentence=listsentence+i
#         print z,i
    print len(data1)
#     print listsentence
    origdata=listsentence.split('###')    
    cc=compareSet()
    dodata=cc.readText(predictWMpath)
    print '@@@@@@@@@@@@@@@@@',len(dodata)
#     for i in range(680):        
#         print dodata[i]
#         print origdata[i]
#         print '$$$$$$$$$$$$$$$$$$$$$$$$'
    dictData=cc.createDict(dodata, origdata)
#     print len(dictData)
#     for i in dictData:
#         print i
    finaldict=cc.getAllDictData(dictData)
    flag=0
    for i in finaldict.keys():
        flag+=1
        print flag,i
        print finaldict[i]
###保存数据
    f=file(DTWMspath,'w')
    pickle.dump(finaldict,f)

#     DMdata,allsentence=cc.getDMDictData(origWMpath,finaldict)
#     zs=sorted(finaldict.keys())
#     zx=[]
# 
#     for i in zs:
#         zx.append(finaldict[i])
#     for i in range(len(zs)):
#         print zx[i]
#         print DMdata[i][0]['sentence']
#         print '&&&&&&&&&&&&&&&&&&&&&&&&&'
#     print 'offlinePredictData结构：'
#     print zx[3]
#     print 'offlineDMData结构：'
#     print DMdata[3][0]['sentence']
    
# #保存数据
#     offlineDMData=file('D:/data/DTofflineDMData.plk','w')
#     pickle.dump(DMdata,offlineDMData)
#     offlinePredictData=file('D:/data/DTofflinePredictData.plk','w')
#     pickle.dump(zx,offlinePredictData)
#     origWMdata=dd.readText(origWMpath)
#     WMDict=dd.creWMDict(origWMdata)
#     with open(origWMSentencepath) as f:
#         origWMSentence=f.read()
#     splitOrigWMSentence=origWMSentence.split('###')
#     for i in WMDict:
#         print i['sentence']
#     zzsentence=[]
#     for i in WMDict:
#         if i['sentence'] not in zzsentence:
#             zzsentence.append(i['sentence'])
#     print len(zzsentence)
#     zzdict={}
#     for i in splitOrigWMSentence:
#         temp=[]
#         for j in WMDict:
#             if j['sentence']==i:
#                 temp.append(j)
#         zzdict[i]=temp
#     print len(zzdict)
#     for i in zzdict:
#         print zzdict[i]
#     predictWM=cc.readText(predictWMpath)   
#  
#  
#     WMdictdata=cc.createDict(predictWM, splitOrigWMSentence)
#   
#     finalWMDictData=cc.getAllDictData(WMdictdata)
#     WMDMdata,WMallsentence=cc.getWMDictData(origWMpath, finalWMDictData)
# #     for i in WMDMdata:
# #         print i
# #         print WMDMdata[0]['sentence'] 
#     zs=sorted(finalWMDictData.keys())
# ##保存数据
# #     WMDMDatapath=file('D:/data/WMDMData.plk','w')
# #     pickle.dump(WMDMdata,WMDMDatapath)
# #     WMPredictDatapath=file('D:/data/WMPredictData.plk','w')
# #     pickle.dump(zxwm,WMPredictDatapath)
# #         
#     for i in range(len(zs)):
#         print zxwm[i],i
#         print WMDMdata[i][0]['sentence'],i
#         print '&&&&&&&&&&&&&&&&&&&&&&&&&'
#     print 'offlinePredictData结构：'
#     print zxwm[500][1]
#     print 'offlineDMData结构：'
#     print WMDMdata[500][0]['sentence']