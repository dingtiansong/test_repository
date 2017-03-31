# -*- coding: utf-8 -*-
'''
Created on 2015年10月28日

@author: song
'''
import pandas as pd
import numpy as np
import nltk
from nltk.probability import FreqDist
# import pickle
import cPickle as pickle
import re
from time import clock as now


class dataMatch():
    '''
    1.处理解析标准数据对应原文
    2.构建要素字典
    3.根据要素字典，将原文转化为标注文本
    '''   
    
    print __doc__
    def cutIndex(self,data):
        cutindex=[]
        index2=[]
        cldata=[]
        for i in range(len(data)):
#             if '---' not in data.values[i][0]:
#                 
            if '----' in data.values[i][0]:
                cutindex.append(i)
        for i in range(0,len(cutindex)-1):
            if cutindex[i]+1==cutindex[i+1]:
                index2.append(cutindex[i+1])
        for i in index2:cutindex.remove(i)
        return cutindex
#     print cutIndex(data)
    def moveN(self,data):
        sa=[]
        for i in data:
            for x in i:
                dd= '---------------------------------------------' not in x
                sa.append(dd)
        aa=np.array(sa)
        mdata=data[aa]
        return mdata
    def cutData(self,data):
        spdata=[]
        xdata=[]
        cin=self.cutIndex(data)
        for i in range(len(cin)):
            temp=[]
            if i == 0 and cin[0] !=0:
                temp=data.values[0:cin[0]]
                tt=self.moveN(temp)
                spdata.append(tt)
#                 print tt[0][0]
                xdata.append(temp)
            elif i==len(cin):
                temp=data.values[cin[len(cin)-1]:cin[len(cin)]]
                tt=self.moveN(temp)
                spdata.append(tt)
#                 print tt[0]
                xdata.append(temp)
            else:
                temp=data.values[cin[i-1]:cin[i]]
                tt=self.moveN(temp)
                spdata.append(tt)
                xdata.append(temp)
            for i in range(len(spdata)):
                ttemp=self.moveN(spdata[i])
#                 print ttemp
#                 xdata[i]=ttemp
        return spdata,xdata
    
    def product(self,cldata,place):
        '''
        cldata为预处理之后的数据
        place为所需数据类型
        报价方：江西银行南昌 谌鹏
        方向：出
        种类：协议存款
        币种：人民币
        金额：
        期限：6个月
        利率：
        预约：
        发布时间：08:27
        原文:江西银行出协议存款（基金通道 按季结息）6个月 9个月 1年 欢迎报价 电话13970935063 微信号248976232
        '''
        lista=[]
        product1=[]
        for i in cldata:
            lista.append(i[place])
            if i[place] not in product1:
                product1.append(i[place])
        return product1,lista
#     def collectData(self,cldata):
#         for i in range(len(cldata)):
            
    def readText(self,filePath):
        textd=[]
        f = open(filePath,"r") 
        lines = f.readlines()#读取全部内容
        dataline=[]
        tmp=[]
        for line in lines:
            if '-------------------------------------------------' in line:
                dataline.append(tmp)
                tmp = []
            else:
                tmp.append(line)
    #     print dataline
        for i in dataline:
            if i !=[] :
                textd.append(i)                
        return textd
###  生成对于字典形式数据
    def creDictOnline(self,Formdata):
        dataDict = []
        for tmp in Formdata:
            tmpDict = {}
            # 报价方：包商银行北京 史琳
#             tmpDict['user'] = '：'.join(tmp[0].split('：')[1:]).strip()
            # 方向：出
            tmpDict['D'] = '：'.join(tmp[1].split('：')[1:]).strip()
            # 种类：资金
            tmpDict['P'] = '：'.join(tmp[3].split('：')[1:]).strip()
            # 对手：限农信
            tmpDict['O'] = '：'.join(tmp[4].split('：')[1:]).strip()
            # 金额：1.0亿元
            tmpDict['A'] = '：'.join(tmp[6].split('：')[1:]).strip()
            # 期限：7天
            tmpDict['T'] = '：'.join(tmp[2].split('：')[1:]).strip()
            # 利率：
            tmpDict['R'] = '：'.join(tmp[5].split('：')[1:]).strip()
            # 预约：
            tmpDict['reserve'] = '：'.join(tmp[7].split('：')[1:]).strip()
            # 发布时间：11:10
