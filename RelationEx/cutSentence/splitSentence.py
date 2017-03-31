# -*- coding: utf-8 -*-
import pickle
from entityRelationExtractionClass7 import initializeModel
def getSeparatorSign():
    signBreak = [u'    ',u' ',u'。',u'.',u'。',u'．',u'；',u';',u'；',u'；',u'，',u',',u'，',u'，',u'    ',u' ']
    signBreak = signBreak + [u'', u'，', u':', u':', u';', u"'", u'"', u'|', u'\\', u'\\', u'*', u'&', u'^', u'%', u'$', u'#', u'@', u'!', u'~', u'`', u'', u'', u'。', u'、', u'＇', u'：', u'∶', u'；', u'?', u'‘', u'’', u'“', u'”', u'〝', u'〞', u'?', u'ˇ', u'﹕', u'︰', u'﹔', u'﹖', u'﹑', u'·', u'¨', u'…', u'.', u'?', u';', u'！', u'′', u'？', u'！', u'～', u'—', u'ˉ', u'｜', u'‖', u'＂', u'〃', u'｀', u'@', u'﹫', u'?', u'?', u'﹏', u'﹋', u'﹌', u'︴', u'々', u'﹟', u'#', u'﹩', u'$', u'﹠', u'&', u'﹪', u'%', u'*', u'﹡', u'﹢', u'﹦', u'﹤', u'‐', u'￣', u'ˉ', u'―', u'﹨', u'?', u'?', u'﹍', u'﹎', u'+', u'=', u'<', u'--', u'＿', u'_', u'-', u'\\', u'ˇ', u'~', u'﹉', u'﹊', u'（', u'）', u'〈', u'〉', u'?', u'?', u'﹛', u'﹜', u'', u'『', u'』', u'〖', u'〗', u'［', u'］', u'《', u'》', u'〔', u'〕', u'{', u'}', u'「', u'」', u'【', u'】', u'︵', u'︷', u'︿', u'︹', u'︽', u'_', u'﹁', u'﹃', u'︻', u'︶', u'︸', u'﹀', u'︺', u'︾', u'ˉ', u'﹂', u'﹄', u'︼', u'．', u'，', u'：', u'；', u'！', u'？', u'-', u'*', u"'", u'—', u'_', u"'", u'"', u'(', u'', u'', u')', u'[', u'', u'', u']', u'<', u'>', u'?', u'{', u'}', u'《', u'', u'', u'》', u'...', u'¨', u'‖', u'／', u'＆', u'～', u'§', u'→', u'|', u'\\', u'＋', u'－', u'±', u'×', u'÷', u'＝', u'≠', u'≡', u'≌', u'≈', u'＜', u'＞', u'≮', u'≯', u'≤', u'≥', u'％', u'', u'‰', u'∞', u'∝', u'√', u'∵', u'∴', u'∷', u'∠', u'⌒', u'⊙', u'○', u'△', u'⊥', u'∪', u'∩', u'∫', u'∑', u'°', u'′', u'″', u'＃', u'#', u'℃', u'＠', u'/', u'>', u'<', u'~', u'?', u'']
    lineBreak = [u'\\n',u'\\t',u'\n',u'\\t']
    separatorList = signBreak + lineBreak
    return separatorList

def isSeparator(tWord):
    breakList = getSeparatorSign()
    if tWord in breakList:
        return 1
    else:
        return 0

def isArmTagRight(wordIndex, sentence, armTag, haveBreak = False):
    #get the word behind the word of wordIndex
    
    #is or not the rightWord is armTag
    try:
        rt = 0
        if wordIndex + 1 < len(sentence):
            if haveBreak:
                breakList = getSeparatorSign()
                for tmp in sentence[wordIndex + 1:]:
                    if tmp in breakList:
                        if tmp and tmp == armTag:
                            rt = 1
                            break
                        elif tmp and tmp[0] == armTag:
                            rt = 1
                            break
                    else:
                        if tmp and tmp == armTag:
                            rt = 1
                        elif tmp and tmp[0] == armTag:
                            rt = 1
                        break
            else:
                rightWord = sentence[wordIndex + 1]
                if rightWord and rightWord == armTag:
                    rt = 1
                elif rightWord and rightWord[0] == armTag:
                    rt = 1
    except Exception as e:
        return 0
    else:
        return rt
def isArmTag(tWord, armTag):
    #armTag = [armTag1,armTag2]
    #get the word behind the word of wordIndex
    try:
        rt = 0
        if not hasattr(armTag, '__iter__'):
            armTag = [armTag]
        for tag in armTag:
            if tWord and tWord == tag:
                rt = 1
                break
            elif tWord and tWord[0] == tag:
                rt = 1
                break
    except Exception as e:
        return 0
    else:
        return rt

def isArmTagBoth(wordIndex, sentence, armTag, haveBreak = False):
    if wordIndex < len(sentence):
        rt1 = isArmTag(sentence[wordIndex],armTag[0])
        rt2 = isArmTagRight(wordIndex, sentence, armTag[1], haveBreak)
        if rt1 and rt2:
            return 1
        else:
            return 0
    else:
        return 0


