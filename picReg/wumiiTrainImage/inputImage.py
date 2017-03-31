#-*- coding:utf-8 -*-
'''

Created on 2016年12月12日

@author: Wenpu Wang

'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy
import os
import pickle
from PIL import Image
from pyocr import pyocr
import pyocr.builders

#1、读取图片
img = cv2.imread("E:/NLP/wumii/10.jpeg")
print img.shape
#转灰度图像 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
grayRowVar = np.var(gray,axis=1) 
#print [list(x) for x in gray]
#求行差
grayDiffRow = cv2.absdiff(gray[:-1,:],gray[1:,:])
grayDiffRow1 = copy.deepcopy(grayDiffRow)
# plt.imshow(grayDiffRow, cmap = plt.cm.gray)
# plt.show()
grayDiffRowSum = np.sum(grayDiffRow,axis=1)
grayDiffRowAvg = np.average(grayDiffRow,axis=1)
grayDiffRowVar = np.var(grayDiffRow,axis=1)
grayDiffRowDiff = cv2.absdiff(grayDiffRow[:,:-1],grayDiffRow[:,1:])
grayDiffRowDiffSum = np.sum(grayDiffRowDiff,axis=1)
colorLine = []
for i in range(len(grayDiffRowSum)):
    #如果grayDiffRowVar < 5，则说明两边颜色按行相等
    #如果grayDiffRowAvg > 10 说明两边颜色按列不相等，或有文字干扰
    #二者同时成立，说明是颜色变化区间的边界
    if grayDiffRowAvg[i] > 10 and grayDiffRowVar[i] < 5:
        colorLine.append(i+1)

print colorLine

#for y in colorLine:
#    cv2.line(img,(-1000,y),(1000,y),(255,0,0),2)

plt.imshow(img)
plt.show()

def getSubList(gray,colorLine):
    grayList = []
    #不同颜色区块划分图片
    if len(colorLine) > 0:
        grayList = [gray[:colorLine[0],]]
        if len(colorLine) > 1:
            for i in range(1,len(colorLine)):
                grayList.append(gray[colorLine[i-1]:colorLine[i],])
        grayList.append(gray[colorLine[-1]:len(gray),])
    else:
        grayList = [gray]
    return grayList

grayList = getSubList(img,colorLine)
#删除太细的区域
grayList0 = []
tUID = 0
for tmp in grayList:
    #删除线
    if len(tmp.shape) > 1:
        if tmp.shape[0] > 1 and tmp.shape[1] > 1:
            #tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY) 
            cv2.imwrite('%s.png'%tUID,tmp, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            
            print tmp.shape
            grayList0.append(tmp)
            #plt.imshow(tmp)
            #plt.show()
            tUID += 1

def getBlackBackground(tgray,taxis=1):
    #颜色反转分析
    #求每行的灰度值合集
    xCumAvg = np.round(np.average(tgray, axis=taxis))
    #求差分
    tList = [xCumAvg[i] for i in range(1,len(xCumAvg)) if xCumAvg[i] == xCumAvg[i-1]]
    #统计最高频的灰度值
    tDict = {}
    for x in tList:
        tDict[x] = tDict.get(x,0)+1
    
    tList = sorted(tDict.items(), key=lambda d:(d[1]), reverse = True)  
    if tList[0][0] > 200:
        #颜色反转：
        tgray = 255 - tgray
    return tgray

def getReflexGray(gray):
    #统计行像素均值
    rowAvg = np.average(gray, axis = 1)
    #均值取整
    rowAvgInt = np.round(rowAvg)
    
    #计算列相邻相等的颜色的次数，并统计，
    tDict = {}
    
    for i in range(1,len(rowAvgInt)):
        if rowAvgInt[i-1] == rowAvgInt[i]:
            tDict[rowAvgInt[i]] = tDict.get(rowAvgInt[i],0) + 1
    
    tList = sorted(tDict.items(), key=lambda d:(d[1]), reverse = True)  
    #统计次数最高的颜色就是背景色
    backgroundColor = tList[0][0]
    tSet = set()
    for i in range(len(rowAvgInt)):
        if rowAvgInt[i] == backgroundColor:
            tSet = tSet | set(gray[i,])
    print backgroundColor
    print tSet
    #将背景色置0，将负值取反
    return np.absolute(gray.astype(np.float32) - backgroundColor).astype(np.uint8)
    



def getTextRow(timg,lineHeight = 5):
    wordImgList = []
    #timg = grayList[2]
    if len(timg.shape) > 2:
        tgray = cv2.cvtColor(timg,cv2.COLOR_BGR2GRAY)
    else:
        tgray = timg
    #颜色折叠
    tgray = getReflexGray(tgray)
    plt.imshow(tgray,cmap='gray')
    plt.show()
    print '----'
    print np.max(tgray,axis=1)
    #二值化
    ret,binary = cv2.threshold(tgray,50,255,cv2.THRESH_BINARY)
    
    print ret
    ##颜色反转，若底色是白色则反转为黑色，否则不变
    #binary = getBlackBackground(binary)
    #切割文本行
    xCumSum = np.sum(binary, axis=1)
    #选出文本行
    inWordList = [i for i in range(len(xCumSum)) if xCumSum[i] > 0]
    #根据连续间距来判断文本行的位置,若间距超过距离lineHeight=5,则认为不在一行
    inWordDiff = np.diff(inWordList)
    if len(inWordList) > 2:
        tmp = (inWordList[0],inWordList[0])
        for i in range(1,len(inWordList)):
            if inWordList[i] - tmp[1] > lineHeight:
                #print tmp
                wordImgList.append(binary[tmp[0]:tmp[1],])
                tmp = (inWordList[i],inWordList[i])
            else:
                tmp = (tmp[0],inWordList[i])
        print tmp
        wordImgList.append(binary[tmp[0]:tmp[1],])
    print len(wordImgList)
    # 1. Sobel算子，x方向求梯度
    #sobel = cv2.Sobel(tgray, cv2.CV_16S, 1, 0, ksize = 3)
    #sobel = cv2.convertScaleAbs(sobel)   # 转回uint8  
    
    
    #按列直方图来划分数据
    xCumSum = np.average(binary, axis=1)
    #plt.subplot(211)
    #plt.imshow(binary,cmap='gray')
    #plt.subplot(212)
    #plt.plot(xCumSum)
    #plt.show()
    return wordImgList


def getSubImage(img2,minLength0 = 1):
    a=np.sum(img2, axis=0)
    #print img2
    #print a
    xList = [i for i in range(len(a)) if a[i] > 0]
    if len(xList) > 3:
        diffList = np.diff(xList)
        dList = [i for i in range(len(diffList)) if diffList[i] > minLength0]
        if len(dList) > 0:
            img3 = [img2[:,xList[0]:xList[dList[0]]+1]]
            i = 0
            if len(dList) > 1:
                for i in range(1,len(dList)):
                    img3.append(img2[:,xList[dList[i-1]+1]:xList[dList[i]]+1])
            img3.append(img2[:,xList[dList[i]+1]:xList[-1]+1])
            return img3
        else:
            return [img2[:,xList[0]:xList[-1]+1]]
    else:
        return [img2]

    
    
    
k = 0
for timg in grayList0:
    wordImgList = getTextRow(timg)
    for i in range(len(wordImgList)):
        num = len(wordImgList)*100+11+i
        ttt = getSubImage(wordImgList[i],minLength0 = 1)
        for kkk in ttt:
            print kkk.shape
            cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            k = k + 1
            #plt.imshow(kkk)
            #plt.show()
        #plt.subplot(num)
        #plt.imshow(wordImgList[i])
        
    
    #plt.show()
    
# 
# plt.imshow(gray,cmap='gray')
# plt.show()
# print np.sum(cv2.absdiff(grayDiffRow1,grayDiffRow))
#         
# 
# 
# 
# edges = cv2.Canny(gray,10,100, apertureSize = 3)
# # 1. Sobel算子，x方向求梯度
# sobel = cv2.Sobel(gray, cv2.CV_16S, 1, 1, ksize = 1)
# sobel = cv2.convertScaleAbs(sobel)   # 转回uint8  
# #转二值图
# ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
# plt.imshow(gray)
# plt.show()


# imgOcr = Image.fromarray(cv2.cvtColor(wordImgList[i],cv2.COLOR_BGR2GRAY))
# tools = pyocr.get_available_tools()[:]
# bu = pyocr.builders.TextBuilder(tesseract_layout=7)
# s = tools[0].image_to_string(imgOcr,lang='chi_sim',builder=bu)
# print s

