#-*- coding:utf-8 -*-
'''

Created on 2016年12月15日

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

def getChangeLine(gray, minAvg = 10, maxVar = 5):
    grayDiffRow = cv2.absdiff(gray[:-1,:],gray[1:,:])
    #grayDiffRowSum = np.sum(grayDiffRow,axis=1)
    grayDiffRowAvg = np.average(grayDiffRow,axis=1)
    grayDiffRowVar = np.var(grayDiffRow,axis=1)
    colorLine = []
    for i in range(len(grayDiffRowAvg)):
        #如果grayDiffRowVar < 5，则说明两边颜色按行相等
        #如果grayDiffRowAvg > 10 说明两边颜色按列不相等，或有文字干扰
        #二者同时成立，说明是颜色变化区间的边界
        if grayDiffRowAvg[i] > minAvg and grayDiffRowVar[i] < maxVar:
            colorLine.append(i+1)
    
    return colorLine

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

def getRealSubImage(grayList, minRow = 150, minCol = 1):
    grayList0 = []
    tUID = 0
    for tmp in grayList:
        #删除线
        if len(tmp.shape) > 1:
            if tmp.shape[0] > minRow and tmp.shape[1] > minCol:
                #tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY) 
                cv2.imwrite('%s.png'%tUID,tmp, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                
                print tmp.shape
                grayList0.append(tmp)
                #plt.imshow(tmp)
                #plt.show()
                tUID += 1
    
    return grayList0

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
    #将背景色置0，
    gray0 = gray.astype(np.float32) - backgroundColor
    #将负值取反
    gray0 = np.absolute(gray0)
    #返回uint8类似的数据
    return gray0.astype(np.uint8)
    
def getTextRow(timg,lineHeight = 5):
    wordImgList = []
    binary = timg
    #timg = grayList[2]
    ##转灰度图
    #tgray = cv2.cvtColor(timg,cv2.COLOR_BGR2GRAY)
    ##颜色折叠
    #tgray = getReflexGray(tgray)
    ##二值化
    #ret,binary = cv2.threshold(tgray,50,255,cv2.THRESH_BINARY)
    ##颜色反转，若底色是白色则反转为黑色，否则不变
    #binary = getBlackBackground(binary)
    
    #切割文本行
    xCumSum = np.sum(binary, axis=1)
    #选出文本行
    inWordList = [i for i in range(len(xCumSum)) if xCumSum[i] > 0]
    #根据连续间距来判断文本行的位置,若间距超过距离lineHeight=5,则认为不在一行
    if len(inWordList) > 2:
        tmp = (inWordList[0],inWordList[0])
        for i in range(1,len(inWordList)):
            if inWordList[i] - tmp[1] > lineHeight:
                #print tmp
                wordImgList.append(binary[tmp[0]:tmp[1],])
                tmp = (inWordList[i],inWordList[i])
            else:
                tmp = (tmp[0],inWordList[i])
        wordImgList.append(binary[tmp[0]:tmp[1],])
    return wordImgList
    
def getT1TextRow(binaryList, firstHight = range(25,31), generalHight = range(33,46), lastHitht = range(28,37)):
    #输入：binaryList为链表，每个元素为二值化图
    #输出：链表，每个元素为二值化图
    #说明：1型文本框格式：
    #第1行为起始用户文本行,只包含用户和发在什么地方的文本，其行高为firstHight
    #第2行为到第n-1行是正常文本,其行高为generalHight
    #第n行是最后一行，只包含评论数和点赞数，其行高为lastHitht
    binaryList0 = []
    if len(binaryList) >= 3:
        m,n = binaryList[0].shape
        if m in firstHight:
            m,n = binaryList[-1].shape
            if m in lastHitht:
                binaryList0.append(binaryList[0])
                for i in range(1,len(binaryList)-1):
                    m,n = binaryList[i].shape
                    if m in generalHight:
                        binaryList0.append(binaryList[i])
                
                binaryList0.append(binaryList[-1])
                
                if len(binaryList0) >= 3:
                    return binaryList0
                else:
                    return []
            else:
                return []
        else:
            return []
    else:
        return []


def getWordList(binary, minLength0 = 1):
    a=np.sum(binary, axis=0)
    #print img2
    #print a
    xList = [i for i in range(len(a)) if a[i] > 0]
    if len(xList) > 3:
        diffList = np.diff(xList)
        dList = [i for i in range(len(diffList)) if diffList[i] > minLength0]
        if len(dList) > 0:
            img3 = [binary[:,xList[0]:xList[dList[0]]+1]]
            i = 0
            if len(dList) > 1:
                for i in range(1,len(dList)):
                    img3.append(binary[:,xList[dList[i-1]+1]:xList[dList[i]]+1])
            img3.append(binary[:,xList[dList[i]+1]:xList[-1]+1])
            return img3
        else:
            return [binary[:,xList[0]:xList[-1]+1]]
    else:
        return [binary]

def getT1NameList(binary, minLength0 = 1):
    a=np.sum(binary, axis=0)
    rtList = []
    #print img2
    #print a
    xList = [i for i in range(len(a)) if a[i] > 0]
    if len(xList) > 3:
        maxLen = 0
        n2 = 0
        for i in range(1,len(xList)):
            #最大的不连续点
            if xList[i] - xList[i-1] > maxLen:
                n2 = i
                maxLen = xList[i] - xList[i-1]
        #文本分块
        twoList = getTextRow(binary[:,:xList[n2-1]+1], lineHeight = 5)
        oneList = getTextRow(binary[:,xList[n2]:], lineHeight = 5)
        if len(twoList) == 1 and len(oneList) == 1:
            rtList.append(getWordList(twoList[0], minLength0))
            rtList.append(getWordList(oneList[0], minLength0))
    return rtList

def getT2NameList(binary, minLength0 = 1):
    #由于有用户头像因此文本行比较高
    #先截图头像，再分两行，两列
    #图片按列统计灰度，最大间距的右侧行高为1行，约为firstHight = range(25,31)
    #最大间距的左侧为一个logo图像和两行，每行行高firstHight = range(25,31)
    a=np.sum(binary, axis=0)
    rtList = []
    #print img2
    #print a
    xList = [i for i in range(len(a)) if a[i] > 0]
    if len(xList) > 3:
        maxLen = 0
        n1 = 0
        n2 = 0
        for i in range(1,len(xList)):
            #第一个不连续点
            if xList[i] - xList[i-1] > 1 and n1 == 0:
                n1 = i
            #最大的不连续点
            if xList[i] - xList[i-1] > maxLen:
                n2 = i
                maxLen = xList[i] - xList[i-1]
        #文本分块
        logoBinary = binary[:,:xList[n1-1]+1]
        twoBinary = binary[:,xList[n1]:xList[n2-1]+1]
        twoList = getTextRow(twoBinary, lineHeight = 5)
        oneBinary = binary[:,xList[n2]:]
        oneList = getTextRow(oneBinary, lineHeight = 5)
        if len(twoList) == 2 and len(oneList) == 1:
            rtList.append(getWordList(twoList[0], minLength0))
            rtList.append(getWordList(twoList[1], minLength0))
            rtList.append(getWordList(oneList[0], minLength0))
    return rtList


def getCommentList(binary, minLength0 = 1):
    return getWordList(binary, minLength0)
    
def getT2TextRow(binaryList, firstHight = range(75,86), generalHight = range(33,46), lastHitht = range(28,37)):
    #输入：binaryList为链表，每个元素为二值化图
    #输出：链表，每个元素为二值化图
    #说明：2型文本框格式：
    #第1行为起始用户文本行,包含用户头像和发在什么地方的文本，其行高为firstHight
    #第2行为到第n-1行是正常文本,其行高为generalHight
    #第n行是最后一行，只包含评论数和点赞数，其行高为lastHitht
    binaryList0 = []
    if len(binaryList) >= 3:
        m,n = binaryList[0].shape
        if m in firstHight:
            m,n = binaryList[-1].shape
            if m in lastHitht:
                binaryList0.append(binaryList[0])
                for i in range(1,len(binaryList)-1):
                    m,n = binaryList[i].shape
                    if m in generalHight:
                        binaryList0.append(binaryList[i])
                
                binaryList0.append(binaryList[-1])
                if len(binaryList0) >= 3:
                    return binaryList0
                else:
                    return []
            else:
                return []
        else:
            return []
    else:
        return []

def getTagList(binary):
    #通过观察可知，圆弧的灰度值在x轴上基本保持不变，但若内部出现文字，则灰度会明显上升，以此原理处理圆弧
    #求列灰度值
    b=np.sum(binary, axis=1)
    len_b = len(b)
    print b
    plt.imshow(binary)
    plt.show()
    #删除上边线和对应的下边线
    startId,endId = 0, 0
    s,t = 0, 0
    for i in range(2,len(b)/2):
        if s == 0:
            if b[i + 1] > b[i] >= b[i - 1]:
                startId = i - 1
                s = 1
                if t > 0:
                    break
        if t == 0:
            print len_b,i
            if b[len_b - i + 1] <= b[len_b - i] < b[len_b - i - 1]:
                endId = i - 1
                t = 1
                if s > 0:
                    break
    if s > 0 or t > 0:
        maxId = max(startId,endId)
        binary1 = binary[maxId:len_b-maxId+1,:]
        
        plt.imshow(binary1,cmap='gray')
        plt.show()
        binary1List = getWordList(binary1, minLength0 = 10)
        for tmp1 in binary1List:
            plt.imshow(tmp1,cmap='gray')
            plt.show()
        binary2List = [binary1List[i] for i in range(1,len(binary1List),3)]
        print len(binary2List)
        binaryList = []
        for binary0 in binary2List:
            binaryList = binaryList + getWordList(binary0, minLength0 = 1)
        return binaryList
    else:
        return []
        
        
    
    
    


def getT3TextRow(binaryList, firstHight = range(20,27), tagHight = range(53,73)):
    #输入：binaryList为链表，每个元素为二值化图
    #输出：链表，每个元素为二值化图
    #说明：3型文本框格式为标签块格式：
    #第1行为标签块起始说明行的高度，其行高为firstHight
    #第2行为到第n行是标签行,其行高为labelHight
    binaryList0 = []
    if len(binaryList) >= 2:
        m,n = binaryList[0].shape
        if m in firstHight:
            binaryList0.append(binaryList[0])
            for i in range(1,len(binaryList)):
                m,n = binaryList[i].shape
                if m in tagHight:
                    binaryList0.append(binaryList[i])
                if len(binaryList0) >= 2:
                    return binaryList0
                else:
                    return []
            else:
                return []
        else:
            return []
    else:
        return []

if __name__=='__main__':
    k = 0
    ImgList = ["E:/NLP/wumii/"+str(x)+".jpeg" for x in range(1,16)]
    for ImgPath in ImgList:
        # 0、加载图片
        #img = cv2.imread("E:/NLP/wumii/13.jpeg")
        img = cv2.imread(ImgPath)
        # 1、图片转灰度图：
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
        # 2、先按行求颜色突变行
        colorLine = getChangeLine(gray, minAvg = 10, maxVar = 5)
        # 3、根据突变行划分出同色的图片块
        grayList = getSubList(gray,colorLine)
        # 4、过滤图片块：块高度大于150的才考虑
        grayList = getRealSubImage(grayList, minRow = 150, minCol = 1)
        # 5、对每个图片块的底色处理，计算相邻行均值相等的灰度的最大频数为底色灰度值，计算每个像素的灰度值=abs(x-底色灰度值)
        grayList0 = []
        for tmp in grayList:
            grayList0.append(getReflexGray(tmp))
        
        # 6、图片块二值化：>50灰度的归为255，否则为0
        binaryList = []
        for tmp in grayList0:
            ret,binary = cv2.threshold(tmp,25,255,cv2.THRESH_BINARY)
            binaryList.append(binary)
            #plt.subplot(211)
            #plt.imshow(tmp,cmap='gray')
            #plt.subplot(212)
            #plt.imshow(binary,cmap='gray')
            #plt.show()
        
        print '-------'+ImgPath
        
        # 7、二值图搜索文本行，输出所有可能的文本行
        for tmp in binaryList:
            tmpList = getTextRow(tmp, lineHeight = 5)
            #过滤符合1型模板的文本组合
            wordList = getT1TextRow(tmpList)
            
            if wordList:
                print 'T1'
                wtList = getT1NameList(wordList[0], minLength0 = 1)
                for kkk1 in wtList:
                    for kkk in kkk1:
                        k = k + 1
                        cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                for i in range(1,len(wordList)-1):
                    wtList = getWordList(wordList[i], minLength0 = 1)
                    for kkk in wtList:
                        k = k + 1
                        cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                wtList = getCommentList(wordList[-1], minLength0 = 1)
                for kkk in wtList:
                    k = k + 1
                    cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            else:
                
                wordList = getT2TextRow(tmpList)
                 
                if wordList:
                    print 'T2'
                    wtList = getT2NameList(wordList[0], minLength0 = 1)
                    for kkk1 in wtList:
                        for kkk in kkk1:
                            k = k + 1
                            cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    for i in range(1,len(wordList)-1):
                        wtList = getWordList(wordList[i], minLength0 = 1)
                        for kkk in wtList:
                            k = k + 1
                            cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    wtList = getCommentList(wordList[-1], minLength0 = 1)
                    for kkk in wtList:
                        k = k + 1
                        cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                
                else:
                    wordList = getT3TextRow(tmpList)
                    if wordList:
                        print 'T3'
                        wtList = getWordList(wordList[0], minLength0 = 1)
                        for kkk in wtList:
                            k = k + 1
                            cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                        
                        wtList = getTagList(wordList[1])
                        for kkk in wtList:
                            k = k + 1
                            cv2.imwrite("E:/NLP/wumii/subImage/QQ_%s.png"%k, kkk, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            
    # 8、根据文本行的类别，进行字符截取
    


