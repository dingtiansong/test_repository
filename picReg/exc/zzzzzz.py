# -*- coding: utf-8 -*-
'''
Created on 2016年12月9日

@author: song

'''
import pickle
import cPickle as pickle
path='D:/data/offlinePredictData.plk'
path1='D:/data/WMDMData.plk'
path2='D:/data/DTWM.plk'
# with open(path) as f:
#     data11=pickle.load(f)
# z=0   
# xx=10 
# for i in data11[xx]:
#     z+=1
#     print z,i

# with open(path2) as f:
#     data12=pickle.load(f)
# dict1=[]
# for i in data12: 
#     for j in i :
#         if j['P'] not in dict1:
#             dict1.append(j['P'])
# #         print j
#         
# for i in dict1 :
#     print i
    
Ddict={'出':['发行','出','融出',],'收':['融入','借','存入']}
offlinePdict={'协议存款':['协议存款','协存'],'银行同存':['银行同存','同存','同业存款'],'非银同存':['非银存款'],'资金':['线下资金','线上资金','资金']}
WMPdict={'保本':['保本','保本理财','理财'],'非保本':['非保本理财','非保','非保本','理财']}
with open(path2) as f:
    data12=pickle.load(f)
    
# for i in data12:
# #     print i
#     print data12[i]
zz='\xb0\xeb\xc4\xea'.decode('gbk').encode('utf-8')
print [zz]

