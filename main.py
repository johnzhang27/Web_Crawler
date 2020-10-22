import time
import sys
import os
import datetime
import schedule

def auto_run():
    os.system('python3 web_crawler.py')

schedule.every().day.at("20:50").do(auto_run)

while 1:
    schedule.run_pending()
    time.sleep(1)