#             tmpDict['time'] = '：'.join(tmp[8].split('：')[1:]).strip()
            # 原文:出7天 1亿起出，欢迎小窗~
            tmpDict['sentence'] = ':'.join(tmp[9].split(':')[1:]).strip()            
            dataDict.append(tmpDict)
        return dataDict
    def creOfflineDict(self,Formdata):
        dataDict = []
        for tmp in Formdata:
            tmpDict = {}
            # 报价方：包商银行北京 史琳
#             tmpDict['user'] = '：'.join(tmp[0].split('：')[1:]).strip()
            # 方向：出
            tmpDict['D'] = '：'.join(tmp[1].split('：')[1:]).strip()
            # 种类：资金
            tmpDict['P'] = '：'.join(tmp[2].split('：')[1:]).strip()
            # 币种：人民币
#             tmpDict['CCY'] = '：'.join(tmp[3].split('：')[1:]).strip()
            # 金额：1.0亿元
            tmpDict['A'] = '：'.join(tmp[4].split('：')[1:]).strip()
            # 期限：7天
            tmpDict['T'] = '：'.join(tmp[5].split('：')[1:]).strip()
            # 利率：
            tmpDict['R'] = '：'.join(tmp[6].split('：')[1:]).strip()
            # 预约：
            tmpDict['reserve'] = '：'.join(tmp[7].split('：')[1:]).strip()
            # 发布时间：11:10
#             tmpDict['time'] = '：'.join(tmp[8].split('：')[1:]).strip()
            # 原文:出7天 1亿起出，欢迎小窗~
            tmpDict['sentence'] = ':'.join(tmp[9].split(':')[1:]).strip()            
            dataDict.append(tmpDict)
        return dataDict

    
    
    
    
    
    def creWMDict(self,Formdata):
# 报价方：中信天津 白文
# 方向：出
# 保本性质：
# 期限：360天
# 利率：
# 金额：
# 投向：
# 风险评级：R2
# 保函：
# 备注：
# 说明书：
# 原文:售一年期理财，价格优，r2，要得赶紧联系哇
        dataDict = []
        for tmp in Formdata:
            tmpDict = {}
            # 报价方：包商银行北京 史琳
#             tmpDict['user'] = '：'.join(tmp[0].split('：')[1:]).strip()
            # 方向：出
            tmpDict['D'] = '：'.join(tmp[1].split('：')[1:]).strip()
            # 种类：保本
            tmpDict['P'] = '：'.join(tmp[2].split('：')[1:]).strip()
            # 币种：人民币
#             tmpDict['CCY'] = '：'.join(tmp[3].split('：')[1:]).strip()
            # 金额：1.0亿元
            tmpDict['A'] = '：'.join(tmp[5].split('：')[1:]).strip()
            # 期限：7天
            tmpDict['T'] = '：'.join(tmp[3].split('：')[1:]).strip()
            # 利率：
            tmpDict['R'] = '：'.join(tmp[4].split('：')[1:]).strip()
            # 风险评级：R2
            tmpDict['Rank'] = '：'.join(tmp[7].split('：')[1:]).strip()
            # 保函：
#             tmpDict['time'] = '：'.join(tmp[8].split('：')[1:]).strip()
            # 备注：
#             tmpDict['PS'] = '：'.join(tmp[9].split('：')[1:]).strip()
            # 说明书：
#             tmpDict['M'] = '：'.join(tmp[10].split('：')[1:]).strip()
            # 原文:出7天 1亿起出，欢迎小窗~
#             if len(tmp)==12:
#             tmpDict['sentence'] = ':'.join(tmp[11].split(':')[1:]).strip() 
#             else :
            zx=''
            for i in range(11,len(tmp)):
                zx+=tmp[i]
            tmpDict['sentence'] = ':'.join(zx.split(':')[1:]).strip() 
