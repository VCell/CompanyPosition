import os
import pandas as pd
import abc
import re
from .global_val import Statics
from . import util

STATE_VOLUME = 2

def holding_reader_factory(ce) -> 'HoldingReader':
    if ce == Statics.CE_DALIAN:
        return DalianHoldingReader()
    elif ce == Statics.CE_ZHENGZHOU:
        return ZhengzhouHoldingReader()
    return None

class PriceReader :

    contract_map = {}

    def __init__(self) -> None:
        datapath = util.get_data_path()
        pricepath = os.path.join(datapath, 'price')
        for filename in os.listdir(pricepath):
            if filename.startswith('.'):
                continue
            contract = filename.split('_')[0]
            path = os.path.join(pricepath, filename)
            df = pd.read_csv(path, index_col="ds")
            self.contract_map[contract] = df

    def get_price(self, date, contract):
        date_str = '-'.join([date[0:4], date[4:6], date[6:8]])
        if contract in self.contract_map:
            if date_str in self.contract_map[contract].index:
                return self.contract_map[contract].loc[date_str]['close']
        return None


class HoldingBoardCompleter:
    
    def __init__(self) -> None:
        self.preday = None
        self.today = None
        self.cur_date = None
        self.pre_date = None

    def key(sr):
        return '%s_%s_%d'%(sr[1], sr[2], sr[3])

    def check(self, sr):
        key = HoldingBoardCompleter.key(sr)
        if sr[0] != self.cur_date:
            if self.cur_date:
                self.preday = self.today
                self.pre_date = self.cur_date
            self.cur_date = sr[0]
            self.today = set()
        self.today.add(key)
        if self.preday!=None and not key in self.preday:
            pos = sr[4] - int(sr[5].replace(',',''))
            return [self.pre_date,sr[1],sr[2],sr[3],pos, None]
        return None

class HoldingReader(abc.ABC):
    # 日期 合约 会员简称 方向 持仓量 增减
    columns = ['date','contract', 'company', 'direction', 'position', 'increment']

    def __init__(self) -> None:
        self.df = pd.DataFrame([], columns=HoldingReader.columns)    
        super().__init__()

    def get_date_list(self):
        ret = self.df['date'].unique()
        ret.sort()
        return ret
    
    def get_contract_list(self, date_range:int):
        cset = None
        end_date = self.df['date'].max()
        iter = util.date_iterator(end_date, date_range)
        for date in iter:
            cur_set = set(self.df[self.df['date']==date]['contract'])
            if len(cur_set) > 0:
                if cset == None:
                    cset = cur_set
                else :
                    cset = cset & cur_set
        return list(cset)

    def get_holding_by_date(self, date):
        return self.df.loc[self.df['date'] == date]
    
    def get_holding(self, company, contract, date, direction):
        res = self.df[(self.df['date']==date) & (self.df['company']==company) &
                  (self.df['contract']==contract) & (self.df['direction']==direction)]
        if len(res) > 0:
            return res.iloc[0].position
        return 0


class DalianHoldingReader(HoldingReader):

    def __init__(self) -> None:
        super().__init__()
        datapath = util.get_data_path()
        basepath = os.path.join(datapath, 'position', Statics.CE_DALIAN)
        completer = HoldingBoardCompleter()
        data=[]
        for datename in sorted(os.listdir(basepath)):
            if datename.startswith('.'):
                continue
            datepath = os.path.join(basepath, datename)
            if not os.path.isdir(datepath):
                continue
            for filename in os.listdir(datepath):
                if datename.startswith('.'):
                    continue
                filepath = os.path.join(datepath, filename)
                if not os.path.isfile(filepath):
                    continue
                with open(filepath, 'r') as f:
                    
                    state = 0
                    contract = ''
                    datestr = ''
                    for line in f.readlines():
                        res = re.match('合约代码：(\S+)\s+Date：([0-9\-]+)', line)
                        if res:
                            contract = res.group(1)
                            datestr = res.group(2).replace('-', '')
                            continue
                        if re.match('名次\s+会员简称\s+持买单量\s+增减\s*', line):
                            state = Statics.POSITION_LONG
                            continue
                        if re.match('名次\s+会员简称\s+持卖单量\s+增减\s*', line):
                            state = Statics.POSITION_SHORT
                            continue
                        if re.match('名次\s+会员简称\s+成交量\s+增减\s*', line):
                            state = STATE_VOLUME
                            continue                    
                        res = re.match('\d+\s+(\S+)\s+([0-9\,\-]+)\s+([0-9\,\-]+)\s*', line)
                        if res:
                            if state != 0 and len(contract)>0 and len(datestr)>0:
                                if state != STATE_VOLUME:
                                    item = [datestr, contract, res.group(1), state, 
                                             int(res.group(2).replace(',', '')), res.group(3)]
                                    sup = completer.check(item)
                                    if sup:
                                        data.append(sup)
                                    data.append(item)
                            else:
                                print('FILE ERROR:', filepath)
        #df追加很慢，需要先数组处理，最后生成df
        self.df = pd.DataFrame(data, columns=['date','contract', 'company', 'direction', 'position', 'increment'])    
 


class ZhengzhouHoldingReader(HoldingReader):

    def __init__(self) -> None:
        super().__init__()
        datapath = util.get_data_path()
        basepath = os.path.join(datapath, 'position', Statics.CE_ZHENGZHOU)
        data = []
        for filename in os.listdir(basepath):
            if filename.startswith('.'):
                continue
            filepath = os.path.join(basepath, filename)
            date = filename[0:8]
            if not os.path.isfile(filepath):
                continue
            with open(filepath, 'r') as f:
                contract = ''
                start = False
                for line in f.readlines():
                    res = re.match('合约：(\S+)\s+日期：\S+', line) 
                    if res:
                        contract = res.group(1)
                        start = True
                        continue
                    if start:
                        res = re.match('\d+\s+\|\S+\s+\|[0-9\,]+\s+\|[0-9\,\-]+\s+\|(\S+)\s+\|([0-9\,]+)\s+\|([0-9\,\-]+)\s+\|(\S+)\s+\|([0-9\,]+)\s+\|([0-9\,\-]+)\s+', line)
                        if res:
                            data.append([date, contract, res.group(1), Statics.POSITION_LONG, 
                                                    int(res.group(2).replace(',', '')), res.group(3)])
                            data.append([date, contract, res.group(4), Statics.POSITION_SHORT, 
                                                    int(res.group(5).replace(',', '')), res.group(6)])
        self.data = pd.DataFrame(data, columns=['date','contract', 'company', 'direction', 'position', 'increment'])   

if __name__ == '__main__':
    reader = ZhengzhouHoldingReader()
    print(reader.data)
