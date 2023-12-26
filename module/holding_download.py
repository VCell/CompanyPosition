# -*- coding:utf-8 -*-

import abc
import requests
import zipfile
import os

from .global_val import Statics
from .util import get_data_path,support_gbk

def holding_downloader_factory(ce) -> 'HoldingDownloader':
    if ce == Statics.CE_DALIAN:
        return DalianHoldingDownloader()
    elif ce == Statics.CE_ZHENGZHOU:
        return ZhengzhouHoldingDownloader()
    return None

class HoldingDownloader(abc.ABC):

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def download(self, date):
        pass

    @abc.abstractmethod
    def exist(self, date) -> bool:
        pass


class DalianHoldingDownloader(HoldingDownloader):

    outpath = ''

    def __init__(self) -> None:
        super().__init__()
        self.outpath = os.path.join(get_data_path(), 'position', Statics.CE_DALIAN)

    def download(self, date):
        tmppath = '/tmp/holding.zip'
        outpath = os.path.join(self.outpath, date)
        url = "http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html"
        data = {'memberDealPosiQuotes.variety': 'a',
                'memberDealPosiQuotes.trade_type': 0,
                'year': date[0:4],
                'month': str(int(date[4:6])-1), #大商所月从0开始
                'day': date[6:8],
                'batchExportFlag': 'batch',
                }
        resp = requests.post(url=url,data=data)
        if resp.status_code == 200:
            if 'Content-Disposition' in resp.headers and resp.headers['Content-Disposition'].startswith('attachment'):
                with open(tmppath, 'wb') as fp:
                    fp.write(resp.content)
                with support_gbk(zipfile.ZipFile(tmppath)) as zfp:
                    zfp.extractall(outpath)
                print("download done: dalian %s"%(date))
            else:
                print('ERROR: %s no data'%(date))
        else:
            print('ERROR: %s http code %d'%(date, resp.status_code))

    def exist(self, date) -> bool:
        outpath = os.path.join(self.outpath, date)
        if os.path.isdir(outpath):
            return True
        return False

class ZhengzhouHoldingDownloader(HoldingDownloader):

    outpath = ''

    def __init__(self) -> None:
        super().__init__()
        self.outpath = os.path.join(get_data_path(), 'position', Statics.CE_ZHENGZHOU)

    def download(self, date):
        pass

    def exist(self, date) -> bool:
        pass