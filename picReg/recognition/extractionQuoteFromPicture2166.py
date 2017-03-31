#-*- coding:utf-8 -*-
'''
Created on 2016年12月6日

@author: Administrator
'''
import cv2 
#import time
import numpy as np
#import matplotlib.pyplot as plt
import copy
import pickle
import uuid
import sys
import time
# import cPickle as pickle
from collections import Counter

class cutTablePicture(object):
    
    #抽取横线和竖线
    def getTableLines(self, edges, lines1, minLength = 50):
        xList = []
        yList = []
        for rho,theta in lines1[:]: 
            a = np.cos(theta)
            b = np.sin(theta)
            if abs(a*b) < 0.00001:
                if a > 0.5:
                    #竖线
                    xList.append(int(rho))
                elif b > 0.5:
                    #横线
                    yList.append(int(rho))
        
        #判断#竖线是不是连续的线
        xListNew = []
        for x in xList:
            tlist = [y[x] for y in edges]
            count = 0
            for i in tlist:
                if i == 255:
                    count += 1
                else:
                    count = 0
                if count > minLength:#连续像素超过20
                    xListNew.append(x)
                    break
        #判断横线是不是连续的线
        yListNew = []
        for y in yList:
            tlist = [x for x in edges[y]]
            count = 0
            for i in tlist:
                if i == 255:
                    count += 1
                else:
                    count = 0
                if count > minLength:#连续像素超过50
                    yListNew.append(y)
                    break
        
        xListNew.sort()
        yListNew.sort()
        return [xListNew,yListNew]
    
    def getQuoteTable(self, xList, yList, minLength = 10):
        #对竖线的处理，取间距最长的两条线：
        diffList = list(np.diff(xList))
        tIndex = diffList.index(max(diffList))
        xListNew = [xList[tIndex],xList[tIndex+1]]
        #对横线的处理，选取等间距数量最多的线列。要求线列的间距大于minLength
        diffList = np.diff(yList)
        #等间距的二次差值=0
        diffList2 = np.diff(diffList)
        tIndexList = []
        tTmp = []
        for i in range(len(diffList2)):
            if diffList2[i] == 0:
                if diffList[i] > minLength:
                    if len(tTmp) == 0:
                        tTmp = [yList[i], i]
            else:
                if len(tTmp) == 2:
                    tIndexList.append((tTmp[0], tTmp[1], i + 2, i + 2 - tTmp[1]))
                    tTmp = []  
        yIndex = sorted(tIndexList, key=lambda d:(d[3],d[0]), reverse = True)[0]  
        yListNew = yList[yIndex[1]:yIndex[2]]
        
        return [xListNew, yListNew]
    
    def getMatrixList(self, xListNew,yListNew,minArea = 100):
        #构造矩形框并计算矩形框面积
        xyMatrixList = []
        for ny in range(len(yListNew)-1):
            y1 = yListNew[ny]
            y2 = yListNew[ny+1]
            tmpList = []
            for nx in range(len(xListNew)-1):
                x1 = xListNew[nx]
                x2 = xListNew[nx+1]
                tmpList.append((x1,y1,x2,y2,abs(x2-x1-1)*abs(y2-y1-1)))
            xyMatrixList.append(tmpList)
        
        #按面积筛选矩形框，逐一删除最小面积的矩形所在的行列，直到所有矩形面积符合要求。，
        xyMatrixListNew = copy.deepcopy(xyMatrixList)
        #yIndex = sorted(tIndexList, key=lambda d:(d[3],d[0]), reverse = True)[0]
        while(len(xyMatrixListNew) > 0):
            tmpArea = minArea
            for i in range(len(xyMatrixListNew)):
                for j in range(len(xyMatrixListNew[i])):
                    if xyMatrixListNew[i][j] < tmpArea:
                        tmpArea = xyMatrixListNew[i][j]
                        minNy = i
                        minNx = j
            
            if tmpArea < minArea:
                del xyMatrixListNew[minNy]
                for i in range(len(xyMatrixListNew)):
                    del xyMatrixListNew[i][minNx]
            else:
                return xyMatrixListNew
    
    
    #切割白盒列表：
    def getWhiteBox(self, edges, xyMatrix):
        (x1,y1,x2,y2) = xyMatrix
        xyArea = (x2 - x1) * (y2 - y1)
        while(x2 - x1 > 1 and y2 - y1 > 1):
            y1List = [x for x in edges[y1][x1:x2]]
            if max(y1List) > 0:
                #包含非零元素，判断非零元素是否是线：
                for i in range(len(y1List)):
                    if y1List[i] > 0:
                        xList = [edges[y][x1+i] for y in range(y1,y2)]
                        if len([x for x in xList if x > 0]) > 0.8*len(xList):
                            #判断是线,则分割数据。
                            if i == 0:
                                xyList = self.getWhiteBox(edges, (x1+1,y1,x2,y2))
                            elif x1 + i == x2:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2 - 1,y2))
                            else:
                                xyList = self.getWhiteBox(edges, (x1,y1,x1 + i - 1,y2))
                                xyList = xyList + self.getWhiteBox(edges, (x1 + i + 1,y1,x2,y2))
                            return xyList
                #判断不是线，则y1向下平移：
                y1 = y1 + 1
            
            x2List = [edges[y][x2] for y in range(y1,y2)]
            if max(x2List) > 0:
                #包含非零元素，判断非零元素是否是线：
                for i in range(len(x2List)):
                    if x2List[i] > 0:
                        yList = [x for x in edges[y1+i][x1:x2]]
                        if len([x for x in yList if x > 0]) > 0.8*len(yList):
                            #判断是线,则分割数据。
                            if i == 0:
                                xyList = self.getWhiteBox(edges, (x1,y1+1,x2,y2))
                            elif y1 + i == y2:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2,y2-1))
                            else:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2,y1 + i - 1))
                                xyList = xyList + self.getWhiteBox(edges, (x1,y1 + i + 1,x2,y2))
                            return xyList
                #判断不是线，则x2向左平移：
                x2 = x2 - 1
            
            y2List = [x for x in edges[y2][x1:x2]]
            if max(y2List) > 0:
                #包含非零元素，判断非零元素是否是线：
                for i in range(len(y2List)):
                    if y2List[i] > 0:
                        xList = [edges[y][x1+i] for y in range(y1,y2)]
                        if len([x for x in xList if x > 0]) > 0.8*len(xList):
                            #判断是线,则分割数据。
                            if i == 0:
                                xyList = self.getWhiteBox(edges, (x1+1,y1,x2,y2))
                            elif x1 + i == x2:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2 - 1,y2))
                            else:
                                xyList = self.getWhiteBox(edges, (x1,y1,x1 + i - 1,y2))
                                xyList = xyList + self.getWhiteBox(edges, (x1 + i + 1,y1,x2,y2))
                            return xyList
                #判断不是线，则y1向上平移：
                y2 = y2 + 1
            
            x1List = [edges[y][x1] for y in range(y1,y2)]
            if max(x1List) > 0:
                #包含非零元素，判断非零元素是否是线：
                for i in range(len(x1List)):
                    if x1List[i] > 0:
                        yList = [x for x in edges[y1+i][x1:x2]]
                        if len([x for x in yList if x > 0]) > 0.8*len(yList):
                            #判断是线,则分割数据。
                            if i == 0:
                                xyList = self.getWhiteBox(edges, (x1,y1+1,x2,y2))
                            elif y1 + i == y2:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2,y2-1))
                            else:
                                xyList = self.getWhiteBox(edges, (x1,y1,x2,y1 + i - 1))
                                xyList = xyList + self.getWhiteBox(edges, (x1,y1 + i + 1,x2,y2))
                            return xyList
                #判断不是线，则x2向左平移：
                x1 = x1 + 1
            
            if xyArea == (x2 - x1) * (y2 - y1):
                return [(x1,y1,x2,y2)]
            else:
                xyArea = (x2 - x1) * (y2 - y1)
        
        return [xyMatrix]
    
    def getClearBlankBox(self, edges, xyMatrix):
        #在白框区域中查找文本最大框
        (x1,y1,x2,y2) = xyMatrix
        yUp = y2
        yDown = -1
        xLeft = x2
        xRight = -1
        for y in range(y1,y2):
            for x in  range(x1,x2):
                if edges[y][x] > 0:
                    yUp = min(yUp,y)
                    yDown = max(yDown,y)
                    xLeft = min(xLeft,x)
                    xRight = max(xRight,x)
        
        if yDown >= 0:
            return (xLeft,yUp,xRight,yDown)
        else:
            return (-1,-1,-1,-1)
    
    
    #先定位区域白线,再递推查找第一个黑点
    def getCharacterBoundary(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 1. Sobel算子，x方向求梯度
        sobel = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize = 3)
        sobel = cv2.convertScaleAbs(sobel)   # 转回uint8  
        # 2. 二值化
        ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        #print type(binary),np.max(binary)
        if np.max(binary) == 0:
            #纯色图片
            return np.array([])
        else:
            # 3. 膨胀和腐蚀操作的核函数
            element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            # 4. 膨胀一次，让轮廓突出
            dilation = cv2.dilate(binary, element2, iterations = 1)
            # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
            erosion = cv2.erode(dilation, element1, iterations = 1)
            # 6. 再次膨胀，让轮廓明显一些
            dilation2 = cv2.dilate(erosion, element2, iterations = 3)
            # 1. 查找轮廓
            img_fc, contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            hierarchy = hierarchy[0]
            region = []
            # 2. 筛选那些扁的
            for i in range(len(contours)):
                cnt = contours[i]
                # 找到最小的矩形，该矩形可能有方向
                rect = cv2.minAreaRect(cnt)
        
                # box是四个点的坐标
                box = cv2.boxPoints(rect)
                box = np.int0(box)
        
                ## 计算高和宽
                #height = abs(box[0][1] - box[2][1])
                #width = abs(box[0][0] - box[2][0])
                #
                ## 筛选那些太细的矩形，留下扁的
                #if(height > width * 1.2):
                #    continue
        
                region.append(box)
            if len(region)>0:
                (xLeft,yUp,xRight,yDown) = (99999,99999,0,0)
                #print 'region-------------'
                for box in region:
                    #print  'box',box
                    xLeft = min([xLeft,min([x[0] for x in box])])
                    yUp = min([yUp,min([x[1] for x in box])])
                    xRight = max([xRight, max([x[0] for x in box])])
                    yDown = max([yDown, max([x[1] for x in box])])
                
                #print '--------'
                #print (xLeft,yUp,xRight,yDown)
                #print '--------'
                
                #img3 = [img[y][xLeft:xRight+1] for y in range(yUp,yDown+1)]
                #return np.array(img3)
                img3 = img[yUp:yDown+1,xLeft:xRight+1]
                #print img3
                return img3
            else:
                return np.array([])
    
    #矩形框切割：
    def getCutColumn(self, edges, xList, yList, minLength = 20):
        xListNew = xList
        yListNew = yList
        
        #确定切割的矩形区域
        xAxis = range(xList[0]+1,xList[1])
        yAxis = range(min(yList)+1,max(yList))
        
        #统计纯白竖线
        xList0 = []
        for x in xAxis:
            yLines = [edges[y][x] for y in yAxis]
            #print yLines
            #纯白线
            if sum(yLines) == 255*len(yList) - 255*2:
                xList0.append(x)
        
        #print xList0
        #统计连续纯白竖线，且长度> minLength的个数
        diffxList0 = np.diff(xList0)
        tTmp = []
        tIndexList = []
        for i in range(len(diffxList0)):
            if diffxList0[i] == 1:
                if len(tTmp) == 0:
                    tTmp = [xList0[i], i]
            else:
                if len(tTmp) == 2:
                    if i + 1 - tTmp[1] > minLength:
                        tIndexList.append((tTmp[0], tTmp[1], i + 1, i + 1 - tTmp[1]))
                    tTmp = []
        
        if tIndexList:
            xListNew = [xList[0]]
            for i in range(1,len(tIndexList)):
                xListNew.append(tIndexList[i][0])
            xListNew.append(xList[1])
            
        return [xListNew, yListNew]
    
    def getTablePicture(self,img):
        #采用高斯滤波器过滤数据
        #img = cv2.GaussianBlur(img,(5,5),0)  
        #转灰度图像 