#             print len(tmp)                            
            dataDict.append(tmpDict)
        return dataDict

    def divdict1(self,dataDict):
        '''生成分类字典'''
        ##用户字典
        userdict=[]
        ##方向字典
        Ddict=[]
        ##产品字典
        Pdict=[]
        ##期限字典
        Tdict=[]
        ##利率字典
        Rdict=[]
        ##原句
        sentdict=[]
        ##资金字典
        Adict=[]
        resdict=[]
        for dic in dataDict:
            for keys in dic.keys():
                if keys=='user':
                    if dic[keys] not in userdict :
                        userdict.append(dic[keys])
                elif keys=='D':
                    if dic[keys] not in Ddict:
                        Ddict.append(dic[keys])
                elif keys=='P':
                    if dic[keys] not in Pdict:
                        Pdict.append(dic[keys])
                elif keys=='T':
                    if dic[keys] not in Tdict:
                        Tdict.append(dic[keys])
                elif keys=='R':
                    if dic[keys] not in Rdict:
                        Rdict.append(dic[keys])
                elif keys=='sentence':
                    if dic[keys] not in sentdict:
                        sentdict.append(dic[keys])
                elif keys=='reserve':
                    if dic[keys] not in resdict:
                        resdict.append(dic[keys])
                elif keys=='A':
                    if dic[keys] not in Adict:
                        Adict.append(dic[keys])
#         finalDict=[userdict,Ddict,Pdict,Tdict,Rdict,sentdict,resdict]
        finalDict=[Ddict,Pdict,Tdict,Rdict]
        return finalDict
    
    def findTransSentence(self,datadict):
        '''找到转换的要素'''
        transset=[]
        for tagsentence in datadict :
            for keys in tagsentence.keys():
#                 print keys
                if keys !='sentence':
                    if tagsentence[keys] not in tagsentence['sentence']:
                        if tagsentence not in transset:
                            transset.append(tagsentence)
        return transset
    def findNoTransSentence(self,datadict,vtype):
        if vtype =='online':
            kinds=7
        elif vtype== 'offline':
            kinds=6
        '''找到转换的要素'''
        transset=[]
        for tagsentence in datadict :
            i=0
            for keys in tagsentence.keys():
#                 print keys
                if keys !='sentence':
                    if tagsentence[keys]  in tagsentence['sentence']:
                        i+=1
            if i == kinds and tagsentence not in transset:
