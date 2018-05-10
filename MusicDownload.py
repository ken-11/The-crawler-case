Skip to content
from __future__ import unicode_literals
This repository
Search
Pull requests
Issues
Marketplace
Explore
    @ken - 11
Sign out
0
0 0 ken - 11 / Music - download
    Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights  Settings
Music - download / MusicDownload.py
4076c59  a day ago


@ken - 11 ken - 11 Update MusicDownload.py
105 lines(90 sloc)  2.94 KB
# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Sun Apr 22 12:14:55 2018
@author: ken
"""
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import urllib
import sys
mname = ''
# 获取歌曲页面的URL


def get_url(url, key):
    driver = webdriver.Chrome()
#    url = input('输入连接地址')
    driver.get(url)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[1]/div[1]/input').send_keys(key)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[1]/div[1]/div/i').click()

    result_url = driver.current_url  # 获取当前网页的URL
    print(result_url)
    driver.close()
    driver.quit()
    return result_url
# 展示该歌名的所有搜索结果


def show_results(url):
    driver = webdriver.Chrome()
    driver.get(url)
#    sleep(1)
    for i in range(1, 1000):  # 假设有一千首歌
        try:
            print('%s' % i + driver.find_element_by_xpath(
                '//*[@id="search_song"]/div[2]/ul[2]/li[%s]/div[1]/a' % i).get_attribute('title'))
        except NoSuchElementException as e:
            print('not found')
            break
    choice = input('请选择 刷新或退出 ')
    if choice == '退出':
        result = 'quit'
    else:
        global mname
        mname = driver.find_element_by_xpath(
            '//*[@id="search_song"]/div[2]/ul[2]/li[%s]/div[1]/a' % choice).get_attribute('title')
        a = driver.find_element_by_xpath(
            '//*[@id="search_song"]/div[2]/ul[2]/li[%s]/div[1]/a' % choice)
        actions = ActionChains(driver)
        actions.move_to_element(a)
        actions.click(a)
        actions.perform()
        sleep(1)
        handlers = driver.window_handles  # 跳转到下一个窗口。
        driver.switch_to.window(handlers[1])
        result = driver.find_element_by_xpath(
            '//*[@id="myAudio"]').get_attribute('src')
        driver.close()
        driver.quit()
    return result


def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per, end=' ')


def choice(url):
    while True:
        result = show_results(url)
        if result == 'quit':
            sys.exit(0)
        else:
            local = 'music\%s.mp3' % mname
            print('download start')
            urllib.request.urlretrieve(result, local, cbk)
            print('\n\n')
            print('finish down %s.mp3' % mname + '\n\n')


def main():
    while True:
        key = input('请输入关键字 ')
#        url = input('请输入链接地址')
        url = 'http://www.kugou.com'
        if not key:
            choice(url)
        elif key == 'quit':
            break
        else:
            result_url = get_url(url, key)
            choice(result_url)


if __name__ == '__main__':
    main()
© 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About
Press h to open a hovercard with more details.
