#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding:utf-8
# Author:Huang lingling

import requests
from bs4 import BeautifulSoup

urls = ["http://lishi.tianqi.com/guiyang1/201609.html"]
file = open('guiyang_weather.txt','w')
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    weather_list = soup.select('div[class="tqtongji2"]')

    for weather in weather_list:
        weather_date = weather.select('a')[0].string.encode('utf-8')
        ul_list = weather.select('ul')
        i=0
        for ul in ul_list:
            li_list= ul.select('li')
            str=""
            for li in li_list:
                str += li.string.encode('utf-8')+','
            if i!=0:
                file.write(str+'\n')
            i+=1
file.close()