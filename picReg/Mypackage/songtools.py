#-*- coding:utf-8 -*-
'''
Created on 2016年12月29日

@author: song

'''
import pickle
from collections import Counter

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
    def imresize(self,im,sz):
        """ 使用 PIL 对象重新定义图像数组的大小 """
        pil_im = Image.fromarray(uint8(im))
        return array(pil_im.resize(sz))
    
    def histeq(self,im,nbr_bins=256):
        """ 对一幅灰度图像进行直方图均衡化 """
        # 计算图像的直方图
        imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
        cdf = imhist.cumsum() # cumulative distribution function
        cdf = 255 * cdf / cdf[-1] # 归一化
        # 使用累积分布函数的线性插值，计算新的像素值
        im2 = interp(im.flatten(),bins[:-1],cdf)
        return im2.reshape(im.shape), cdf