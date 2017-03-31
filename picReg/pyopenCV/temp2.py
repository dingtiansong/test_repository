#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''

import cv2
from numpy import *
from PIL import Image
from pylab import *
# load image
image_sudoku_original = cv2.imread('trans2.jpg')
# gray image
image_sudoku_candidates = image_sudoku_original.copy()
image_sudoku_gray = cv2.cvtColor(image_sudoku_original, cv2.COLOR_BGR2GRAY)
zzz = [[[46, 106]], [[924, 190]], [[808, 905]], [[23, 803]]]
zzz1 = [
    (46.873004354136356,
     106.55370101596532),
    (924.66690856313494,
     190.15312046444137),
    (808.55660377358481,
     905.39259796806971),
    (23.650943396226467,
     803.21552975326563)]
x = [zzz1[1], zzz1[0], zzz1[3], zzz1[2]]
xz = [zzz[1], zzz[0], zzz[3], zzz[2]]
approximation = xz
for i in range(len(approximation)):
    cv2.line(
        image_sudoku_candidates, (approximation[
            (i %
             4)][0][0], approximation[
            (i %
             4)][0][1]), (approximation[
                 ((i + 1) %
                  4)][0][0], approximation[
                 ((i + 1) %
                     4)][0][1]), (255, 0, 0), 2)
# cv2.imshow("contours", image_sudoku_candidates)
#
# cv2.waitKey()
# cv2.destroyAllWindows()
figure()
imshow(image_sudoku_candidates)
show()
# 左上角、右上角、右下角、左下角
fp = np.array([array([p[0], p[1]]) for p in x], np.float32)
print 'points2:', fp
tp = np.array([[900, 0], [0, 0], [0, 900], [900, 900]], np.float32)
ind = [0, 3, 1, 2]
fp1 = fp[ind]
tp1 = tp[ind]

print fp1, tp1

# Transformation matrix


pers = cv2.getPerspectiveTransform(fp1, tp1)
# remap the image
# figure()
# imshow(image_sudoku_original)
warp = cv2.warpPerspective(image_sudoku_original, pers, (900, 900))
warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

# show image
figure()
imshow(warp)
title('Adjust Picture')
axis('off')
show()


def transforImg(img, xyQuadrangle):
    '''xyQuadrangle顺序：右上，左上，左下，右下'''
    # xyQuadrangle=np.array(xyQuadrangle,np.float32)
    if len(xyQuadrangle) == 4:
        x = []
        y = []
        for i in xyQuadrangle:
            x.append(i[0])
            y.append(i[1])
        targetMapx = int((max(x) - min(x)) * 1.2)
        targetMapy = int((max(y) - min(x)) * 1.2)
        targetMap = np.array([[targetMapx, 0], [0, 0], [0, targetMapy], [
                             targetMapx, targetMapy]], np.float32)
        pers = cv2.getPerspectiveTransform(xyQuadrangle, targetMap)
        warp = cv2.warpPerspective(img, pers, (targetMapx, targetMapy))
        return warp
    else:
        print '无法确定目标框，请检查！'
#     # return warp
#
xx = transforImg(image_sudoku_original, fp)
figure()
subplot(1, 2, 1)
imshow(image_sudoku_candidates)
title('candidate Piceture')
axis('off')
subplot(1, 2, 2)
imshow(xx)
title('Adjust Picture<su>')
axis('off')
show()
