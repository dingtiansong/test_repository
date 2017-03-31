# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 09:41:00 2016

@author: song
"""
##Create the factor dictionary
##import pandas as pd
from pandas import Series
from pandas import DataFrame
from sklearn.externals import joblib
import numpy as np
# from astropy.modeling.utils import comb
# from sklearn import metrics

class getProductRelation():
    '''
    classdocs
    '''
    factor=['D','P','T','R','M']
    dict = []
    maxFactor = 15
    sentence=['D1','T1','M1','P1','M2','P2']
    correct_set=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])
    
    def __init__(self, factor,maxFactor,sentence,correct_set):
        '''
        Constructor
        '''
        if factor != '':
            self.factor = factor
        if maxFactor != '':
            self.maxFactor = maxFactor
        if sentence != '':
            self.sentence = sentence
        if correct_set != '':
            self.correct_set = correct_set
        self.dict = self.dictCre(factor,maxFactor)
    
    def dictCre(self, factor, value_max):
        length = len(factor)+1    
        base = []    
        for i in range (length - 1):
            for j in range(1, value_max + 1):
                word = str(factor[i]) + str(j)
                base.append(word)
        aa = []
        for i in range(1, length):
            aa+=([i] * value_max)
        fdict=Series(aa, index = base)
        return fdict
        
    ## Calculate  feature  value
    
    def value_f1(self, index1, sentence):
        if(index1 == 0):
            value_f1 = 0           
        else:
            valuef1_index = index1-1
            value_f1=self.dict[sentence[valuef1_index]]
        return value_f1 
        
    def value_b1(self, index1,index2,sentence):
        if(index2-index1 == 1):
            value_b1 = 0 
        else :                
            valueb1_index = index1+1
            value_b1 = self.dict[sentence[valueb1_index]]
        return value_b1
        
    def value_f2(self, index2, index1, sentence):
        if(index2-index1 == 0):
            value_f2 = 0           
        else:
            valuef2_index=index2-1
            value_f2=self.dict[sentence[valuef2_index]]
        return value_f2
        
    def value_b2(self,index2,sentence):
        if(index2==len(sentence)-1):
            value_b2=0           
        else:
            valueb2_index=index2+1
            value_b2=self.dict[sentence[valueb2_index]]
        return value_b2
        
    def value_m(self,index1,index2,sentence):
        value_m=0
        if(index2-index1>2):
            for factor in sentence[index1+2:index2] :
                if (factor[0] in sentence[index1] or factor[0] in sentence[index2]):
                    value_m+=1
        return value_m
    
    
    ##Create feature vector 
                  
    def fvactor(self,entity1,entity2,sentence): 
        index1=min(sentence.index(entity1),sentence.index(entity2))
        index2=max(sentence.index(entity1),sentence.index(entity2))
        distence=index2-index1
        length=len(sentence)    
        factor1=self.value_f1(index1,sentence)
        factorself1=self.dict[entity1]
        factor2=self.value_b1(index1,index2,sentence)
        factor3=self.value_m(index1,index2,sentence)
        factor4=self.value_f2(index1,index2,sentence)
        factorself2=self.dict[entity2]
        factor5=self.value_b2(index2,sentence)
        fvactor=[factor1,factorself1,factor2,factor3,factor4,factorself2,factor5,distence,length]
        return fvactor
      
      
    ##demo
      
    def allset(self,sentence):
        all_set={}
        i=0
        for factor1 in sentence:
            for factor2 in sentence[sentence.index(factor1):len(sentence)]:
                if(factor1[0]!=factor2[0]):
                    i+=1
                    all_set[i]=[factor1,factor2]
        return all_set
    
    
    ##find right combinations
    
    def getRightset(self,correct_set,sentence): 
        judgement_set={}
        i=1
        allpro_set=self.allset(sentence)
        allright_set=self.allset(correct_set)  
        for valset in allpro_set.values() :
            if valset in allright_set.values() or [valset[1],valset[0]] in allright_set.values() :
                valset.append('1')
                judgement_set[i]=valset
            else:
                valset.append('0')
                judgement_set[i]=valset
            i+=1
        return judgement_set
    
    ##get  all set (wrong or right , tagged with 0 or 1) 
    
    
    def alljudgementset(self,allcorrect_set,sentence):
        allju_set=self.getRightset(allcorrect_set[0],sentence)   
        if len(allcorrect_set)==4 and allcorrect_set[0]=='D1' :
            i=0
            ju_set=self.getRightset(allcorrect_set,sentence)
            for valset in ju_set.values():
                i=i+1
                if valset[2]=='1' :
                    allju_set[i]=valset
            if  len(allju_set)!=len(ju_set):
                print( 'Error: Set Error!! ')  
        else: 
            for correct in allcorrect_set :
                i=0
                ju_set=self.getRightset(correct,sentence)
                for valset in ju_set.values():
                    i=i+1
                    if valset[2]=='1' :
                        allju_set[i]=valset
            if  len(allju_set)!=len(ju_set):
                print( 'Error: Set Error!! ')             
        return allju_set
    
    
    ##divide into different group by relation types 
    ##classification
    
    
    def realationset(self,factor):
        k=1
        realation_type={}
        for i in range(0,len(factor)-1):
            for j in range(i+1,len(factor)):
                realation_type[k]=[factor[i],factor[j]]
                k+=1
        return realation_type
    
    def divSet(self,alljudgement,factor):
        classify_set= alljudgement   
        rel_type=self.realationset(factor)
        for valset in classify_set.values():
            for i in rel_type :
                if (rel_type[i][0] in valset[0] and rel_type[i][1] in valset[1]) or (rel_type[i][0] in valset[1] and rel_type[i][1] in valset[0]):                
                    valset.append(i)
#                 else :
#                     print "ERRROR : do not contain this relationship!! please cheak your data!!"
#                     break
        return classify_set
    
    
    
    ####################################################################################3
    
    def dataset(self,sentence,factor,allcorrect_set):
        alljudgement_set=self.alljudgementset(allcorrect_set,sentence)
        classify_set=self.divSet(alljudgement_set,factor)
        data_set={}
        i=1
        for valset in classify_set.values() :
            entity1=valset[0]
            entity2=valset[1]
            data_set[i]=self.fvactor(entity1,entity2,sentence)
            data_set[i].append(valset[2])
            data_set[i].append(valset[3])
            data_set[i].append(valset[0])
            data_set[i].append(valset[1])
            i=i+1
        return data_set
        
    ##create dataset for analysis  
        
    
    def dataout(self,sentence,factor,allcorrect_set):
        ## need pandas
        real=self.realationset(factor) ##show the relation types
        ##print (' data has been done!!')
        print ('relation tag:  %s'%real)
        data=self.dataset(sentence, factor, allcorrect_set)
        data_frame=DataFrame(data).T
        data_frame.columns=['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length','relation_state','relation_type','entity1R','entity2R']
        return data_frame
    
##get data collection
    def Crexy(self,factor,numsentence): 
        allframe=DataFrame()
        allsentenceset={}
        allcorrectset={}
        for i in range(1,numsentence+1):
            senten=str('sentence')+str(i)
            correct=str('correct_set')+str(i)
            sentence = eval(senten)
            correct_set=eval(correct)
            allsentenceset[i]=sentence
            allcorrectset[i]=correct_set
        for i in range(1,numsentence+1):
            dataframe=self.dataout(allsentenceset[i],factor,allcorrectset[i])
            allframe=allframe.append(dataframe)
        return allframe
    
    def factorIn(self,f,combine):
        for factor in combine:
            if f in factor:
                return True
    def getFindResult0(self, xList, tmp):
        if [tmp[0], tmp[1]] in xList:
            return True
        elif [tmp[1], tmp[0]] in xList:
            return True
        else:
            return False
    def getFindResult(self, xList, xfind):
        if (self.getFindResult0(xList, [xfind[0],xfind[2]]) 
            and self.getFindResult0(xList, [xfind[0],xfind[3]])
            and self.getFindResult0(xList, [xfind[1],xfind[2]])
            and self.getFindResult0(xList, [xfind[1],xfind[3]])):
            return True
        else:
            return False
    def getProduct(self,sentence,needfactor,modeltype):
        factorMatrix={}
        featureMatrix={}
        i=0
        rel_type=self.realationset(needfactor)
        allrelation=self.allset(sentence)
        for pairs in allrelation.values():
            for j in rel_type:
                if (rel_type[j][0] in pairs[0] and rel_type[j][1] in pairs[1]) or (rel_type[j][0] in pairs[1] and rel_type[j][1] in pairs[0]):                
                    pairs.append(j)
            factorMatrix[i]=self.fvactor(pairs[0], pairs[1], sentence)
            featureMatrix[i]=self.fvactor(pairs[0], pairs[1], sentence)
            factorMatrix.values()[i].append(pairs[2])
            factorMatrix.values()[i].append(pairs[0])
            factorMatrix.values()[i].append(pairs[1])
            i=i+1
        svmmodel = joblib.load(modeltype)        
        data_frame2=DataFrame(featureMatrix).T
        x=np.array(data_frame2)
        y=svmmodel.predict(x)        
        for i in range(len(y)):
            factorMatrix.values()[i].append(y[i])  
        data_frame1=DataFrame(factorMatrix).T 
        data_frame1.columns=['entity1f','entity1','entity1b','numbtw','entity2f','entity2','entity2b','distence','length','relation_type','entity1R','entity2R','relation_est']
        xList=data_frame1[['entity1R','entity2R','relation_est']]
        xList11={}
        z=0
        for comb1 in xList.values:
            if comb1[2]==1:
                xList11[z]=comb1[:2]
                z=z+1
        xList1=DataFrame(xList11).T
        allcomb1=[]
        allcomb={}
#         k=1
        xlen=len(xList1.values)
        for i in range(xlen-1):
            for j in range(i+1,xlen):
#                 if xList.values[i][2]==1 and xList.values[j][2]==1:
                        allcomb1.append([xList1.values[i][0],xList1.values[i][1],xList1.values[j][0],xList1.values[j][1]])  
#                         allcomb1[k]= [xList1[i][0],xList1[i][1],xList1[j][0],xList1[j][1]]                    
#                         if self.getFindResult(self, xList1.values, comb):
#                             allcomb=[k]= comb
#                         k=k+1
                         
        allcomb1
        c=[]
        for x in xList1.values:
            c.append(list(x))
        m=1
#         for comb in allcomb1.values():
        for comb in allcomb1:
            if self.getFindResult(c, comb):
                allcomb[m]=comb
                m=m+1
         
        rightProduct=[]
        j=0 
        for com in allcomb.values():
            i=0
            for f in needfactor :
                if self.factorIn(f, com) :
                    i=i+1
#                     print i
                if i==len(needfactor):
                    com.sort()
                    rightProduct.append(com)
                    j=j+1
        new_rightProduct=[]
        for product in rightProduct :
            if product not in new_rightProduct:
                new_rightProduct.append(product) 
        finalproduct=DataFrame(new_rightProduct)   
#         finalproduct.columns=['方向','产品','利率','期限']   
        return data_frame1,finalproduct,allcomb1,xList1,allcomb,xList

        
        
