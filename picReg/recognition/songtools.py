#-*- coding:utf-8 -*-
'''
Created on 2016年12月29日

@author: song

'''
import pickle
from PIL import Image
from numpy import *
from collections import Counter
import cv2

class songtools(object):
    '''个人常用工具函数'''
    print __doc__
    def storeData(self,datapath,data):
        """将pkl格式的数据存储到本地"""
        with open(datapath, "wb") as f:
            pickle.dump(data, f)
        f.close() 

    def readdata(self,datapath):
        '''读取pkl格式的数据'''
        with open(datapath,'r') as f:
            data1=pickle.load(f)
        f.close()   
        return data1     
    def rankFreq(self,wordlist):
        '''数据列表，按频率排列'''
        di=Counter(wordlist)    
        fdist1=sorted(di.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        return fdist1

    def transforImg(self,img, xyQuadrangle):
        '''
        xyQuadrangle顺序：右上，左上，左下，右下
        调整图片
        '''
        # xyQuadrangle=np.array(xyQuadrangle,np.float32)
        if len(xyQuadrangle) == 4:
            x = []
            y = []
            for i in xyQuadrangle:
                x.append(i[0])
                y.append(i[1])
            targetMapx = int((max(x) - min(x)) * 1.2)
            targetMapy = int((max(y) - min(x)) * 1.2)
            targetMap = np.array([[targetMapx, 0], [0, 0], [0, targetMapy], [targetMapx, targetMapy]], np.float32)
            pers = cv2.getPerspectiveTransform(xyQuadrangle, targetMap);
            warp = cv2.warpPerspective(img, pers, (targetMapx, targetMapy));
            return warp
        else:
            print '无法确定目标框，请检查！'