#         print img
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #边缘检测
        edges = cv2.Canny(gray,10,50, apertureSize = 3)
        ###查看数据图像
        #plt.imshow(edges,)
        #plt.xticks([]),plt.yticks([])
        #plt.show()
        
        #直线检测hough transform
        lines = cv2.HoughLines(edges,1,np.pi/180,300)
        lines1 = lines[:,0,:]#提取为为二维
        #从检测到的直线中统计所有的竖线和横线
        [xListNew,yListNew] = self.getTableLines(edges, lines1, minLength = 50)
        #print xListNew
        #print yListNew
#         #画线
#         for x in xListNew:
#             cv2.line(img,(x,-1000),(x,1000),(255,0,0),1)
#         for y in yListNew:
#             cv2.line(img,(-1000,y),(1000,y),(255,0,0),1)
#         #查看数据图像
#         plt.imshow(img,)
#         plt.xticks([]),plt.yticks([])
#         plt.show()
        
        
        
        #组合竖线和横线并判断，获得数据表范围内的竖线和横线(边界竖线和表内横线)
        [xListNew,yListNew] = self.getQuoteTable(xListNew, yListNew, minLength = 10)
        #print xListNew
        #print yListNew
#         ##画线
#         for x in xListNew:
#             cv2.line(img,(x,-1000),(x,1000),(0,255,0),1)
#         for y in yListNew:
#             cv2.line(img,(-1000,y),(1000,y),(0,255,0),1)
#         #查看数据图像
#         plt.imshow(img,)
#         plt.xticks([]),plt.yticks([])
#         plt.show()
        
        #根据最外围的文本框进行列切割
        [xListNew,yListNew] = self.getCutColumn(edges, xListNew, yListNew, minLength = 15)
        #形成文本数据框,删除小面积的矩形
        xyMatrixNew = self.getMatrixList(xListNew,yListNew,minArea = 40)
        
        return xyMatrixNew
    
    def getSubPicMat(self,img,xyMatrixNew,dictName = []):
        picDict = {}
        for iRow in range(len(xyMatrixNew)):
            subPicDict = {}
            rowList = xyMatrixNew[iRow]
            if len(rowList) == len(dictName):
                for jCol in range(len(rowList)):
                    img2 = []
                    (x1,y1,x2,y2,area0) = rowList[jCol]
                    #只选项小数据框中的文本部分
                    #(xLift,yUp,xRight,yDown) = cq.getCharacterBoundary(edges, (x1,y1,x2,y2), minLength = 3)
                    (xLeft,yUp,xRight,yDown) = (x1,y1,x2,y2)
                    #抠图
                    if xLeft >= 0:
                        img2 = [img[y][xLeft:xRight+1] for y in range(yUp,yDown+1)]
                        img2 = np.array(img2)
                        subPicDict[dictName[jCol]] = copy.deepcopy(img2)
                        #数据存储
                        #cv2.imwrite("E:/NLP/QDFile/subgraphRGB/QQ_%s_%s.png"%(iRow,jCol), img2, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                picDict[iRow] = subPicDict
            else:
                print "The length is not consistent,xyMatrixNew columns:%s and dict names:%s"%(len(rowList),len(dictName))
                picDict[iRow] = {}
        return picDict
    
    def getPSPicture(self, img):
        #img = cv2.imread('E:/NLP/QDFile/subgraphRGB/QQ_4_0.png')
        img2 = copy.deepcopy(img)
        aDict = {}
        for tmp1 in img2:
            for tmp2 in tmp1:
                aDict[tuple(tmp2)] = aDict.get(tuple(tmp2),0)+1
        
        aList = sorted(aDict.items(), key=lambda d:(d[1]), reverse = True)  
        if len(aList) >= 4:
            if aList[1][1] > 300:
                imageValue = np.array(aList[1][0])
                #[228, 175, 82]  
                #(0, 124, 229) 344
                #(81, 81, 32) 1189 
                m,n,s = img2.shape #行，列，像素
                for i in range(n):
                    for j in range(m):
                        if tuple(img2[j][i]) == tuple(imageValue):
                            break
                        else:
                            img2[j][i] = imageValue
                    for j in range(m)[::-1]:
                        if tuple(img2[j][i]) == tuple(imageValue):
                            break
                        else:
                            img2[j][i] = imageValue
        return img2
    
    def getMinPic(self,img,minValue):
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
            return img[yUp-1:yDown+2,xLeft-1:xRight+2]
        else:
            return np.array([])
    
    def getBinaryImage(self,img,x = 0, y = 255, Methods = cv2.THRESH_OTSU+cv2.THRESH_BINARY):
        if np.max(img) <> np.min(img):
            img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            #转二值图
            ret,img2=cv2.threshold(img2, x, y, Methods)
            ##颜色反转，如果均值大于200,说明底色是白色，文字是黑色，需要颜色反转
            if np.mean(img2) > 200:
                img2 = 255 - img2
            #图像裁剪
            img2 = self.getMinPic(img2,0)
            ## img2=cv2.resize(img2,(len(img2[0])*5,len(img2)*5),interpolation=cv2.INTER_CUBIC)
            #k = k + 1
            #cv2.imwrite("E:/NLP/QDFile/subgraphRGB9/QQ_%s.png"%k, img2, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            
            #查看数据图像
            #plt.imshow(img2,)
            #plt.xticks([]),plt.yticks([])
            #plt.show()
            
            #histr = cv2.calcHist([img2],[0],None,[256],[0,256])
            #plt.plot(histr)
            #plt.show()
            if img2.shape[0] > 0 and img2.shape[1] > 0:
                return img2
            else:
                return None
        else:
            return None

