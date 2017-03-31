#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
# If you have PCV installed, these imports should work
from PCV.geometry import homography, warp
from PCV.localdescriptors import sift
from scipy import ndimage
from PIL import Image
from pylab import *
import cv2
imgpath='D:/picreg/photoreg/data/trans2.jpg'
# im = array(Image.open(imgpath).convert('L'))
im=array(cv2.cvtColor(cv2.imread(imgpath),cv2.COLOR_BGR2GRAY))
# im = array(Image.open(imgpath))
# 标记角点
def f(zz,j):
    x=[]
    for i in zz:
        x.append(i[j])
    return x
figure()
imshow(im)
zz=[(46.873004354136356, 106.55370101596532), (924.66690856313494, 190.15312046444137), (808.55660377358481, 905.39259796806971), (23.650943396226467, 803.21552975326563)]
x=f(zz,0)
y=f(zz,1)
plot(x,y,'r*')
# 添加标题，显示绘制的图像
title('Plotting: "empire.jpg"')
gray()
show()

x = ginput(4)
print x
# x=[(45.886554621848745, 105.04621848739521), (926.55882352941182, 189.07983193277346), (805.55042016806726, 898.32352941176487), (32.441176470588289, 804.20588235294133)]
# 左上角、右上角、右下角、左下角
fp = array([array([p[1],p[0],1]) for p in x]).T
tp = array([[0,0,1],[0,1000,1],[1000,1000,1],[1000,0,1]]).T
# # 估算单应矩阵
H = homography.H_from_points(tp,fp)
# print tp,fp
# print H
# 辅助函数，用于进行几何变换
def warpfcn(x):
    x = array([x[0],x[1],1])
    xt = dot(H,x)
    xt = xt/xt[2]
    # print xt
    return xt[0],xt[1]
# print
# # 用全透视变换对图像进行变换
im_g = ndimage.geometric_transform(im,warpfcn,(1000,1000))
print im_g.shape
savepath='D:/picreg/photoreg/data/results2.png'

figure()
gray()
subplot(1,2,1)
imshow(im)
axis('off')
subplot(1,2,2)
imshow(im_g)
axis('off')
show()
# cv2.imwrite(savepath,im_g)
# cv2.namedWindow("Image")
# cv2.imshow("Image", im_g)
# cv2.waitKey (0)
# cv2.destroyAllWindows()

# xyQuadrangle=[(45.886554621848745, 105.04621848739521), (926.55882352941182, 189.07983193277346), (805.55042016806726, 898.32352941176487), (32.441176470588289, 804.20588235294133)]
# img=array(cv2.cvtColor(cv2.imread(imgpath),cv2.COLOR_BGR2GRAY))
# def warpfcn(x,H):
#     x = array([x[0],x[1],1])
#     xt = dot(H,x)
#     xt = xt/xt[2]
#     print xt
#     return xt[0],xt[1]

# def adjustImg(img,xyQuadrangle,warpfcn):
#
#     fp = array([array([p[1], p[0], 1]) for p in xyQuadrangle]).T
#     tp = array([[0, 0, 1], [0, 500, 1], [500, 500, 1], [500, 0, 1]]).T
#     H = homography.H_from_points(tp, fp)
#     im_g = ndimage.geometric_transform(img, warpfcn(xyQuadrangle,H), (500, 500))
#     return im_g
# img2=adjustImg(img,xyQuadrangle,warpfcn)
# cv2.imwrite('tableSample4.png', img2)