#-*- coding:utf-8 -*-
'''
Created on 2017年1月4日

@author: song
'''
from PIL import Image
from pylab import *

# 读取图像到数组中
ImagePath='D:/imagedata/wumi.jpg'
# img1=Image.open(ImagePath)
# img1.show()
# im = array(Image.open(ImagePath))
# # 绘制图像
# imshow(im)
# # 一些点
# x = [100,100,400,400]
# y = [200,500,200,500]
# # 使用红色星状标记绘制点
# plot(x,y,'r*')
# # 绘制连接前两个点的线
# plot(x[:2],y[:2])
# # 添加标题，显示绘制的图像
# title('Plotting: "test.jpg"')
# show()

im = array(Image.open(ImagePath).convert('L'))
show()
# 新建一个图像
print im.shape
y,x=im.shape
z=[]
point1=[]
for i in range(x):
#     print i
    z.append((61-im[:,i].sum()/255-30)*1.5)
    if im[:,i].sum()/255==y:
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
contour(im, origin='image')
axis('equal')
# axis('off')
# for i in im:
#     print i
plot([-30]*(x+30),'r')
plot(z,'g')
plot(12,'r')
plt.xlim(0,x) 
plt.ylim(5,100) 
show()