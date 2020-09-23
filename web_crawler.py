import requests
import json
import html
import string
import codecs
import time
import datetime
import pymysql
from bs4 import BeautifulSoup
import password
pymysql.install_as_MySQLdb()
class alberta_case(object):
    region = None
    confirmed_cases = None
    active_cases = None
    recovered_cases = None
    in_hospital = None
    in_intensive_care = None
    deaths = None
    date = None
class save_daily_case_num(object):
    def __init__(self,items):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = password.password
        self.db = 'COVID19_Alberta'
        self.run(items)
    def run(self,items):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user,
        password = self.password, db = self.db)
        cur = db.cursor()
        parameters = []
        for item in items:
            parameters.append((item.region, item.confirmed_cases, item.active_cases,item.recovered_cases,item.in_hospital,item.in_intensive_care,item.deaths,item.date))
        sql="insert into alberta_cases(region,confirmed_cases,active_cases,recovered_cases,in_hospital,in_intensive_care,deaths,date) values(%s, %s, %s, %s, %s, %s, %s, %s )"  

        try:
            ret=cur.executemany(sql,parameters)
            db.commit()
            print(u'success, total %s data' %str(ret))
        except  Exception as e:
            print(e)
            db.rollback()
        cur.close()

if __name__ == '__main__':
    items = []
    target = 'https://www.alberta.ca/covid-19-alberta-data.aspx'
    req = requests.get(url=target)
    html = req.text
    bf = BeautifulSoup(html)
    #print(bf)
    texts = bf.tbody.find_all('tr')
    #print(texts)
    for tag in texts:
        item = alberta_case()
        tag_region = tag.find_all('th')
        item.region = tag_region[0].getText().strip()
        tags = tag.find_all('td')
        item.confirmed_cases = tags[0].getText().strip()
        item.active_cases = tags[1].getText().strip()
        item.recovered_cases = tags[2].getText().strip()
        item.in_hospital = tags[3].getText().strip()
        item.in_intensive_care = tags[4].getText().strip()
        item.deaths = tags[5].getText().strip()
        item.date = datetime.datetime.now()

        items.append(item)

    save_daily_case_num(items)