#                     if tagsentence not in transset:
                transset.append(tagsentence)
        return transset
    def storeDict(self,dict_path,dict_data):
        """将数据到本地"""
        with open(dict_path, "wb") as f:
            pickle.dump(dict_data, f)
        f.close() 

    def printOffline(self,sentoffline,dictionary):              
            '''线下数据输出'''
            m=0
            for i in sentoffline:
                m+=1
                print '这是第',m,'段数据：'
                print '--------------------------------'
                print '原文：',i['sentence']
                print '方向：',i['D']
                if i['D'] in i['sentence']:
                    print i['D']
                else: print 'NA'
                print '种类：',i['P']
                if i['P'] in i['sentence']:
                    print i['P']
                else: print 'NA'
                print '利率：',i['R']
                if i['R'] in i['sentence']:
                    print i['R']
                else: print 'NA'
                print '期限：',i['T']
                if i['T'] in i['sentence']:
                    print i['T']
                else: print 'NA'
                print '金额：',i['A']
                if i['A'] in i['sentence']:
                    print i['A']
                else: print 'NA'
                print '预约：',i['reserve']
                if i['reserve'] in i['sentence']:
                    print i['reserve']
                else: print 'NA'
                print '--------------------------------'
            totalnum=len(dictionary)
            print m
            print totalnum
            print '包含转换的报价比例为' ,float(m)/totalnum    
    def saveOffline(self,sentoffline,dictionary,sofflinepath):              
            '''线下数据输出'''
            m=0
            with open(sofflinepath,'wb') as f:
                for i in sentoffline:
                    m+=1
                    temp1='这是第%s段数据：'%(m)
                    temp2='--------------------------------'
                    temp3='原文：'+i['sentence']
                    temp4='方向：'+i['D']
                    if i['D'] in i['sentence']:
                        temp5=i['D']                    
                    else: temp5='NA'
                    temp6='种类：'+i['P']
                    if i['P'] in i['sentence']:
                        temp7=i['P']
                    else: temp7='NA'                   
                    temp8= '利率：'+i['R']
                    if i['R'] in i['sentence']:
                        temp9=i['R']
                    else: temp9= 'NA'
                    temp10='期限：'+i['T']
                    if i['T'] in i['sentence']:
                        temp11= i['T']
                    else: temp11= 'NA'
                    temp12= '金额：'+i['A']
                    if i['A'] in i['sentence']:
                        temp13= i['A']
                    else: temp13= 'NA'
                    temp14= '预约：'+i['reserve']
                    if i['reserve'] in i['sentence']:
                        temp15= i['reserve']
                    else: temp15= 'NA'
                    temp17= '--------------------------------'
                    sseries=[temp1+'\n',temp2+'\n',temp3+'\n',temp4+'\n',temp5+'\n',temp6+'\n',temp7+'\n',temp8+'\n',temp9+'\n',temp10+'\n',temp11+'\n',temp12+'\n',temp13+'\n',temp14+'\n',temp15+'\n',temp17+'\n']                        
                    f.writelines(sseries)            
            totalnum=len(dictionary)
            print m
            print totalnum
            print '包含转换的报价比例为' ,float(m)/totalnum    
    def printOnline(self,sentonline,dictionary):              
            '''线上数据输出'''
            m=0
            for i in sentonline:
                m+=1
                print '这是第',m,'段数据：'
                print '--------------------------------'
                print '原文：',i['sentence']
                print '方向：',i['D']
                if i['D'] in i['sentence']:
                    print i['D']
                else: print 'NA'
                print '模式：',i['P']
                if i['P'] in i['sentence']:
                    print i['P']
                else: print 'NA'
                print '利率：',i['R']
                if i['R'] in i['sentence']:
                    print i['R']
                else: print 'NA'
                print '期限：',i['T']
                if i['T'] in i['sentence']:
                    print i['T']
                else: print 'NA'
                print '金额：',i['A']
                if i['A'] in i['sentence']:
                    print i['A']
                else: print 'NA'
                print '预约：',i['reserve']
                if i['reserve'] in i['sentence']:
                    print i['reserve']
                else: print 'NA'
                print '对手：',i['O']
                if i['O'] in i['sentence']:
                    print i['O']
                else: print 'NA'
                print '--------------------------------'
            totalnum=len(dictionary)
            print m
            print totalnum
            print '包含转换的报价比例为' ,float(m)/totalnum 
    def saveOnline(self,sentonline,dictionary,sonlinepath):
            '''线上数据输出'''
            m=0
            with open(sonlinepath,'wb') as f:
                for i in sentonline:
                    m+=1
                    temp1='这是第%s段数据：'%(m)
                    temp2='--------------------------------'
                    temp3='原文：'+i['sentence']
                    temp4='方向：'+i['D']
                    if i['D'] in i['sentence']:
                        temp5=i['D']                    
                    else: temp5='NA'
                    temp6='模式：'+i['P']
                    if i['P'] in i['sentence']:
                        temp7=i['P']
                    else: temp7='NA'                   
                    temp8= '利率：'+i['R']
                    if i['R'] in i['sentence']:
                        temp9=i['R']
                    else: temp9= 'NA'
                    temp10='期限：'+i['T']
                    if i['T'] in i['sentence']:
                        temp11= i['T']
                    else: temp11= 'NA'
                    temp12= '金额：'+i['A']
                    if i['A'] in i['sentence']:
                        temp13= i['A']
                    else: temp13= 'NA'
                    temp14= '预约：'+i['reserve']
                    if i['reserve'] in i['sentence']:
                        temp15= i['reserve']
                    else: temp15= 'NA'
                    temp17= '对手：'+i['O']
                    if i['O'] in i['sentence']:
                        temp17=i['O']
                    else: temp17= 'NA'
                    temp18='--------------------------------'
                    sseries=[temp1+'\n',temp2+'\n',temp3+'\n',temp4+'\n',temp5+'\n',temp6+'\n',temp7+'\n',temp8+'\n',temp9+'\n',temp10+'\n',temp11+'\n',temp12+'\n',temp13+'\n',temp14+'\n',temp15+'\n',temp17+'\n',temp17+'\n',temp18+'\n']                        
                    f.writelines(sseries)      
    def getdata(self,vdatapath):
        f = open(vdatapath,"r")  
        lines = f.readlines()
        data=lines[1:]
        for sentence in data:
            if '这是第' in sentence:
                data.remove(sentence)
        return data
    def lenSort(self,dictList):
        dictList.sort(lambda x,y :cmp(len(x),len(y)),reverse=True)
        return dictList

    def creTotalOfflineDict(self,data):            
        totalAdict=[]
        totalRdict=[]
        totalPdict=[]
        totalTdict=[]
        totalDdict=[]
        totalRedict=[]
        totalOriginalSentence=[]
        for i in range(len(data)/15):
            if data[i*15+1] not in totalOriginalSentence:
                totalOriginalSentence.append(data[i*15+1])
            if data[i*15+3] not in totalDdict:
                totalDdict.append(data[i*15+3])
            if data[i*15+5] not in totalPdict:
                totalPdict.append(data[i*15+5])
            if data[i*15+7] not in totalRdict:
                totalRdict.append(data[i*15+7])
            if data[i*15+9] not in totalTdict:
                totalTdict.append(data[i*15+9])         
            if data[i*15+11] not in totalAdict:
                totalAdict.append(data[i*15+11])  
            if data[i*15+13] not in totalRedict and any(data[i*15+13]):
                totalRedict.append(data[i*15+13])     
        totaldict=[totalOriginalSentence,totalDdict,totalPdict,totalRdict,totalTdict,totalAdict,totalRedict]
        for i in totaldict:
