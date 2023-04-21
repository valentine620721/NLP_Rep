import pandas as pd
import numpy as np
import math
import time
import datetime
import os
import cv2
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis

calss SSIMSimilar:
    def __init__(self,dataset,base_start_date,base_end_date):
        pass

class DTWSimilar:
    def __init__(self):
        pass

    def getDtwDataset(stockid,filepath):
        name = os.listdir(filepath)[0]
        ext = name.split('.')[1]
        if ext == 'csv':
            dataset = pd.read_csv(filepath+'//'+stockid+'.csv',delimiter=',')
        elif ext == 'xls':
            dataset = pd.read_excel(filepath+'//'+stockid+'.xls')
        elif ext == 'xlsx':
            dataset = pd.read_excel(filepath+'//'+stockid+'.xlsx')
        dataset = dataset[['date','close']]
        dataset = dataset.astype({'date':str,'close':float})
        dataset['date'] = pd.to_datetime(dataset['date'],format='%Y%m%d')
        dataset.set_index(['date'],inplace=True)
        return dataset
    
    

    def getDTWrank(dataset,base_start_date,base_end_date):
        
        ##定義base與predict兩個區間第一個收盤價的差，並做比較區間的ABS
        def Transform_ABS(df,df_window_name):
            base_abs = round(abs(df.iat[0,0] - df_window_name.iat[0,0]),2)
            if df.iat[0,0] > df_window_name.iat[0,0]:
                df_window_name_abs = df_window_name + base_abs 
            elif df.iat[0,0] < df_window_name.iat[0,0]:
                df_window_name_abs = df_window_name - base_abs
            else:
                df_window_name_abs = df_window_name
            return df_window_name_abs

        base_period_df = dataset[base_start_date:base_end_date]     # get base period
        window_size = len(base_period_df)                           # cal move window size
        move_step = round(window_size*2/3)                          # move 2/3*windowsize

        ##將比較區間Y軸(close)基準點調整與base區間一致
        start_rownum = dataset[:base_start_date].shape[0]
        s_num = start_rownum-window_size
        e_num = start_rownum
        dtw_distance = {'start_date':[],'end_date':[],'similar':[]}

        for n in range(1,math.floor(start_rownum/window_size)):
            window_name = r'data_window_'+str(n)
            df_window_name = dataset[s_num:e_num]
            df_window_name_abs = Transform_ABS(base_period_df,df_window_name)
            df_window_name_abs = df_window_name_abs
            dtw_path = dtw.distance(np.array(base_period_df), np.array(df_window_name_abs))
            s_idx = df_window_name_abs.index[0]
            e_idx = df_window_name_abs.index[window_size-1]
            s_idx = pd.to_datetime(s_idx,format= '%Y-%m-%d')
            e_idx = pd.to_datetime(e_idx,format= '%Y-%m-%d')
            dtw_distance['start_date'].append(s_idx.date())
            dtw_distance['end_date'].append(e_idx.date())  
            dtw_distance['similar'].append(dtw_path)
            n += 1
            s_num = s_num - window_size
            e_num = e_num - window_size

        dtw_distance = pd.DataFrame(dtw_distance)
        ##cal rank
        dtw_distance['rank'] = dtw_distance['similar'].rank(axis=0 ,method='dense',ascending=True)
        dtw_distance = dtw_distance.sort_values(by='rank',ascending=True)
        dtw_distance.reset_index(inplace = True, drop = True)
        return dtw_distance





class CorrSimilar:
    def __init__(self):
        pass

    def getCorrDataset(stockid,filepath):
        name = os.listdir(filepath)[0]
        ext = name.split('.')[1]
        if ext == 'csv':
            dataset = pd.read_csv(filepath+'//'+stockid+'.csv',delimiter=',')
        elif ext == 'xls':
            dataset = pd.read_excel(filepath+'//'+stockid+'.xls')
        elif ext == 'xlsx':
            dataset = pd.read_excel(filepath+'//'+stockid+'.xlsx')
        dataset = dataset[['date','close','high','low','open','vol']]
        dataset = dataset.astype({'date':str,'close':float,'high':float,'low':float,'open':float,'vol':float})
        dataset['date'] = pd.to_datetime(dataset['date'],format='%Y%m%d')
        dataset.set_index(['date'],inplace=True)
        return dataset
    
    

    def getCorrRank(dataset,base_start_date,base_end_date):

        base_period_df = dataset[base_start_date:base_end_date]
        window_size = len(base_period_df)
        move_step = round(window_size*2/3)
        
        ##取得date_start對應的row number,初始化第一個window參數
        start_rownum = dataset[:base_start_date].shape[0]
        s_num = start_rownum-window_size
        e_num = start_rownum
        corr_similar = {'start_date':[],'end_date':[],'corr':[]}

        for n in range(1,math.floor(start_rownum/window_size)):
            window_name = r'data_window_'+str(n)
            df_window_name = dataset[s_num:e_num]
            s_idx = df_window_name.index[0]
            e_idx = df_window_name.index[window_size-1]
            s_idx = pd.to_datetime(s_idx,format= '%Y-%m-%d')
            e_idx = pd.to_datetime(e_idx,format= '%Y-%m-%d')
    
            corr_open = round(np.corrcoef(list(base_period_df['open']),list(df_window_name['open']))[0][1],2)
            corr_high = round(np.corrcoef(list(base_period_df['high']),list(df_window_name['high']))[0][1],2)
            corr_low = round(np.corrcoef(list(base_period_df['low']),list(df_window_name['low']))[0][1],2)
            corr_colse = round(np.corrcoef(list(base_period_df['close']),list(df_window_name['close']))[0][1],2)
            corr_vol = round(np.corrcoef(list(base_period_df['vol']),list(df_window_name['vol']))[0][1],2)
    
            corr_window_name = round((corr_open+corr_high+corr_low+corr_colse+corr_vol)/5,2)
    
            corr_similar['start_date'].append(s_idx.date())
            corr_similar['end_date'].append(e_idx.date())  
            corr_similar['corr'].append(corr_window_name)
            s_num = s_num - window_size
            e_num = e_num - window_size

        corr_similar = pd.DataFrame(corr_similar)
        corr_similar['rank'] = corr_similar['corr'].rank(axis=0 ,method='dense',ascending=False)
        #corr_similar = corr_similar[corr_similar['corr']>0.5]    #保留中度以上相關
        corr_similar = corr_similar.sort_values(by='rank',ascending=True)
        corr_similar.reset_index(inplace = True, drop = True)
        return corr_similar


