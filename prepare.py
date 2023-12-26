#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

'''
Created on 2023-12-26

@author: vcell
'''

from module.global_val import Config
from module.holding_download import holding_downloader_factory
from module.data_reader import holding_reader_factory
import sys
import time
from module import util

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('example: prepare.py dalian 20231225')
        exit(1)
    ce = sys.argv[1]
    downloader = holding_downloader_factory(ce)
    if not downloader:
        print('unknown commodity exchange')
        exit(1)

    date_iter = util.date_iterator(sys.argv[2], Config.period)
    for date in date_iter:
        if not downloader.exist(date):
            downloader.download(date)
            # 有限频 
            time.sleep(5)
    
    reader = holding_reader_factory(ce)
    clist = reader.get_contract_list(Config.period)

    print(', '.join(('\'' + i + '\'' for i in clist)))
        


