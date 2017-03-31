# -*- coding: utf-8 -*-
'''
Created on 2016年12月22日

@author: song

'''
from songtools import songtools
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import cPickle as pickle
from  nltk import FreqDist
from extractionQuoteFromPicture2 import cvPredictiveText
savepath1='D:/picreg/trainData/dataMatrix.pkl'
savepath2='D:/picreg/trainData/wordlist.pkl'
savehistorypath='D:/picreg/trainData/historydata.pkl'
saveStandWordDictPath='D:/picreg/trainData/StandWordDict.pkl'
picpath='D:/picreg/trainData/image'
standwordpath='D:/picreg/trainData/trainImage.txt'
newtrainImageDict='D:/picreg/trainData/newtrainImage/trainImage.txt'
newpicpath='D:/picreg/trainData/newtrainImage/image'
##读入待识别图片

aa=cvPredictiveText()
bb=songtools()
##读入历史数据
sss=aa.saveHistoryData(picpath, standwordpath,1100)
print sss[0]
newsss=aa.updateData(sss, newpicpath, newtrainImageDict, 1,130)
bb.storeData(savehistorypath, newsss)

# print newsss[2]['1101']
# for i in range(1000,1100):
#     print newsss[2][str(i)]
# print sss[2]
# zz,xxx=aa.readPic(picpath, 1, 30)
# print len(xxx)
# print len(newsss[2])
# dataMatrix=aa.readdata(savepath1)
# wordlist=aa.readdata(savepath2)
# inverdict=aa.readdata(saveStandWordDictPath)
##得到识别结果
# newdict={}
# for i in inverdict:
#     ind=int(i)+1000
# #     print int(i)+1000
#     newdict[str(ind)]=inverdict[i]
# print inverdict['0'],newdict[''],len(inverdict)
candidateImage=cv2.imread(picpath+"/%s.png"%(1001))
historydata=bb.readdata(savehistorypath)  
word=aa.predictWord(candidateImage,historydata)
print word     