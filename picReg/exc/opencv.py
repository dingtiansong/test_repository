# -*- coding: utf-8 -*-
'''
Created on 2016年11月22日

@author: song

'''
import cv2
import numpy as np
eimgpath='D:/picreg/image/cat.png' 
img = cv2.imread(eimgpath)  
cv2.namedWindow("Image") 
cv2.imshow("Image", img)
cv2.waitKey (0) 
cv2.destroyAllWindows()

emptyImage = np.zeros(img.shape, np.uint8)  
##设置图片保存质量
cv2.imwrite("D:/picreg/image/cat2.jpg", img,[int(cv2.IMWRITE_JPEG_QUALITY), 5])
cv2.imwrite("D:/picreg/image/cat5.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) 
###设置图片保存压缩级别
cv2.imwrite("D:/picreg/image/cat4.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])   
cv2.imwrite("D:/picreg/image/cat3.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 1]) 

