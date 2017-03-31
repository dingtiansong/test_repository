# -*- coding: utf-8 -*-
'''
Created on 2016年10月12日

@author: song
'''
from pandas import Series
import copy
class getFeatureVector(object):
    '''
    classdocs
    '''
    factor=['C','D','P','T','R','A','Z','Y','X','U']
    
    #Z表示中英文逗号
    #Y表示中英文句号
    #X表示中英文分号
    #U表示换行符
    vType = factor[:5]
    maxFactor = 30
    vPunctuation = [u'。',u'.',u'。',u'．',u'；',u';',u'；',u'；',u'，',u',',u'，',u'，',u'    ',u' ',u'\\n']
    vWordList = vPunctuation
    for i in vType:
        for j in range(maxFactor):
            vWordList.append('%s%s'%(i,j))
    vType = ['C','D','P','T','R','A']
    verbTag = 'D'
    serialTag = 'C'
    nounTag = 'P'

    
    def __init__(self, factor=[], maxFactor=0):
        '''
        Constructor
        '''
        if factor:
            self.factor = factor
            self.vType = factor[1:5]
            self.serialTag = factor[0]
            self.verbTag = factor[1]
            self.nounTag = factor[2]
        if maxFactor:
            self.maxFactor = maxFactor
        self.dict = self.dictCre(self.factor, self.maxFactor)
        self.vWordList = self.vPunctuation
        for i in self.factor:
            for j in range(self.maxFactor):
                self.vWordList.append('%s%s'%(i,j))
        
    
    ##生成元素对照字典
    def dictCre(self, factor, value_max): 
        base = []    
        for i in factor:
            for j in range(value_max):
                word = '%s%s' %(i, j + 1)
                base.append(word)
        aa = []
        for i in range(len(factor)):
            aa+=([i+1] * value_max)
        fdict=Series(aa, index = base)
        return fdict
    
    ##将句子中符号转换为标注

    def punctans(self,sentence):
        sentence1 = copy.copy(sentence)
        for e in sentence1:
            if e == u'，' or e ==u',' or e == u' ' or e == u'    ':
                sentence1[sentence1.index(e)]='Z1'
            elif e==u'。' or e == u'.':
                sentence1[sentence1.index(e)]='Y1'
            elif e==u';' or e==u'；':
                sentence1[sentence1.index(e)]='X1'
            elif e == u'\\n' :
                sentence1[sentence1.index(e)]='U1'
        return sentence1   
    
    ##目标元素前面第一个元素
    def cutfactor_f1(self,index,sentence):
        if (index==0):
            value_f1=0
        else:
            value_f1_index=index-1
            value_f1=self.dict[sentence[value_f1_index]]
        return value_f1
    
    ##目标元素前面第二个元素    
    def cutfactor_f2(self,index,sentence):
        if (index<2):
            value_f2=0
        else:
            value_f2_index=index-2
            value_f2=self.dict[sentence[value_f2_index]]
        return value_f2
    ##目标元素前面第三个元素       
    def cutfactor_f3(self,index,sentence):
        if (index<3):
            value_f3=0
        else:
            value_f3_index=index-3
            value_f3=self.dict[sentence[value_f3_index]]
        return value_f3

    ##目标元素后面第一个元素       
    def cutfactor_b1(self,index,sentence):
        if (index==len(sentence)-1):
            value_b1=0
        else:
            value_b1_index=index+1
            value_b1=self.dict[sentence[value_b1_index]]
        return value_b1

    ##目标元素后面第二个元素    
    def cutfactor_b2(self,index,sentence):
        if (index>len(sentence)-3):
            value_b2=0
        else:
            value_b2_index=index+2
            value_b2=self.dict[sentence[value_b2_index]]
        return value_b2

    ##目标元素后面第三个元素    
    def cutfactor_b3(self,index,sentence):
        if (index>len(sentence)-4):
            value_b3=0
        else:
            value_b3_index=index+3
            value_b3=self.dict[sentence[value_b3_index]]
        return value_b3
    
    # def factorset(index,sentence,needfactor):
    #     num=0
    #     for factor in sentence[:index]:
    #         if factor in needfactor:
    #             num+=1
    #     return num
    
            
    ##目标元素与前面第一个相同元素之间的距离        
    def cutfactor_len(self,sentence,index):
        if (index!=0): 
            for i in range(1,index+1):
                lengthcut=i-1
                indexb=index-i
    #             print i
                if sentence[indexb][0]==sentence[index][0] :
                    break
    #         lengthcut=lengthcut0
    #         if lengthcut0<(index-1):
    #                 lengthcut=lengthcut0
    #         else :
    #                 lengthcut=0                   
        else :
            lengthcut=0        
        return lengthcut

    ##生成特征向量
    def fvector(self,sentence,factor0):
        index=sentence.index(factor0)
        tWord = factor0
        aa8=self.getIsDFirst(tWord, sentence, self.vType)
        aa9=self.getIsDLeft(tWord, sentence, self.verbTag)
        aa10=self.getIsDRight(tWord, sentence, self.verbTag)
        aa11=self.getIsExistVerb(tWord, sentence, self.verbTag)
        aa12=self.getIsFirstWord(tWord, sentence)
        aa13=self.getIsFourTag(tWord, sentence, self.vType)
        aa14=self.getIsLastWord(tWord, sentence)
        aa15=self.getIsPLeftD(tWord, sentence, self.nounTag, self.verbTag)
        aa16=self.getIsSerialRight(tWord, sentence, self.serialTag)
        aa17=self.getWordID(tWord, self.vWordList)
        aa18=self.getWordTags(tWord, self.vWordList)
        
        #index=sentence.index(factor0)
        sentence1=self.punctans(sentence)
        aa1=self.cutfactor_len(sentence1,index)  
        aa2=self.cutfactor_f1(index,sentence1)
        aa3=self.cutfactor_f2(index,sentence1)
        aa4=self.cutfactor_f3(index,sentence1)
        aa5=self.cutfactor_b1(index,sentence1)
        aa6=self.cutfactor_b2(index,sentence1)
        aa7=self.cutfactor_b3(index,sentence1)  
        vector=[aa1,aa2,aa3,aa4,aa5,aa6,aa7,aa8,aa9,aa10,aa11,aa12,aa13,aa14,aa15,aa16,aa17,aa18]
        return vector
        # The word itself    当前目标节点词本身
    def getWordID(self, tWord, vWordList):
        try:
            wordIDList = vWordList.index(tWord)
        except Exception as e:
            print e
            return ''
        else:
            return wordIDList
        
    # POS-tags    当前目标结点词的词性标记
    def getWordTags(self, tWord, vWordList):
        if tWord in vWordList:
            if tWord in self.dict.keys():
                return self.dict[tWord]
            else:
                return 0   #0表示标点
        else:
            return 0
    
    # First-word or not    如果当前目标结点词位于句首,则设为1，否则为0    行首
    def getIsFirstWord(self, tWord, sentence):
        try:
            if tWord == sentence[0]:
                tmp = 1
            else:
                tmp = 0
        except Exception as e:
            print e
            return 0
        else:
            return tmp
        
    # Last-word or not    如果当前目标结点词位于句尾,则设为1，否则为0    行尾
    def getIsLastWord(self, tWord, sentence):
        try:
            if tWord == sentence[-1]:
                tmp = 1
            else:
                tmp = 0
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    
    # D-left/D-right    如果在句子开头或句子结尾和当前目标结点词之间有动词存在，则设为1，否则为0    
    def getIsDLeft(self, tWord, sentence, verbTag):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in sentence[:wordIndex]:
                if i[0] == verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    
    def getIsDRight(self, tWord, sentence, verbTag):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            #如果tWord为最后一个词，则sentence[minId+1:] == []
            for i in sentence[wordIndex+1:]:
                if i[0] == verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # Serial-right    如果当前目标结点词的右边是词语“序号”，则设为1否则设为0    
    def getIsSerialRight(self, tWord, sentence, serialTag):
        try:
            wordIndex = sentence.index(tWord)
            print sentence[wordIndex+1]
            print serialTag
            if sentence[wordIndex+1][0] == serialTag:
                tmp = 1
            else:
                tmp = 0
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    
    # 词性信息    当前词和其前后各两个词的词性  
    # 词    当前词及其前后各一个词    
    # L_V    当前词之前的句子中是否有动词    
    def getIsExistVerb(self, tWord, sentence, verbTag):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in sentence[:wordIndex]:
                if i[0] == verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # M_F_DT    当前词之前的句子中第一个是否是DT    是否D\是否P\是否T\是否A\是否R
    def getIsDFirst(self, tWord, sentence, vType):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            vTypeDict = {}
            for i in range(len(vType)):
                vTypeDict[vType[i]] = i + 1
            for i in sentence[:wordIndex]:
                if i[0] in vType:
                    tmp = vTypeDict[i[0]]
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # L_V_N    当前词之前的句子中第一个方向词前是否有产品词标识
    def getIsPLeftD(self, tWord, sentence, nounTag, verbTag):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in range(wordIndex):
                if sentence[i][0] == nounTag:
                    PIndex = i
                    for j in range(PIndex,wordIndex):
                        if sentence[j][0] == verbTag:
                            tmp = 1
                            break
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # CLASS    当前词之前的句子是否是可单独解析块    是否有4元素
    def getIsFourTag(self, tWord, sentence, vType):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            tDict = {}
            for i in sentence[:wordIndex]:
                if i[0] in vType:
                    if i[0] not in tDict.keys():
                        tDict[i[0]] = [i]
                    else:
                        tDict[i[0]].append(i)
            if len(tDict) == 4:
                tmp = 1
            else:
                tmp = 0
        except Exception as e:
            print e
            return 0
        else:
            return tmp

