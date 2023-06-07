import pandas as pd
import numpy as np
import math
import time
import datetime
import os
import cv2
import talib
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import matplotlib
matplotlib.use('agg') ##For webserver render, Must be before importing matplotlib.pyplot or pylab
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc

'''Get SSIM Similar Rank...'''
calss SSIMSimilar:
    def __init__(self,dataset,base_start_date,base_end_date):
        pass
    
    def getSSIMRank(dataset,base_start_date,base_end_date):
        ##del old img
        base_path = 'baseimg_result//'
        window_path = 'windowimg_result//'
        for f in os.listdir(base_path):
            os.remove(os.path.join(base_path,f))     
        for f in os.listdir(window_path):
            os.remove(os.path.join(window_path,f))
        
        dataset = dataset.sort_index() 
        dataset = dataset[['close','open','high','low']]
        base_start_date = datetime.datetime.strptime(base_start_date,'%Y-%m-%d').date()
        base_end_date   = datetime.datetime.strptime(base_end_date,'%Y-%m-%d').date()

        base_period_df = dataset[base_start_date:base_end_date]
        window_size = len(base_period_df)
        ##移動步=window_size * 1/2
        move_step = round(window_size*1/2)
        
        ##基準區間K線圖
        base_period_df['Date_num'] = list(map(lambda x:mdates.date2num(x),base_period_df.index))
        ##繪製K線圖
        fig = plt.figure(figsize=(10,10))
        grid = plt.GridSpec(10, 10, wspace=0.5, hspace=0.5)
        ohlc = base_period_df[['Date_num','open','high','low','close']].astype(float)
        ohlc.loc[:,'Date_num'] = range(len(ohlc))  
        ax1 = fig.add_subplot(grid[0:8,0:12])
        candlestick_ohlc(ax1,ohlc.values.tolist(),width = .7,colorup='red',colordown='green')
        ax1 = plt.gca()
        ax1.axes.xaxis.set_visible(False)
        ax1.axes.yaxis.set_visible(False)

        plt.savefig('baseimg_result//'+'base.png')
        plt.close()
        
        ##定義兩個區間第一個收盤價的差，並做比較區間的ABS轉換
        def Transform_ABS(dataset,df_window_name):
            base_abs = round(abs(dataset.iat[0,0] - df_window_name.iat[0,0]),2)
            if dataset.iat[0,0] > df_window_name.iat[0,0]:
                df_window_name_abs = df_window_name + base_abs 
            elif dataset.iat[0,0] < df_window_name.iat[0,0]:
                df_window_name_abs = df_window_name - base_abs
            else:
                df_window_name_abs = df_window_name
            return df_window_name_abs

        def getBaseabs(dataset,df_window_name):
            base_abs = round(dataset.iat[0,0] - df_window_name.iat[0,0],2)
            return base_abs
        
        ##準備compare視窗的數據(起點切齊)
        start_rownum = dataset[:base_start_date].shape[0]
        s_num = start_rownum-window_size
        e_num = start_rownum

        df_compare_abs = pd.DataFrame()
        for n in range(1,math.floor(start_rownum/window_size)):
            ## prepare drawing dataset by window size
            df_compare = dataset[s_num:e_num]
            close_compare_abs = Transform_ABS(pd.DataFrame(base_period_df['close']),pd.DataFrame(df_compare['close']))
            ##取得收盤價的abs值
            base_abs = getBaseabs(pd.DataFrame(base_period_df['close']),pd.DataFrame(df_compare['close']))
            open_compare_abs = pd.DataFrame(df_compare['open']) + base_abs
            high_compare_abs = pd.DataFrame(df_compare['high']) + base_abs
            low_compare_abs = pd.DataFrame(df_compare['low']) + base_abs
            #vol_compare = df_compare['vol']
            df_compare_abs = pd.concat([close_compare_abs,open_compare_abs,high_compare_abs,low_compare_abs],join = 'outer',axis = 1)
            
            ##繪製compare window K線圖
            df_compare_abs['Date_num'] = list(map(lambda x:mdates.date2num(x),df_compare_abs.index))
            fig = plt.figure(figsize=(10,10))
            grid = plt.GridSpec(10, 10, wspace=0.5, hspace=0.5)
            ohlc = df_compare_abs[['Date_num','open','high','low','close']].astype(float)
            ohlc.loc[:,'Date_num'] = range(len(ohlc))  
            #繪製K線
            ax1 = fig.add_subplot(grid[0:8,0:12])   ##繪製K線尺寸
            candlestick_ohlc(ax1,ohlc.values.tolist(),width = .7,colorup='red',colordown='green')
            ax1 = plt.gca()
            ax1.axes.xaxis.set_visible(False)
            ax1.axes.yaxis.set_visible(False)

            s_idx = df_compare_abs.index[0]
            e_idx = df_compare_abs.index[window_size-1]
            s_idx = pd.to_datetime(s_idx,format= '%Y-%m-%d')
            e_idx = pd.to_datetime(e_idx,format= '%Y-%m-%d')
            plt.savefig('windowimg_result//'+str(s_idx.date())+'_'+str(e_idx.date())+'.png')
            plt.close()
            
            n += 1
            s_num = s_num - window_size
            e_num = e_num - window_size

        ## 定義SSIM函式
        def ssim(img1, img2):
            # 計算圖像的亮度、對比度和結構
            c1 = (0.01 * 255) ** 2
            c2 = (0.03 * 255) ** 2
            img1 = img1.astype(np.float64)
            img2 = img2.astype(np.float64)
            mu1 = cv2.GaussianBlur(img1, (11, 11), 1.5)
            mu2 = cv2.GaussianBlur(img2, (11, 11), 1.5)
            mu1_sq = mu1 ** 2
            mu2_sq = mu2 ** 2
            mu1_mu2 = mu1 * mu2
            sigma1_sq = cv2.GaussianBlur(img1 ** 2, (11, 11), 1.5) - mu1_sq
            sigma2_sq = cv2.GaussianBlur(img2 ** 2, (11, 11), 1.5) - mu2_sq
            sigma12 = cv2.GaussianBlur(img1 * img2, (11, 11), 1.5) - mu1_mu2

            # 計算SSIM指標
            ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))
            return np.mean(ssim_map)
        
        ##進行圖片SSIM比對
        base_filepath = 'baseimg_result'
        compare_filepath = 'windowimg_result'
        ##讀取base、compare圖片
        base_img = cv2.imread('baseimg_result//base.png',cv2.IMREAD_GRAYSCALE)

        SSIM_rank = {'start_date':[],'end_date':[],'similar':[],'strength':[]}
        img_list = os.listdir(compare_filepath)
        for img in img_list:
            start_date = img.split('_')[0]
            end_date_ext = img.split('_')[1]
            end_date = end_date_ext.split('.')[0]
            compare_img = cv2.imread(compare_filepath+'//'+img,cv2.IMREAD_GRAYSCALE)
            ssim_value = ssim(base_img, compare_img)
            if ssim_value >= 0.92:
                strength = "H" 
            elif ssim_value >= 0.9 and ssim_value<0.92:
                strength = "M"
            else:
                strength = "L"
               
            start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    
    
'''Get DTW Similar Rank...'''    

class DTWSimilar:
    def __init__(self,dataset,base_start_date,base_end_date):
        pass    

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



'''Get Corr Similar Rank...'''

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


