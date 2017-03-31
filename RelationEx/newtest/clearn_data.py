#coding:utf-8
import sys
import xlrd
import re
from string import punctuation
reload(sys)
sys.setdefaultencoding('UTF-8')
def open_excel(file):
    """读取数据"""
    data = xlrd.open_workbook(file)
    return data

def excel_table_byindex(file,by_index=0):
    # 根据索引获取Excel表格中的数据
    #   参数:file：Excel文件路径  ，by_index：表的索引
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    dict={}
    for rownum in range( 1 ,nrows - 5):#略去第一行和后面五行
        row = table.row_values(rownum)
        row_dict={}
        for colnum in range(3,ncols):
            row_clonum=row[colnum].split("|")
            if colnum ==3:
                row_dict.setdefault("CUTsentence", row_clonum)
            elif colnum ==4:
                row_dict.setdefault("Labelsentence",row_clonum)
            elif colnum ==5:
                row_dict.setdefault("TAGsentence",row_clonum)
            elif colnum==6:
                row_dict.setdefault("QUOTEextraction",row_clonum)
            #print table.col_values(colnum)[0]#得到列名
            #row_dict.setdefault(table.col_values(colnum)[0],row[colnum])
            # print row[colnum]
        dict.setdefault(rownum,row_dict)
    return dict

def delete_line():
    """删除分割线 |"""


def delete_front_back_punctuation(TAGsentence):
    """删除标注句首尾符号"""
    delete_front_back_punc = []
    #英文punctuation---!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    #中问文标点-----！“”#￥&‘’（）*+，-。、：；《=》?？@【】、………——{}~
    # front_back_punc = [" ","","\\n","【","】","，","：","（","）","-","。","；","、","！"]
    chinese_punc="！“”#￥&‘’（）*+，-。、：；《=》?？@【】{}~"
    special_punc=["\\n"," ",""]
    #back_punc = ["(", ")", ":", "【", "】", " ", "；", "，", "（", "）", "\n", "：", "-", "。", ""]
    front = 0
    back = len(TAGsentence)
    TAGsentence1=[]
    for i in range(len(TAGsentence)):
        TAGsentence1.append(TAGsentence[i].strip())

    for i in range(len(TAGsentence1)):
        if TAGsentence[i].strip() not in chinese_punc and TAGsentence[i].strip() not in punctuation and TAGsentence[i].strip() not in special_punc:
            front = i
            break

    for i in range(1, len(TAGsentence1)):
        if TAGsentence[-i].strip() not in chinese_punc and TAGsentence[-i].strip() not in punctuation and TAGsentence[-i].strip() not in special_punc:
            back = len(TAGsentence) - i + 1
            break
    delete_front_back_punc = TAGsentence1[front:back]
    return delete_front_back_punc

def delete_middle_punctuation(TAGsentence):
    """删除句中除句号（。）、分号（；）、逗号（，）、换行（\n）之外的所有符合"""
    delete_middle=[]
    middle_keep_punc = u"。；，.;,"
    specical_punc=["\\n","{S}"]
    pattern = "[DPTRAC][1-9].*"
    for i in range(len(TAGsentence)):
        if TAGsentence[i].strip() in middle_keep_punc or TAGsentence[i].strip() in specical_punc or re.match(pattern,TAGsentence[i].strip()):
            delete_middle.append(TAGsentence[i])
    return delete_middle

def delete_cut_tag(QUOTEextraction):
    """删除分割标注（{Q}）"""
    QUOTEextraction= " ".join(QUOTEextraction).strip().split("{Q}")
    return QUOTEextraction

def preprocess_data(dict_sentences):
    """整理数据格式"""
    for serial_num in dict_sentences:
        for key in dict_sentences[serial_num]:
            if key=="TAGsentence":
                """去掉两头和中间不要的字符"""
                TAGsentence=delete_front_back_punctuation(dict_sentences[serial_num][key])
                TAGsentence=delete_middle_punctuation(TAGsentence)
                dict_sentences[serial_num]["TAGsentence"]=TAGsentence
            elif key=="QUOTEextraction":
                QUOTEextraction=delete_cut_tag(dict_sentences[serial_num][key])
                dict_sentences[serial_num]["QUOTEextraction"]=QUOTEextraction
    return dict_sentences

def get_preprocessed_dataA(data_path):
    """

    """
    data_path = data_path
    data = open(data_path)
    dict_sentences = excel_table_byindex(data_path)
    # 整理数据格式
    dict_preprocessed_sentences = preprocess_data(dict_sentences)
    return dict_preprocessed_sentences


"""
{句子序号：{
QUOTEextraction:报价抽取
Labelsentence:文本标注
TAGsentence：分句
CUTsentence:关键词筛选QUOTE
}}
"""
data_path=u"C:/Users/song/Desktop/data.xls"
#data=open(data_path)
#dict_sentences=excel_table_byindex(data_path)
# 整理数据格式
#dict_preprocessed_sentences=preprocess_data(dict_sentences)
dict_preprocessed_sentences=get_preprocessed_dataA(data_path)