#             print i
            self.lenSort(i)
        return totaldict
    def creTotalOnlineDict(self,data):    
        '''生成线上字典'''        
        totalAdict=[]
        totalRdict=[]
        totalPdict=[]
        totalTdict=[]
        totalDdict=[]
        totalRedict=[]
        totalOpp=[]
        totalOriginalSentence=[]
        for i in range(len(data)/17):
            if data[i*17+1] not in totalOriginalSentence:
                totalOriginalSentence.append(data[i*17+1])
            if data[i*17+3] not in totalDdict:
                totalDdict.append(data[i*17+3])
            if data[i*17+5] not in totalPdict:
                totalPdict.append(data[i*17+5])
            if data[i*17+7] not in totalRdict:
                totalRdict.append(data[i*17+7])
            if data[i*17+9] not in totalTdict:
                totalTdict.append(data[i*17+9])         
            if data[i*17+11] not in totalAdict:
                totalAdict.append(data[i*17+11])  
            if data[i*17+13] not in totalRedict and data[i*17+13] !='\n':
                totalRedict.append(data[i*17+13])     
            if data[i*17+15] not in totalOpp and data[i*17+15] !='\n':
                totalOpp.append(data[i*17+15])     
        totaldict=[totalOriginalSentence,totalDdict,totalPdict,totalRdict,totalTdict,totalAdict,totalRedict,totalOpp]
        return totaldict
    def creorigOfflineDict(self,data):     
        '''
        生成线下字典
        '''       
        totalAdict=[]
        totalRdict=[]
        totalPdict=[]
        totalTdict=[]
        totalDdict=[]
        totalRedict=[]
        totalOriginalSentence=[]
        for i in range(len(data)/15):
            if data[i*15+1] not in totalOriginalSentence:
                totalOriginalSentence.append(data[i*15+1])
            if data[i*15+3] not in totalDdict:
                totalDdict.append(data[i*15+3])
            if data[i*15+5] not in totalPdict:
                totalPdict.append(data[i*15+5])
            if data[i*15+7] not in totalRdict:
                totalRdict.append(data[i*15+7])
            if data[i*15+9] not in totalTdict:
                totalTdict.append(data[i*15+9])         
            if data[i*15+11] not in totalAdict:
                totalAdict.append(data[i*15+11])  
            if data[i*15+13] not in totalRedict:
                totalRedict.append(data[i*15+13])     
        totaldict=[totalOriginalSentence,totalDdict,totalPdict,totalRdict,totalTdict,totalAdict,totalRedict]
        return totaldict
    def transChunk(self,data):
        '''
        按句对数据进行分块
        '''  
        chunkdata=[]
        dataline=[]
        tmp=[]
        for line in data:
            if '--------------------------------' in line:
                dataline.append(tmp)
                tmp = []
            else:
                tmp.append(line)
    #     print dataline
        for i in dataline:
            if i !=[] :
                chunkdata.append(i)                
        return chunkdata
    def tagFactor(self,tagsentence):
        '''
        对标注后序列进行编号
        '''
        replacesentence=[]
        slen=len(tagsentence)
        for i in range(slen):
            if i == 0:
                tempfactor=tagsentence[0]+str(1)