#分句节点判断
def getSentenceShortList(sentence):
    sLength = len(sentence)
    sList = []
    #长句分句点判断
    for i in range(sLength):
        tWord = sentence[i]
        wordIndex = i
        #1、是否隔断点（如符号、空格、\n、\t等）
        if isSeparator(tWord):
            #是\n
            if isArmTag(tWord,armTag=u'\\n') or isArmTag(tWord,armTag=u'\n'):
                sList.append(i)
            #后面是序号
            elif isArmTagRight(wordIndex, sentence, armTag = 'C', haveBreak = False):
                sList.append(i)
            #后面是产品，且再后面有方向
            elif isArmTagBoth(wordIndex+1, sentence, armTag=['P','D'], haveBreak = False):
                sList.append(i)
            #是；且后面有方向或产品
            elif isArmTagBoth(wordIndex+1, sentence, armTag=[';','P'], haveBreak = False):
                sList.append(i)
            elif isArmTagBoth(wordIndex+1, sentence, armTag=[';','D'], haveBreak = False):
                sList.append(i)
            #后面是产品，且再后面有冒号
            elif isArmTagBoth(wordIndex+1, sentence, armTag=['P',':'], haveBreak = False):
                sList.append(i)
            #后面是方向，且再后面有冒号
            elif isArmTagBoth(wordIndex+1, sentence, armTag=['D',':'], haveBreak = False):
                sList.append(i)
    #长句分句操作
    if sList:
        if sList[-1] < sLength - 1:
            sList.append(sLength - 1)
        rtList = []
        i0 = 0
        tmp = []
        for i in range(sLength):
            tWord = sentence[i]
            wordIndex = i
            if i < sList[i0]:
                tmp.append(sentence[i])
            else:
                tmp.append(sentence[i])
                rtList.append(tmp)
                tmp = []
                i0 = i0 + 1
    else:
        rtList = [sentence]
        
    return rtList


def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
        rstring += unichr(inside_code)
    return rstring

#数据清洗#删除没有元素的list,删除必要元素外的其他元素
def delExtraTag(sentenceList,tagList):
    rtList = []
    for tList in sentenceList:
        if tList:
            tmpList = []
            for tmp in tList:
                if tmp in tagList:
                    tmpList.append(tmp)
            if tmpList:
                rtList.append(tmpList)
    return rtList

#对无符号序列进行分句
def getSentenceShortList2(sentence):
    sLength = len(sentence)
    sList = []
    #一句话包含两个及以上方向的，需要切分
    if len([x for x in sentence if isArmTag(x,armTag=[u'D'])]) > 1:
        #长句分句点判断
        for i in range(sLength):
            tWord = sentence[i]
            wordIndex = i
            if isArmTag(tWord,armTag=[u'R', u'T', u'A']):
                #R/T/A后面是产品、方向，再后面是R/T/A
                if isArmTagBoth(wordIndex+1, sentence, armTag=['P','D'], haveBreak = False):
                    if wordIndex + 3 < len(sentence):
                        if isArmTag(sentence[wordIndex + 3], armTag=[u'R', u'T', u'A']):
                            print tWord
                            sList.append(i)
                #R/T/A后面是方向,后面仍有元素的
                elif isArmTagRight(wordIndex, sentence, armTag = 'D', haveBreak = False):
                    if wordIndex + 2 < len(sentence):
                        print tWord
                        sList.append(i)
        #长句分句操作
        if sList:
            if sList[-1] < sLength - 1:
                sList.append(sLength - 1)
            rtList = []
            i0 = 0
            tmp = []
            for i in range(sLength):
                tWord = sentence[i]
                wordIndex = i
                if i < sList[i0]:
                    tmp.append(sentence[i])
                else:
                    tmp.append(sentence[i])
                    rtList.append(tmp)
                    tmp = []
                    i0 = i0 + 1
        else:
            rtList = [sentence]
    else:
        rtList = [sentence]
    return rtList

#对比两个二维列表的匹配率
def getRightParByList(pList,rList):
    p1List = []
    for tmp in pList:
        tmp.sort()
        p1List.append("|".join(tmp))
    
    r1List = []
    for tmp in rList:
        tmp.sort()
        r1List.append("|".join(tmp))
    
    rt = 0
    for tmp in p1List:
        if tmp in r1List:
            rt = rt + 1
            
    return [rt, len(r1List),len(p1List)]
    

#设计拼接规则


