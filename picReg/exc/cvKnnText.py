#-*- coding:utf-8 -*-
# import cv2
# import os
# import struct
# import numpy as np
# from matplotlib import pyplot as plt
# cells = []
# for i in range(15):
#     imgPath = 'E:/NLP/QDFile/subImage/QQ_%s.png'%(i)
#     img = cv2.imread(imgPath)
#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     m,n = gray.shape
#     if m < 14:
#         gray = np.row_stack((gray,np.array([0]*n*(14-m)).reshape(14-m, n)))
#         m = 14
#     if n < 14:
#         gray = np.column_stack((gray,np.array([0]*m*(14-n)).reshape(m, 14-n)))
#         n = 14
#     cells.append(list(gray.reshape(1,-1)))
#     print gray.shape
#     print gray
#     #cells.append(gray)
# 
# print gray.reshape(1,-1).shape
# x = np.array(cells)
# print x.shape
# train = x[:8,:].reshape(-1,196).astype(np.float32) # Size = (2500,400)
# test = x[8:,:].reshape(-1,196).astype(np.float32) # Size = (2500,400)
# dd = ['出','收','收','收','收','收','出','收','收','出','收','收','收','收','收']
# dd = [0,1,1,1,1,1,0,1,1,0,1,1,1,1,1]
# train_labels = np.array(dd)[:8][:,np.newaxis]
# test_labels = np.array(dd)[8:][:,np.newaxis]
# print train_labels
# print train.shape
# 
# print cells
 
import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread('D:/picreg/image/digits.png') 
##开发窗口
cv2.namedWindow("Image")
##展示图片   
cv2.imshow("Image", img)   
cv2.waitKey (0)
##释放窗口  
cv2.destroyAllWindows()
##转灰度 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
# Now we split the image to 5000 cells, each 20x20 size
##先行等分再列等分，划分为5000个单元

cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

print '单元数量：',len(cells)
print '单元列长度：',len(cells[0])
# Make it into a Numpy array. It size will be (50,100,20,20)
x = np.array(cells)
print x.shape
# print x[:,:50].shape
#Now we prepare train_data and test_data.
train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)
print '训练集形状：',train.shape
print train
#Create labels for train and test data
k = np.arange(10)
# print k
train_labels = np.repeat(k,250)[:,np.newaxis]
print train_labels
# print np.repeat(k,250)
test_labels = train_labels.copy()

# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
ret, results, neighbours ,dist = knn.findNearest(test, 1)
print "result: ", results,"\n"
# print "neighbours: ", neighbours,"\n"
# print "distance: ", dist
# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
# print test_labels
# print results
matches = results==test_labels
correct = np.count_nonzero(matches)
accuracy = correct * 100.0/results.size
print accuracy