#                 print tempfactor
            else :
                m=0
                for j in tagsentence[:i]:
                    if tagsentence[i] == j:
                        m+=1
                tempfactor=tagsentence[i]+str(m+1)
#                 print tempfactor
            replacesentence.append(tempfactor)
        return replacesentence
            
    def findAllFactorIndex(self,factor,sentence):
        '''
        找出所有句中所有factor的位置
        '''
        startindex=0
        numlist=[]
        while True:
            index=sentence.find(factor,startindex)
            if index == -1:     
                break    
            numlist.append(index)
            startindex=index+1
        return numlist

    def generateTagSentence(self,vdict,needtag,sentence):
        '''
        根据字典将原文转化为标注序列
        '''
        datadict=[]
        tagsentence=sentence
        rightOrigSentence=[]
#         m=0
        for i in needtag:
            for j in vdict[i]:
                jn=j.replace('\n','')
                if jn in tagsentence and jn != '':                    
#                     print jn,m
                    rightOrigSentence.append(jn)
                    tagsentence=tagsentence.replace(jn,i)
                    z=self.findAllFactorIndex(jn, sentence)
                    datadict.append((jn,z))                   
        aaa=re.sub('[^DPTRA]','',tagsentence)  
#         print aaa                 
        tagsentence2=self.tagFactor(aaa)
#         dat=self.reverseDict(datadict)
#                     print tagsentence
        return tagsentence2,rightOrigSentence,datadict##,dat

    def reverseDict(self,datadict):
        tempdict={}
        origFactor=[]
        for i in datadict:
            if len(i[1])==1 :
                tempdict[str(i[1][0])]=i[0]
#                 print i[0],i[1]
            else:
                for j in i[1]:
                    tempdict[str(j)]=i[0]
        sortkey=sorted([int(i) for i in tempdict.keys()])
        for key in sortkey:
            origFactor.append(tempdict[str(key)])
        return origFactor
            
        
if __name__=='__main__':  

    offlinefilePath = 'C:/Users/john64pc/Desktop/offlinedata1031.txt'
    dict_path='C:/Users/john64pc/Desktop/offlinedict.txt'
    onlinefilePath='C:/Users/john64pc/Desktop/onlineText.txt'
    ##处理过之后的数据
    doneofflinedatapath=r'C:/Users/john64pc/Desktop/DMdata/offlineTextcombine1104.txt'
    doneonlinedatapath='C:/Users/john64pc/Desktop/DMdata/onlineTextcombine1104.txt'
    ##储存地址
    sonlinepath='C:/Users/john64pc/Desktop/DMdata/sonlinedata.txt'
    sofflinepath='C:/Users/john64pc/Desktop/DMdata/sofflinedata.txt'
    
    dd=dataMatch()
    ##处理线下数据
    cldata2 = dd.readText(offlinefilePath)
    dictionary2=dd.creOfflineDict(cldata2)
    sent2=dd.findTransSentence(dictionary2)
    type1='offline'
    nosent2=dd.findNoTransSentence(dictionary2,type1)
