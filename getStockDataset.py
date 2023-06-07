import cx_Oracle


class getDataset:
    def __init__(self,hostname,port,servicename,id,passwd,sqlstr,stockid):
        pass

    def getOracleDataset(hostname,port,servicename,id,passwd,sqlstr,stockid,stockname):
        try:
            # 建立與Oracle數據庫的連接
            dsn = cx_Oracle.makedsn(host = hostname, port = port, service_name = servicename) 
            conn = cx_Oracle.connect(user=id, password=passwd, dsn = dsn)
            # 創建游標對象
            cursor = conn.cursor()
            cursor.execute(sqlstr,{"stockid":stockid,"stockname":stockname})
            # 獲取數據集
            dataset = cursor.fetchall()
            
            columns = ['datetime','stockid','stockname','close','open','high','low','vol']
            dataset = pd.DataFrame(dataset,columns = columns)
            
            dataset = dataset.astype({'datetime':str,'stockid':str,'stockname':str,'close':float,'open':float,'high':float,'low':float,'vol':float})
            dataset['datetime'] = pd.to_datetime(dataset['datetime'],format = '%T%m%d')
            #新增Drop = False避免index被drop掉
            dataset.set_index(['datetime'],inplace=True,drop=False)
            dataset.sort_index(inplace = True)
            
            return dataset
            # 關閉游標和連接
            cursor.close()
            conn.close()

        except cx_Oracle.DatabaseError as error:
            print('Database Error:',error)
            return None
      
     def getNews(hostname,port,servicename,id,passwd,sqlstr,stockid,startdate,enddate):
            try:
                # 建立與Oracle數據庫的連接
                dsn = cx_Oracle.makedsn(host = hostname, port = port, service_name = servicename) 
                conn = cx_Oracle.connect(user=id, password=passwd, dsn = dsn)
                # 創建游標對象
                cursor = conn.cursor()
                cursor.execute(sqlstr,{"stockid":stockid,"startdate":startdate,"enddate":enddate})
                # 獲取數據集
                dataset = cursor.fetchall()
            
                columns = ['id','datetime','stock_id','path','summary','sent']
                dataset = pd.DataFrame(dataset,columns = columns)
                
                return dataset
                # 關閉游標和連接
                cursor.close()
                conn.close()
         except cx_Oracle.DatabaseError as error:
            print('Database Error:',error)
            return None