class cutWordImage(object):
    def getWordList(self, diffList,tRange):
        bestList = []
        tmp = 0
        for i in range(len(diffList)):
            tmp = tmp + diffList[i]
            if tmp in tRange:
                if i + 1 < len(diffList):
                    tmp1 = diffList[:i+1]
                    tmp2 = self.getWordList(diffList[i+1:],tRange)
                    #print tmp2
                    for tmp3 in tmp2:
                        bestList.append([tmp1]+tmp3)
                else:
                    bestList.append([diffList])
        return bestList
    
    #对单位短语分字
    def getWordImage(self, img, tLine, tRange = [11,12,13,14,15]):
        img2 = img
        xCumSum = np.sum(img2, axis=0)
    
        #先找到极小点
        tList = [0]
        for i in range(len(xCumSum)-5):
            if xCumSum[i+2] == np.min(xCumSum[i:i+5]) and xCumSum[i+2] <= tLine:
                
                tList.append(i+2)
    
        tList.append(len(xCumSum))
        #计算极小点之间的距离
        diffList = np.diff(tList)
        wordList = self.getWordList(diffList,tRange)
        #print wordList
        if len(wordList) > 0:
            if len(wordList) == 1:
                idList = []
                sId = 0
                for i in wordList[0]:
                    sId = sId + len(i)
                    idList.append(tList[sId])
                return idList
            else:
                sd0 = float('Inf')
                rt = []
                for tmpList in wordList:
                    sd = np.var(np.array([np.sum(x) for x in tmpList]))
                    if sd < sd0:
                        sd0 = sd
                        rt = tmpList
                if len(rt) > 0:
                    idList = []
                    sId = 0
                    for i in rt:
                        sId = sId + len(i)
                        idList.append(tList[sId])
                    return idList
                else:
                    return []
        else:
            return []
    
    #图片分割
    def getSubImage(self,img2,minLength0 = 1):
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
    
    
    def getSubImage1(self,tmp):
        tmpSubImg = []
        if tmp.shape[1] > 20: 
            a=np.sum(tmp, axis=0)
            tLine = np.percentile([x for x in a if x > 0],50)#非0的25%分位数作为基准线，文本分界点必然在基准线以下
            #定位单位和姓名间的短线位置
            subsectionId = tuple()
            #场景1：机构名称-姓名
            for i in range(len(a)-6):
                if len(a[i:]) >= 6:
                    b1 = a[i:i+6]
                    b2 = [0,  255,  255,  255,  255,  0]
                    if np.sum(b1 == b2) == len(b1):
                        subsectionId = (i,i+6)
                        break
            #场景2：机构名称-...
            if len(subsectionId) == 0: 
                b1 = a[-5:]
                b2 = [0,  255,  255,  255,  255]
                if np.sum(b1 == b2) == len(b1):
                    #plt.imshow(tmp)
                    #plt.show()
                    subsectionId = (len(a)-5,len(a))
            #print 'offer--'
            #print subsectionId
            
            if len(subsectionId) > 0:
                #分割出单位短语
                img21 = tmp[:,:subsectionId[0]]
                if len(img21) > 0:
                    xListNew = self.getWordImage(img21,tLine,tRange = [11,12,13,14,15])
                    if len(xListNew) > 0:
                        xListNew.insert(0,0)
                        for i in range(1,len(xListNew)):
                            tmpSubImg.append(img21[:,xListNew[i-1]:xListNew[i]])
                    else:
                        tmpSubImg.append(img21)
                    tmpSubImg.append(tmp[:,subsectionId[0]:subsectionId[1]])
                #分割出姓名短语
                img21 = tmp[:,subsectionId[1]:]
                if len(img21) > 0:
                    xListNew = self.getWordImage(img21,tLine,tRange = [11,12,13,14,15])
                #print '-----'
                #print xListNew
                    if len(xListNew) > 0:
                        #print np.sum(img21, axis=0)
                        #print xListNew
                        xListNew.insert(0,0)
                        for i in range(1,len(xListNew)):
                            tmpSubImg.append(img21[:,xListNew[i-1]:xListNew[i]])
                    else:
                        tmpSubImg.append(img21)
            else:
                #场景3：机构名称
                img21 = tmp
                if len(img21) > 0:
                    xListNew = self.getWordImage(img21,tLine,tRange = [11,12,13,14,15])
                    if len(xListNew) > 0:
                        xListNew.insert(0,0)
                        for i in range(1,len(xListNew)):
                            tmpSubImg.append(img21[:,xListNew[i-1]:xListNew[i]])
                    else:
                        tmpSubImg.append(img21)
                else:
                    tmpSubImg.append(tmp)
        else:
            tmpSubImg.append(tmp)
        return tmpSubImg
    
    def getSubImage2(self,tmp,b2 = [0,  255,  255,  255,  255,  0]):
        tmpSubImg = []
        if tmp.shape[1] > 17:
            a=np.sum(tmp, axis=0)
            #tLine = np.percentile([x for x in a if x > 0],25)#非0的25%分位数作为基准线，文本分界点必然在基准线以下
            tLine = 765
            #定位单位和姓名间的短线位置
            subsectionIdList = [(0,len(a))]
            for i in range(len(a)-len(b2)):
                if len(a[i:]) >= len(b2):
                    b1 = a[i:i+len(b2)]
                    if np.sum(b1 == b2) == len(b1):
                        subsectionIdList[-1] = (subsectionIdList[-1][0],i)
                        subsectionIdList.append((i+len(b2),len(a)))
            
            #分割出单位短语
            if len(subsectionIdList) > 0:
                for i in range(len(subsectionIdList)):
                    subsectionId = subsectionIdList[i]
                    img21 = tmp[:,subsectionId[0]:subsectionId[1]]
                    xListNew = self.getWordImage(img21,tLine,tRange = [5,6,7,8,9,10,11])
                    if len(xListNew) > 0:
                        xListNew.insert(0,0)
                        for j in range(1,len(xListNew)):
                            tmpSubImg.append(img21[:,xListNew[j-1]:xListNew[j]])
                        if i + 1 < len(subsectionIdList):
                            tmpSubImg.append(tmp[:,subsectionIdList[i][1]:subsectionIdList[i+1][0]])
                    else:
                        tmpSubImg.append(img21)
            else:
                img21 = tmp
                if len(img21) > 0:
                    xListNew = self.getWordImage(img21,tLine,tRange = [11,12,13,14,15])
                    if len(xListNew) > 0:
                        xListNew.insert(0,0)
                        for i in range(1,len(xListNew)):
                            tmpSubImg.append(img21[:,xListNew[i-1]:xListNew[i]])
                    else:
                        tmpSubImg.append(img21)
        else:
            tmpSubImg.append(tmp)
        return tmpSubImg
    