if __name__=='__main__': 
    #1、长句分句
    sentence = [u'C1', u'\\n', u'\\n', u'\uff0c', u'P1', u'T1', u'T2', u'\uff0c', u'R1', u'R2', u'\uff0c', u'\\n', u'C2', u'\\n', u'\\n', u'\\n', u'C3', u'\\n', u'\\n', u'C4', u'P2', u'T3', u'A1', u'R3', u'\uff1b', u'\\n', u'C5', u'P3', u'T4', u'A2', u'R4', u'\uff1b', u'\\n', u'C6', u'P4', u'T5', u'A3', u'R5', u'\uff1b', u'\\n', u'\\n', u'C7', u'P5', u'\uff0c', u'\uff0c', u'A4', u'\uff0c', u'T6', u'\uff0c', u'R6', u'\uff0c', u'\uff1b', u'\\n', u'C8', u'P6', u'\uff0c', u'\uff0c', u'A5', u'\uff0c', u'T7', u'\uff0c', u'R7']
    #print getSentenceShortList(sentence)
    
    json_path = 'E:/work/infoEx/model_sentences.pickle'
    with open(json_path, "rb") as f:
        allData = pickle.load(f)
    f.close()
    kkk = 0
    kk2 = 0
    tModel = initializeModel()
    rNum = [0,0,0,0,0,0,0,0]
    rnList = []
    for i in allData.keys():
        tDict = allData[i]['trainData']
        if len([x for x in tDict['result'] if x > 0]) > 0:
            sentence = tDict['sentence']
            #句子第一次分句
            sentenceList = getSentenceShortList(sentence)
            vType = [u'D',u'P',u'T',u'R',u'A']
            tagList = ['%s%s'%(x,y) for x in vType for y in range(35)]
            
            print delExtraTag(sentenceList,tagList)
            #数据清洗，删去非模型元素
            sentence0 = delExtraTag(sentenceList,tagList)
            print 'start'
            #获取预测的结果
            pList = []
            for tmp in sentence0:
    #                     tmp0 = tModel.getEntityRelationResult("|".join(tmp))
    #                     for st in tmp0:
    #                         pList.append(st.split('|'))
                #二次分句
                tmpList = getSentenceShortList2(tmp)
                for tmp2 in tmpList:
                    tmp0 = tModel.getEntityRelationResult("|".join(tmp2))
                    for st in tmp0:
                        pList.append(st.split('|'))
            print 'pList:%s'%pList
            #获取正确的结果
            rList = []
            for tmp in allData[i]['QUOTEextraction']:
                if len(tmp) > 3:
                    rList.append([x for x in tmp if x])
            print rList
            rpNum = getRightParByList(pList,rList)
            if rpNum[0] == rpNum[1] and rpNum[1] == rpNum[2]:
                #正确预测的句子数量
                rNum[0] = rNum[0]+1
                
            if rpNum[1] > 0:
                #有正确的句子数量
                rNum[3] = rNum[3]+1
                if rpNum[0] == rpNum[1] and rpNum[1] == rpNum[2]:
                    #有正确的句子预测正确的数量
                    rNum[2] = rNum[2]+1
                else:
                    rnList.append(i)
            #句子的数量
            rNum[1] = rNum[1]+1
            #正确预测的记录数
            rNum[4] = rNum[4]+rpNum[0]
            #正确的记录数
            rNum[5] = rNum[5]+rpNum[1]
            #预测的记录数
            rNum[6] = rNum[6]+rpNum[2]
            print rpNum,rNum
            
            print '一共%s个句子，正确预测了%s个，'%(rNum[1],rNum[0])
            print '其中有结果的句子有%s个，准确预测了%s个'%(rNum[3],rNum[2])
            print '正确的记录有%s个，预测的有%s个，准确的有%s个'%(rNum[5],rNum[6],rNum[4])
            
    print rnList
            
    #ll = [u'D1', u'P1', u'T1', u'P2', u'D2', u'T2', u'R1', u'T3', u'R2', u'T4', u'R3', u'T5', u'R4', u'T6', u'R5', u'T7', u'R6', u'T8', u'R7', u'D3', u'T9', u'P3']
    #ll = [u'P1', u'D1', u'T1', u'R1', u'T2', u'R2', u'T3', u'R3', u'T4', u'R4', u'T5', u'R5', u'T6', u'R6', u'T7', u'R7', u'P2', u'D2', u'T8', u'R8', u'T9', u'R9', u'T10', u'R10', u'T11', u'R11', u'T12', u'R12', u'T13', u'R13', u'T14', u'R14', u'P3', u'D3', u'T15', u'R15', u'T16', u'R16', u'D4', u'P4', u'T17', u'R17', u'T18', u'R18', u'T19', u'R19', u'D5', u'P5', u'T20', u'R20', u'T21', u'R21', u'T22', u'R22', u'P6', u'T23', u'R23', u'P7', u'D6', u'T24', u'R24', u'T25', u'R25', u'T26', u'R26', u'T27', u'R27', u'P8', u'D7', u'T28', u'R28', u'T29', u'R29']
    #print getSentenceShortList2(ll)
    
    
    
    
#     #数据拼接判断
#     def getSentenceAllList(sentenceList):
        #数据填补原则：
        #1、只有当数据缺失D或P时才填补
        #2、只有判断出并列结构时才向前填补
        #3、
        

#         #元素齐全
#         #元素不全
#         #只有1个元素的，3种选择：忽略、向后靠拢，向前靠拢
#         #只有2个元素的，
#         #有3个元素的时候，基于补项的靠拢，观察前方是否有项可填补。
        






