# -*- coding: utf-8 -*-
'''
Created on 2016年12月15日

@author: song
'''
  
import cv2  
import numpy as np  
from matplotlib import pyplot as plt  

##demo
original_picpath='D:/picreg/72.png'  
template_picpath='D:/picreg/72-1.jpg'


# original_picpath='D:/picreg/73.png'  
# template_picpath='D:/picreg/73-2.jpg' 
img = cv2.imread(original_picpath,0)  
img2 = img.copy()  
template = cv2.imread(template_picpath,0)  
w,h = template.shape[::-1]  
 
# 6 中匹配效果对比算法  
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',  
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']  
  
for meth in methods:  
    img = img2.copy()  
  
    method = eval(meth)  
  
    res = cv2.matchTemplate(img,template,method)  
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  
  
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:  
        top_left = min_loc  
    else:  
        top_left = max_loc  
    bottom_right = (top_left[0] + w, top_left[1] + h)  
  
    cv2.rectangle(img,top_left, bottom_right, 255, 2)  
  
    print meth  
    plt.subplot(221), plt.imshow(img2,cmap= "gray")  
    plt.title('Original Image'), plt.xticks([]),plt.yticks([])  
    plt.subplot(222), plt.imshow(template,cmap= "gray")  
    plt.title('template Image'),plt.xticks([]),plt.yticks([])  
    plt.subplot(223), plt.imshow(res,cmap= "gray")  
    plt.title('Matching Result'), plt.xticks([]),plt.yticks([])  
    plt.subplot(224), plt.imshow(img,cmap= "gray")  
    plt.title('Detected Point'),plt.xticks([]),plt.yticks([])  
    plt.show()  