class cvPredictiveText(object):
    dataPath = 'E:/NLP/QDFile/imageData.pkl'
    knn = cv2.ml.KNearest_create()
    trainStr = {}
 
    
    def __init__(self,tPath = 'D:/picreg/trainData/imageData.pkl',historypath='D:/historydata216b1600.pkl'):
        if tPath and historypath:
            self.dataPath = tPath
            self.historydatapath=historypath
        history_file=open('D:/historydata216b1600.pkl', 'rb')
        self.historydata=pickle.load(history_file)
        pkl_file = open(tPath, 'rb')
        allData = pickle.load(pkl_file)
        pkl_file.close()
        train = allData['data']
        train_labels = np.arange(len(train))
        self.trainStr = allData['label']
        self.knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
    def convertToBinary(self,image):
        '''
        1.图片并转为二值化,按列存为向量
        '''
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        elif len(image.shape) == 2:
            gray = image
        else:
            print 'ERROR: the shape is ',image.shape
        x = np.array(gray)
        wordindex=x.sum()/255
        wordvector=x.reshape((1600,-1),order='F').T
        return wordindex,wordvector
    #
    # def readPic2(self,imageDatapath):
    #     olddata = open('D:/picreg/trainData/imageData.pkl', 'rb')
    #     data1= pickle.load(olddata)


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
#         print targetID
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
        return targetmatrix,targetindex,newvectorlist,newID

    def compareVector(self,cutpart,targetmatrix,targetindex,transvectorlist,wordindex0): 
