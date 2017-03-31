# -*- coding: utf-8 -*-
'''
Created on 2016年8月24日

@author: john64pc
'''
import numpy as np
from getProductRelation import getProductRelation
from pandas import DataFrame
from matchData2 import dataMatch
import pandas as pd 

# offlinefilePath = 'C:/Users/john64pc/Desktop/offlinedata1031.txt'
# dict_path='C:/Users/john64pc/Desktop/offlinedict.txt'
# onlinefilePath='C:/Users/john64pc/Desktop/onlineText.txt'
# ##处理过之后的数据
# doneofflinedatapath=r'C:/Users/john64pc/Desktop/DMdata/offlineTextcombine1104.txt'
# doneonlinedatapath='C:/Users/john64pc/Desktop/DMdata/onlineTextcombine1104.txt'
# ##储存地址
# sonlinepath='C:/Users/john64pc/Desktop/DMdata/sonlinedata.txt'
# sofflinepath='C:/Users/john64pc/Desktop/DMdata/sofflinedata.txt'
# 
# dd=dataMatch()
# ##处理线下数据
# cldata2 = dd.readText(offlinefilePath)
# dictionary2=dd.creOfflineDict(cldata2)
# sent2=dd.findTransSentence(dictionary2)
# type1='offline'
# nosent2=dd.findNoTransSentence(dictionary2,type1)
# #     dd.printOffline(nosent2,dictionary2)
# ##    储存线下数据
# #     dd.saveOffline(sent2, dictionary2,sofflinepath)
# ##处理线上数据
# clondata=dd.readText(onlinefilePath)  
# dictionary3=dd.creDictOnline(clondata)
# sent3=dd.findTransSentence(dictionary3)
# ##全匹配数据
# type2='online'
# nosent3=dd.findNoTransSentence(dictionary3,type2)
# ##  储存线上数据
# #     dd.saveOnline(sent3, dictionary3, sonlinepath)
# #     dd.printOnline(nosent3,dictionary3) 
# #     dd.printOnline(sent3,dictionary3) 
# 
# #     with open(sonlinepath,'r') as f: 
# #         dddd=f.readlines()
# #     for i in dddd:
# #         print i
# donedata=dd.getdata(doneofflinedatapath)
# allDict=dd.creTotalOfflineDict(donedata)
# dictindex=['sentence','D','P','R','T','A','RE']
# dictoff=pd.Series(allDict,dictindex)
# needtag=['D','P','R','T','A','RE']
# 
# testsentence='民生银行10月31同业资金吸收价格： 隔夜：2.35% 7天：2.80% 14天：2.80% 1月：2.80% 3月：2.95% 6月：3.00% 9月：3.01% 1年： 3.05%'
# testsentence2=' 北京银行收同存今日吸收指导价 7d（类定期）3.05% 14d（类定期）3.05% 4m及以上 3.2%'
# testsentence1='上海银行诚收同业存款 7D 2.9 1M 3.05 2M 3.1 3M 3.1 4M 2.9 6M 2.8 上海银行浦西分行 仇东佳 021-52863602 15021786991'
# testsentence13='今日吸收人民币资金价格 7天 2.63% 14天 2.6% 1个月 2.74% 3个月 2.8% 6个月 2.89% 1年 3.04% '
# testsentence12='今日吸收美元资金价格 7天 0.55% 1个月 0.78% 3个月 1.15% 6个月 1.51% 1年 1.83% '
# testsentence123='今日出金融机构非保理财：3M 3.55% 6M 3.5% 9M 3.6%，12M 3.85%' 
# testsentence14='诚收福费廷业务（一手、二手），国内证，国际证 '
# testsentence15='收票收票，各期限国股银票，有出的请联系'
# dd=dataMatch()
testTagSentence,ooo,dict1=dd.generateTagSentence(dictoff, needtag, testsentence)
# tlist=dd.reverseDict(dict1)
# vlist=''
# print '报价原文：',testsentence
# print '标注序列：',testTagSentence
# for t in tlist:
#     print t
#     vlist+=t+'|'
# print vlist

##training  data
######################################################################################
#online data test 
# sentence=['D1','T1','M1','P1','M2','P2','P3']
# correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
# modeltype='train_modelonline.m'
# factor=['D','P','T','M']


# Offline Data test
sentence=['D1', 'P1', 'T1', 'R1', 'T2', 'R2']
# sentence=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
correct_set=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
modeltype='train_modeloffline.m'
factor=['D','P','T','R']
needfactor=['D','T','R']
maxFactor = 20
numsentence=60
#dict = dictCre(factor,15)
tmp = getProductRelation(factor,maxFactor,sentence,correct_set)
matrixv,product,allp,xl,allcomb,xll=tmp.getProduct(sentence,factor,modeltype)
print matrixv
print product
# m=0
# print '\n'
# for i in  product.values:
#     m+=1
#     zproduct=''
#     for j in i:
#         zproduct+=tlist[testTagSentence.index(j)]+'     '
#     print '这是第%s段报价：'%(m),'\n',zproduct
    
