# -*- coding: utf-8 -*-
'''
Created on 2016年10月24日

@author: song
'''

import pickle
fd = u'E:/work/infoEx/preprocessed_sentences.pickle'
with open(fd, 'rb') as f:
    allData = pickle.load(f)
f.close()
print allData[1]
for i in allData.keys():
    print i