#         print wordindex0
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
#                 if flag1>((14-2*cutpart)*20-5):
#                     if targetindex[j] not in wordindex and targetindex[j] !=[]:
#                         wordindex.append(targetindex[j])
#                     print wordindex
                if wordindex0<30 and flag1==((14-2*cutpart)*20):
#                     print wordindex0
                    if targetindex[j] not in wordindex and targetindex[j] !=[]:
                            wordindex.append(targetindex[j])
                else:
                    if flag1>((14-2*cutpart)*20-2):
                        if targetindex[j] not in wordindex and targetindex[j] !=[]:
                            wordindex.append(targetindex[j])
#                     print wordindex
        return wordindex        
    
    def seeTheRight(self,path1):
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
    def predictWord(self,candidateImage,historydata):
        dataMatrix,wordlist,inverdict=historydata
        ##切割列数
        cutpart=4
        ##平移列数
        movestep=2    
        targetmatrix,targetindex,newvector,newID=self.getWord(candidateImage, wordlist, dataMatrix)
        candidatelist=self.moveToCompare(newvector,movestep)
        result1=self.compareVector(cutpart,targetmatrix, targetindex, candidatelist,newID)
        if result1 !=[]:
            predictword=[]
#                 print result1
            for j in result1:
#                 print '预测可能词：',inverdict[str(i)]
                predictword.append(inverdict[str(j)])
            di=Counter(predictword)    
            fdist1=sorted(di.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
#             print '可能预测词：',fdist1.keys()[0],'            预测概率为：',fdist1.freq(fdist1.keys()[0])
#             if fdist1.keys()[0]==inverdict2[str(i)]:
#                 flagx+=1
#             else: print '识别错误，请检查！！'
#             if fdist1.freq(fdist1.keys()[0]) !=1:
#                 print '可能预测词：',fdist1.keys()[1],'            预测概率为：',fdist1.freq(fdist1.keys()[1])  
        else:
            print '无法识别，请检查！' 
            tUID = str(uuid.uuid1(1600))
            #print tUID
            #print dist[0,0]
            cv2.imwrite(tUID+'.png',candidateImage, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            return '*'
        return   fdist1[0][0]
    def saveHistoryData(self,picpath,standwordpath,picnum):
        '''
                    存储数据:history[向量矩阵,索引列表,字典] 
        '''
        startnum=1
        standwordlist,inverdict=self.seeTheRight(standwordpath)
        dataMatrix,wordlist=self.readPic(picpath,startnum,picnum)
        historydata=[dataMatrix,wordlist,inverdict]     
        return historydata
    
    def updateData(self,historydata,newpicpath,newstandwordpath,newstartnum,newpicnum):
        dataMatrix,wordlist,inverdict=historydata
#         print len(wordlist), inverdict['1143']
        newstandwordlist,newinverdict=self.seeTheRight(newstandwordpath)
#         print len(newinverdict)
        newdataMatrix,newwordlist=self.readPic(newpicpath,newstartnum,newpicnum)        
        updateMatrix=np.concatenate((dataMatrix,newdataMatrix))
        updatewordlist=wordlist+newwordlist
        adddict={}
#         print len(inverdict)
#         print newinverdict['110']
        for i in range(newpicnum):
            adddict[str(i+len(dataMatrix))]=newinverdict[str(i)]
#         print len(adddict),'#####'
        dictMerged=dict(inverdict)
        dictMerged.update(adddict)
#         print dictMerged['1020']
        newdata=[updateMatrix,updatewordlist,dictMerged]   
        return  newdata     
    def getMinPic(self,img,minValue = 0):
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
    
    def getNormalizePic(self,gray,mLength=20,nLength = 100):
        m,n = gray.shape
        if m > 20:
            print "error:m = %s"%(m)
            return np.array([])
        else:
            gray1 = np.row_stack((gray,np.array([0]*n*(mLength-m)).reshape(mLength-m, n)))
            m = mLength
            
            gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
            n = nLength
               
#             if n <= 15:
#                 nLength = 20
#                 gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#                 n = nLength
#             elif n <= 30:
#                 nLength = 30
#                 gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#                 n = nLength
#             elif n <= 45:
#                 nLength = 45
#                 gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#                 n = nLength
#             elif n <= 60:
#                 nLength = 60
#                 gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#                 n = nLength
#             else:
#                 nLength = 200
#                 gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
#                 n = nLength
        return gray1
    
    def getReadImg1(self,gray, minValue=0, mLength=20, nLength=80, minDist = 2):
        imgMin = self.getMinPic(gray,minValue)
        if len(imgMin) > 0:
            imgLength = 1
            for i in imgMin.shape:
                imgLength = imgLength * i
            if imgLength > 1 and imgLength <= mLength*nLength:
                gray1 = self.getNormalizePic(imgMin,mLength,nLength).reshape(-1,mLength*nLength).astype(np.float32)
                #print type(gray1)
                #print gray1.shape
                ret, results, neighbours ,dist = self.knn.findNearest(gray1, 1)
                if dist[0,0] == 0:
                    return self.trainStr[int(results[0,0])]
                elif dist[0,0] <= minDist*65025 and np.sum(gray1)/255 > 25:
                    return self.trainStr[int(results[0,0])]
                else:
                    #print imgMin
                    #print dist[0,0]
                    #图片聚类超限，判定失败，存储图片
                    tUID = str(uuid.uuid1(1600))
                    #print tUID
                    #print dist[0,0]
                    cv2.imwrite(tUID+'.png',gray, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    return '*'
            else:
                return ''
        else:
            return ''
        #print results.shape
        #print type(results)
    
    def getReadImg(self,gray,minValue = 0,mLength=20,nLength = 80,minDist = 2):
        imgMin = self.getMinPic(gray,minValue)
        if len(imgMin) > 0:
            imgLength = 1
            for i in imgMin.shape:
                imgLength = imgLength * i
            if imgLength > 1 and imgLength <= mLength*nLength:
                gray1 = self.getNormalizePic(imgMin,mLength,nLength)
#                 print gray1 ,'#######'    
#                 cv2.imwrite('D:/picreg/trainData/%.png'%(i),gray1)
                predictword = self.predictWord(gray1,self.historydata)
        else:
            return ''
        return predictword
def extractionQBImage(imgPath,tPath = 'imageData.pkl'):
#     print imgPath
    
    img = cv2.imread(imgPath)
#     print type(img)
    picId = 0
    #加载采集特定图片表格的类
    cq = cutTablePicture()
    cw = cutWordImage()
    cp = cvPredictiveText(tPath,'historydata.pkl')

    xyMatrixNew = cq.getTablePicture(img)
    #验证数据是否正常
    colNum = 9
    compliance = True
    for y in xyMatrixNew:
        if len(y) != colNum:
            compliance = False
            break
    strList = []
    if compliance:
        #数据正常进行抠图
        #循环抠图
        dictName = ['direction','term','quantity','price',
                    'label','original','offer','telephone',
                    'update','match']
        
        picDict = cq.getSubPicMat(img, xyMatrixNew, dictName[:9])
        strDict = {}
        #print len(picDict)
        for tKey in picDict.keys():
            subStrDict = {}
            subPicDict = picDict[tKey]
            
            '''
            ------------
            #0处理方向  direction
            ------------
            '''
            #为避免方向词外围颜色的影响，填充背景像素
            subImg = cq.getPSPicture(subPicDict['direction'])
            #将图片转灰度图，然后转二值化图，最后裁剪至最小图
            #subImg = cq.getBinaryImage(subImg,x = 0, y = 255, Methods = cv2.THRESH_OTSU+cv2.THRESH_BINARY)
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            
            tmpStr = []
            tmp1 = subImg
            if tmp1 is not None and len(tmp1) > 0:
                #识别文本
                tmp1Str = cp.getReadImg(tmp1)
                tmpStr.append(tmp1Str)
            subStrDict['direction'] = ''.join(tmpStr)
            
            '''
            ------------
            #1处理期限 term
            ------------
            '''
            subImg = subPicDict['term']
            #将图片转灰度图，然后转二值化图，最后裁剪至最小图
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                #图片切字，按列灰度值为0的列作为分界，将图片裁剪为一个一个小图
                tmpSubImg = cw.getSubImage(subImg, minLength0 = 1)
                #循环识图
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['term'] = ''.join(tmpStr)
            
            
            '''
            ------------
            #2处理数量 quantity
            ------------
            '''
            subImg = subPicDict['quantity']
            #将图片转灰度图，然后转二值化图，最后裁剪至最小图
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                #图片切字，按列灰度值为0的列作为分界，将图片裁剪为一个一个小图
                tmpSubImg = cw.getSubImage(subImg, minLength0 = 1)
                #循环识图
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['quantity'] = ''.join(tmpStr)
            '''
            ------------
            #3处理价格 price
            ------------
            '''
            subImg = subPicDict['price']
            #将图片转灰度图，然后转二值化图，最后裁剪至最小图
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                #图片切字，按列灰度值为0的列作为分界，将图片裁剪为一个一个小图
                tmpSubImg = cw.getSubImage(subImg, minLength0 = 1)
                #循环识图
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['price'] = ''.join(tmpStr)
            
            '''
            ------------
            #4处理标签 label
            ------------
            '''
            subImg = cq.getPSPicture(subPicDict['label'])
            #subImg = cq.getBinaryImage(subImg,x = 0, y = 255, Methods = cv2.THRESH_OTSU+cv2.THRESH_BINARY)
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                #图片切字，按连续3列的列灰度值为0的列组合作为分界，将图片裁剪为一个一个小图
                tmpSubImg = cw.getSubImage(subImg, minLength0 = 3)
                #循环识图
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['label'] = ','.join(tmpStr)
            
            '''
            ------------
            #5处理原文original
            ------------
            '''
            
                     
            
            '''
            ------------
            #6处理对手方offer
            ------------
            '''   
            subImg = subPicDict['offer']
            #subImg = cq.getBinaryImage(subImg,x = 0, y = 255, Methods = cv2.THRESH_OTSU+cv2.THRESH_BINARY)
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                tmpSubImg = []
                #图片切字，按列灰度值为0的列作为分界，将图片裁剪为一个一个小图
                for tmp in cw.getSubImage(subImg, minLength0 = 3):
                    #特定图片场景的切字：中文字符-中文字符，或中文字符-
                    tmpSubImg = tmpSubImg + cw.getSubImage1(tmp)
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        #if tmp1Str == '*':
                        #    plt.imshow(tmp1)
                        #    plt.show()
                        tmpStr.append(tmp1Str)
            subStrDict['offer'] = ''.join(tmpStr)
            
            '''
            ------------
            #7处理联系方式 telephone
            ------------
            '''
            
            subImg = subPicDict['telephone']
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                tmpSubImg = []
                for tmp in cw.getSubImage(subImg, minLength0 = 3):
                    tmpSubImg = tmpSubImg + cw.getSubImage2(tmp)
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['telephone'] = ''.join(tmpStr)
            
            
            
            '''
            ------------
            #8处理更新时间 update
            ------------
            '''
            
            subImg = subPicDict['update']
            subImg = cq.getBinaryImage(subImg,x = 127, y = 255, Methods = cv2.THRESH_BINARY)
            tmpStr = []
            if subImg is not None:
                tmpSubImg = []
                for tmp in cw.getSubImage(subImg, minLength0 = 3):
                    b2 = [0,1020,1020,0]
                    tmpSubImg = tmpSubImg + cw.getSubImage2(tmp,b2)
                for tmp1 in tmpSubImg:
                    if tmp1 is not None and len(tmp1) > 0:
                        tmp1Str = cp.getReadImg(tmp1)
                        tmpStr.append(tmp1Str)
            subStrDict['update'] = ''.join(tmpStr)
            
            '''
            ------------
            #end 数据汇总
            ------------
            '''
            
            dictName0 = ['direction','term','quantity','price','label','offer','telephone','update']
            tList = []
            for x in dictName0:
                tList.append(subStrDict[x])
            strList.append(tList)
            strDict[tKey] = subStrDict
    #return strDict
    return strList



if __name__=='__main__':
    strList = []
    #读取数据
    #img = cv2.imread('E:/NLP/QDFile/pd12.png')
    if len(sys.argv) >= 3:
        #sys.argv[1] = '数据集路径'
        #sys.argv[2] = '要训练的图片路径'
        dataPath = sys.argv[1]
        imgPath = sys.argv[2]
        strList = extractionQBImage(dataPath,imgPath)
    elif len(sys.argv) == 2:
        dataPath = 'D:/picreg/trainData/imageData.pkl'
        imgPath = sys.argv[1]
        strList = extractionQBImage(imgPath,dataPath)
    
    dataPath = 'D:/picreg/trainData/imageData.pkl'
    imgPath = 'D:/picreg/trainData/1.png'
    strList = extractionQBImage(imgPath,dataPath)
    
    #dataPath = 'E:/NLP/QDFile/imageStr.pkl'
    #pkl_file = open(dataPath, 'wb')
    #pickle.dump(strDict, pkl_file)
    #pkl_file.close()
    
    #dataPath = 'E:/NLP/QDFile/imageStr.pkl'
    #pkl_file = open(dataPath, 'rb')
    #strDict = pickle.load(pkl_file)
    #pkl_file.close()
    if strList:
        dictName = ['direction','term','quantity','price',
                    'label','offer','telephone','update']
        for tmp in strList:
            i = 0
            for t1Key in dictName:
                print t1Key,tmp[i],
                i = i + 1
            print '\n'
    else:
        print 'please input image path'
                #print tmp
                #plt.imshow(tmp1,)
                #plt.show()
#             plt.hist(tmp.ravel(),256,[0,256]);
#             plt.show()
    
    