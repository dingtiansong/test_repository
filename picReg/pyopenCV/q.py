#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
from PIL import Image
from pylab import *
import numpy as np  
import matplotlib.pyplot as plt  
import cv2
#读取图片
img = cv2.imread("D:/imagedata/subImage2/QD2.jpg") 
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#转灰度
gray1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
print gray1.shape
# print gray1[0]

show()
# 新建一个图像
print gray1.shape
y,x=gray1.shape
z=[]
point1=[]
for i in range(x):
#     print i
    z.append((y-gray1[:,i].sum()/255-30))
    if gray1[:,i].sum()/255==y:
        point1.append(i)
aa=[]
for i in range(1,len(point1)):
    zz=point1[i]-point1[i-1]
    if zz>1:
#         print zz
        aa.append(zz)
print aa  ,len(aa)     
# plt.figure(1)#创建图表1  
plt.figure(2)#创建图表2     
# 不使用颜色信息
gray()
# 在原点的左上角显示轮廓图像
contour(gray1, origin='image')
axis('equal')
# axis('off')
# for i in im:
#     print i
plot([-30]*(x+30),'r')
plot(z,'g')
plot(12,'r')
plt.xlim(0,x) 
plt.ylim(0,y) 
show()
#二值化
ret, thresh = cv2.threshold(gray1 , 127, 255, cv2.THRESH_BINARY)
print ret,thresh
cv2.imshow('image',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