##demo
if __name__=='__main__': 
    factor = ['C','D','P','T','R','A','Z','Y','X','U']#,'。','；']
    maxFactor = 30
    cutvector = getFeatureVector(factor,maxFactor)
    
    
    import pickle
    fd = u'C:/Users/Administrator.PC-20150820KBVI/Desktop/preprocessed_sentences.pickle'
    with open(fd, 'rb') as f:
        allData = pickle.load(f)
    errorList = []
    for i in allData.keys():
    #sentence = ['D1','C1','P1',',,，','D2','R1',';',' ','T2','R2','T3','D3','T4','R4','T5','R5']
    #factor0=sentence[0]
        print '%s---------'%i
        
       
        #vPunctuation = [u'。',u'.',u'。',u'．',u'；',u';',u'；',u'；',u'，',u',',u'，',u'，',u'    ',u' ',u'\\n']
        #print vPunctuation
        #for k in allData[i]['Labelsentence']:
        
        sentence0 = allData[i]['TAGsentence']
        tDict = {'sentence':[],'feature':[],'result':[]}
        num = 0
        for k in range(len(sentence0)):
            tmp = sentence0[k]
            if tmp in cutvector.vWordList:
                tDict['sentence'].append(tmp)
                tDict['result'].append(0)
                num = num + 1
            elif tmp.strip() in cutvector.vWordList:
                tDict['sentence'].append(tmp.strip())
                tDict['result'].append(0)
                num = num + 1
            if sentence0[k].strip() == u'{S}' and num > 0:
                tDict['result'][num - 1] = 1
        #index=1
        sentence = tDict['sentence']
        if sentence and sentence != ['']:
            for factor in sentence:
                aa=cutvector.fvector(sentence, factor)
                tDict['feature'].append(aa)
        allData[i]['trainData'] = tDict
    for i in allData[2].keys():
        print i
        print allData[2][i]
#     json_path = 'C:/Users/Administrator.PC-20150820KBVI/Desktop/modelsentences.pickle'
#     with open(json_path, "wb") as f:
#         pickle.dump(allData, f)
#     f.close()
    
    for i in allData.keys():
        tDict = allData[i]['trainData']
        if len(tDict['feature']) > 0:
            if len([x for x in tDict['result'] if x > 0]) > 0:
                #print i,len(tDict['feature']),len(tDict['result']),len(tDict['feature'])-len(tDict['result'])==0
                #print tDict['feature']
                for j in range(len(tDict['feature'])):
                    tmp = [i,tDict['result'][j]]
                    
                    print tmp + tDict['feature'][j]
    