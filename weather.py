#coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import random


url = 'http://www.weather.com.cn/weather/101020100.shtml'
res = requests.get(url)
res.encoding = 'utf-8'

soup = BeautifulSoup(res.text, 'html.parser')
value = soup.find('input', id="hidden_title").attrs['value']

with open('/home/sirius/mysite/weather.txt', 'w') as f:
    f.write('上海 ' + value)
