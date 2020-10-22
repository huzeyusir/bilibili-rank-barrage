# -*- coding: utf-8 -*-

"""
Created on Wed May 20 16:49:37 2020
BILIBILI 视频列表信息爬取
@author: huzey
"""
"""
爬取思路
1.分别在不同排行榜下爬取信息
2.信息包含有：视频BV号,BV地址，视频排名，视频名称，综合评分，up主名称
3.将这些信息保存在一个DataFrame里，最后保存为Excel表格
使用方法：在标记处直接修改保存地址，运行后就可得到一堆csv文件
！！！请勿随意改动
针对2020.10.16以后，改版的新的B站排行榜网页
https://www.bilibili.com/v/popular/rank/all
"""
import requests
import re
from bs4 import BeautifulSoup
import traceback

class Spider:#常用的爬取方法的简单封装
    def __init__(self,url):
        self.url=url
        
    def getHTML(self):#获取html的对应代码
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
       
        try:
            response=requests.get(url=self.url,headers=headers,timeout=20)
            response.raise_for_status()
            response.encoding="utf_8_sig"
            return response.text
        except:
            return "网页访问失败"
        
    def setSoup(self):#获取soup对象
        html=self.getHTML()
        self.soup=BeautifulSoup(html,'html.parser')
    
    def findTag(self,tagName):#按照标签名查找标签
        return self.soup.find_all(tagName)
    
    def findTagByAttrs(self,tagName,attrs):
        return self.soup.find_all(tagName,attrs)
    
    def getBeautifyHTML(self):
        return self.soup.prettify()
"""
# 大人，时代变了！
def getURLFromBilibili():# 获取各种各样排行的榜单的信息
    date={
        #1:'日排行',
        3:'三日排行',
        7:'周排行',
        30:'月排行'
    }
    #总共收集8个分区的弹幕
    areatype={
        #0:'全站',
        1:'动画',  
        #168:'国漫相关',
        3:'音乐',
        129:'舞蹈',
        4:'游戏',
        36:'科技',
        #188:'数码',
        160:'生活',
        119:'鬼畜',
        155:'时尚',
        #5:'娱乐',
        #181:'影视'
    }
    ranktype={
       'all':'全站',
       #'origin':'原创'
    }
    submit={
        '0':'全部投稿',
        #'1':'近期投稿'
    }  
    urlDict={}#存放相应url的字典
    for ranktypeItem in ranktype.keys():
        for areatypeItem in areatype.keys():
            for submitItem in submit.keys():
                for dateTypeItem in date.keys():
                    title=ranktype[ranktypeItem]+'_'+areatype[areatypeItem]+'_'+submit[submitItem]+'_'+date[dateTypeItem]
                    destinaTionUrl='https://www.bilibili.com/ranking/{}/{}/{}/{}'.format(ranktypeItem,areatypeItem,submitItem,dateTypeItem)
                    urlDict[title]=destinaTionUrl
                    
    return urlDict
"""

def getURLFromBilibili():
    areatype={
        'all':'全站',
        'bangumi':'番剧',
        'guochan':'国产动画',
        'guochuang':'国创相关',
        'documentary':'纪录片',
        'douga':'动画',
        'music':'音乐',
        'dance':'舞蹈',
        'game':'游戏',
        'technology':'科技',  #后改名为知识
        'digital':'数码',
        'life':'生活',
        'food':'美食',
        'kichiku':'鬼畜',
        'fashion':'时尚',
        'ent':'娱乐',
        'cinephile':'影视',
        'movie':'电影',
        'tv':'电视剧',
        'origin':'原创',
        'rookie':'新人',
    }
    urlDict={}#存放相应url的字典
    for areatypeItem in areatype.keys():
        title=areatype[areatypeItem]
        destinaTionUrl='https://www.bilibili.com/v/popular/rank/{}'.format(areatypeItem)
        urlDict[title]=destinaTionUrl         
    return urlDict


def getPage(url):
    # 爬取单个页面,核心代码，返回页面的list
    spider=Spider(url)
    spider.setSoup()
    itemList=spider.findTagByAttrs('li','rank-item')
    pageContentList=[]
    for item in itemList:
       
        pageContentItem=[]
        for title in item.find_all('a','title'):
            pageContentItem.append(title.string)
            #print(title.string)
               
        for bvurl in item.find_all('a',class_="title"):
            BVurl=bvurl.get("href")
            tempadd = 'https:'
            pageContentItem.append(tempadd + BVurl)
            #print(BVurl)   
          
        for playnum in item.find_all('span','data-box'):
            pattern=r">([^<]+)<"
            n=re.findall(pattern,playnum.__str__())[0]
            pageContentItem.append(n)
            #print(n)

        
        pageContentItem.append(item.find_all('div','pts')[0].div.string)
        pageContentList.append(pageContentItem)
        
    return pageContentList   


urlDict = getURLFromBilibili()
import pandas as pd 
import os

"""修改文件存储地址"""
out_path="D:/bilibili/2020_10_21/"

if not os.path.exists(out_path):
    os.makedirs(out_path)
    print("Path:",out_path)

for urlName in urlDict:
    print("正在处理"+urlName+"页面...")
    url=urlDict[urlName]
    #在字典里查找
    pageList=getPage(url)
    #print(pageList) 
    
    PageName = str(urlName)    
    BvDataFrame = pd.DataFrame(pageList,columns=['tittle','url',"view",'barrage','uploader','score'])          
    BvDataFrame.to_csv(out_path+PageName+'.csv',index=False,encoding='utf_8_sig')


