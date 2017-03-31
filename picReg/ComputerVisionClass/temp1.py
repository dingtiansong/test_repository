#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
import cv2
from pylab import *
from scipy import ndimage
from PCV.geometry import homography

##
imgpath = 'D:/picreg/photoreg/data/trans2.jpg'
cim = cv2.imread(imgpath)
im = array(cv2.cvtColor(cim, cv2.COLOR_BGR2GRAY))

# 边框坐标：左上角、右上角、右下角、左下角
xyQuadrangle = [
    (45.886554621848745,
     105.04621848739521),
    (926.55882352941182,
     189.07983193277346),
    (805.55042016806726,
     898.32352941176487),
    (32.441176470588289,
     804.20588235294133)]


def mapingMatrix(xyQuadrangle):
    x1 = []
    for i in xyQuadrangle:
        x1.append(i[0])
    high = int((max(x1) - min(x1)) * 1.2)
    fp = array([array([p[1], p[0], 1]) for p in xyQuadrangle]).T
    tp = array([[0, 0, 1], [0, high, 1], [high, high, 1], [high, 0, 1]]).T
    H = homography.H_from_points(tp, fp)
    return high, H

high, H = mapingMatrix(xyQuadrangle)

fp = array([array([p[1], p[0], 1]) for p in xyQuadrangle]).T
tp = array([[0, 0, 1], [0, high, 1], [high, high, 1], [high, 0, 1]]).T
# pers = cv2.getPerspectiveTransform(tp, fp);
# remap the image
warp = cv2.warpPerspective(cim, H, (high, high))
warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

# show image
cv2.imshow("contours", warp_gray)
cv2.waitKey()
cv2.destroyAllWindows()


# def warpfcn(x):
#     x = array([x[0],x[1],1])
#     xt = dot(H,x)
#     xt = xt/xt[2]
#     return xt[0],xt[1]
# im_g = ndimage.geometric_transform(im,warpfcn,(high,high))
# cv2.imwrite('tableSample4.png', im_g)


############show the picture#######################
# figure()
# gray()
# subplot(1,2,1)
# imshow(im)
# axis('off')
# subplot(1,2,2)
# imshow(im_g)
# axis('off')
# show()
