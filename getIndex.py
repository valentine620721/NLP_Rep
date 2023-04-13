#Import the libraries
import numpy as np
import pandas as pd
import datetime
from getStockDataset import getOracleDataset

## 定義參數
base_start_date = '2020-10-01'
base_end_date = '2020-12-31'


class getFibnacciIndex:
    def __init__(self,dataset,base_start_date,base_end_date):
        pass

##定義斐波函數(含上升或下降)
    def fibnacci(df,start_date,end_date):
        columns = ['close','open','high','low']
        df = df[columns]
        start_date = base_start_date
        end_date = base_end_date
        df_Fibon = df[start_date:end_date]

        maximum_price = df_Fibon['close'].max()
        minimum_price = df_Fibon['close'].min()
        ##取max,min的日期
        max_idx = df_Fibon[df_Fibon['close']==maximum_price].index[0]
        min_idx = df_Fibon[df_Fibon['close']==minimum_price].index[0]
    
        Diff = maximum_price - minimum_price
        if max_idx > min_idx:
            level_0 = maximum_price
            level_1 = maximum_price - Diff * 0.236   
            level_2 = maximum_price - Diff * 0.382  
            level_3 = maximum_price - Diff * 0.618     
            level_4 = maximum_price - Diff * 0.786
            level_5 = minimum_price
        elif min_idx > max_idx:
            level_0 = minimum_price
            level_1 = minimum_price - Diff * 0.236   
            level_2 = minimum_price - Diff * 0.382  
            level_3 = minimum_price - Diff * 0.618     
            level_4 = minimum_price - Diff * 0.786
            level_5 = maximum_price
        return level_0,level_1,level_2,level_3,level_4,level_5 
