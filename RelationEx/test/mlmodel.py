# -*- coding: utf-8 -*-
'''
Created on 2016年8月23日

@author: song
'''
from test.getProductRelation import getProductRelation
from sklearn import svm
import numpy

    ### convert data type 

factor=['D','P','T','R','M','A']
#dict = dictCre(factor,15)
sentence=['D1','T1','M1','P1','M2','P2']
correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
maxFactor = 15
numsentence=18
tmp = getProductRelation(factor,maxFactor,sentence,correct_set)
##print tmp.Crexy(factor,numsentence)
sentence=['D1','T1','M1','P1','M2','P2']
print tmp.allset(sentence)
print tmp.allset(sentence)
### svm model 
data=tmp.Crexy(factor,numsentence)
data[['distence','length']]=data[['distence','length']].astype(int)
data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']]=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b']].astype(int)
x=data[['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length']]
y = data['relation_state'].astype(int)
x1= numpy.array(x)
y1=numpy.array(y)
svmmodel = svm.SVC().fit(x1, y1)
##print svmmodel.predict(x1)
    
######################################################################################
factor=['D','P','T','R','M','A']
sentence=['D1','T1','M1','P1','M2','P2']
correct_set=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
maxFactor = 15
numsentence=31
sentence=['D1','T1','M1','P1','M2','P2'] 
aa=getProductRelation(factor,maxFactor,sentence,correct_set).getProduct(sentence,factor) 
print aa
# bb=getProductRelation(factor,maxFactor,sentence,correct_set).dataout(sentence, factor, correct_set)
# print bb
### convert data type 
##training  data

