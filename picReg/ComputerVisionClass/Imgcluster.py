# -*- coding: utf-8 -*-
'''
@Time : 2017/1/10 16:05

@author: song
'''
import imtools
import pickle
from numpy import *
from PIL import Image
import pcv
from scipy.cluster.vq import *
# 获取 selected-fontimages 文件下图像文件名，并保存在列表中
imlist = imtools.get_imlist('D:/picreg/trainData/image/')
imnbr = len(imlist)

# 载入模型文件
# with open('a_pca_modes.pkl','rb') as f:
#     immean = pickle.load(f)
#     V = pickle.load(f)
# 创建矩阵，存储所有拉成一组形式后的图像
immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')
V,S,immean = pca.pca(immatrix)
# 投影到前 40 个主成分上
immean = immean.flatten()