import cx_Oracle


class getDataset:
    def __init__(self,hostname,port,servicename,id,passwd,sqlstr,stockid):
        pass

    def getOracleDataset(hostname,port,servicename,id,passwd,sqlstr,stockid):
        try:
            # 建立與Oracle數據庫的連接
            dsn = cx_Oracle.makedsn(host = hostname, port = port, service_name = servicename) 
            conn = cx_Oracle.connect(user=id, password=passwd, dsn = dsn)
            # 創建游標對象
            cursor = conn.cursor()
            cursor.execute(sqlstr,{"stockid":stockid})    ## 查詢條件使用參數
            # 獲取數據集
            dataset = cursor.fetchall()
            return dataset
            # 關閉游標和連接
            cursor.close()
            conn.close()

        except cx_Oracle.DatabaseError as error:
            print('Database Error:',error)
