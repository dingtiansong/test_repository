#-*- coding:utf-8 -*-
'''

Created on 2016年12月21日

@author: Wenpu Wang

'''
import numpy as np
import cv2
from cutTextBox import cutTextBox
import matplotlib.pyplot as plt
class cutTextLines(object):
    def getRealSubImage(self, grayList, minRow = 150, minCol = 1):
        grayList0 = []
        tUID = 0
        for tmp in grayList:
            #删除线
            if len(tmp.shape) > 1:
                if tmp.shape[0] > minRow and tmp.shape[1] > minCol:
                    #tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY) 
                    #cv2.imwrite('%s.png'%tUID,tmp, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    grayList0.append(tmp)
                    tUID += 1
        
        return grayList0
    
    def getReflexGray(self, gray):
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
    
    def getTextRow(self, timg, lineHeight = 5):
        wordImgList = []
        binary = timg
        cv2.imwrite('tagImage.png',timg, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        plt.imshow(timg,cmap='gray')
        plt.show()
        
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
    
    def getTextLines(self, grayList):
        grayList = self.getRealSubImage(grayList, minRow = 150, minCol = 1)
        binaryLineList = []
        for tmp in grayList:
            # 5、对每个图片块的底色处理，计算相邻行均值相等的灰度的最大频数为底色灰度值，计算每个像素的灰度值=abs(x-底色灰度值)
            tmp1 = self.getReflexGray(tmp)
            # 6、图片块二值化：>25灰度的归为255，否则为0
            ret,binary = cv2.threshold(tmp1,25,255,cv2.THRESH_BINARY)
            # 7、二值图搜索文本行，输出所有可能的文本行
            tmpList = self.getTextRow(binary, lineHeight = 5)
            
            binaryLineList.append(tmpList)
        
        return binaryLineList
            
    
if __name__=='__main__':
    
    ctb = cutTextBox()
    ctl = cutTextLines()
    
    # 0、加载图片
    img = cv2.imread("E:/NLP/wumii/15.jpeg")
    # 1、图片转灰度图：
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    # 2、先按行求颜色突变行
    # 3、根据突变行划分出同色的图片块
    
    grayList = ctb.getTextBox(gray)
    print len(grayList)
    
    binaryLineList = ctl.getTextLines(grayList)
    
    print len(binaryLineList)
    sss = 0
    for tmp1 in binaryLineList:
        for tmp in tmp1:
            plt.imshow(tmp)
            plt.show()
            cv2.imwrite('newImage/%r'%sss+'.png',tmp, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            sss += 1
        