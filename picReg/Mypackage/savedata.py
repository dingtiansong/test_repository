# -*- coding: utf-8 -*-
'''
@Time : 2017/2/16 14:48

@author: song
'''
import cv2
import numpy as np
import pickle

def convertToBinary(image):
    '''
    1.图片并转为二值化,按列存为向量
    '''
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        gray = image
    else:
        print 'ERROR: the shape is ', image.shape
    x = np.array(gray)
    wordindex = x.sum() / 255
    wordvector = x.reshape((1600, -1), order='F').T
    return wordindex, wordvector
def seeTheRight(path1):
    with open(path1) as f:
        data1=f.readlines()
    datalist=[]
    inverdict={}
    for i in data1:
        xx= i.split('{S}')
        datalist.append(xx)
        inverdict[xx[1].strip()]=xx[0]
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

def readPic(picpath,startnum,picnum):
    '''
    1.历史数据批量存储，建立索引
    '''
#         picId = 0
    img0=cv2.imread(picpath+"/%s.png"%(0))
    wordindex0,dataMatrix=convertToBinary(img0)
    index0=[wordindex0]
#         xxxxx=np.concatenate((dataMatrix,dataMatrix))
#         print 'zzzzzzzzz'
#         print xxxxx[1]
    for i in range(startnum,picnum):
        vpath=picpath+"/%s.png"%(i)
        image = cv2.imread(vpath)
        wordindex,wordvector=convertToBinary(image)
#             print wordindex
        index0.append(wordindex)
#             print index0
        dataMatrix=np.concatenate((dataMatrix,wordvector))
    return dataMatrix,index0,wordindex0


def saveHistoryData(picpath, standwordpath, picnum):
    '''
                存储数据:history[向量矩阵,索引列表,字典]
    '''
    startnum = 1
    standwordlist, inverdict = seeTheRight(standwordpath)
    dataMatrix, wordlist ,wordindex0= readPic(picpath, startnum, picnum)
    historydata = [dataMatrix, wordlist, inverdict]
    return historydata

picpath='C:/Users/John64pc/Desktop/2165/subImage'
standwordpath='C:/Users/John64pc/Desktop/2165/qbTrainImage.txt'
picnum=1265
daya1=saveHistoryData(picpath, standwordpath, picnum)

datapath='D:/historydata216b1600.pkl'
def storeData(datapath, data):
    """将数据到本地"""
    with open(datapath, "wb") as f:
        pickle.dump(data, f)
    f.close()
storeData(datapath,daya1)
# for i in daya1[2]:
#     print i
historypath='D:/picreg/trainData/historydata.pkl'
with open(historypath,'rb') as f :
    data=pickle.load(f)
print data
# for i in data[2]:
#     print i
