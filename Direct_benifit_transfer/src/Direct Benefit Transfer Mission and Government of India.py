# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:29:11 2019

@author: uday.gupta
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import os

def Job():
    """Short summary.

    Returns
    -------
    type
        Description of returned object.

    """
    d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
    d.get("https://dbtbharat.gov.in/page/frontcontentview/?id=NjU=")
    wait=WebDriverWait(d,40)
    path=["C:/Users/uday.gupta/Desktop/Parivahan/state wise 2018-19_final.xlsx","C:/Users/uday.gupta/Desktop/Parivahan/state wise final 2017-18 _Final.xlsx","C:/Users/uday.gupta/Desktop/Parivahan/state wise 2016-17_final.xlsx"]
    year=['2018-19','2018-17','2017-16']
    main_dataframe=pd.DataFrame(columns=['SNo.','Period','State', 'Ministry', 'Scheme Name', 'Benefit Type',
           'DBT Fund Transfer'])
    for i in tqdm(range(1,4)):
        #i=1
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="about"]/div/div[5]/div/div/div[2]/ul[2]/li[{}]/a'.format(i)))).click()
        time.sleep(2)
        xls=pd.ExcelFile(path[i-1])
        Start=year[i-1][:4]
        End='20'+year[i-1][5:8]
        period=datetime.strftime(datetime.strptime('31 03 {}'.format(End),'%d %m %Y'),'%d/%m/%Y')
        state=xls.sheet_names
        for state_value in state:
            #state_value='Tamil Nadu'
            if  state_value != 'Andaman and Nicobar  ':
                df = pd.read_excel(xls,state_value)
                #df.shape
                #df1=df[1:len(df)-2]
                df1=df[1:len(df)-2]
                new_header = ['SNo.', 'Ministry', 'Scheme Name', 'Benefit Type','DBT Fund Transfer']
                df_state=df1[1:]
                #df_state.columns.values
                df_state.columns = new_header
                df_state['Period']= period
                df_state['State']= state_value
                #df_state.columns.values
            else:
                #state_value = 'Andaman and Nicobar  '
                df = pd.read_excel(xls,state_value)
                #df.shape
                df1=df[1:len(df)-9]
    #            df1=df.drop(df.index[0]).reset_index(drop =True)

                #c=df.columns[0:5]
                #new_header = ['SNo.', 'Ministry', 'Scheme Name', 'Benefit Type','DBT Fund Transfer']
                df_state=df1[1:]
                new_cl = list(df_state.columns)
    #            df_state1.rename(columns = {"Scheme wise DBT in Andaman and Nicobar Islands FY 2016-17":'SNo.','Unnamed 1': 'Ministry','Unnamed 2':'Scheme Name', 'Unnamed 3':'Benefit Type','Unnamed: 4':'DBT Fund Transfer'})
                df_state = df_state.rename(columns = {new_cl[0]:'SNo.',new_cl[1]: 'Ministry',new_cl[2]:'Scheme Name', new_cl[3]:'Benefit Type',new_cl[4]:'DBT Fund Transfer'})
    #            c.rename(index = {'Scheme wise DBT in Andaman and Nicobar Islands FY 2016-17':'SNo.','Unnamed 1': 'Ministry', 'Unnamed 2':'Scheme Name', 'Unnamed 3':'Benefit Type', 'Unnamed: 4':'DBT Fund Transfer'}, inplace=True)
                #from_col=df_state1.columns[0:5]
                #df_state1.columns[0:5] = new_header
                df_state.drop(df_state.columns[5:9], axis=1, inplace=True)
                df_state['Period']= period
                df_state['State']= state_value
            main_dataframe=pd.concat([main_dataframe,df_state],axis=0,ignore_index=True,sort=False)
        os.remove(path[i-1])
    main_dataframe.to_csv("E:/Hdfc/Direct_benifit_transfer/res/Direct Benefit Transfer Mission and Government of India.csv")
    d.close()
#from crontab import CronTab
    
    
import schedule
schedule.every().days.at("12:10").do(Job())
"""
This function  written to schedule the execution of the Job function. It will execute the job function every day at 11:30 pm and send that mail to recipients.

"""
while True:

    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)

import urllib 
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from tqdm import tqdm 

def insert_into_database(Main_DataFrame):
    #    Main_DataFrame = pd.read_csv("E:/Hdfc/Direct_benifit_transfer/res/Direct Benefit Transfer Mission and Government of India1.csv")

    quoted1 = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=RBI_newDB;UID=developer;PWD=D$pa#2020")
    #engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted)
    engine1 = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted1)
    query = "SELECT * FROM [RBI_newDB].[dbo].[EXT_STATE_DIM_NEW]"
    query1 = "SELECT * FROM [RBI_newDB].[dbo].[EXT_DISTRICT_DIM_NEW]"
    #Main_DataFrame1.read_sql('EMPLOYEES_PROVIDENT_FUND_ORGANISATION',engine,if_exists='append', index=False)
    state_dim = pd.read_sql(query,engine1)
    district_dim = pd.read_sql(query1,engine1)
    d_list = list(state_dim.STATE)
    for i,j in tqdm(enumerate(list(Main_DataFrame['State']))):
            name=process.extractOne(j, d_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['State'][i]=name[0]
            else:
                Main_DataFrame['State'][i]=np.nan
        
    data = pd.merge(Main_DataFrame,state_dim[['EXT_STATE_SEQ_ID', 'STATE']],left_on = ['State'],right_on = ['STATE'] ,how ='inner' )
    data = data.drop(columns= ['Unnamed: 0', 'SNo.','STATE'])
    data['Period'] = pd.to_datetime(data['Period']).dt.strftime('%m/%d/%Y')
    data.to_sql('Direct Benefit Transfer Mission and Government of India',engine1,if_exists='append', index=False)
    print('inserted into database')

Main_DataFrame = pd.read_csv("E:/Hdfc/Direct_benifit_transfer/res/Direct Benefit Transfer Mission and Government of India1.csv")
insert_into_database(Main_DataFrame)




