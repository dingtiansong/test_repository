#coding=utf-8
'''
Created on 2016年11月16日

@author: WangWP
'''
import cv2 
import time
import numpy as np
import matplotlib.pyplot as plt

#抽取横线和竖线
def getTableLines(edges, lines1, minLength = 50):
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

def getQuoteTable(xList, yList, minLength = 10):
    #对竖线的处理，取间距最长的两条线：
    diffList = list(np.diff(xList))
    tIndex = diffList.index(max(diffList))
    xListNew = [xList[tIndex],xList[tIndex+1]]
    #对横线的处理，选取等间距数量最多的线列。要求线列的间距大于minLength
    diffList = np.diff(yList)
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

def getMatrixList(xListNew,yListNew):
    #构造矩形框
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
    
    #计算面积筛选矩形框
    #删除面积最小100像素的矩形框所在的行列
    delRow = []
    delCol = []
    for i in range(len(xyMatrixList)):
        tmp = xyMatrixList[i]
        for j in range(len(tmp)):
            if tmp[j][4] < 100:
                delRow.append(i)
                delCol.append(j)
    
    #删除行列，得到理论上的数据框行列
    trueRow = set(range(len(xyMatrixList))) - set(delRow)
    trueCol = set(range(len(xyMatrixList[0]))) - set(delCol)
    
    #生成真实的数据框
    xyMatrixListTrue = []
    for i in trueRow:
        tmp = xyMatrixList[i]
        xyMatrixListTrue.append([tmp[j] for j in trueCol])
    return xyMatrixListTrue

#根据数据框构造最小图片集
#先定位区域白线,再递推查找第一个黑点
def getCharacterBoundary(edges, xyMatrix, minLength = 3):
    (x1,y1,x2,y2) = xyMatrix
    isWhiteLine = False
    yUp = -1
    for y in range(y1,y2):
        xList = [x for x in edges[y][x1+1:x2]]
        #第一条纯白线
        if max(xList) == 0:
            isWhiteLine = True
            blackPointCount = 0
        #纯白线之后的第一个连续4个值的边界点
        if isWhiteLine:
            if max(xList) == 255:
                blackPointCount += 1
            else:
                blackPointCount = 0
            if blackPointCount > minLength:
                yUp = y + 1 - blackPointCount
                break
    if yUp >= 0:
        print '有数据'
    else:
        print '没有数据'
    
    
    isWhiteLine = False
    yDown = -1
    print 'ssss'
    print x1,y1,x2,y2
    for y in range(y2,y1,-1):
        xList = [x for x in edges[y][x1+1:x2]]
        #第一条纯白线
        if max(xList) == 0:
            isWhiteLine = True
            blackPointCount = 0
        #纯白线之后的第一个边界点
        if isWhiteLine:
            if max(xList) == 255:
                blackPointCount += 1
            else:
                blackPointCount = 0
            if blackPointCount > minLength:
                yDown = y - 1 + blackPointCount
                break
    if yDown >= 0:
        print '有数据'
    else:
        print '没有数据'
    
    isWhiteLine = False
    xLift = -1
    for x in range(x1,x2):
        yList = [edges[y][x] for y in range(y1+1,y2)]
        #第一条纯白线
        if max(yList) == 0:
            isWhiteLine = True
            blackPointCount = 0
        #纯白线之后的第一个边界点
        if isWhiteLine:
            if max(yList) == 255:
                blackPointCount += 1
            else:
                blackPointCount = 0
            if blackPointCount > minLength:
                xLift = x + 1 - blackPointCount
                break
    if xLift >= 0:
        print '有数据'
    else:
        print '没有数据'
    
    isWhiteLine = False
    xRight = -1
    for x in range(x2,x1,-1):
        yList = [edges[y][x] for y in range(y1+1,y2)]
        #第一条纯白线
        if max(yList) == 0:
            isWhiteLine = True
            blackPointCount = 0
        #纯白线之后的第一个边界点
        if isWhiteLine:
            if max(yList) == 255:
                blackPointCount += 1
            else:
                blackPointCount = 0
            if blackPointCount > minLength:
                xRight = x - 1 + blackPointCount
                break
    if xRight >= 0:
        print '有数据'
    else:
        print '没有数据'
    
    if xLift>=0 and xRight >= 0 and xRight >= 0 and yDown >= 0:
        return (xLift,yUp,xRight,yDown)
    else:
        return (-1,-1,-1,-1)

