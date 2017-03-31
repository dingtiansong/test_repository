#-*- coding:utf-8 -*-
'''

Created on 2016年12月21日

@author: Wenpu Wang

'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy
from cutTextBox import cutTextBox
from cutTextLines import cutTextLines
from locateStr4 import myLocate

class cutWordList(object):
    def getTextRow(self, timg, lineHeight = 5):
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
        
    def getT1TextRow(self, binaryList, firstHight = range(25,31), generalHight = range(33,46), lastHitht = range(28,37)):
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
    
    
    def getWordList(self,binary, minLength0 = 0):
        #plt.imshow(binary)
        #plt.show()
        minLength0 = 0
        if minLength0 == 0:
            return self.getWordListByConnect(binary)
        return self.getWordListByFixedStep(binary, minLength0)
    
    def getWordListTuple(self,binary, minLength0=0):
        #plt.imshow(binary)
        #plt.show()
        minLength0 = 0
        if minLength0 == 0:
            binary0 = copy.copy(binary)
            image, contours, hierarchy = cv2.findContours(binary0, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            tupleList = []
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                tupleList.append((x,x+w))
            OutlineList = self.getMergeOutline(tupleList)
            return OutlineList
        else:
            a=np.sum(binary, axis=0)
            #print img2
            #print a
            xList = [i for i in range(len(a)) if a[i] > 0]
            if len(xList) > 3:
                diffList = np.diff(xList)
                dList = [i for i in range(len(diffList)) if diffList[i] > minLength0]
                if len(dList) > 0:
                    img3 = [(xList[0], xList[dList[0]]+1)]
                    i = 0
                    if len(dList) > 1:
                        for i in range(1,len(dList)):
                            img3.append((xList[dList[i-1]+1],xList[dList[i]]+1))
                    img3.append((xList[dList[i]+1],xList[-1]+1))
                    return img3
                else:
                    return [(xList[0],xList[-1]+1)]
            else:
                return []
    
    def getWordListByFixedStep(self, binary, minLength0 = 1):
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
    
    def isIntersectionInterval(self,tuple1,tuple2):
        if tuple1[0]<tuple2[0]<tuple1[1] or tuple1[0]<tuple2[1]<tuple1[1]:
            return True
        elif tuple2[0]<tuple1[0]<tuple2[1] or tuple2[0]<tuple1[1]<tuple2[1]:
            return True
        elif tuple1 == tuple2:
            return True
        else:
            return False
                
    
    def getMergeOutline(self, tupleList):
        sortedTupleList = sorted(tupleList, key=lambda d:(d[0],d[1]))
        mergeOutlineList = []
        tmp = sortedTupleList[0]
        for tmp1 in sortedTupleList[1:]:
            if self.isIntersectionInterval(tmp1,tmp):
                tmp = (min(tmp[0],tmp1[0]),max(tmp[1],tmp1[1]))
            else:
                mergeOutlineList.append(tmp)
                tmp = tmp1
        mergeOutlineList.append(tmp)
        return mergeOutlineList
    
    def getWordListByConnect(self, binary):
        binary0 = copy.copy(binary)
        image, contours, hierarchy = cv2.findContours(binary0, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        tupleList = []
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            tupleList.append((x,x+w))
        OutlineList = self.getMergeOutline(tupleList)
        
        if len(OutlineList) > 0:
            return [binary[:,x[0]:x[1]] for x in OutlineList]
        else:
            return [binary]
    
    def getT1NameList(self, binary, minLength0 = 1, maxLength = 20):
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
            if maxLen > maxLength:
                #文本分块
                twoList = self.getTextRow(binary[:,:xList[n2-1]+1], lineHeight = 5)
                oneList = self.getTextRow(binary[:,xList[n2]:], lineHeight = 5)
                if len(twoList) == 1 and len(oneList) == 1:
                    rtList.append(self.getWordList(twoList[0], minLength0))
                    rtList.append(self.getWordList(oneList[0], minLength0))
            else:
                oneList = self.getTextRow(binary[:,xList[0]:xList[-1]+1], lineHeight = 5)
                rtList.append(self.getWordList(oneList[0], minLength0))
        return rtList
    
    def getT2NameList(self, binary, minLength0 = 1):
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
            twoList = self.getTextRow(twoBinary, lineHeight = 5)
            oneBinary = binary[:,xList[n2]:]
            oneList = self.getTextRow(oneBinary, lineHeight = 5)
            if len(twoList) == 2 and len(oneList) == 1:
                rtList.append(self.getWordList(twoList[0], minLength0))
                rtList.append(self.getWordList(twoList[1], minLength0))
                rtList.append(self.getWordList(oneList[0], minLength0))
        return rtList
    
    def getCommentList(self, binary, minLength0 = 1):
        return self.getWordList(binary, minLength0)
        
    def getT2TextRow(self, binaryList, firstHight = range(75,86), generalHight = range(33,46), lastHitht = range(28,37)):
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
    
    def getTagList(self, binary):
        #通过观察可知，圆弧的灰度值在x轴上基本保持不变，但若内部出现文字，则灰度会明显上升，以此原理处理圆弧
        #求列灰度值
        b=np.sum(binary, axis=1)
        len_b = len(b)
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
            #plt.imshow(binary1)
            #plt.show()
            #plt.imshow(binary1,cmap='gray')
            #plt.show()
            binary1List = self.getWordListByFixedStep(binary1, minLength0 = 10)
            #for tmp1 in binary1List:
            #    plt.imshow(tmp1,cmap='gray')
            #    plt.show()
            #for tmp in binary1List:
            #    plt.imshow(tmp)
            #    plt.show()
            binary2List = [binary1List[i] for i in range(1,len(binary1List),3)]
            print len(binary2List)
            binaryList = []
            for binary0 in binary2List:
                #plt.imshow(binary0)
                #plt.show()
                binaryList = binaryList + self.getWordList(binary0, minLength0 = 1)
            return binaryList
        else:
            return []
    
    def getTagList2(self, binary):
        ml = myLocate()
        
        cv2.imshow('aaaa',binary)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        #cv2.imwrite("E:/NLP/QDFile/subgraphRGB/QQ_%s_%s.png"%(5555,5555), binary, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        binaryList = []
        binary1List = ml.operationThresh(binary)
        for binary0 in binary1List:
                #plt.imshow(binary0)
                #plt.show()
            binaryList = binaryList + self.getWordList(binary0, minLength0 = 1)
        return binaryList
    
    def getT3TextRow(self, binaryList, firstHight = range(20,27), tagHight = range(53,73)):
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

    
    def getWordListOfMould(self, tmpList):
        rt_wordList = []
        #过滤符合1型模板的文本组合
        wordList = self.getT1TextRow(tmpList)
        if len(wordList) > 0:
            print 'T1'
            wtList = self.getT1NameList(wordList[0], minLength0 = 1)
            rt_wordList.append(wtList)
            for i in range(1,len(wordList)-1):
                wtList = self.getWordList(wordList[i], minLength0 = 1)
                rt_wordList.append(wtList)
            wtList = self.getCommentList(wordList[-1], minLength0 = 1)
            rt_wordList.append(wtList)
        else:
            wordList = self.getT2TextRow(tmpList)
            if len(wordList) > 0:
                print 'T2'
                wtList = self.getT2NameList(wordList[0], minLength0 = 1)
                rt_wordList.append(wtList)
                for i in range(1,len(wordList)-1):
                    wtList = self.getWordList(wordList[i], minLength0 = 1)
                    rt_wordList.append(wtList)
                wtList = self.getCommentList(wordList[-1], minLength0 = 1)
                rt_wordList.append(wtList)
            else:
                wordList = self.getT3TextRow(tmpList)
                if len(wordList) > 0:
                    print 'T3'
                    wtList = self.getWordList(wordList[0], minLength0 = 1)
                    rt_wordList.append(wtList)
                    wtList = self.getTagList2(wordList[1])
                    rt_wordList.append(wtList)
        
        return rt_wordList
    
    def mergePixelListByColor(self, binary1, binary2):
        tlist = []
        i, j = 0, 0
        i0, j0 = i, j
        isBreak = False
        while(i < len(binary1) and j < len(binary2)):
            #先判断开始一致的情况
            if abs(binary1[i][0] - binary2[j][0]) < 2:
                while(i < len(binary1) and j < len(binary2) and not isBreak):
                    #判断结尾一致
                    if abs(binary1[i][1] - binary2[j][1]) < 2:
                        isBreak = True
                    #判断结尾不一致
                    else:
                        #小的加1，跳到判断结尾一致
                        if binary1[i][1] < binary2[j][1]:
                            i = i + 1
                        else:
                            j = j + 1
                if isBreak:
                    isBreak = False
                else:
                    i = len(binary1) - 1
                    j = len(binary2) - 1
                    isBreak = True
                #输出数据，取数量最多的list
                if i - i0 > j - j0:
                    tlist = tlist + binary1[i0:i+1]
                elif i - i0 < j - j0:
                    tlist = tlist + binary2[j0:j+1]
                else:
                    #两个list相等
                    if binary1[i][1] - binary1[i0][0] <= binary2[j][1] - binary2[j0][0]:
                        tlist = tlist + binary1[i0:i+1]
                    else:
                        tlist = tlist + binary2[j0:j+1]
                i = i + 1
                j = j + 1
                i0, j0 = i, j 
            else:
                #开始不一致的情况下，判断小的结尾＜大的开始+1
                if binary2[j][0] + 1 > binary1[i][1]:
                    tlist = tlist + binary1[i0:i+1]
                    i = i + 1
                    i0 = i
                elif binary1[i][0] + 1 > binary2[j][1]:
                    tlist = tlist + binary2[j0:j+1]
                    j = j + 1
                    j0 = j
                else:
                    while(i < len(binary1) and j < len(binary2) and not isBreak):
                        #判断结尾一致
                        if abs(binary1[i][1] - binary2[j][1])<2:
                            isBreak = True
                        #判断结尾不一致
                        else:
                            #小的加1，跳到判断结尾一致
                            if binary1[i][1] < binary2[j][1]:
                                i = i + 1
                            else:
                                j = j + 1
                    if isBreak:
                        isBreak = False
                    else:
                        i = len(binary1) - 1
                        j = len(binary2) - 1
                        isBreak = True
                    #输出数据，取数量最多的list
                    if i - i0 > j - j0:
                        tlist = tlist + binary1[i0:i+1]
                    elif i - i0 < j - j0:
                        tlist = tlist + binary2[j0:j+1]
                    else:
                        #两个list相等
                        if binary1[i][1] - binary1[i0][0] <= binary2[j][1] - binary2[j0][0]:
                            tlist = tlist + binary1[i0:i+1]
                        else:
                            tlist = tlist + binary2[j0:j+1]
                    i = i + 1
                    j = j + 1
                    i0, j0 = i, j
        
        #while结束：说明至少有一个数列结束
        if i < len(binary1):
            tlist = tlist + binary1[i:]
        elif j < len(binary2):
            tlist = tlist + binary2[j:]
        
        return tlist
        
    def getPixelListByColor(self, img):
        ret,binary = cv2.threshold(img[:,:,0],127,255,cv2.THRESH_BINARY)
        wtList0 = cwl.getWordListTuple(binary, minLength0 = 1)
        ret,binary = cv2.threshold(img[:,:,1],127,255,cv2.THRESH_BINARY)
        wtList1 = cwl.getWordListTuple(binary, minLength0 = 1)
        ret,binary = cv2.threshold(img[:,:,2],127,255,cv2.THRESH_BINARY)
        wtList2 = cwl.getWordListTuple(binary, minLength0 = 1)
        wtList3 = self.mergePixelListByColor(wtList0, wtList1)
        wtList4 = self.mergePixelListByColor(wtList3, wtList2)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        if len(wtList4) > 0:
            return [binary[:,x[0]:x[1]] for x in wtList4]
        else:
            return [binary] 
        
    
if __name__=='__main__':
    
    ctb = cutTextBox()
    ctl = cutTextLines()
    cwl = cutWordList()
    
    # 0、加载图片
    img = cv2.imread("E:/NLP/wumii/13.jpeg")
    # 1、图片转灰度图：
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    # 2、先按行求颜色突变行
    # 3、根据突变行划分出同色的图片块
    
    grayList = ctb.getTextBox(gray)
    
    binaryLineList = ctl.getTextLines(grayList)
    print len(binaryLineList)
    print binaryLineList
#     for tmp in binaryLineList:
#         for tmp0 in tmp:
#             plt.imshow(tmp0)
#             plt.show()
    wordListOfLine = [cwl.getWordListOfMould(tmpList) for tmpList in binaryLineList]
    
    print len(wordListOfLine)
    print wordListOfLine[0]
    
    print type(wordListOfLine[0])
    print type(wordListOfLine[0][0])
    #块、行、字、
    print type(wordListOfLine[0][0][0][0])
    for tmp1 in wordListOfLine:
        for tmp2 in tmp1:
            for tmp3 in tmp2:
                print len(wordListOfLine),len(tmp1),len(tmp2),len(tmp3)
                print type(tmp3)
#     for tmp in wordListOfLine:
#         for tmp0 in tmp:
#             plt.imshow(tmp.astype(np.uint8))
#             plt.show()
            
    
    
    