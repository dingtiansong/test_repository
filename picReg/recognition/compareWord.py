# -*- coding: utf-8 -*-
'''
Created on 2016年12月15日

@author: song
'''
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import cPickle as pickle
from  nltk import FreqDist

class compareword(object):
    '''
    1.将图片转化为数值形式储存
    2.对比图像寻找相同映射的图像    
    '''
#     print __doc__
    
    def convertToBinary(self,image):
        '''
        1.图片并转为二值化,按列存为向量
        '''       
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        x = np.array(gray)
        wordindex=x.sum()/255
        wordvector=x.reshape((1600,-1),order='F').T
        return wordindex,wordvector
        
    def readPic(self,picpath,startnum,picnum):
        '''
        1.历史数据批量存储，建立索引
        '''
#         picId = 0
        img0=cv2.imread(picpath+"/%s.png"%(0))
        wordindex0,dataMatrix=self.convertToBinary(img0)
        index0=[wordindex0]
#         xxxxx=np.concatenate((dataMatrix,dataMatrix))
#         print 'zzzzzzzzz'
#         print xxxxx[1]
        for i in range(startnum,picnum):
            vpath=picpath+"/%s.png"%(i)
            image = cv2.imread(vpath)
            wordindex,wordvector=self.convertToBinary(image)
#             print wordindex
            index0.append(wordindex) 
#             print index0
            dataMatrix=np.concatenate((dataMatrix,wordvector))
        return dataMatrix,index0,wordindex0
    
    def getWordIndex(self,wordlist,targetID):
        '''
        1.得到可能的目标字范围
        '''
        print targetID
#         targetID=1000

        targetlist=range(targetID-5,targetID+5)
#         print targetlist
        targetindex=[]
        for i in range(len(wordlist)):
            if wordlist[i] in targetlist:
                targetindex.append(i)
        if targetindex==[]:
            print 'warning:这可能是一个新词，请检查！'
        return targetindex
                
    def moveToCompare(self,dvector,step):
        '''
        1.平移比较数据
        '''
        transvectorlist=[]
        ##左平移
        for i in range(0,step+1):
            steplen=[0]*20*i
#             print steplen,11
            dvector=list(dvector)
#             print type(dvector)
            movevector=dvector+steplen            
            returnvector=movevector[i*20:]
#             print returnvector
#             print len(returnvector)
            transvectorlist.append(returnvector)
        ##右平移
        for i in range(1,step+1):
            steplen=[0]*20*i
            movevector=steplen+dvector
            returnvector=movevector[:-i*20]
#             print returnvector
#             print len(returnvector)
            transvectorlist.append(returnvector)   
        ##transvectorlist=[原始，左移1，左移2，...，右移1，右移2，...]            
        return transvectorlist

                
    def getWord(self,newimage,wordlist,dataMatrix):
        '''
        1.对比数据找到相同字符
        变量说明：targetindex，目标范围内的历史字典索引
        
        '''
        newID,newvector=self.convertToBinary(newimage)
#         print 'testing:',newID
        targetindex=self.getWordIndex(wordlist, newID)
#         print dataMatrix.shape
#         print len(dataMatrix[0])
#         print dataMatrix[2].shape
        targetmatrix=dataMatrix[targetindex,:]
        ##新图向量
        newvectorlist=newvector[0]
#         print len(targetmatrix[1])
        return targetmatrix,targetindex,newvectorlist

    def compareVector(self,cutpart,targetmatrix,targetindex,transvectorlist,wordindex0): 
#         print targetindex
        wordindex=[]
        for j in range(0,len(targetmatrix)):                
            for i in range(0,len(transvectorlist)) :
                dovector=targetmatrix[j] - np.array(transvectorlist[i])
#                 print dovector
#                 print dovector[0]
#                 middovector=dovector[41:221]
                middovector=dovector[(cutpart*20+1):((14-cutpart)*20+1)]
#                 print [(cutpart*20+1),((13-cutpart)*20+1)]
                flag1=0
                for i in middovector:
                    if i == 0:
                        flag1+=1
                    
#                 print flag1,targetindex[j]
                
#                 print len(middovector)
                if wordindex0<55 and flag1==((14-2*cutpart)*20):
                    print wordindex0
                    if targetindex[j] not in wordindex and targetindex[j] !=[]:
                            wordindex.append(targetindex[j])
                else:
                    if flag1>((14-2*cutpart)*20-5):
                        if targetindex[j] not in wordindex and targetindex[j] !=[]:
                            wordindex.append(targetindex[j])
