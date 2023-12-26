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


class HoldingReader(abc.ABC):
    
    data = []

    def __init__(self) -> None:
        super().__init__()

    def get_date_list(self):
        ret = self.data['date'].unique()
        ret.sort()
        return ret
    
    def get_contract_list(self, date_range:int):
        cset = None
        end_date = self.data['date'].max()
        iter = util.date_iterator(end_date, date_range)
        for date in iter:
            cur_set = set(self.data[self.data['date']==date]['contract'])
            if len(cur_set) > 0:
                if cset == None:
                    cset = cur_set
                else :
                    cset = cset & cur_set
        return list(cset)

    def get_holding_by_date(self, date):
        return self.data.loc[self.data['date'] == date]


class DalianHoldingReader(HoldingReader):

    def __init__(self) -> None:
        super().__init__()
        data_path = util.get_data_path()
        self.path = os.path.join(data_path, 'position', 'dalian')
        data = []
        for datename in os.listdir(self.path):
            if datename.startswith('.'):
                continue
            datepath = os.path.join(self.path, datename)
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
                                # 日期 合约 会员简称 方向 持仓量 增减
                                if state != STATE_VOLUME:
                                    data.append([datestr, contract, res.group(1), state, 
                                                 int(res.group(2).replace(',', '')), res.group(3)])
                            else:
                                print('FILE ERROR:', filepath)
        self.data = pd.DataFrame(data, columns=['date','contract', 'company', 'direction', 'position', 'increment'])         



class ZhengzhouHoldingReader(HoldingReader):

    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    reader = DalianHoldingReader()
    print(reader.get_contract_list())
    print(reader.get_date_list())
