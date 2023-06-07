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
  








