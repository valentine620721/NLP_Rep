import cx_Oracle


class getOracleDataset:
    def __init__(self):
        pass

    def getOracleDataset(hostname,port,servicename,id,passwd,sqlstr):
        # 建立與Oracle數據庫的連接
        dsn_tns = cx_Oracle.makedsn(hostname, port, servicename) # 指定主機、端口號、服務名稱
        conn = cx_Oracle.connect(user=id, password=passwd, dsn=dsn_tns)
        
        # 創建游標對象
        cursor = conn.cursor()
        cursor.execute(sqlstr)
        
        # 獲取結果集
        dataset = cursor.fetchall()

        # 關閉游標和連接
        cursor.close()
        conn.close()

        return dataset
