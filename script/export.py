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
    contracts = ['jm2405', 'm2403', 'p2403', 'c2405', 'v2401', 'pp2404', 'l2402', 'lh2403', 'pp2403', 
                 'y2407', 'pp2401', 'l2403', 'eg2401', 'jd2403', 'jd2402', 'eb2404', 'v2405', 'y2405', 
                 'p2401', 'i2405', 'eb2403', 'lh2405', 'l2401', 'v2404', 'pp2402', 'i2401', 'm2401', 
                 'cs2403', 'y2401', 'i2403', 'a2403', 'eg2405', 'pg2402', 'c2407', 'eb2401', 'cs2407', 
                 'eb2402', 'i2406', 'm2405', 'eg2402', 'm2411', 'v2403', 'eg2403', 'p2402', 'i2409', 
                 'l2405', 'y2403', 'i2404', 'c2403', 'i2402', 'm2407', 'pp2405', 'c2409', 'm2408', 
                 'v2402', 'm2409', 'c2401', 'y2408', 'p2405']
    for code in contracts:
        exchange.SetContractType(code)
        data = {}
        rs = exchange.GetRecords(PERIOD_D1)
        for r in rs:
            ts = r.Time/1000
            data[ts] = r
        Log("code:", code, " count:", len(data))
        output(code, data)
