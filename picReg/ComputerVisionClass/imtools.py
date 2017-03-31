# -*- coding: utf-8 -*-
'''
Created on 2017年1月6日

@author: song
'''
import os 
from PIL import Image
from numpy import *


def get_imlist(path):
    
    """ 返回目录中所有 JPG 图像的文件名列表 """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.png')]

def imresize(im,sz):
    """ 使用 PIL 对象重新定义图像数组的大小 """
    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))

def histeq(im,nbr_bins=256):
    """ 对一幅灰度图像进行直方图均衡化 """
    # 计算图像的直方图
    imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # 归一化
    # 使用累积分布函数的线性插值，计算新的像素值
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape), cdf

def compute_average(imlist):
    """ 计算图像列表的平均图像 """
    # 打开第一幅图像，将其存储在浮点型数组中
    averageim = array(Image.open(imlist[0]), 'f')
    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print imname + '...skipped'
    averageim /= len(imlist)
    # 返回 uint8 类型的平均图像
    return array(averageim, 'uint8')

def pca(X):
    """ 主成分分析：
    输入：矩阵 X，其中该矩阵中存储训练数据，每一行为一条训练数据
    返回：投影矩阵（按照维度的重要性排序）、方差和均值 """
    # 获取维数
    num_data,dim = X.shape
    # 数据中心化
    mean_X = X.mean(axis=0)
    X = X - mean_X
    if dim>num_data:
        # PCA- 使用紧致技巧
        M = dot(X,X.T) # 协方差矩阵
        e,EV = linalg.eigh(M) # 特征值和特征向量
        tmp = dot(X.T,EV).T # 这就是紧致技巧
        V = tmp[::-1] # 由于最后的特征向量是我们所需要的，所以需要将其逆转
        S = sqrt(e)[::-1] # 由于特征值是按照递增顺序排列的，所以需要将其逆转
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA- 使用 SVD 方法
        U,S,V = linalg.svd(X)
        V = V[:num_data] # 仅仅返回前 nun_data 维的数据才合理
        # 返回投影矩阵、方差和均值
    return V,S,mean_X