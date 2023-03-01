import cx_Oracle


class getOracleDataset:
    def __init__(self,hostname,port,servicename,id,passwd,sqlstr):
        pass

    def getOracleDataset(hostname,port,servicename,id,passwd,sqlstr):
        try:
            # 建立與Oracle數據庫的連接
            dsn = cx_Oracle.makedsn(host = hostname, port = port, service_name = servicename) 
            conn = cx_Oracle.connect(user=id, password=passwd, dsn = dsn)
            # 創建游標對象
            cursor = conn.cursor()
            cursor.execute(sqlstr)
            # 獲取數據集
            dataset = cursor.fetchall()
            # 關閉游標和連接
            cursor.close()
            conn.close()
            return dataset
            print("Connect to Oracle Database successful.")

        except:
            print('Connect to Oracle Database error! Failed  connect to oracle database...')
