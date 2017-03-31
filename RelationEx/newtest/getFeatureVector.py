#-*- coding:utf-8 -*-
'''
Created on 2016年10月12日

@author: Administrator
'''
from collections import Counter

class getFeatureVector(object):
    #符号序列,句号、分号、逗号、换行,中文半角、英文半角、中文全角、英文全角
    vPunctuation = ['。','.','。','．','；',';','；','；','，',',','，','，','\n']
    #vType = ['C', 'D', 'P', 'T', 'R', 'A']
    vType = ['C', 'D', 'P', 'T', 'A']
    vTypeDict = {'C':0,'D':1,'P':2, 'T':3 , 'A':4}
    maxFactor = 30
    vWordList = []
    serialTag = 'C'
    verbTag = 'D'
    nounTag = 'P'
    timeTag = 'T'
    amountTag = 'A'
    
    def __init__(self, vType = [], num = 0):
        '''
        Constructor
        '''
        if vType:
            self.vType = vType
            #序号词标记
            self.serialTag = vType[0]
            #方向词标记
            self.verbTag = vType[1]
            #产品词标记
            self.nounTag = vType[2]
            #期限词标记
            self.timeTag = vType[3]
            #金额或利率词标记
            self.amountTag = vType[4]
            #词性字典
            self.vTypeDict = {vType[0]:0,vType[1]:1,vType[2]:2,vType[3]:3,vType[4]:4}
        if num:
            self.maxFactor = num
        
        #元素序列
        self.vWordList = self.vPunctuation
        for i in self.vType:
            for j in range(self.maxFactor):
                self.vWordList.append('%s%s'%(i,j))
    
    # The word itself    当前目标节点词本身
    def getWordID(self, tWord):
        try:
            wordIDList = self.vWordList.index(tWord)
        except Exception as e:
            print e
            return ''
        else:
            return wordIDList
        
    # POS-tags    当前目标结点词的词性标记
    def getWordTags(self, tWord):
        if tWord in self.vWordList:
            if tWord in self.vPunctuation:
                return 0
            else:
                return self.vTypeDice[tWord[0]]
        else:
            return ''
    
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
    def getIsDLeft(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in sentence[:wordIndex]:
                if i[0] == self.verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    
    def getIsDRight(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            #如果tWord为最后一个词，则sentence[minId+1:] == []
            for i in sentence[wordIndex+1:]:
                if i[0] == self.verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # Serial-right    如果当前目标结点词的右边是词语“序号”，则设为1否则设为0    
    def getIsSerialRight(self, tWord, sentence):
        try:
            wordIndex = sentence.index(tWord)
            if sentence[wordIndex+1] == self.serialTag:
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
    def getIsExistVerb(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in sentence[:wordIndex]:
                if i[0] == self.verbTag:
                    tmp = 1
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # M_F_DT    当前词之前的句子中第一个是否是DT    是否D\是否P\是否T\是否A\是否R
    def getIsDFirst(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in sentence[:wordIndex]:
                if i[0] in self.vType[1:]:
                    tmp = self.vTypeDict[i[0]]
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # L_V_N    当前词之前的句子中第一个方向词前是否有产品词标识
    def getIsPLeftD(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            for i in range(wordIndex):
                if sentence[i][0] == self.nounTag:
                    PIndex = i
                    for j in range(PIndex,wordIndex):
                        if sentence[j][0] == self.verbTag:
                            tmp = 1
                            break
                    break
        except Exception as e:
            print e
            return 0
        else:
            return tmp
    # CLASS    当前词之前的句子是否是可单独解析块    是否有4元素
    def getIsFourTag(self, tWord, sentence):
        try:
            tmp = 0
            wordIndex = sentence.index(tWord)
            tDict = {}
            for i in sentence[:wordIndex]:
                if i[0] in self.vType[1:]:
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

if __name__=='__main__': 
    sentence16=['D1','P1','T1','R1','T2','R2','T3','R3','T4','R4','T5','R5','T6','R6','T7','R7','T8','R8','T9','R9','T10','R10']
    vType = ['C','D','P','T','R']
    num = 20
    vector = getFeatureVector(vType, num)
    sentence = sentence16
    for tWord in sentence:
        print '-----------------'
        print (vector.getIsDFirst(tWord, sentence)
            ,vector.getIsDLeft(tWord, sentence)
            ,vector.getIsDRight(tWord, sentence)
            ,vector.getIsExistVerb(tWord, sentence)
            ,vector.getIsFirstWord(tWord, sentence)
            ,vector.getIsFourTag(tWord, sentence)
            ,vector.getIsLastWord(tWord, sentence)
            ,vector.getIsPLeftD(tWord, sentence)
            ,vector.getIsSerialRight(tWord, sentence)
            ,vector.getWordID(tWord)
            ,vector.getWordTags(tWord)
            )
    
    