###online product
# sentence1=['D1','T1','M1','P1','M2','P2']
# correct_set1=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])
# 
# sentence2=['D1','T1','M1','M2','P1','P2']
# correct_set2=(['D1','T1','M1','P1'],['D1','T2','M2','P2'],['D1','T1','M2','P1'],['D1','T2','M1','P2'])
# 
# sentence3=['D1','T1','M1','P1']
# correct_set3=(['D1','T1','M1','P1'])
# 
# sentence4=['D1','M1','T1','P1','P2']
# correct_set4=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
# 
# sentence5=['D1','T1','M1','P1','M2','P2']
# correct_set5=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])
# 
# sentence6=['D1','T1','P1','M1']
# correct_set6=(['D1','T1','M1','P1'])
# 
# sentence7=['D1','T1','M1','P1','P2']
# correct_set7=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
# 
# sentence8=['D1','T1','T2','T3','M1','P1']
# correct_set8=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'])
# 
# sentence9=['D1','T1','T2','T3','T4','M1','P1','P2']
# correct_set9=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'],['D1','T4','M1','P1'],['D1','T1','M1','P2'],['D1','T2','M1','P2'],['D1','T3','M1','P2'],['D1','T4','M1','P2'])
# 
# sentence10=['D1','T1','M1','P1','M2','P2']
# correct_set10=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
# 
# sentence11=['D1','T1','M1','P1','P2']
# correct_set11=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
# 
# sentence12=['D1','T1','M1','P1','M2','P2']
# correct_set12=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])
# 
# sentence13=['D1','T1','M1','P1','P2','P3']
# correct_set13=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])
# 
# sentence14=['D1','T1','M1','P1','M2','P2']
# correct_set14=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
# 
# sentence15=['D1','T1','M1','P1','P2']
# correct_set15=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
# 
# sentence16=['D1','T1','M1','T2','M2','P1']
# correct_set16=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])
# 
# sentence17=['D1','T1','M1','P1','P2','P3']
# correct_set17=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])
# 
# sentence18=['D1','T1','M1','P1','M2','P2']
# correct_set18=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
# 
# sentence19=['D1', 'P1', 'A1', 'T1']
# correct_set19=(['D1', 'P1', 'A1', 'T1'])
#   
# sentence20=['D3', 'T1', 'R1', 'T2', 'R2', 'T3', 'R3', 'T4', 'R4', 'T5', 'R5', 'T6', 'R6', 'T7', 'R7', 'P5', 'A1']
# correct_set20=([ 'D3','P4','T1', 'R1'],['D3','P4','T2','R2'],['D3', 'P4','T3', 'R3'],['D3','P4', 'T4', 'R4'],['D3','P4', 'T5', 'R5'],['D3', 'P4','T6', 'R6'],['D3','P4', 'T7', 'R7'])
#  
# sentence21=['T1', 'P1', 'D1', 'R1', 'A1']
# correct_set21=(['T1', 'P1', 'D1', 'R1'])
#  
# sentence22=['D1', 'A1', 'T1', 'P1']
# correct_set22=(['D1', 'A1', 'T1', 'P1'])
# 
# sentence23=['D1', 'T1', 'P1', 'A1']
# correct_set23=(['D1', 'T1', 'P1', 'A1'])
#  
# sentence24=['D1', 'P1', 'P2', 'T1', 'R1', 'A1']
# correct_set24=(['D1', 'P1', 'T1', 'R1'] ,['D1', 'P2', 'T1', 'R1'])
#  
# sentence25=['D1', 'A1', 'P1', 'T1', 'T2']
# correct_set25=(['D1','A1','P1','T1'],['D1','A1','P1','T2'])
#  
# sentence26=['P1', 'T1', 'P2', 'R1', 'D1', 'T2', 'P3', 'R2', 'A1', 'D2', 'D3', 'P4', 'D4', 'P5', 'P6']
# correct_set26=(['D1', 'T2', 'P3', 'R2'])
#  
# sentence27=['D1', 'P1', 'P2', 'T1', 'R1']
# correct_set27=(['D1','T1','R1','P1'],['D1','T1','R1','P2'])
#  
# sentence28=['D1', 'A1', 'P1', 'T1', 'R1', 'T2', 'R2']
# correct_set28=(['D1','T1','R1','P1'],['D1','T2','R2','P1'])
#  
# sentence29=['D1', 'T1', 'A1', 'P1', 'P2']
# correct_set29=(['D1','T1','A1','P1'],['D1','T1','A1','P2'])
#  
# sentence30=['D1', 'A1', 'P1', 'P2', 'T1', 'A2', 'P3', 'P4', 'P5']
# correct_set30=(['D1','T1','A1','P1'],['D1','T1','A1','P2'])
#  
# sentence31=['D1', 'P1', 'A1', 'T1', 'R1']
# correct_set31=(['D1','T1','R1','P1'])
 
 
####offline product
# sentence1=['D1','P1','T1','R1','T2','R2']
# correct_set1=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])
# 
# sentence2=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set2=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
# 
# sentence3=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set3=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
# 
# sentence4=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set4=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
# 
# sentence5=['D1','P1','T1','R1','T2','R2','T3','R3']
# correct_set5=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'])
# 
# sentence6=['D1','P1','T1','R1','T2','R2','T3','R3']
# correct_set6=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'])
# 
# sentence7=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set7=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])
# 
# sentence8=['D1','P1','T1','R1']
# correct_set8=(['D1','P1','T1','R1'])
# 
# sentence9=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set9=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])
# 
# sentence11=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
# correct_set11=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'])
# 
# sentence12=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set12=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
# 
# sentence13=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4']
# correct_set13=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'])
# 
# sentence14=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set14=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
# 
# sentence15=['D1','P1','T1','R1']
# correct_set15=(['D1','P1','T1','R1'])
# 
# sentence16=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9','T10','R10']
# correct_set16=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9'],['D1','P1','T10','R10'])
# 
# sentence17=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set17=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])
# 
# sentence18=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set18=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])
# 
# sentence19=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7']
# correct_set19=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'])
# 
# sentence20=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9']
# correct_set20=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'],['D1','P1','T9','R9'])
# 
# sentence10=['D1','P1','P2','T1','R1','T2','R2','T3','R3','T4','R4']
# correct_set10=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P2','T1','R1'],['D1','P2','T2','R2'],['D1','P2','T3','R3'],['D1','P2','T4','R4'])
