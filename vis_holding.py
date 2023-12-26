#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

'''
Created on 2023-12-26

@author: vcell
'''

import pandas as pd

import plotly.offline 
import plotly.graph_objs as go
from module.global_val import Statics
import module.data_reader as data_reader

def draw_company_holding(company, contract):
    holding_reader = data_reader.DalianHoldingReader()
    price_reader = data_reader.PriceReader()
    data = holding_reader.data
    long_df = data.loc[(data['company'] == company) & (data['contract'] == contract) & 
                       (data['direction'] == Statics.POSITION_LONG)]
    short_df = data.loc[(data['company'] == company) & (data['contract'] == contract) & 
                        (data['direction'] == Statics.POSITION_SHORT)]
    long_df = long_df.sort_values(by="date",ascending=False)
    short_df = short_df.sort_values(by="date",ascending=False)
    datelist = holding_reader.get_date_list()
    pricelist = [price_reader.get_price(x, contract) for x in datelist]
    trace_long = go.Scatter(x=long_df['date'], y=long_df['position'], name='long_holding')
    trace_short = go.Scatter(x=short_df['date'], y=short_df['position'], name='short_holding')
    trace_price = go.Scatter(x=datelist, y=pricelist, name='price', yaxis='y2')
    layout = go.Layout(title='%s %s'%(company, contract),
                   yaxis=dict(title='holding'),
                   yaxis2=dict(title='price', overlaying='y', side='right')
                   )
    fig = go.Figure(data=[trace_price, trace_long, trace_short], layout=layout)
    fig.show()

if __name__ == '__main__':
    draw_company_holding('摩根大通', 'i2405')