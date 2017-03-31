# -*- coding: utf-8 -*-
'''
Created on 2016年12月19日

@author: song
'''
import cPickle as pickle
# path1='D:/picreg/trainData/trainImage.txt'
# savepath1='D:/picreg/trainData/dataMatrix.pkl'
# savepath2='D:/picreg/trainData/wordlist.pkl'
# savepath3='D:/picreg/trainData/list2.pkl'
savepath4='D:/picreg/trainData/list3.pkl'
path2='D:/picreg/trainData/textImage.txt'
with open(path2) as f:
    data1=f.readlines()

datalist=[]
for i in data1:
    xx= i.split('{S}')
    datalist.append(xx)
# print  datalist
wordlist=[]
for i in datalist:
    if i[0] not in wordlist:
        wordlist.append(i[0])

print '总词数：',len(datalist)
samelist=[]

for i in wordlist:
    ss=[i]
    for j in datalist:
        if i == j[0]:
            ss.append(j[1])
    if ss not in samelist:
        samelist.append(ss)
# for i in  samelist:
#     if len(i)>2:
#         print i[0],i[1:]
# with open('D:/picreg/trainData/rightword1.txt','w') as f:
#     f.writeline(samelist)
# f.close()
print '去重词数：',len(samelist)
print '重复字数：' ,len(datalist)-len(samelist)
with open(savepath4) as f:
    data11=pickle.load(f)
# ##查看
regnum=0
print data11
for i in data11:
    regnum+=len(i)
print regnum 
print len(data11) 
print '消除重复数：%s,消除比例为：%s'%(regnum-len(data11),(regnum-len(data11))/float(len(datalist)-len(samelist)))


        
        
        

    