# print matrixv
# print tmp.dictCre(factor, 10)
# print tmp.fvactor('M1','P2',sentence)
# print tmp.value_f2(5, 2, sentence)
#####特征矩阵
# matrixa=tmp.Crexy(factor, numsentence)
# print matrixa
# matrixa.to_csv('E:\matrix.csv')
# print tmp.dataout(sentence, factor, correct_set)
# print tmp.getRightset(correct_set[0], sentence)
# print tmp.allset(correct_set),len(correct_set)
# print tmp.alljudgementset(correct_set, sentence)
# print tmp.getRightset(correct_set,sentence)
# print tmp.dataset(sentence, factor, correct_set)
# print tmp.allset(sentence)
# datamatrix=tmp.Crexy(factor,numsentence)
# print datamatrix
# print product
# print DataFrame(allp)
# # print xl.values[1][:2]
# # print allcomb
# print xl,xll,product
# print ['R3','T4'] in xl.values
# print allp.values()[1][1] in allp.values()[1]
# tmp.getFindResult0(xl.values,['R3','T4'])
# cc=list(xl.values)
# for ccc in xl.values:
#     aaa.ap
# print matrixv
# def getFindResult0(xList, tmp):
#         if [tmp[0], tmp[1]] in xList:
#             return True 
#         elif [tmp[1], tmp[0]] in xList:
#             return True
#         else:
#             return False
#         
# def testComb(xList,comb):
#     if [comb[0],comb[1]] in xList or [comb[1],comb[0]] in xList:
#         return True
#     else:
#         return False
# def testAllComb(xList,allcomb):
#     if (testComb(xList,[allcomb[0],allcomb[3]])
#         and testComb(xList,[allcomb[0],allcomb[3]])
#         and testComb(xList,[allcomb[1],allcomb[2]])
#         and testComb(xList,[allcomb[1],allcomb[3]])):
#         return True
#     else:
#         return False
# print xl
# print product
# print testComb(xl.values, ['D1','D1'])    
# testAllComb(xl,['D1','T1','D1','P1'])        
# print ['D1','T1','D1','P1'][1]
# print getFindResult0(xl.values,[allp.values()[1][2],allp.values()[1][0]])
# def getFindResult(xList, xfind):
#         if (getFindResult0(xList, [xfind[0],xfind[2]]) 
#             and getFindResult0(xList, [xfind[0],xfind[3]])
#             and getFindResult0(xList, [xfind[1],xfind[2]])
#             and getFindResult0(xList, [xfind[1],xfind[3]])):
#             return True
#         else:
#             return False
# print xl.values,len(xl)      
# print getFindResult(xl.values,['D1', 'T3', 'D1', 'T5'])

# for comb in allp.values():
#     if  getFindResult(xl.values,comb):
#         print comb
#          
# m=1
# allcomb={}

# for comb in allp.values():
#     if getFindResult(xl.values, comb):
#             allcomb[m]=comb
#             m=m+1
# print allcomb
# xList=bb[['entity1R','entity2R','relation_est']]
# print xList
# print xList.values[1][0:2]+xList.values[2][0:2]
# xlen= len(xList)
#         allcomb={}
#         k=1
#         print len(factor)
#         for i in range(xlen-1):
#             for j in range(i,xlen):
#                 if xList.values[i][2]==1 and xList.values[j][2]==1:
#                     allcomb[k]= [xList.values[i][0],xList.values[i][1],xList.values[j][0],xList.values[j][1]]
#                     k=k+1
# 
#     def factorIn(f,combine):
#         for factor in combine:
#             if f in factor:
#                 return True
# 
#     rightProduct=[]
#     j=0 
#     for com in allcomb.values():
#         i=0
#         for f in factor :
#             if factorIn(f, com) :
#                 i=i+1
#             if i==len(factor):
#                 com.sort()
#                 rightProduct.append(com)
#                 j=j+1
#     
#     ##print  rightProduct                  
#     
#     
#     ##去重
#     new_rightProduct=[]
#     for product in rightProduct :
#         if product not in new_rightProduct:
#             new_rightProduct.append(product)
# print new_rightProduct
#     

    
#     def isGroup(xfind):
#         tmp = ''.join(xfind)
#         rt = True
#         for e in factor: 
#             if e not in tmp:
#                 rt = False
#                 break
#         return rt
#     def getFindResult0(xList, tmp):
#         if [tmp[0], tmp[1]] in xList:
#             return True
#         elif [tmp[1], tmp[0]] in xList:
#             return True
#         else:
#             return False
#     def getFindResult(xList, xfind):
#         if (getFindResult0(xList, [xfind[0],xfind[2]]) 
#             and getFindResult0(xList, [xfind[0],xfind[3]])
#             and getFindResult0(xList, [xfind[1],xfind[2]])
#             and getFindResult0(xList, [xfind[1],xfind[3]])):
#             return True
#         else:
#             return False    
#     
#     def getTransTwoFour(xList):
#         n = len(xList)
#         relation4 = []
#         if n > 1:
#             for i in range(n-1):
#                 for j in range(i+1,n):
#                     xfind = xList[i][:2] + xList[j][:2]
#                     if isGroup(xfind):
#                         if getFindResult(xList, xfind):
#                             xfind.sort()
#                             if xfind not in relation4:
#                                 relation4.append(xfind)
#         return relation4
#     
#     
#     def getTransFourTwo(self, extraction):
#         relation2 = []
#         for tmp in extraction:
#             xList = self.getRelationSet(tmp)
#             for pairs in xList:
#                 if self.classification(pairs, relation2) == 0:
#                     relation2.append(pairs)
#         return relation2
#     
#     def getExtraction(self, xList):
#         xList = [x for x in xList if x[2] == 1]
#         return self.getResult(xList)
# 
#     
# 
#     
#     def getResult(xList):
#         n = len(xList)
#         rt = []
#         if n > 1:
#             for i in range(n-1):
#                 for j in range(i+1,n):
#                     xfind = xList[i][:2] + xList[j][:2]
#                     if isGroup(xfind):
#                         if getFindResult(xList, xfind):
#                             xfind.sort()
#                             if xfind not in rt:
#                                 rt.append(xfind)
#         
#         return rt
# print getTransTwoFour(xList)