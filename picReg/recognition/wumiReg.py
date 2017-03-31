#-*- coding:utf-8 -*-
'''
Created on 2017年1月3日

@author: song

'''
from pytesser import *
from PIL import Image
im = Image.open('D:/wumiz.png')
text = image_to_string(im)
print "识别结果为: "
print text.decode("utf8")