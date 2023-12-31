#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

'''
Created on 2023-12-26

@author: vcell
'''

import pandas as pd

import plotly.graph_objs as go
from module.global_val import Statics
import module.data_reader as data_reader
from plotly.subplots import make_subplots
from module import util
from module.company_position import CompanyPosition

def draw_company_holding(company, contract, date_iter):
    holding_reader = data_reader.DalianHoldingReader()
    price_reader = data_reader.PriceReader()

    datadf = pd.DataFrame(columns=['date', 'price', 'long_holding', 'short_holding', 'profit'])
    long_obj = None
    short_obj = None
    for date in date_iter:
        price = price_reader.get_price(date, contract)
        profit = 0
        if price: 
            long_holding = holding_reader.get_holding(company, contract, date, Statics.POSITION_LONG)
            short_holding = holding_reader.get_holding(company, contract, date, Statics.POSITION_SHORT)
            if long_holding > 0:
                if long_obj == None:
                    long_obj = CompanyPosition(company, contract, Statics.POSITION_LONG, long_holding, date, price)
                else :
                    long_obj.update(long_holding, date, price)
                    profit += long_obj.get_op_profit()
            if short_holding > 0:
                if short_obj == None:
                    short_obj = CompanyPosition(company, contract, Statics.POSITION_SHORT, short_holding, date, price)
                else :
                    short_obj.update(short_holding, date, price)
                    profit += short_obj.get_op_profit()
            datadf.loc[datadf.shape[0]] = [date, price, long_holding, short_holding, profit]

    trace_long = go.Scatter(x=datadf['date'], y=datadf['long_holding'], name='long_holding')
    trace_short = go.Scatter(x=datadf['date'], y=datadf['short_holding'], name='short_holding')
    trace_price = go.Scatter(x=datadf['date'], y=datadf['price'], name='price')
    trace_profit = go.Scatter(x=datadf['date'], y=datadf['profit'], name='profit')
    print(datadf)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}]])
    fig.add_trace(trace_price, row=1, col=1, secondary_y=False)
    fig.add_trace(trace_long, row=1, col=1, secondary_y=True)
    fig.add_trace(trace_short, row=1, col=1, secondary_y=True)
    fig.add_trace(trace_price, row=2, col=1, secondary_y=False)
    fig.add_trace(trace_profit, row=2, col=1, secondary_y=True)
    fig.show()

if __name__ == '__main__':
    date_iter = util.date_iterator('20231226', 30)
    draw_company_holding('国泰君安', 'i2401', date_iter)