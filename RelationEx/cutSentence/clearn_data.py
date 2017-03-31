#coding:utf-8
'''
Created on 2016年10月17日

@author:sunxianpeng
'''
import sys
import xlrd
import re
import pickle
from string import punctuation

reload(sys)
sys.setdefaultencoding('UTF-8')

class clearn_data(object):
    def __init__(self):
        """Constructor
        """
    pass

    def open_excel(self,file):
        """读取数据"""
        data = xlrd.open_workbook(file)
        return data

    def excel_table_byindex(self,file, by_index=0):
        # 根据索引获取Excel表格中的数据
        #   参数:file：Excel文件路径  ，by_index：表的索引
        data = self.open_excel(file)
        table = data.sheets()[by_index]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        dict = {}
        for rownum in range(1, nrows - 5):  # 略去第一行和后面五行
            row = table.row_values(rownum)
            row_dict = {}
            for colnum in range(ncols):
                row_clonum = row[colnum].split("|")
                if colnum==0:
                    row_dict.setdefault("sentence",row_clonum)
                elif colnum==1:
                    row_dict.setdefault("sample", row_clonum)
                elif colnum==2:
                    row_dict.setdefault("punctuation", row_clonum)
                elif colnum == 3:
                    row_dict.setdefault("CUTsentence", row_clonum)
                elif colnum == 4:
                    row_dict.setdefault("Labelsentence", row_clonum)
                elif colnum == 5:
                    row_dict.setdefault("TAGsentence", row_clonum)
                elif colnum == 6:
                    row_dict.setdefault("QUOTEextraction", row_clonum)
                    # print table.col_values(colnum)[0]#得到列名
                    # row_dict.setdefault(table.col_values(colnum)[0],row[colnum])
                    # print row[colnum]
            dict.setdefault(rownum, row_dict)
        return dict

    def delete_line(self):
        """删除分割线 |"""

    def delete_front_back_punctuation(self,TAGsentence):
        """删除标注句首尾符号"""
        delete_front_back_punc = []
        # 英文punctuation---!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        # 中问文标点-----！“”#￥&‘’（）*+，-。、：；《=》?？@【】、………——{}~
        # front_back_punc = [" ","","\\n","【","】","，","：","（","）","-","。","；","、","！"]
        chinese_punc = "！“”#￥&‘’（）*+，-。、：；《=》?？@【】{}~"
        special_punc = ["\\n", " ", ""]
        # back_punc = ["(", ")", ":", "【", "】", " ", "；", "，", "（", "）", "\n", "：", "-", "。", ""]
        front = 0
        back = len(TAGsentence)
        TAGsentence1 = []
        for i in range(len(TAGsentence)):
            TAGsentence1.append(TAGsentence[i].strip())

        for i in range(len(TAGsentence1)):
            if TAGsentence[i].strip() not in chinese_punc and TAGsentence[i].strip() not in punctuation and TAGsentence[
                i].strip() not in special_punc:
                front = i
                break

        for i in range(1, len(TAGsentence1)):
            if TAGsentence[-i].strip() not in chinese_punc and TAGsentence[-i].strip() not in punctuation and \
                            TAGsentence[-i].strip() not in special_punc:
                back = len(TAGsentence) - i + 1
                break
        delete_front_back_punc = TAGsentence1[front:back]
        return delete_front_back_punc

    def delete_middle_punctuation(self,TAGsentence):
        """删除句中除句号（。）、分号（；）、逗号（，）、换行（\n）之外的所有符合"""
        delete_middle = []
        middle_keep_punc = u"。；，.;,"
        specical_punc = ["\\n", "{S}"]
        pattern = "[DPTRAC][1-9].*"
        for i in range(len(TAGsentence)):
            if TAGsentence[i].strip() in middle_keep_punc or TAGsentence[i].strip() in specical_punc or re.match(
                    pattern, TAGsentence[i].strip()):
                delete_middle.append(TAGsentence[i])
        return delete_middle

    def delete_cut_tag(self,QUOTEextraction):
        """删除分割标注（{Q}）"""
        result=[]
        QUOTEextraction = " ".join(QUOTEextraction).strip().split("{Q}")
        for i in range(len(QUOTEextraction)):
            list=QUOTEextraction[i].split(" ")
            result.append(list)
        print result
        return result

    def preprocess_data(self,dict_sentences):
        """整理数据格式"""
        for serial_num in dict_sentences:
            for key in dict_sentences[serial_num]:
                if key == "TAGsentence":
                    """去掉两头和中间不要的字符"""
                    TAGsentence = self.delete_front_back_punctuation(dict_sentences[serial_num][key])
                    TAGsentence = self.delete_middle_punctuation(TAGsentence)
                    dict_sentences[serial_num]["TAGsentence"] = TAGsentence
                elif key == "QUOTEextraction":
                    QUOTEextraction = self.delete_cut_tag(dict_sentences[serial_num][key])
                    dict_sentences[serial_num]["QUOTEextraction"] = QUOTEextraction
        return dict_sentences

    def get_preprocessed_dataA(self,data_path):
        """
        得到处理后数据
        """
        data_path = data_path
        data = open(data_path)
        dict_sentences = self.excel_table_byindex(data_path)
        print dict_sentences
        errorList = []
        allData = dict_sentences
        for i in allData.keys():
            text1 = []
            text2 = []
            for j1 in allData[i]['TAGsentence']:
                if j1 and j1 != u'{S}':
                    text1.append(j1)
            for j2 in allData[i]['Labelsentence']:
                if j2:
                    text2.append(j2)
            #print text2
            #print text1
            if text1 and text2:
                for j in range(len(text2)):
                    if text2[j] == text1[0]:
                        break
                for k in range(len(text1)):
                    if text2[k+j] != text1[k]:
                        errorList.append(i)
                        break
        print errorList
        
        # 整理数据格式
        dict_preprocessed_sentences = self.preprocess_data(dict_sentences)
        return dict_preprocessed_sentences

    def store_to_json(self,json_path,dict_data):
        """将数据到本地json"""
        with open(json_path, "wb") as f:
            pickle.dump(dict_data, f)
        f.close()
    def read_json(self,json_path):
        """读取本地json数据"""
        with open(json_path) as f:
            dataDict = pickle.load(f)
        f.close()
        return dataDict