#     dd.printOffline(nosent2,dictionary2)
##    储存线下数据
#     dd.saveOffline(sent2, dictionary2,sofflinepath)
    ##处理线上数据
    clondata=dd.readText(onlinefilePath)  
    dictionary3=dd.creDictOnline(clondata)
    sent3=dd.findTransSentence(dictionary3)
    ##全匹配数据
    type2='online'
    nosent3=dd.findNoTransSentence(dictionary3,type2)
##  储存线上数据
#     dd.saveOnline(sent3, dictionary3, sonlinepath)
#     dd.printOnline(nosent3,dictionary3) 
#     dd.printOnline(sent3,dictionary3) 

#     with open(sonlinepath,'r') as f: 
#         dddd=f.readlines()
#     for i in dddd:
#         print i
    donedata=dd.getdata(doneofflinedatapath)
    allDict=dd.creTotalOfflineDict(donedata)
    dictindex=['sentence','D','P','R','T','A','RE']
    dictoff=pd.Series(allDict,dictindex)
## 保存字典
#     outoffline = file('C:/Users/john64pc/Desktop/DMdata/offlineDict.pkl', 'w')    
#     pickle.dump(dictoff,outoffline)
    with open('C:/Users/john64pc/Desktop/DMdata/offlineDict.pkl') as f:
        data1=pickle.load(f)
    f.close()
#     for i in dictoff.values:
#         for j in i :
#             print j
    ###报价标注
    needtag=['D','P','R','T','A','RE']
    sentence=dictoff['sentence'][1]
    regexp =u'[\u4E00-\u9FA5]'
#     zzz,ooo=dd.generateTagSentence(dictoff, needtag, sentence)
#     print zzz
    nu=1
    for sentenc in dictoff['sentence']:
        nu+=1
        zzz,ooo,dict1=dd.generateTagSentence(dictoff, needtag, sentenc)
        print '这是第%s段'%(nu)+sentenc.replace('\n','')
        print '标注文本:',zzz
        print '要素原文：'
        factz=''
        vlist=''
#         for i in ooo:
#                 factz+=i+'|'
#         print factz
        for i in dict1:
            print i[0],i[1]
        tlist=dd.reverseDict(dict1)
        for t in tlist:
            vlist+=t+'|'
        print vlist
        print '\n'
    ###线上
    donedata2=dd.getdata(doneonlinedatapath)
    allDict2=dd.creTotalOnlineDict(donedata2)
    dictindex=['sentence','D','P','R','T','A','RE','O']
#     dictOnline=pd.Series(allDict2,dictindex)
#     f = file('C:/Users/john64pc/Desktop/DMdata/onlineDict.pkl', 'w')    
#     pickle.dump(dictOnline,f)
    
##    读取文件
#     with open('C:/Users/john64pc/Desktop/DMdata/onlineDict.pkl') as f:
#         data2=pickle.load(f)
#     f.close()
#     for i in data2:
#         for j in i :
#             print j
#     for i in allDict:
#         for j in i :
#             print j
#     for i in donedata:
#         print i
#     data=donedata
#     totalDdict=[]
#     wa=dd.divdict1(dictionary2)
#     prodict=pd.Series(wa,index=['D','P','T','R'])
#     for i in prodict['D']:
#         for j in i:
#             for ind in range(len(data)/15):
#                 if data[i*15+2] == j:
#                     totalDdict.append(data[i*15+3])

#########################################统计分布########################

#     for i in data:
#         print i      

##各变量的频率分布
#     aa=FreqDist(lista)
#     for word in aa.items():
#         for factor in word:
#             print factor 
        
#     for i in index1:
#         for j in i:
#             print j[0]
