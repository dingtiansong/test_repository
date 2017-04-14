# -*- coding: utf-8 -*-
'''
@Time : 2017/4/11 17:14

@author: song
'''
from sumdata import MatchFactor
import pickle
from tagFactor import TagFactor

if __name__=='__main__':
    newdatapath2 = 'D:\\work\\tags\\data\\newdata3.pkl'
    with open(newdatapath2, 'rb') as f:
        data = pickle.load(f)
    mf=MatchFactor()
    tf=TagFactor()
    sentence_index, all_redo_data=mf.gether_data(data)
    dict=mf.sentence_order(data,sentence_index)
    total_dict=mf.create_total_Dict(data)
    allsentence=[]

    # for i in all_redo_data:
    #     for j in i[1]:
    #         print j[0],j[1],j[2],j[3]
    #         print '匹配位置：', dict[str(i[0])].find(j[0])+13, dict[str(i[0])].find(j[0])+len(j[0])+13
    #         print dict[str(i[0])][j[2]-13:j[3]-13],'&&&&&&&&'
    #     print '-------------------------------------------'
    #     print dict[str(i[0])]
    #     allsentence.append(dict[str(i[0])])
    #     print '*******************************************'


    test_sentence=u'''湖滨农商行赵磊(1307956997)  14:53:08
 3.24借七天1亿，押利率'''
    test_sentence1=u'''
出  AA存单  3M4.95  ！
出  AA存单  3M4.95  ！
出  AA存单  3M4.95  ！'''

    test_sentence2='''玫瑰诚借 1-7天  2亿，求小窗玫瑰玫瑰'''

    test_sentence3='''【经理】陈立广（唐山银行）(94696767)  14:32:17
 唐山银行（1900亿+城商行）近期业务：
1.【收】收资金，收资金，收资金，任意期限，价格美丽。欢迎各位领导同事小窗。
2.【出】各期限高高高价理财（4.6%-4.8%）,4.6%-4.8%,3w,7.2个亿,4千万,5亿,1亿
联系人：陈立广，电话：15176574515（微信同号）
            柳清：15130574269'''
    test_sentence4=' 3.24借7天1.2亿，押利率'
    needtag=['D','P','T']


    for i in all_redo_data:
        sentence3= dict[str(i[0])]
        sentence1= '\n'.join(sentence3.split('\n')[1:])
        sentence2 = sentence3.split('\n')[0]
        print sentence2 ,'^^^^^^^^^^^^^^^^^^'
        print sentence1
        final_tag_sentence, orig_factor, factor_list, sortkey\
            =mf.generate_tag_sentence(total_dict,needtag,sentence1)
        print final_tag_sentence
        print orig_factor
        print factor_list
        print  sortkey
        print '-------------------------------------------------------------------------------------'

    # for i in all_redo_data:
    #     test_sentence= dict[str(i[0])]
    #     price_regx = re.compile(r'[0-9]{0,2}\.[0-9]{0,3}%')
    #     period_regx = re.compile(r'[0-9]\.?[0-9]*[个千]?[ewEW万亿]')
    #     print 'price match:', price_regx.findall(test_sentence)
    #     print 'period match:', period_regx.findall(test_sentence)
    #     print test_sentence

    # price_regx = re.compile(r'[0-9]{0,2}\.[0-9]{0,3}%')
    # amount_regx=re.compile(r'[0-9]\.?[0-9]*[千个]?[weWE万亿]')
    # temp_regx=re.compile(r'亿')
    # print temp_regx.findall(test_sentence3)
    # zz= amount_regx.findall(test_sentence3)
    # print price_regx.findall(test_sentence3)
    # print zz
    # print mt.endpos
    # import sys
    # print sys.getdefaultencoding()
    # for i in zz:
    #     print test_sentence3.find(i),test_sentence3.find(i)+len(i)
    #     print test_sentence3[test_sentence3.find(i):test_sentence3.find(i)+len(i)]