# -*- coding:utf-8 -*-
'''
@author = Administrator
'''
#import Opencv library
import cv2
from pylab import *
#load image
image_sudoku_original = cv2.imread('trans2.jpg')
#gray image
image_sudoku_gray = cv2.cvtColor(image_sudoku_original,cv2.COLOR_BGR2GRAY)
# adaptive threshold
thresh = cv2.adaptiveThreshold(image_sudoku_gray,255,1,1,11,15)
# show image
cv2.imshow("contours", thresh)
cv2.waitKey()
cv2.destroyAllWindows()

# find the countours
image, contours0, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# size of the image (height, width)
h, w = image_sudoku_original.shape[:2]

# copy the original image to show the posible candidate
image_sudoku_candidates = image_sudoku_original.copy()
cv2.imshow('candidate',image_sudoku_original)
cv2.waitKey()
cv2.destroyAllWindows()
# biggest rectangle
size_rectangle_max = 0;
for i in range(len(contours0)):
    # aproximate countours to polygons
    approximation = cv2.approxPolyDP(contours0[i], 4, True)

    # has the polygon 4 sides?
    if (not (len(approximation) == 4)):
        continue;
    # is the polygon convex ?
    if (not cv2.isContourConvex(approximation)):
        continue;
        # area of the polygon
    size_rectangle = cv2.contourArea(approximation)
    # store the biggest
    if size_rectangle > size_rectangle_max:
        size_rectangle_max = size_rectangle
        big_rectangle = approximation
print 'big_rectangle:',big_rectangle,approximation[(i % 4)][0][0]
# show the best candidate
approximation = big_rectangle
for i in range(len(approximation)):
    cv2.line(image_sudoku_candidates, (approximation[(i % 4)][0][0], approximation[(i % 4)][0][1]),
             (approximation[((i + 1) % 4)][0][0], approximation[((i + 1) % 4)][0][1]), (255, 0, 0), 2)
# show image
cv2.imshow("contours", image_sudoku_candidates)
cv2.waitKey()
cv2.destroyAllWindows()

import numpy as np
from numpy import *

def f(zz,j):
    x=[]
    for i in zz:
        x.append(i[j])
    return x






zzz=[(46.873004354136356, 106.55370101596532), (924.66690856313494, 190.15312046444137), (808.55660377358481, 905.39259796806971), (23.650943396226467, 803.21552975326563)]
x=[zzz[1],zzz[0],zzz[3],zzz[2]]
# fp = array([array([p[1],p[0],1]) for p in x])
# x=[(926, 189),(45, 105), (32, 804),(805, 898)]
# 左上角、右上角、右下角、左下角
fp = np.array([array([p[0],p[1]]) for p in x],np.float32)
print 'points2:',fp
tp = np.array([[900,0],[0,0],[0,900],[900,900]],np.float32)

# Transformation matrix
print 'points1:',tp
pers = cv2.getPerspectiveTransform(fp, tp);
print pers
# remap the image
figure()
imshow(image_sudoku_original)
zz=[(46.873004354136356, 106.55370101596532), (924.66690856313494, 190.15312046444137), (808.55660377358481, 905.39259796806971), (23.650943396226467, 803.21552975326563)]

x1=f(zz,0)
y1=f(zz,1)
plot(x1,y1,'r*')
# 添加标题，显示绘制的图像
title('Plotting: "empire.jpg"')
gray()
show()
warp = cv2.warpPerspective(image_sudoku_original, pers, (900, 900));
warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

# show image
cv2.imshow("contours", warp_gray)
cv2.waitKey()
cv2.destroyAllWindows()




#
# import math
# import numpy as np
#
# # sudoku representation
# sudoku = np.zeros(shape=(9 * 9, IMAGE_WIDHT * IMAGE_HEIGHT))
#
#
# def Recognize_number(x, y):
#     """
#     Recognize the number in the rectangle
#     """
#     # square -> position x-y
#     im_number = warp_gray[x * IMAGE_HEIGHT:(x + 1) * IMAGE_HEIGHT][:, y * IMAGE_WIDHT:(y + 1) * IMAGE_WIDHT]
#
#     # threshold
#     im_number_thresh = cv2.adaptiveThreshold(im_number, 255, 1, 1, 15, 9)
#     # delete active pixel in a radius (from center)
#     for i in range(im_number.shape[0]):
#         for j in range(im_number.shape[1]):
#             dist_center = math.sqrt((IMAGE_WIDHT / 2 - i) ** 2 + (IMAGE_HEIGHT / 2 - j) ** 2);
#             if dist_center > 6:
#                 im_number_thresh[i, j] = 0;
#
#     n_active_pixels = cv2.countNonZero(im_number_thresh)
#
#     if n_active_pixels > N_MIN_ACTVE_PIXELS:
#         image, contour, hierarchy = cv2.findContours(im_number_thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#
#         biggest_bound_rect = [];
#         bound_rect_max_size = 0;
#         for i in range(len(contour)):
#             bound_rect = cv2.boundingRect(contour[i])
#             size_bound_rect = bound_rect[2] * bound_rect[3]
#             if size_bound_rect > bound_rect_max_size:
#                 bound_rect_max_size = size_bound_rect
#                 biggest_bound_rect = bound_rect
#
#         x_b, y_b, w, h = biggest_bound_rect;
#         x_b = x_b - 1;
#         y_b = y_b - 1;
#         w = w + 2;
#         h = h + 2;
#
#         im_t = cv2.adaptiveThreshold(im_number, 255, 1, 1, 15, 9);
#         number = im_t[y_b:y_b + h, x_b:x_b + w]
#
#         if number.shape[0] * number.shape[1] > 0:
#             number = cv2.resize(number, (IMAGE_WIDHT, IMAGE_HEIGHT), interpolation=cv2.INTER_LINEAR)
#             ret, number2 = cv2.threshold(number, 127, 255, 0)
#
#             number = number2.reshape(1, IMAGE_WIDHT * IMAGE_HEIGHT)
#             sudoku[x * 9 + y, :] = number;
#
#         else:
#             sudoku[x * 9 + y, :] = np.zeros(shape=(1, IMAGE_WIDHT * IMAGE_HEIGHT));
#
#
# for i in range(SUDOKU_SIZE):
#     for j in range(SUDOKU_SIZE):
#         Recognize_number(i, j);
#
# cv2.imwrite("number.jpg",cv2.resize(sudoku[2, :].reshape(IMAGE_WIDHT, IMAGE_HEIGHT), (IMAGE_WIDHT * 5, IMAGE_HEIGHT * 5)));
# #show image
# imgNum = cv2.imread('number.jpg')
# cv2.imshow("contours", imgNum)
# cv2.waitKey()
# cv2.destroyAllWindows()