#矩形框切割：
def getCutColumn(edges, xList, yList, minLength = 10):
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
    
if __name__=='__main__':
    #读取数据
    #img = cv2.imread('D:/ProgramFilesOffice/Python/Python27/QQ2016.png')
    img = cv2.imread('C:/Users/John64pc/Desktop/picreg/Quoteboard.png')
    plt.subplot(131),plt.imshow(img,)
    print '========================'
    plt.xticks([]),plt.yticks([]) 
    #转灰度图像 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    plt.subplot(132),plt.imshow(gray,)
    plt.xticks([]),plt.yticks([])  
    
    #描绘轮廓
    edges = cv2.Canny(gray,10,50, apertureSize = 3)
    plt.subplot(133),plt.imshow(edges,)
    plt.xticks([]),plt.yticks([])
    plt.show()  
    #hough transform
    lines = cv2.HoughLines(edges,1,np.pi/180,25)
    lines1 = lines[:,0,:]#提取为为二维
    cv2.imwrite("C:/Users/John64pc/Desktop/picreg/QQ_ALL.png", edges, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]) 
    cv2.imshow('Result', edges)  
    cv2.waitKey(0)
    plt.imshow(edges,cmap='gray', interpolation='bicubic')
    plt.show() 
     
    #统计所有的竖线和横线
    [xListNew,yListNew] = getTableLines(edges, lines1, minLength = 50)
    print xListNew
    print yListNew
    
    #获得数据表的竖线和横线
    [xListNew,yListNew] = getQuoteTable(xListNew, yListNew, minLength = 10)
    print xListNew
    print yListNew
    
    
    #根据最外围的文本框进行列切割
    [xListNew,yListNew] = getCutColumn(edges, xListNew, yListNew, minLength = 8)
    print xListNew
    print yListNew
    
    
    #画线
    for x in xListNew:
        cv2.line(img,(x,-1000),(x,1000),(255,0,0),1)
    for y in yListNew:
        cv2.line(img,(-1000,y),(1000,y),(255,0,0),1)
    
    cv2.imshow('Result', img)  
    cv2.waitKey(0) 
    
    #形成文本数据框
    xyMatrixNew = getMatrixList(xListNew,yListNew)
    
    print xyMatrixNew
    print '----------------------------'
    for irow in xyMatrixNew:
        for ij in irow:
            print ij
            (x1,y1,x2,y2,area0) = ij
            (xLift,yUp,xRight,yDown) = getCharacterBoundary(edges, (x1,y1,x2,y2), minLength = 1)
    
            #抠图
            if xLift >= 0:
                img2 = [gray[y][xLift:xRight+1] for y in range(yUp,yDown+1)]
                print img2
                img2 = np.array(img2)
                #转二值图
                ret,img2=cv2.threshold(img2,170,255,cv2.THRESH_BINARY) 
                img2=cv2.resize(img2,(len(img2[0])*10,len(img2)*10),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite("C:/Users/John64pc/Desktop/picreg/QQ_%s_%s.png"%(x1,y1), img2, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    
    #pip2 install pyocr
    from PIL import Image
    from pyocr import pyocr
    print 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    tools = pyocr.get_available_tools()[:]
#     print("Using '%s'" % (tools[0].get_name()))
    
    for irow in xyMatrixNew:
        tmpWord = []
        for ij in irow:
            imgPath = "C:/Users/John64pc/Desktop/picreg/QQ_%s_%s.png"%(ij[0],ij[1])
#             print '-----%s,%s-----'%(ij[0],ij[1])
            try:
                #s = tools[0].image_to_string(Image.open(imgPath),lang='chi_sim')
                s = tools[0].image_to_string(Image.open(imgPath),lang='chi_sim')
                print s
            except Exception as e:
                print e
                tmpWord.append('-')
            else:
                print s
                tmpWord.append(s)
        print tmpWord
                    
            
    
    
#     import cv2.cv as cv
#     import tesseract
#      
#     api = tesseract.TessBaseAPI()
#     api.Init(".","eng",tesseract.OEM_DEFAULT)
#     api.SetPageSegMode(tesseract.PSM_AUTO)
#      
#     image=cv.LoadImage("eurotext.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
#     tesseract.SetCvImage(image,api)
#     text=api.GetUTF8Text()
#     conf=api.MeanTextConf()
    