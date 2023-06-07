import platfrom
from flask import Flask,request
from flask_cors import CORS '''一份瀏覽器技術規範，提供Web服務從不同網域傳來沙盒指令碼的方法，以避開瀏覽器的同源政策'''
from getIndex import getFibnacciIndex
from getSimilar import DTWSimilar
from getSimilar import CorrSimilar
from getSimilar import aHashSimilar
from getStockDataset import getOracleDataset
import cx_Oracle

if (platform.system() == 'Windows'):
  cx_Oracle.init_oracle_client(lib_dir = r"C:\Program Files\Oracle\instantclient")
  
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

## DB connection info
dbhostname = r'172.17.240.7'
if (platform.system() != 'Windows'):
  dnhostname =  r'172.17.240.8'

dbport = r'1521'
dbservicename = r'orcl'
dbuser = r'eason'
dbpass = r'password'

sqlstr_stockdata  = r'''
select date as datetime, stock_id as stockid,name as stockname,close as close, open as open, high as high, low as low,vol as vol
from v_stockdata where stock_id = :stockid or name =:stockname
'''

sqlstr_news = r'''
select ID as id, DATETIME as datetime,STOCK_ID as stock_id, PATH as path, SUMMARY as summary, SENT as sent
from NEWS where STOCK_ID = :stockid and DATETIME between TO_DATE(:startdate,'YYYY-MM-DD') and TO_DATE(:enddate,'YYYY-MM-DD')
'''

def get_dataset(stockid,stockname):
  return getOracleDataset.getOracleDataset(dbhostname,dbport,dbservicename,dbuser,dbpass,sqlstr_stockdata,stockid,stockname)

def convert_date(dataset,date_column_name,format = '%Y-%m-%d'):
  dataset[data_column_name] = dataset[date_column_name].apply(lambda x: x.strftime(format))
  return dataset

def get_news_dataset(stockid,startdate,enddate):
  return getOracleDataset.getNews(dbhostname,dbport,sbservicename,dbuser,dbpass,sqlstr_news,stockid,startdate,enddate)

@app.route("/history")
def get_history():
  keyword = request.args.get('kkeyword')
  if (keyword is None):
    return 'keyword is required',400
  
  dataset = get_dataset(keyword,keyword)
  if (dataset is None or len(dataset)==0):
    return 'data not found',404
  #轉換日期格式
  convert_date(dataset,'datetime')
  return dataset.to_dict(orient = 'records')

@app.route("/similar")
def run_similar():
  stockid = request.args.get('stockid')
  model = request.args.get('model')
  startdate = request.args.get('startdate')
  enddate = request.args.get('enddate')
  if (stockis is None or model is None or startdate is None or enddate is None):
    return 'params is required',400
  if (model != 'ALL' and model != 'DTW' and model != 'CORR' and model != 'AHASH'):
    return 'model is invalid',400
  
  dataset = get_dataset(stockid,None)
  if (dataset is None or len(dataset) == 0):
    return 'data not found',400
  
  request = []
  if (model == 'ALL' or model == 'DTW'):
    results.extend(DTWSimilar.getDTWrank(dataset,startdate,enddate).to_dict(orients = 'records'))
  if (model == 'ALL' or model == 'CORR'):
    results.extend(CorrSimilar.getCorrrank(dataset,startdate,enddate).to_dict(orients = 'records'))
  if (model == 'ALL' or model == 'AHASH'):
    results.extend(aHashSimilar.getaHashrank(dataset,startdate,enddate).to_dict(orients = 'records'))
  return results


  








