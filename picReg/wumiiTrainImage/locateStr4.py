#coding:utf-8
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

class myLocate(object):
    """ """
    def readImg(self,imgPath):
        """ 读取图片"""
        img=cv2.imread(imgPath)
        return img

    def getImgPathList(self,imgDir):
        """图片路径列表"""
        imgPathList=[]
        imgNameList=os.listdir(imgDir)
        for l in imgNameList:
            imgPath=imgDir+"/"+l
            imgPathList.append(imgPath)
        return imgPathList

    def showImg(self,name,img):
        """ 显示图片"""
        cv2.imshow(name,img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def delStrUp(self,thresh,imgTest,xMax):
        """去掉图片上方的空白"""
        m1,n1=imgTest.shape#181 720
        xList1=[]
        for x in range(m1):
            tNdarry= thresh[x][:]
            #print type(tNdarry)
            tNdarryBool=tNdarry!=0
            #print len(tNdarry)
            if True in tNdarryBool:
                xList1.append(x)
        xMax1=max(xList1)
        result=thresh[xMax1+1:xMax+1]
        return result

    def tailorRow(self,thresh):
        """删除圈上下的空白行"""
        m,n=thresh.shape#181 720
        xList=[]
        for x in range(m):
            tNdarry= thresh[x][:]
            #print type(tNdarry)
            tNdarryBool=tNdarry!=0
            #print len(tNdarry)
            if True in tNdarryBool:
                xList.append(x)

        xMin=min(xList)
        xMax=max(xList)#
        imgTest=thresh[xMin:xMax+1]
        #去掉上方的字
        #imgTest=self.delStrUp(thresh,imgTest,xMax)
        #self.showImg("imgTest",imgTest)
        return imgTest

    def tailorColumn(self,thresh):
        """ 去掉圈左右的灰度值为0的列"""
        m,n=thresh.shape
        #print threshT.shape
        yList=[]
        for y in range(n):
            tNdarry= thresh[:,y]
            #print tNdarry
            #print type(tNdarry)
            tNdarryBool=tNdarry!=0
            #print len(tNdarry)
            if True in tNdarryBool:
                yList.append(y)
        yMin=min(yList)
        yMax=max(yList)
        imgTest=thresh[:,yMin:yMax]

        return imgTest

    def getContinutIndexDict(self,sumCol):
        """ 找到列表中连续的不为0 的 下标"""
        #找到第一个零元素
        tDict={}
        tList=[]

        zeroFirstIndex=sumCol.index(0)

        controlIndex=0
        for i in range(zeroFirstIndex,len(sumCol)-1):
            sum1=sumCol[i]
            if sum1==0:
                tList.append(i)
            else:
                if len(tList)!=0:
                    tDict[controlIndex]=tList
                    controlIndex+=1
                    tList=[]
        return tDict

    def cutByColSapce(self,img_Col):
        """ 包含多个图形的分成多个图(目前只有行上存在多个图)"""
        imgList=[]
        m,n=img_Col.shape
        sumCol=[]
        for y in range(n):#列投影，计算每一列的和
            tNdarry = img_Col[:, y]
            sum1=sum(tNdarry)
            sumCol.append(sum1)
        if 0 in sumCol:
            # 获取列投影为零的列标
            continutIndexDict = self.getContinutIndexDict(sumCol)
            # 将不为零的图像切出
            yMin = 0#
            yMax=n
            for k in continutIndexDict:
                tList = continutIndexDict[k]
                yMax1 = max(tList) + 1
                yMin1 = min(tList)
                img = img_Col[:, yMin:yMin1]
                #self.showImg("t", img)
                yMin = yMax1
                imgList.append(img)
            #收尾
            if yMin<n:
                imgList.append(img_Col[:,yMin:n])
        else:
            imgList.append(img_Col)
        return imgList

    def getFirstSegment(self,tNdarry):
        """获取第一组灰度值为255的最大下标 """
        index=[]
        k=0
        for i in range(len(tNdarry)):
            val=tNdarry[i]
            if val==0:
                if k==0:
                    continue
                else:
                    break
            else:
                index.append(i)
                k+=1
        if len(index)==0:
            print tNdarry
        maxIndex=max(index)
        return maxIndex

    def getSecondSegment(self,tNdarry):
        """ 获取最后一组灰度值为255的最小下标"""
        index = []
        k = 0
        for i in range(1,len(tNdarry)):
            val = tNdarry[-i]
            if val == 0:
                if k == 0:
                    continue
                else:
                    break
            else:
                index.append(len(tNdarry)-i)
                k += 1
        minIndex = min(index)
        return minIndex

    def scanRow(self,thresh):
        """ 行扫描，确定字符的行定位"""
        m,n=thresh.shape
        tList=[]
        for x in range(m):
            tNdarry =thresh[x][:]
            #print tNdarry
            first=self.getFirstSegment(tNdarry)
            if first>0.5*n:
                continue
            else:
                second = self.getSecondSegment(tNdarry)
                if second<0.5*n:
                    continue
                else:
                    midNDarry = tNdarry[first+1:second]
                    midNDarryBool=midNDarry!=0
                    #print midNDarry
                    if True in midNDarryBool:
                        tList.append(x)
        minN=min(tList)
        maxN=max(tList)
        return minN, maxN

    def scanCol(self,thresh):
        """ 扫描列，确定字符的列定位"""
        m,n=thresh.shape
        tList=[]
        for y in range(n):
            tNdarry =thresh[:,y]
            tNdarryBool1=tNdarry!=0
            first=self.getFirstSegment(tNdarry)
            if first>0.5*m:
                continue
            else:
                second = self.getSecondSegment(tNdarry)
                if second<0.5*m:
                    continue
                else:
                    midNDarry = tNdarry[first+1:second]
                    #print midNDarry
                    midNDarryBool=midNDarry!=0
                    #print midNDarry
                    if True in midNDarryBool:
                        tList.append(y)
        minN=min(tList)
        maxN=max(tList)
        #imgtest=thresh[:,minN:maxN]
        #self.showImg("t",imgtest)
        return minN,maxN

    def operationThresh(self,thresh):
        """ 对二值图操作，从中获取 字符串区域"""
        result = []
        img_Row = self.tailorRow(thresh)  # 删除圈上下空白行
        #self.showImg("t",img_Row)
        img_Col = self.tailorColumn(img_Row)  # 删除圈左右无用的信息
        #行上可能有几个图形，将其按列拆分得到图像列表
        imgList = self.cutByColSapce(img_Col)
        for i in range(len(imgList)):
            img = imgList[i]
            minRow, maxRow = self.scanRow(img)
            minCol, maxCol = self.scanCol(img)
            test = img[minRow:maxRow, minCol:maxCol]
            result.append(test)
        return result
if __name__=="__main__":
    ml = myLocate()
    imgPath = "E:\sunxianpeng_files\processImage\T3\img\\5.png".replace("\\", "/")
    #
    img=ml.readImg(imgPath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 二值图
    #
    tList=ml.operationThresh(thresh)
    for img in tList:
        ml.showImg("t",img)