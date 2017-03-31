#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
import cv2
import numpy as np

tilt = np.pi * 35 / 180

a = np.zeros((3, 3))

a[0][0] = 1
a[1][1] = np.sin(tilt)
a[1][2] = -np.sin(tilt)
a[2][2] = np.cos(tilt)
a[2][2] = np.cos(tilt)
imgpath='D:/picreg/photoreg/data/Ga.jpg'
src = cv2.imread(imgpath)
width, height, depth = src.shape

output = cv2.warpPerspective(src, a, (width, height))
savepath='D:/picreg/photoreg/data/results.png'
cv2.imwrite(savepath, output)

