#-*- coding:utf-8 -*-
'''
Created on 2016年12月8日

@author: Administrator
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy
import os
import pickle
from _codecs import encode
#图片处理：
# #1、读取图片
# img = cv2.imread('E:/NLP/QDFile/pd5.png')
# #转灰度图像 
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#2、切割最小图片
def getMinPic(img,minValue = 0):
    (m,n) = img.shape
    yUp = m
    yDown = -1
    xLeft = n
    xRight = -1
    for y in range(m):
        for x in range(n):
            if img[y][x] > minValue:
                yUp = min(yUp,y)
                yDown = max(yDown,y)
                xLeft = min(xLeft,x)
                xRight = max(xRight,x)
    if yDown >= 0:
        return img[yUp:yDown+1,xLeft:xRight+1]
    else:
        return np.array([])




def getNormalizePic(gray):
    m,n=gray.shape
    if m > 50:
        print "error:m = %s"%(m)
        return np.array([])
    else:
        mLength = 50
        gray1 = np.row_stack((gray,np.array([0]*n*(mLength-m)).reshape(mLength-m, n)))
        m = mLength
        
        nLength = 100
        gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        n = nLength
               
#         if n <= 15:
#             nLength = 20
#             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#             n = nLength
#         elif n <= 30:
#             nLength = 30
#             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#             n = nLength
#         elif n <= 45:
#             nLength = 45
#             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#             n = nLength
#         elif n <= 60:
#             nLength = 60
#             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#             n = nLength
#         else:
#             nLength = 200
#             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#             n = nLength
    return gray1


#图片处理：
def getReadImg(pathList):
    cells = []
    for i in pathList:
        #1、读取图片
        img = cv2.imread(i)
        #转灰度图像 
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #转二值图
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        #2、切割最小图片
        imgMin = getMinPic(binary)
        #3、将图片补零，判断长度在区间(0,15]扩充至20，区间(15,30]扩充至40，
        #区间(30,45]扩充至60，区间(45,60]扩充至80，区间(60+)扩充至200
        gray1 = getNormalizePic(imgMin)
        gray1 = gray1.reshape(1,-1)
        cells.append(list(gray1))
    
    return cells


#历史图片数据读取
dataPath = 'E:/NLP/wumii/TrainFile/trainData/wumiiData.pkl'
pkl_file = open(dataPath, 'rb')
allData = pickle.load(pkl_file)
pkl_file.close()
cells = list(allData['data'])
print len(cells[0])
print type(cells[0])
cellSet0 = set([tuple(list(tmp)) for tmp in cells])

#新图片数据读取
filePath='E:/NLP/wumii/TrainFile/nonrecognitionImage'
fileList = os.listdir(filePath)
pathList = [filePath+'/'+x for x in fileList]
cells1 = getReadImg(pathList)
cellSet1 = set([tuple(tmp[0]) for tmp in cells1])
print type(cells1)
print type(cells1[0])
print type(cells1[0][0])
#去重校验
cellSet = cellSet1 - cellSet0
#更新图片数据，并输出，进行人工识图
filePath='E:/NLP/wumii/TrainFile/newTrain/newImage'
picId = 0
for tmp in cells1:
    if tuple(tmp[0]) in cellSet:
        cellSet = cellSet - set([tuple(tmp[0])])
        tImg = tmp[0].reshape(50,100)
        cv2.imwrite(filePath+"/%s.png"%(picId), tImg, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        picId += 1

print 'run is end!'
