# -*- coding: utf-8 -*-
'''
Created on 2016年12月20日

@author: song

'''
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import cPickle as pickle
from compareWord import compareword
savepath3='D:/picreg/trainData/list1-180-2-3.pkl'
saveStandWordDictPath='D:/picreg/trainData/StandWordDict.pkl'
saveDistictDictPath='D:/picreg/trainData/DistictDict.pkl'

with open(saveDistictDictPath) as f3:
    data13=pickle.load(f3)
with open(savepath3) as f1:
    data11=pickle.load(f1)
 
with open(saveStandWordDictPath) as f2:
    inverdict=pickle.load(f2)   
# for i in data11:
#     print '******************************'
#     for j in i:
#         print inverdict[str(j)],j

print len(inverdict)       
print data11