#                     print wordindex
        return wordindex        
    def storeData(self,datapath,data):
        """将数据到本地"""
        with open(datapath, "wb") as f:
            pickle.dump(data, f)
        f.close() 

    def readdata(self,datapath):
        with open(datapath) as f:
            data1=pickle.load(f)
        f.close()   
        return data1      
    def seeTheRight(self,path1):
        with open(path1) as f:
            data1=f.readlines()
        datalist=[]
        inverdict={}
        for i in data1:
            xx= i.split('{S}')
            datalist.append(xx)
            inverdict[xx[1].strip()]=xx[0]
#         print  inverdict

        
        wordlist=[]
        for i in datalist:
            if i[0] not in wordlist:
                wordlist.append(i[0])
        
#         print '总词数：',len(datalist)
        samelist=[]
        worddict={}
        for i in wordlist:
            ss=[i]
            for j in datalist:
                if i == j[0]:
                    ss.append(j[1].strip())      
            if ss not in samelist:
                samelist.append(ss)
        for i in  samelist:
            if len(i)>2:
                worddict[i[0]]=i[1:]
        return worddict,inverdict
    def scalecompare(self,picpath,startnum,picnum,movestep):
        list2=[]
        dataMatrix,wordlist,wordindex0=aa.readPic(picpath,startnum,picnum)

        for i in range(startnum,picnum):
            newimage=cv2.imread(picpath+"/%s.png"%(i))
    #         dataMatrix,wordlist=aa.readPic(picpath,i+1,1000)
            targetmatrix,targetindex,newvector=aa.getWord(newimage, wordlist, dataMatrix)
            list1=aa.moveToCompare(newvector,movestep)
        #     print targetindex
            result1=aa.compareVector(cutpart,targetmatrix, targetindex, list1,wordindex0)
            if len(result1)!=1 and result1 not in list2:
                list2.append(result1)   
        return list2
    def predictWord(self,candidateImage,dataMatrix,wordlist,inverdict):
        ##切割列数
        cutpart=4
        ##平移列数
        movestep=2    
        targetmatrix,targetindex,newvector=self.getWord(candidateImage, wordlist, dataMatrix)
        candidatelist=self.moveToCompare(newvector,movestep)
        result1=self.compareVector(cutpart,targetmatrix, targetindex, candidatelist)
        if result1 !=[]:
            predictword=[]
#                 print result1
            for j in result1:
#                 print '预测可能词：',inverdict[str(i)]
                predictword.append(inverdict[str(j)])
            fdist1=FreqDist(predictword)
#             print '可能预测词：',fdist1.keys()[0],'            预测概率为：',fdist1.freq(fdist1.keys()[0])
#             if fdist1.keys()[0]==inverdict2[str(i)]:
#                 flagx+=1
#             else: print '识别错误，请检查！！'
#             if fdist1.freq(fdist1.keys()[0]) !=1:
#                 print '可能预测词：',fdist1.keys()[1],'            预测概率为：',fdist1.freq(fdist1.keys()[1])  
        else:
            print '这可能是一个新词，请检查！' 
        return   fdist1.keys()[0]
    def saveHistoryData(self,picpath,standwordpath,startnum,picnum):
        
        standwordlist,inverdict=aa.seeTheRight(standwordpath)
        dataMatrix,wordlist,wordindex0=aa.readPic(picpath,startnum,picnum)
        historydata=[dataMatrix,wordlist,inverdict]     
        return historydata
    
    def updateData(self,historydata,newpicpath,newstandwordpath,newstartnum,newendnum):
        dataMatrix,wordlist,inverdict=historydata
        newstandwordlist,newinverdict=aa.seeTheRight(standwordpath)
        newdataMatrix,newwordlist,newwordindex0=aa.readPic(picpath,newstartnum,newendnum)        
        updateMatrix=np.concatenate((dataMatrix,newdataMatrix))
        updatewordlist=wordlist+newwordlist
        adddict={}
        for i in newinverdict:
            adddict[str(int(i)+len(inverdict))]=newinverdict[i]
        
        dictMerged=dict(inverdict)
        
        updatedict=dictMerged.update(adddict)
        newdata=[updateMatrix,updatewordlist,updatedict]   
        return  newdata
            
        
        
if __name__=='__main__':
    testpicpath='D:/picreg/trainData/newtrainImage/image'  
    picpath='D:/picreg/trainData/image'
    picpath2='D:/picreg/trainData/subImage'
    standwordpath='D:/picreg/trainData/trainImage.txt'
    savepath1='D:/picreg/trainData/dataMatrix.pkl'
    savepath2='D:/picreg/trainData/wordlist.pkl'
