#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
# import numpy as np
# from numpy import *
# import cv2
#
# x=[(45, 105), (926, 189), (805, 898), (32, 804)]
# # 左上角、右上角、右下角、左下角
# fp = np.array([array([p[1],p[0],1]) for p in x],np.float32).T
# tp = np.array([[0,0,1],[0,1000,1],[1000,1000,1],[1000,0,1]],np.float32).T
# # Transformation matrix
# pers = cv2.getPerspectiveTransform(tp, fp);
# print pers

import cv2
import numpy as np

img = cv2.imread('1original.jpg',0)
image_sudoku_original = cv2.imread('trans2.jpg')
src = np.array([[50,50],[450,450],[70,420],[420,70]],np.float32)
dst = np.array([[0,0],[299,299],[0,299],[299,0]],np.float32)

ret = cv2.getPerspectiveTransform(src,dst)
print ret

warp = cv2.warpPerspective(image_sudoku_original, ret, (299, 299));
warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)