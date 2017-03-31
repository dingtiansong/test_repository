# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 09:41:00 2016

@author: song
"""

print (__doc__)
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
#     sentence=['D1','T1','M1','P1','M2','P2']
#     correct_set=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])
    sentence=['D1','P1','T1','R1','T2','R2']
    correct_set=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])
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
        factor4=self.value_f2(index2,index1,sentence)
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

        
        
        









































###online product
sentence1=['D1','T1','M1','P1','M2','P2']
correct_set1=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
sentence2=['D1','T1','M1','M2','P1','P2']
correct_set2=(['D1','T1','M1','P1'],['D1','T1','M2','P2'],['D1','T1','M2','P1'],['D1','T1','M1','P2'])
         
sentence3=['D1','T1','M1','P1']
correct_set3=(['D1','T1','M1','P1'])
         
sentence4=['D1','M1','T1','P1','P2']
correct_set4=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
         
sentence5=['D1','T1','M1','P1','M2','P2']
correct_set5=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
sentence6=['D1','T1','P1','M1']
correct_set6=(['D1','T1','M1','P1'])
         
sentence7=['D1','T1','M1','P1','P2']
correct_set7=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
         
sentence8=['D1','T1','T2','T3','M1','P1']
correct_set8=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'])
         
sentence9=['D1','T1','T2','T3','T4','M1','P1','P2']
correct_set9=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'],['D1','T4','M1','P1'],['D1','T1','M1','P2'],['D1','T2','M1','P2'],['D1','T3','M1','P2'],['D1','T4','M1','P2'])
         
sentence10=['D1','T1','M1','P1','M2','P2']
correct_set10=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
sentence11=['D1','T1','M1','P1','P2']
correct_set11=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
         
sentence12=['D1','T1','M1','P1','M2','P2']
correct_set12=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
sentence13=['D1','T1','M1','P1','P2','P3']
correct_set13=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])
         
sentence14=['D1','T1','M1','P1','M2','P2']
correct_set14=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
sentence15=['D1','T1','M1','P1','P2']
correct_set15=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
         
sentence16=['D1','T1','M1','T2','M2','P1']
correct_set16=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])
         
sentence17=['D1','T1','M1','P1','P2','P3']
correct_set17=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])
         
sentence18=['D1','T1','M1','P1','M2','P2']
correct_set18=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
         
       
sentence19=['D1','P1','P2','P3','P4','P5','T1','M1']
correct_set19=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'],['D1','P4','T1','M1'],['D1','P5','T1','M1'])
       
sentence20=['D1','T1','M1','P1','P2']
correct_set20=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence21=['D1','T1','M1','P1','P2']
correct_set21=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence22=['D1','T1','M1','P1','P2','P3']
correct_set22=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'])
       
sentence23=['D1','T1','M1','P1','P2','P3']
correct_set23=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'])
       
sentence24=['D1','M1','T1','P1','P2','P3']
correct_set24=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'])
       
sentence25=['D1','T1','M1','P1','P2']
correct_set25=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence26=['D1','T1','M1','P1','P2']
correct_set26=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence27=['D1','M1','T1','P1']
correct_set27=(['D1','P1','T1','M1'])
       
sentence28=['D1','T1','M1','P1']
correct_set28=(['D1','P1','T1','M1'])
       
sentence29=['D1','T1','M1','M2','P1']
correct_set29=(['D1','P1','T1','M1'],['D1','P1','T1','M2'])
       
sentence30=['D1','T1','M1','P1']
correct_set30=(['D1','P1','T1','M1'])
       
sentence31=['D1','T1','M1','P1']
correct_set31=(['D1','P1','T1','M1'])
       
sentence32=['D1','T1','M1','M2','P1']
correct_set32=(['D1','P1','T1','M1'],['D1','P1','T1','M2'])
       
sentence33=['D1','T1','T2','M1','P1']
correct_set33=(['D1','P1','T1','M1'],['D1','P1','T2','M1'])
       
sentence34=['D1','T1','T2','T3','M1','P1']
correct_set34=(['D1','P1','T1','M1'],['D1','P1','T2','M1'],['D1','P1','T3','M1'])
       
sentence35=['D1','T1','M1','P1','P2']
correct_set35=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence36=['D1','T1','M1','M2','P1','P2']
correct_set36=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'])
       
sentence37=['D1','T1','M1','P1','P2']
correct_set37=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence38=['D1','T1','T2','T3','M1','P1','P2']
correct_set38=(['D1','P1','T1','M1'],['D1','P1','T2','M1'],['D1','P1','T3','M1'],['D1','P2','T1','M1'],['D1','P2','T2','M1'],['D1','P2','T3','M1'])
       
sentence39=['D1','T1','P1','P2','M1']
correct_set39=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence40=['D1','T1','P1','M1','T2','P2','M2']
correct_set40=(['D1','P1','T1','M1'],['D1','P2','T2','M2'])
       
sentence41=['D1','M1','T1','P1']
correct_set41=(['D1','P1','T1','M1'])
       
sentence42=['D1','P1','T1','M1']
correct_set42=(['D1','P1','T1','M1'])
       
sentence43=['D1','P1','T1','M1']
correct_set43=(['D1','P1','T1','M1'])
       
sentence44=['D1','T1','T2','M1','P1']
correct_set44=(['D1','P1','T1','M1'],['D1','P1','T2','M1'])
       
sentence45=['D1','T1','M1','P1','P2']
correct_set45=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
       
sentence46=['D1','T1','T2','M1','P1']
correct_set46=(['D1','P1','T1','M1'],['D1','P1','T2','M1'])
       
sentence47=['D1','T1','M1','P1']
correct_set47=(['D1','P1','T1','M1'])
       
sentence48=['D1','M1','P1','M2','P2','T1']
correct_set48=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
       
sentence49=['D1','T1','M1','P1','P2','P3']
correct_set49=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'])
       
sentence50=['D1','T1','M1','P1']
correct_set50=(['D1','P1','T1','M1'])
    
sentence51=['D1','T1','M1','P1','M2','P2','M3','P3']
correct_set51=(['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3'])
    
    
sentence52=['D1','T1','M1','T2','M2','P1']
correct_set52=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
sentence53=['D1','P1','T1','M1','P2','T2','M2','M3']
correct_set53=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3'])
    
    
sentence54=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
correct_set54=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4'])
    
    
sentence55=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
correct_set55=(['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2'])
    
    
sentence56=['D1','T1','M1','P1','M2','P2']
correct_set56=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
    
sentence57=['D1','P1','T1','M1','T2','M2']
correct_set57=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])  
    
sentence58=['D1','T1','M1','P1','M2','P2']
correct_set58=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence59=['D1','T1','M1','P1','M2','P2']
correct_set59=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence60=['D1','T1','M1','P1','M2','P2']
correct_set60=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence61=['D1','T1','M1','P1','M2','P2']
correct_set61=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence62=['D1','T1','M1','P1','M2','P2']
correct_set62=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence63=['D1','T1','M1','T2','M2','P1']
correct_set63=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])
    
sentence64=['D1','T1','M1','P1','M2','P2']
correct_set64=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence65=['D1','T1','P1','M1','T2','P2','M2']
correct_set65=(['D1','P1','T1','M1'],['D1','P2','T2','M2'])
    
sentence66=['D1','M1','P1','M2','P2','T1']
correct_set66=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
    
sentence67=['D1','T1','M1','P1','M2','P2','M3','P3']
correct_set67=(['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3'])
    
    
sentence68=['D1','T1','M1','T2','M2','P1']
correct_set68=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
sentence69=['D1','P1','T1','M1','P2','T2','M2','M3']
correct_set69=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3'])
    
    
sentence70=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
correct_set70=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4'])
    
    
sentence71=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
correct_set71=(['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2'])
    
    
sentence72=['D1','T1','M1','P1','M2','P2']
correct_set72=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
    
sentence73=['D1','P1','T1','M1','T2','M2']
correct_set73=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
sentence74=['D1','T1','M1','P1','M2','P2']
correct_set74=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence75=['D1','T1','M1','P1','M2','P2']
correct_set75=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence76=['D1','T1','M1','P1','M2','P2']
correct_set76=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence77=['D1','T1','M1','P1','M2','P2']
correct_set77=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence78=['D1','T1','M1','P1','M2','P2']
correct_set78=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence79=['D1','T1','M1','T2','M2','P1']
correct_set79=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])
    
sentence80=['D1','T1','M1','P1','M2','P2']
correct_set80=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence81=['D1','T1','P1','M1','T2','P2','M2']
correct_set81=(['D1','P1','T1','M1'],['D1','P2','T2','M2'])
    
sentence82=['D1','M1','P1','M2','P2','T1']
correct_set82=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
    
sentence83=['D1','T1','M1','P1','M2','P2','M3','P3']
correct_set83=(['D1','P1','T1','M1'],['D1','P2','T1','M2'],['D1','P3','T1','M3'])
    
    
sentence84=['D1','T1','M1','T2','M2','P1']
correct_set84=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
sentence85=['D1','P1','T1','M1','P2','T2','M2','M3']
correct_set85=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P2','T2','M3'])
    
    
sentence86=['D1','P1','T1','M1','P2','T2','M2','P3','T3','M3','M4']
correct_set86=(['D1','P1','T1','M1'],['D1','P2','T2','M2'],['D1','P3','T3','M3'],['D1','P3','T3','M4'])
    
    
sentence87=['D1','T1','M1','P1','P2','T2','M2','P3','P4']
correct_set87=(['D1','P1','T1','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M2'],['D1','P4','T2','M2'])
    
    
sentence88=['D1','T1','M1','P1','M2','P2']
correct_set88=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
    
sentence89=['D1','P1','T1','M1','T2','M2']
correct_set89=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
sentence90=['D1','T1','M1','P1','M2','P2']
correct_set90=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence91=['D1','T1','M1','P1','M2','P2']
correct_set91=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence92=['D1','T1','M1','P1','M2','P2']
correct_set92=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence93=['D1','T1','M1','P1','M2','P2']
correct_set93=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence94=['D1','T1','M1','P1','M2','P2']
correct_set94=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence95=['D1','T1','M1','T2','M2','P1']
correct_set95=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])
    
sentence96=['D1','T1','M1','P1','M2','P2']
correct_set96=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])
    
sentence97=['D1','T1','P1','M1','T2','P2','M2']
correct_set97=(['D1','P1','T1','M1'],['D1','P2','T2','M2'])
    
sentence98=['D1','M1','P1','M2','P2','T1']
correct_set98=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
sentence99=['D1','T1','M1','M2','M3','P1','P2','P3']
correct_set99=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P3','T1','M2'],['D1','P1','T1','M3'],['D1','P2','T1','M3'],['D1','P3','T1','M3'])
    
sentence100=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set100=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
    
sentence101=['D1','M1','M2','T1','P1','P2']
correct_set101=(['D1','P1','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M1'],['D1','P1','T1','M2'])
    
sentence102=['D1','M1','M2','M3','T1','P1','P2']
correct_set102=(['D1','P1','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M1'],['D1','P2','T1','M2'],['D1','P1','T1','M3'],['D1','P2','T1','M3'])
    
sentence103=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set103=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
    
# 104.出资金7000万（1个月及以上），押利率债或者上清存单，限银行，欢迎小窗
sentence104=['D1','M1','T1','P1','P2']
correct_set104=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
    
# 105.出资金1.7亿+7000万（1个月及以上），押利率债或者上清存单，限银行，欢迎小窗
sentence105=['D1','M1','M2','T1','P1','P2']
correct_set105=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'])
    
# 106.出7天7000w 14天7000w 压券宽松~~
sentence106=['D1','T1','M1','T2','M2','P1']
correct_set106=(['D1','P1','T1','M1'],['D1','P1','T2','M2'])
    
# 107.出散量5天或14天900w，押券宽松
sentence107=['D1','T1','T2','M1','P1']
correct_set107=(['D1','P1','T1','M1'],['D1','P1','T2','M1'])
    
# 108.出7d 1000w 押券宽松
sentence108=['D1','T1','M1','P1']
correct_set108=(['D1','P1','T1','M1'])
    
# 109.出 14D 1300W 押券宽松 求带走
sentence109=['D1','T1','M1','P1']
correct_set109=(['D1','P1','T1','M1'])
    
# 110.出2M、3M 6000万资金，限银行农信，押中债利率或3A
sentence110=['D1','T1','T2','M1','P1','P2','P3']
correct_set110=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'],['D1','P1','T2','M1'],['D1','P2','T2','M1'],['D1','P3','T2','M1'])
    
# 111.出隔夜5000W 押利率
sentence111=['D1','T1','M1','P1']
correct_set111=(['D1','P1','T1','M1'])
    
# 112.借隔夜 押利率 2.5亿 押AAA存单3亿
sentence112=['D1','T1','P1','M1','P2','M2']
correct_set112=(['D1','P1','T1','M1'],['D1','P2','T1','M2'])
    
# 113.出14天及以上期限资金7+1.5亿，押利率或上清存单，欢迎小窗
sentence113=['D1','T1','M1','M2','P1','P2']
correct_set113=(['D1','P1','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M1'],['D1','P2','T1','M2'])
    
# 114.借隔夜3000-5000万，押利率押存单，中债上清都行。求抖窗
sentence114=['D1','T1','M1','P1','P2','P3','P4']
correct_set114=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'],['D1','P4','T1','M1'])
    
# 115.出9天内、2M及以上期限2.2亿,限银行农信，押中债利率或3A.
sentence115=['D1','T1','M1','P1','P2','P3']
correct_set115=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P3','T1','M1'])
    
# 116.借隔夜1.3E/1.5E 押利率，上午还款~~~
sentence116=['D1','T1','M1','M2','P1']
correct_set116=(['D1','P1','T1','M1'],['D1','P1','T1','M2'])
    
# 117.借隔夜资金 1亿 押利率
sentence117=['D1','T1','M1','P1']
correct_set117=(['D1','P1','T1','M1'])
    
# 118.出资金3亿+1亿+5000万+3000万（7天及以上），押利率债或者上清存单，限银行农信，欢迎小窗
sentence118=['D1','M1','M2','M3','T1','P1','P2']
correct_set118=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P2','T1','M2'],['D1','P2','T1','M3'],['D1','P1','T1','M2'],['D1','P1','T1','M3'])
    
# 119.出资金2.5亿+1亿+5000万+3000万（7天及以上），5000万（4天）押利率债或者上清存单，限银行农信，欢迎小窗
sentence119=['D1','M1','M2','M3','M4','T1','M5','T2','P1','P2']
correct_set119=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P2','T1','M2'],['D1','P2','T1','M3'],['D1','P1','T1','M2'],['D1','P1','T1','M3'],['D1','P1','T2','M2'],['D1','P2','T2','M2'])
    
# 120.借7天、14天1E，押存单或利率
sentence120=['D1','T1','T2','M1','P1','P2']
correct_set120=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T2','M1'],['D1','P2','T2','M1'])
    
# 121.出1M资金2.9亿，押利率或上清存单
sentence121=['D1','T1','M1','P1','P2']
correct_set121=(['D1','P1','T1','M1'],['D1','P2','T1','M1'])
    
# 104.出14天及以上期限资金1.7+0.7亿，押利率或上清存单，限银行农信
sentence122=['D1','T1','M1','M2','P1','P2']
correct_set122=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'])
    
sentence123=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set123=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
     
sentence124=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set124=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
      
sentence125=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set125=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
     
sentence126=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set126=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
     
sentence127=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set127=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
    
sentence128=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set128=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
    
sentence129=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set129=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])
    
sentence130=['D1','M1','M2','T1','M3','T2','P1','P2']
correct_set130=(['D1','P1','T1','M1'],['D1','P2','T1','M1'],['D1','P1','T1','M2'],['D1','P2','T1','M2'],['D1','P1','T2','M3'],['D1','P2','T2','M3'])


# sentence51=['D1', 'P1', 'M1', 'T1']
# correct_set51=(['D1', 'P1', 'M1', 'T1'])  
###########################################################
##############################################################
#########################################################

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
# sentence28=['D1', 'M1', 'P1', 'T1', 'R1', 'T2', 'R2']
# correct_set28=(['D1','T1','R1','P1'],['D1','T2','R2','P1'])
#   
# sentence29=['D1', 'T1', 'M1', 'P1', 'P2']
# correct_set29=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
#   
# sentence30=['D1', 'M1', 'P1', 'P2', 'T1', 'M2', 'P3', 'P4', 'P5']
# correct_set30=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])
#   
# sentence31=['D1', 'P1', 'M1', 'T1', 'R1']
# correct_set31=(['D1','T1','R1','P1'])
  
  
# # ####offline product
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
#    
# # 21.资金: 兴业天津今日吸金价格, 收各期限人民币同业存款 14天 2.90% 1个月 2.97% 2个月 2.90% 3个月 2.75% 4-9个月 2.90% 1年 2.90% 价可谈，欢迎碰价： 13682073789（微信同号）。
# sentence21=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
# correct_set21=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'])
#    
# # 22.今日同存吸收指导价：7天2.20%，14天2.40%，1个月2.85%，2个月2.75%，3个月2.85%，6个月2.95%，1年3.00%。欢迎金主电联或小窗（0554-6688088,18955498285）
# sentence22=['P1','D1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7']
# correct_set22=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'])
#    
# # 23.【今日报价】2016年9月19日 各期限吸收存款指导价初步定为：1个月2.75%，2个月2.75%，3个月2.75%，5个月2.80%，其他期限暂停吸收。
# sentence23=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4']
# correct_set23=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'])
#    
# # 24.今日民生同业存放价格： 7天：2.35 14天：2.5 一个月：2.9 三个月：2.9 六个月：2.8 九个月：2.8 
# sentence24=['P1','D1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
# correct_set24=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'])
#    
# # 25.上海银行2016年9月19日吸收同业存款价格】：7D2.0%,14D(跨季）:2.9%, 1M3.0%,2M2.75%，4M（跨年）2.7%，美元: 3M-1.1%, 6m-1.45%,1y-1.65% 
# sentence25=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set25=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])
#    
# # 26.昨日同存吸收指导价：7天2.15%，14天2.30%，1个月2.85%，2个月2.75%，3个月2.80%，6个月2.90%，1年2.95%。
# sentence26=['P1','D1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7']
# correct_set26=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'])
#    
# # 27.【收】线下资金，隔夜2.7%，7天2.9%。 
# sentence27=['D1','P1','T1','R1','T2','R2']
# correct_set27=(['D1','P1','T1','R1'],['D1','P1','T2','R2'])
#    
# # 28.我行今天吸存价格： 14d 2.6% 21d 2.66% 1m 2.75% 3m 2.73% 6m 2.75% 欢迎各大银行以及城商农商的伙伴小窗 广东农行龙忠勋13600351414
# sentence28=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5']
# correct_set28=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'])
#    
# # 29.今日中行大量吸收同业存款: 7d 2.24% 14d 2.39% 1m 2.48% 3m 2.49% 9m 2.65% 1y 2.69% 
# sentence29=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6']
# correct_set29=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'])
#    
# # 30.中国银行株洲分行吸收大量线下同存资金 活期1.8% 7D1.24% 14D2.39% 1M2.48% 3M2.49% 6M2.51% 9M2.65% 12M2.69% 另低价收福费廷，出各期限保本非保理财 欢迎爱的小窗！谢婉华 18673325866
# sentence30=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8']
# correct_set30=(['D1','P1','T1','R1'],['D1','P1','T2','R2'],['D1','P1','T3','R3'],['D1','P1','T4','R4'],['D1','P1','T5','R5'],['D1','P1','T6','R6'],['D1','P1','T7','R7'],['D1','P1','T8','R8'])

