# -*- coding: utf-8 -*-
'''
Created on 2016年12月15日

@author: song
'''

datapath='D:/data/WMsentence.txt'
with open(datapath) as f:
    data1=f.readlines()
listsentence=''
z=0
for i in data1:
#     z+=1
    listsentence=listsentence+i
#     print z,i
print len(data1)
# print listsentence
za=listsentence.split('###')
for i in za:
    z+=1
    print z,i
print za[2]
# with open(r'D:/zz.txt','w') as dz:
#     dz.writelines(za)

# with open(r'D:/zz.txt','r') as dz:
#     zzz=dz.readlines()
# for i in zzz:
#     z+=1
#     print z,i    