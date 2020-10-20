import time
import sys
import os
import datetime

def auto_run():
    while True:
        os.system('python3 web_crawler.py')
        time.sleep(86400)

auto_run()