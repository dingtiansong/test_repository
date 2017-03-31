#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
from PCV.geometry import homography, warp
from PCV.localdescriptors import sift
from scipy import ndimage
from PIL import Image
from pylab import *

# 仿射扭曲 im1 到 im2 的例子
im1 = array(Image.open('testflower.jpg').convert('L'))
im2 = array(Image.open('testwall.jpg').convert('L'))
# 选定一些目标点

figure()
imshow(im2)
gray()
y = ginput(4)
# 左上角、右上角、右下角、左下角
tp = array([array([p[1],p[0],1]) for p in y]).T
im3 = warp.image_in_image(im1,im2,tp)
figure()
gray()
imshow(im3)
axis('equal')
axis('off')
show()