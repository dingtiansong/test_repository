# -*- coding: utf-8 -*-
'''
@Time : 2017/4/5 13:40

@author: song
'''
'''
检查数据标注位置是否正确
'''
import pickle

path = 'D:\\work\\tags\\data\\learning_quote_origin_element2.pkl'
newdatapath2 = 'D:\\work\\tags\\data\\newdata2.pkl'
newdatapath3 = 'D:\\work\\tags\\data\\newdata3.pkl'
with open(path, 'rb') as f:
    data1=[]
    info = pickle.load(f)
k = 0
for i in range(len(info)):
    tmp = info[i]
    keyword = tmp[1]
    original = tmp[2]
    beginIndex = tmp[4] - 13
    endIndex = tmp[5] - 13
    print type(original), len(original)
    if original[beginIndex:endIndex] == keyword:
        data1.append(info[i])
        k = k + 1
    else:
        print '--------'
        print original
        print original[beginIndex:endIndex]
        print keyword
        print i, tmp[4], tmp[5]
        print '-------'
    print k, len(info)
newdata=[]
for i in range(len(data1)):
    if i!=88:
        print i
        newdata.append(data1[i])
    # f1 = file(newdatapath3, 'wb')
    # pickle.dump(newdata, f1, True)


print '----'
for i in newdata[2]:
    print i
