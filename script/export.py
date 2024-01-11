#!/usr/local/bin/python3.8
import pandas as pd
import time
import os

def output(code, data):
    outdata = []
    for key in sorted(data):
        ds = time.strftime("%Y-%m-%d", time.localtime(key))
        outdata.append([ds, data[key].Open, data[key].Close])
    df = pd.DataFrame(outdata,columns=['ds','open', 'close'])
    outpath = os.path.join('/Users/lishiyuan/quant/CompanyPosition/data/price',code + '_D1.csv')
    df.to_csv(outpath)

def main():
    while not exchange.IO("status"):
        LogStatus("正在等待与交易服务器连接, " + _D())
    Log("account:",exchange.GetAccount())
    exchange.IO("mode", 0)
    contracts = ['v2403', 'i2406', 'm2403', 'eb2404', 'y2405', 'i2409', 'c2409', 'jm2405', 'y2403', 'l2405', 'jd2403', 'i2404', 'm2405', 'pp2404', 'pg2402', 'eg2403', 'a2403', 'pp2405', 'cs2407', 'v2401', 'm2407', 'm2409', 'p2405', 'i2405', 'jd2402', 'cs2403', 'lh2405', 'y2407', 'c2403', 'v2405', 'i2403', 'lh2403', 'v2402', 'i2402', 'm2408', 'c2405', 'eb2403', 'c2407', 'eg2405', 'pp2403', 'eb2402']
    for code in contracts:
        exchange.SetContractType(code)
        data = {}
        rs = exchange.GetRecords(PERIOD_D1)
        for r in rs:
            ts = r.Time/1000
            data[ts] = r
        Log("code:", code, " count:", len(data))
        output(code, data)
