# -*- coding: utf-8 -*-
'''
@Time : 2017/1/12 11:42

@author: song
'''

from PIL import Image
from matplotlib import *
from pylab import *
path1='C:/Users/John64pc/Desktop/work/1.jpg'
aa=Image.open(path1)
figure()
imshow(aa)
show()