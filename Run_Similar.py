from getSimilar import DTWSimilar
from getStockDataset import getDataset
import pandas as pd

stockid = '2330'
filepath = '..//data_source'
base_start_date = '2020-10-01'
base_end_date = '2020-12-31'

hostname = r'172.16.241.27'
port = r'1521'
servicename = r'TFMGDM'
id = r'fmgdm'
passwd = r'Fubon#123'
sqlstr = r'''
select 
日期 as datetime,股票代號 as ID,股票名稱 as name,收盤價 as close,開盤價 as open,最高價 as high,最低價 as low,"成交量(股)" as vol
from v_ODS_CMNY_M002 where 股票代號 = :stockid
'''

dataset_2330 = getDataset.getOracleDataset(hostname,port,servicename,id,passwd,sqlstr,stockid)
columns = ['datetime','ID','name','close','open','high','low','vol']
dataset_2330 = pd.DataFrame(dataset_2330,columns=columns)
