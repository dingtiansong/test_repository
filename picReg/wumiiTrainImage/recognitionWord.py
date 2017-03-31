#-*- coding:utf-8 -*-
'''

Created on 2016年12月22日

@author: Wenpu Wang

'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy
import uuid
import pickle
from cutTextBox import cutTextBox
from cutTextLines import cutTextLines
from cutWordList import cutWordList
import time


class recongnitionWordList(object):
    
    #模型训练
    def getKnnModel(self, train, train_labels):
        
        knn = cv2.ml.KNearest_create()
        print train.dtype
        print train_labels.dtype
        print train.shape
        print train_labels.shape
        knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
        return knn
    
    def getNormalizePic(self,gray):
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
                    
        # if n <= 15:
        #     nLength = 20
        #     gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        #     n = nLength
        # elif n <= 30:
        #     nLength = 30
        #     gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        #     n = nLength
        # elif n <= 45:
        #     nLength = 45
        #     gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        #     n = nLength
        # elif n <= 60:
        #     nLength = 60
        #     gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        #     n = nLength
        # else:
        #     nLength = 200
        #     gray1 = np.column_stack((gray1,np.array([0]*m*(nLength-n)).reshape(m, nLength - n)))
        #     n = nLength
        return gray1
    
    #2、切割最小图片
    def getMinPic(self, img, minValue = 0):
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
    
    
    #文本识别
    def getRecongnitionWord(self, binary, knn, train_labelstr, minDist = 2):
        
        binary1 = self.getMinPic(binary, minValue = 0)
        binary1 = self.getNormalizePic(binary1).reshape(1,-1).astype(np.float32)
        #plt.imshow(binary)
        #plt.show()
        ret, results, neighbours ,dist = knn.findNearest(binary1, 1)
        
        if dist[0,0] == 0:
            return train_labelstr[int(results[0,0])]
        elif dist[0,0] <= minDist*65025 and np.sum(binary1)/255 > 25:
            return train_labelstr[int(results[0,0])]
        else:
            #print imgMin
            #print dist[0,0]
            #图片聚类超限，判定失败，存储图片
            tUID = str(uuid.uuid1(1600))
            #time.sleep(1)
            #print tUID
            #print dist[0,0]
            cv2.imwrite('newImage/'+tUID+'.png',binary, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            return '*'
    
    

if __name__=='__main__':
    
    ctb = cutTextBox()
    ctl = cutTextLines()
    cwl = cutWordList()
    rwl = recongnitionWordList()
    
    # 0、加载图片
    img = cv2.imread("E:/NLP/wumii/15.jpeg")
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
    
    #读取图片数据
    pkl_file = open('E:/NLP/wumii/TrainFile/trainData/wumiiData.pkl', 'rb')
    modelDict = pickle.load(pkl_file)
    pkl_file.close()
    
    train = modelDict['data'].astype(np.float32)
    train_labelstr = modelDict['label']
    train_labels = np.arange(len(train_labelstr))
    
    print train.dtype
    
    modelKNN = rwl.getKnnModel(train, train_labels)
    
    #pip2 install pyocr
    from PIL import Image
    from pyocr import pyocr
     
    tools = pyocr.get_available_tools()[:]
#     print("Using '%s'" % (tools[0].get_name()))
#     for ij in xyMatrixNew:
#         imgPath = "D:/ProgramFilesOffice/Python/Python27/QQ_%s_%s.png"%(ij[0],ij[1])
#         print '-----%s,%s-----'%(ij[0],ij[1])
#         print tools[0].image_to_string(Image.open(imgPath),lang='chi_sim')
    
    #图片块
    for tmp1 in wordListOfLine:
        #文本块
        for tmp2 in tmp1:
            #文本行
            for tmp3 in tmp2:
                #文字
                if isinstance(tmp3, list):
                    for tmp4 in tmp3:
                        #print tools[0].image_to_string(Image.fromarray(tmp4),lang='chi_sim'),'-',
                        print rwl.getRecongnitionWord(tmp4, modelKNN, train_labelstr),' ',
                    print '\n'
                elif isinstance(tmp3, np.ndarray):
                    #print tools[0].image_to_string(Image.fromarray(tmp4),lang='chi_sim'),' ',
                    print rwl.getRecongnitionWord(tmp3, modelKNN, train_labelstr),' ',
                else:
                    pass
            print '\n'
    
    print 'run is over!'
    
    