if __name__=='__main__':
    """
    {句子序号：{
    sentence:原句子
    sample:（对应名字）
    punctuation:（对应名字）
    QUOTExtraction:报价抽取
    Labelsentence:文本标注
    TAGsentence：分句
    CUTsentence:关键词筛选
    }}
    """
    data_path=u"E:/work/infoEx/cutsen_data.xls"
    json_path=r"E:/work/infoEx/preprocessed_sentences.pickle"
    # 整理数据格式
    clearn_data=clearn_data()#get_preprocessed_dataA(data_path)
    dict_preprocessed_sentences=clearn_data.get_preprocessed_dataA(data_path)
    clearn_data.store_to_json(json_path,dict_preprocessed_sentences)
    #data=clearn_data.read_json(json_path)
    #print data
    print "存储完成"
    factor = ['C','D','P','T','R','A','Z','Y','X','U']#,'。','；']
    maxFactor = 30
    vPunctuation = [u'。',u'.',u'。',u'．',u'；',u';',u'；',u'；',u'，',u',',u'，',u'，',u'    ',u' ',u'\\n']
    vWordList = vPunctuation
    vType = factor[:5]
    for i in vType:
        for j in range(maxFactor):
            vWordList.append('%s%s'%(i,j))
    
    import pickle
    fd = u'E:/work/infoEx/preprocessed_sentences.pickle'
    with open(fd, 'rb') as f:
        allData = pickle.load(f)
    errorList = []
    for i in allData.keys():
        sentence0 = allData[i]['TAGsentence']
        tDict = {'sentence':[],'result':[]}
        num = 0
        for k in range(len(sentence0)):
            tmp = sentence0[k]
            if tmp in vWordList:
                tDict['sentence'].append(tmp)
                tDict['result'].append(0)
                num = num + 1
            elif tmp.strip() in vWordList:
                tDict['sentence'].append(tmp.strip())
                tDict['result'].append(0)
                num = num + 1
            if sentence0[k].strip() == u'{S}' and num > 0:
                tDict['result'][num - 1] = 1
        #index=1
        sentence = tDict['sentence']
#         if sentence and sentence != ['']:
#             for factorID in range(len(sentence)):
#                 aa=cutvector.fvector(sentence, factorID)
        allData[i]['trainData'] = tDict
    json_path=r"E:/work/infoEx/model_sentences.pickle"
    with open(json_path, "wb") as f:
        pickle.dump(allData, f)
    f.close()
    