#    储存说明：list+图库(1)+匹配程度（180）+平移位数（3）+切割部分（2）.pkl
#    eg:list1-180-3-2.pkl
    savepath3='D:/picreg/trainData/list1-180-2-3.pkl'
    saveStandWordDictPath='D:/picreg/trainData/StandWordDict.pkl'
    saveDistictDictPath='D:/picreg/trainData/DistictDict.pkl'
    aa=compareword()
    ##图库数量
    picnum=1105
    ##图片对比开始位置
    startnum=1
    ##切割列数
    cutpart=4
    ##平移列数
    movestep=2    
    ##标准字表
    standwordlist,inverdict=aa.seeTheRight(standwordpath)

#     for i in standwordlist:
#         print i,'*****'
    newtrainImageDict='D:/picreg/trainData/newtrainImage/trainImage.txt'
    standwordlist2,inverdict2=aa.seeTheRight(newtrainImageDict)
    print inverdict2[str(40)]
########################demo############################################    
    ##读入新图
    dataMatrix,wordlist,wordindex0=aa.readPic(picpath,startnum,picnum)
#     print dataMatrix
    starttime1=time.time()
    flagz=0
    flagx=0
    flagy=0
    for i in range(1100):
#         print i
        if inverdict[str(i)] in standwordlist:
            print '***************************************************'
            flagz+=1
#             print '这是一个新词！'
#             print '这是第%s张图片：'%(i),inverdict[str(i)]
     
#         newimage2=cv2.imread(picpath+"/%s.png"%(376))
            newimage=cv2.imread(picpath+"/%s.png"%(i))    
     
            targetmatrix,targetindex,newvector=aa.getWord(newimage, wordlist, dataMatrix)
            list1=aa.moveToCompare(newvector,movestep)
        #     print targetindex
            result1=aa.compareVector(cutpart,targetmatrix, targetindex, list1,wordindex0)
    #         print result1  
            if result1 !=[]:
                flagy+=1
                predictword=[]
#                 print result1
                for j in result1:
    #                 print '预测可能词：',inverdict[str(i)]
                    predictword.append(inverdict[str(j)])
                fdist1=FreqDist(predictword)
#                 print '可能预测词：',fdist1.keys()[0],'            预测概率为：',fdist1.freq(fdist1.keys()[0])
                if fdist1.keys()[0]==inverdict[str(i)]:
                    flagx+=1
                else: print '识别错误，请检查！！','可能预测词：',fdist1.keys()[0]
                
                if fdist1.freq(fdist1.keys()[0]) !=1:
                    print '可能预测词：',fdist1.keys()[1],'            预测概率为：',fdist1.freq(fdist1.keys()[1])            
    print '图库中已有图数量：',flagz  
    print '可识别图像数量：',flagy
    print '识别正确数量：',flagx
     
    if flagx !=0:
        print '可识别比例为：', float(flagx)/flagz
        print '识别准确率：',float(flagx)/flagy
    endtime1=time.time()
    print '耗时：',endtime1-starttime1
###批量处理
#     starttime=time.time()
#     list2=aa.scalecompare(picpath,startnum, picnum, movestep)
#     endtime=time.time() 
#     costtime=endtime-starttime
#     print list2  
#     print '耗时：',costtime
#     #储存列表
#     aa.storeData(savepath1, dataMatrix)
#     aa.storeData(savepath2, wordlist)
#     aa.storeData(savepath3, list2)
#     aa.storeData(saveStandWordDictPath, inverdict)
#     aa.storeData(saveDistictDictPath, standwordlist)
#     savepath3='D:/picreg/trainData/list1-180-2-3.pkl'
#     saveStandWordDictPath='D:/picreg/trainData/StandWordDict.pkl'
#     saveDistictDictPath='D:/picreg/trainData/DistictDict.pkl'
#     
#     with open(savepath3) as f1:
#         data11=pickle.load(f1)
#     print data11
#     with open(saveStandWordDictPath) as f2:
#         inverdict=pickle.load(f2)   
#     for i in data11:
#         print '******************************'
#         for j in i:
#             print inverdict[str(j)],j
#          
#     ##查看
#     regnum=0
#     for i in data11:
#         regnum+=len(i)
#     print '可识别重复总数：',regnum 
#     print '可识别去重总数：',len(data11)  
#     print '可去除重复数：',regnum-len(data11)
#     print data11
#     for i in data11:
# #         print '******************************'
#         for j in i:
#             print inverdict[str(j)],j,
#         print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@'


        