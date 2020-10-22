#  -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:01:25 2020
@author: huzey

读取Rank List2 产生的csv文件，并下载为txt文件，里面包含time comment两个类别
csv文件和产生的txt文件在同一文件夹下
程序会自动为不同分区建立子文件夹
使用方法：在标记处直接修改保存地址，运行后就可得到一堆csv文件
！！！请勿随意改动
为防止IP被屏蔽，爬取一个分区休息3min
针对2020.10.16改版之后的新B站排行榜
https://www.bilibili.com/v/popular/rank/all
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import operator
import numpy as np
   

# 获取url
def getHTMLText(url):
    try:
        # print("获取url当中")
        re=requests.get(url,timeout=5000)
        re.raise_for_status()
        re.encoding=re.apparent_encoding
        print("获取url完成")
        return re.text
    except:
        print("获取Url失败")

def parsePage(text):
    try:
        # print("解析文本...")
        keyStr = re.findall(r'"cid":[\d]*',text)
        # B站有两种寻址方式，一种是API，一种是正则表达式搜索，第二种多一些
        if not keyStr:
            # 若列表为空，则等于“False”
            keyStr = re.findall(r'cid=[\d]*', text)
            key = eval(keyStr[0].split('=')[1])
        else:
            key = eval(keyStr[0].split(':')[1])
        commentUrl = 'https://comment.bilibili.com/' + str(key) + '.xml'  
        #  弹幕存储地址
        # print("获取弹幕")
        commentText=getHTMLText(commentUrl)
        soup = BeautifulSoup(commentText, "html.parser")
        # soup2=BeautifulSoup(text,"html.parser")
        commentList={}
        
        # find()方法，获取文本，去掉空格
        for comment in soup.find_all('d'):
            time=float(comment.attrs['p'].split(',')[0])
            # tag.attrs（标签属性，字典类型）
            commentList[time]=comment.string
        newDict=sorted(commentList.items(),key=operator.itemgetter(0))
        # 字典排序
        commentList=dict(newDict)
        print("解析文本完成")
        return commentList,key
    except:
        print("解析失败")
        
        
 
def float2time(f):
    timePlus=int(f)
    m=timePlus//60
    s=timePlus-m*60
    return str(m)+':'+str(s).zfill(2)
 
def ioFunc(commentList,root):
    print("写入文本中...")
    path = root + '.txt'
    print(path)
    f = open(path, 'w',encoding='utf-8')
    ws = "{:7}\t{}\n".format('time', 'comment')
    f.write(ws)
    lastTime=0
    for time,string in commentList.items():# 记得items()
        lastTime = float2time(time)
        ws = "{:7}\t{}\n".format(lastTime,string)
        f.write(ws) 
        #  手动换行



# 并非要爬取所有内容
#已经没有月周日排行榜了
"""在此处修改要爬取的分区"""
typeItem =  ['动画','音乐','舞蹈','游戏','科技','生活','鬼畜','时尚']
import time 
import re     
import os
"""在此处修改地址"""
filepath = 'D:/bilibili/2020_10_21/'

"""每次爬取记得修改分区（因为一次爬取太多会被B站屏蔽IP，烦死了）"""
for typetemp in typeItem :#  在这里修改分区   typeItem4   
    filename = filepath + str(typetemp) + '.csv'
    print(filename)
    with open(filename,encoding='utf_8_sig') as file:
        BVInfo = pd.read_csv(file)
        BVUrl = BVInfo['url']
        Title = BVInfo['tittle']
        AllTittle=[]
        for OneUrl in BVUrl:
            #  .values 去掉可恶的name，dtype
            OneTittle = BVInfo[BVInfo.url== OneUrl]['tittle'].values 
            # print("标题：",OneTittle,type(OneTittle))
            print('网址：',OneUrl,type(OneUrl))
            temp_url = re.search(r"(?<=https://www.bilibili.com/video/)\S+",OneUrl).group() # 使用group(num) 或 groups() 匹配对象函数来获取匹配内容。
            # print(temp_url)
            StrOneTittle = str(OneTittle)
            
            text=getHTMLText(OneUrl)
            
            try:
                commentList,key=parsePage(text)
            except:
                print("解析跳过")
                # 跳过解析失败的
                continue    
            # 判断是否有文件夹存在，如果没有就创建
            DocPath  = filepath+str(typetemp)+ '/'
            
            if not os.path.exists(DocPath):
                os.makedirs(DocPath) 
                print(DocPath)
                
                
            SavePath =  DocPath + str(key)
            if not os.path.exists(  SavePath + '_'+temp_url ):
                # 弹幕编号 + BV号
                ioFunc(commentList,SavePath +'_'+temp_url)
                print("Finish.")

    time.sleep(180) #表示秒  爬取一个分区休息3min
    print("----Pause---3min----")








