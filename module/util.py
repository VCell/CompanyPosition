import os
import zipfile
import datetime

def get_data_path():
    workpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(workpath, '..', 'data')
    return datapath

#zip解gbk时会识别为cp437
def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        real_name = name.encode('cp437').decode('gbk')
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file

def date_iterator(end_date, period):
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    start_time = (end_date - datetime.timedelta(days=period - 1))
    for i in range(start_time.toordinal(), end_date.toordinal() + 1):
        date = datetime.date.fromordinal(i).strftime('%Y%m%d')
        yield date