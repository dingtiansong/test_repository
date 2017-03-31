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
# 
# #图片处理：
# # #1、读取图片
# # img = cv2.imread('E:/NLP/QDFile/pd5.png')
# # #转灰度图像 
# # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# #2、切割最小图片
# def getMinPic(img,minValue = 0):
#     (m,n) = img.shape
#     yUp = m
#     yDown = -1
#     xLeft = n
#     xRight = -1
#     for y in range(m):
#         for x in range(n):
#             if img[y][x] > minValue:
#                 yUp = min(yUp,y)
#                 yDown = max(yDown,y)
#                 xLeft = min(xLeft,x)
#                 xRight = max(xRight,x)
#     if yDown >= 0:
#         return img[yUp:yDown+1,xLeft:xRight+1]
#     else:
#         return np.array([])
# 
# 
# 
# 
# def getNormalizePic(gray):
#     m,n=gray.shape
#     if m > 20:
#         print "error:m = %s"%(m)
#         return np.array([])
#     else:
#         mLength = 20
#         gray1 = np.row_stack((gray,np.array([0]*n*(mLength-m)).reshape(mLength-m, n)))
#         m = mLength
#         
#         nLength = 80
#         gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#         n = nLength
#                
# #         if n <= 15:
# #             nLength = 20
# #             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
# #             n = nLength
# #         elif n <= 30:
# #             nLength = 30
# #             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
# #             n = nLength
# #         elif n <= 45:
# #             nLength = 45
# #             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
# #             n = nLength
# #         elif n <= 60:
# #             nLength = 60
# #             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
# #             n = nLength
# #         else:
# #             nLength = 200
# #             gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
# #             n = nLength
#     return gray1
# 
# 
# #图片处理：
# def getReadImg(pathList):
#     cells = []
#     for i in pathList:
#         #1、读取图片
#         img = cv2.imread(i)
#         #转灰度图像 
#         gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#         #2、切割最小图片
#         imgMin = getMinPic(gray)
#         #3、将图片补零，判断长度在区间(0,15]扩充至20，区间(15,30]扩充至40，
#         #区间(30,45]扩充至60，区间(45,60]扩充至80，区间(60+)扩充至200
#         gray1 = getNormalizePic(imgMin)
#         gray1 = gray1.reshape(1,-1)
#         cells.append(list(gray1))
#     
#     return cells
# 
# 
# 
# 
# filePath='E:/NLP/QDFile/subImagepd15/trainData0'
# imagePath = filePath+'/image'
# labelPath = filePath+'/trainImage.txt'
# dataPath = filePath+'/imageData.pkl'# fileList = os.listdir(imagePath)
# fileIdList = [int(x.split('.')[0]) for x in fileList]
# pathList = [imagePath + '/' + x for x in fileList]
# cells = getReadImg(pathList)
# x = np.array(cells)
# train = x.reshape(-1,1600).astype(np.float32)
# train_labelsid = fileIdList
# 
# # #存储训练image&label
# # allData = {'data':train,'label':train_labels}
# # dataPath = 'E:/NLP/QDFile/imageData.pkl'
# # pkl_file = open(dataPath, 'wb')
# # pickle.dump(allData, pkl_file)
# # pkl_file.close()
# 
#  
# f = open(labelPath,'rb')
# lines = f.readlines()#读取全部内容 
# #fp.read().decode("utf-8-sig")
# f.close()
# fDict = {}
# for tmp in lines:
#     fValue,fId = tmp.split('{S}')
#     fDict[int(fId)] = fValue.lstrip("\xef\xbb\xbf").strip()
# print fDict
# 
# train_labels = [fDict[x] for x in train_labelsid]
# allData = {'data':train,'label':train_labels}
# 
# pkl_file = open(dataPath, 'wb')
# pickle.dump(allData, pkl_file)
# pkl_file.close()

labelPath = 'E:/NLP/wumii/wumiiTrainContainsTrainData/subImageLabel.txt'
f = open(labelPath,'rb')
lines = f.readlines()#读取全部内容 
f.close()
fDict = {}
fList = []
for tmp in lines:
    fId,fValue = tmp.split('{S}')
    fValue = fValue.lstrip("\xef\xbb\xbf").strip()
    if fValue != '':
        fList.append(fValue.lstrip("\xef\xbb\xbf").strip())
    #fDict[fId] = fValue.lstrip("\xef\xbb\xbf").strip()

print len(fList)



pkl_file = open('imageData.pkl', 'rb')
modelData = pickle.load(pkl_file)
pkl_file.close()

train = modelData['data'].astype(np.uint8)
train_labels = fList

tList = list(train)
tDict = {}
for i in range(len(tList)):
    tTup = tuple(tList[i])
    tDict[tTup] = tDict.get(tTup,[])+[i]

print len(tDict)
print type(tList[i])
print tList[i].dtype

cells = []
train_labels0 = []
for tkey,tvalue in tDict.items():
    cells.append(np.array(tkey))
    train_labels0.append(train_labels[tvalue[0]])
    
    if len(tvalue) > 1:
        tmp = [train_labels[i] for i in tvalue]
        if len(set(tmp)) > 1:
            print tmp
            for kk in tmp:
                print kk
            print tvalue

train0 = np.array(cells)
print train0.dtype
print len(train0)
print len(train_labels0)

allData = {'data':train0,'label':train_labels0}
pkl_file = open('wumiiData.pkl', 'wb')
pickle.dump(allData, pkl_file)
pkl_file.close()

            #for i in tvalue:
            #    img = tList[i].reshape(50,100)
             #   plt.imshow(img)
             #   plt.show()



