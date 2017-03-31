#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
from PIL import Image
from pylab import *
# import pca
from numpy import *
from scipy.ndimage import filters
im1 = array(Image.open('wumi.png').convert('L'))
im3=filters.gaussian_filter(im1,5)
im4 = filters.gaussian_filter(im1,10)
im2=filters.gaussian_filter(im1,3)
Imgdata=[im1,im2,im3,im4]
figure()
gray()
for i in range(1,5):
    subplot(2, 2, i)
    imshow(Imgdata[i-1])
    axis('off')
show()
