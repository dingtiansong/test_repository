#-*- coding:utf-8 -*-
'''

Created on 2016年12月21日

@author: Wenpu Wang

'''
import numpy as np
import cv2
import matplotlib.pyplot as plt

class cutTextBox(object):
    def getChangeLine(self, gray, minAvg = 10, maxVar = 5):
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

    def getSubList(self, gray, colorLine):
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
    
    
    def getTextBox(self, img):
        if len(img.shape) == 3:
            # 1、图片转灰度图：
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        elif len(img.shape) == 2:
            gray = img.copy()
        else:
            gray = []
        if isinstance(gray, np.ndarray):
            # 2、先按行求颜色突变行
            colorLine = self.getChangeLine(gray, minAvg = 10, maxVar = 5)
            # 3、根据突变行划分出同色的图片块
            imgList = self.getSubList(img,colorLine)
        
            return imgList
        else:
            return []
    

if __name__=='__main__':
    
    ctb = cutTextBox()
    
    # 0、加载图片
    Imgpic=6
    ImgNo=0
    for i in range(1,Imgpic):
#     for i in range(1,Imgpic):
#         imgpath='D:/imagedata/wm0%s.jpeg'%(i)
        imgpath='D:/imagedata/%s.png'%(i)        
        img = cv2.imread(imgpath)
        
        imgList = ctb.getTextBox(img)
        
#         print len(imgList)
        zz=0

        for tmp in imgList:
            zz+=1
            gray = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)            
            Imgwidth,Imglenth=gray.shape
            if  Imgwidth>10: 
                ImgNo+=1         
#                 aa='D:/imagedata/cutImg/0%s/%s.png'%(i+8,ImgNo)
                aa='D:/imagedata/cutImg/%s/%s.png'%(i+8,ImgNo)
                print aa
                cv2.imwrite(aa,gray)
#             plt.imshow(gray,cmap='gray')
#             plt.show()
