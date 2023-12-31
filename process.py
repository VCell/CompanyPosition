#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

'''
Created on 2023-12-26

@author: vcell
'''

import os
import pandas as pd
from module.data_reader import holding_reader_factory, PriceReader
from module.global_val import Config, Statics
from module import util
from module.company_position import CompanyPosition
import sys

def update_position_map(posmap, company, contract, direction, position, date, price):
    if not contract in posmap:
        posmap[contract] = {}   
    if not company in posmap[contract]:
        posmap[contract][company] = {}
    if not direction in posmap[contract][company]:
        posmap[contract][company][direction] = CompanyPosition(company, contract, direction, position, date, price)
    else :
        posmap[contract][company][direction].update(position, date, price)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('example: prepare.py dalian 20231225')
        exit(1)
    ce = sys.argv[1]
    holding_reader = holding_reader_factory(sys.argv[1])
    if not holding_reader:
        print('unknown commodity exchange')
        exit(1)

    date_iter = util.date_iterator(sys.argv[2], Config.period)
    datadir = util.get_data_path()
    result_path = os.path.join(datadir, 'result')
    posmap = {}
    price_reader = PriceReader()
    contracts = holding_reader.get_contract_list(Config.period)

    for date in date_iter:
        datepd = holding_reader.get_holding_by_date(date)
        for item in datepd.itertuples():
            price = price_reader.get_price(date, item.contract)
            if price:
                update_position_map(posmap, item.company, item.contract, item.direction, item.position, 
                                date, price_reader.get_price(date, item.contract))
    print(posmap.keys())

    for contract in contracts:
        data = []
        if not contract in posmap.keys():
            continue
        for company in posmap[contract].keys():
            if Config.separate_direction:
                for k,v in posmap[contract][company].items():
                    data.append([v.contract, v.company, v.direction, v.get_rate()])
            else:
                if len(posmap[contract][company]) > 1:
                    long_pos = posmap[contract][company][Statics.POSITION_LONG]
                    short_pos = posmap[contract][company][Statics.POSITION_SHORT]
                    data.append([long_pos.contract, long_pos.company, Statics.POSITION_LONG, long_pos.get_join_rate(short_pos)])
                else:
                    for k,v in posmap[contract][company].items():
                        data.append([v.contract, v.company, v.direction, v.get_rate()])
        data.sort(key=lambda x: x[3])
        df = pd.DataFrame(data,columns=['contract','company', 'direction', 'rate'])
        df.to_csv(os.path.join(result_path, contract+'.csv'))
