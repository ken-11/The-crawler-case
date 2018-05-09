# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:57:47 2018

@author: Administrator
"""
from selenium import webdriver
import os
import time
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import hashlib
import logging
import sys
from collections import deque

# 获取logger的实例
logger = logging.getLogger("taonvlang")
# 指定logger的输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# 文件日志，终端日志
file_handler = logging.FileHandler("taonvlang.log")
file_handler.setFormatter(formatter)

#consle_handler = logging.StreamHandler(sys.stdout)
#consle_handler.setFormatter(formatter)
# 设置默认的级别
logger.setLevel(logging.INFO)

# 保存已经处理过的URL链接
downloadpages = deque()

def mkdir(path):
# 创建本地路径
    if not os.path.exists(path):
        os.makedirs(path)
        print(path,"已创建")

url = "https://mm.taobao.com/search_tstar_model.htm?"
outputPath = "mPhotos/"

# 滚屏操作
def scroll_to_bottom(driver):
    for _ in range(2): # 让它滚屏两次
        try:
            # 浏览器执行一段JS代码完成滚屏操作
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            logger.info("滚屏")
        except:
            break
        
def hashStr(strInfo):
    """
     对字符串做HASH
    """
    h = hashlib.sha256() # md5,sh1,sha256
    h.update(strInfo.encode("utf-8"))
    return h.hexdigest()        
        
def saveImg(url, LocalPath):
    #把图片下载到本地
    global downloadpages
    #在已经爬取的队列中查找来去重
    if url in downloadpages:
        logger.error(url+"已经下载")
        return None
    downloadpages.append(url) # 把已经处理过的链接放入队列
    try:
        data = urlopen("http:"+url.strip()).read()
        imgName = LocalPath+'/'+hashStr(time.ctime())+'.jpg'
        with open(imgName,"wb") as f:
            f.write(data)
    except:
        logger.error("downloaded error in"+url)

# 获取美女主页的图片
def getImgs(url,name,city):
    # 保证本地的美女文件夹已经创建
    mkdir(outputPath+name+"--"+city)
    try:
        # urlopen 
        #可以用basicSpider中的downloadHtml
        data = urlopen("http:"+url).read().decode("GBK")
        #匹配真正图片的URL
        pattern = re.compile('<img[\s\S]*?src="([\s\S]*?)"')
        imgsUrl = re.findall(pattern, data)
        
        # 在入待爬队列之前去重
        imgsUrl = list(set(imgsUrl))
        num = 1
        for it in imgsUrl:
            logger.info(it)
            saveImg(it, outputPath+name+"--"
                    +city)
            num += 1   
            if num > 4: #人为的控制每个模特只抓少量的图片数据
                break
    except:
        logger.error("getImgs error")

if __name__ == "__main__":  
    # 准备工作
    driver = webdriver.Chrome()
    # 创建本地的路径
    mkdir(outputPath)    
    # 打开主页
    driver.get(url)
    scroll_to_bottom(driver)
    time.sleep(1)    
    
    # 获取信息，直到获取成功
    num = 1
    while True:
        if num > 3:
            break
        try:
            # 从pagesource中提取出想要抓取的女郎的信息
            pattern = re.compile('<li class="item">[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?<span class="name">([\s\S]*?)</span>[\s\S]*?<span class="city">([\s\S]*?)</span>')
            girlsItem = re.findall(pattern,
                                   driver.page_source)
            for it in girlsItem:
                logger.info(it[0]+" "+it[1]+" "+it[2])
                # 爬取主页信息
                getImgs(it[0], it[1], it[2])
        except:
            logger.info("没有获取到首页信息")
            continue # 一页出错，处理下一页
        #下一页跳转
        driver.find_element_by_class_name(
                    'page-next').click()
        scroll_to_bottom(driver)
        time.sleep(1)
        num += 1
    
    # 移出日志handler
    logger.removeHandler(file_handler)
             
    
        
    
    

        



