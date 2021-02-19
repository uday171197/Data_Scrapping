# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 17:42:50 2019

@author: uday.gupta
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time
import calendar
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from tqdm import tqdm,trange

d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
d.get("https://nsp.gov.in/dashboard/inner25.jsp?state_name=Maharashtra")
time.sleep(5)
d.maximize_window()
wait=WebDriverWait(d,100)
#table declearation
Column_value=['Period','State','Parameter','District','Value']
main_Dataframe=pd.DataFrame(columns=Column_value)

#to find the year value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[4]'))).click()
Academic_year=Select(d.find_element_by_xpath('//*[@id="academic"]'))
Academic_year_options = [x.text for x in Academic_year.options]
#print(Academic_year)
#Sr_no=1
#to find all the state value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[2]'))).click()
state_value=Select(d.find_element_by_xpath('//*[@id="states"]'))
state_value_options=[x.text for x in state_value.options]
#Sr_no=1
#for to select the year value
for Academic_year_index in trange(1,len(Academic_year_options)):
    #Academic_year_index=2
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[4]'))).click()
    Academic_year=Select(d.find_element_by_xpath('//*[@id="academic"]'))
    Academic_year.select_by_index(Academic_year_index)
    time.sleep(1)
    Year=Academic_year.first_selected_option.text
    Start_year=Year[:4]
    End_year=Year[5:9]
    period=datetime.strftime(datetime.strptime('31 03 {}'.format(End_year),'%d %m %Y'),'%d/%m/%Y')
    #print (Academic_year.first_selected_option.text)
    # to print the value
    #print (Academic_year.first_selected_option.get_attribute("value"))

    #this will select the State values
    Parameter=['Received Applications','Verified Applications', 'Disbursement Amount']
    
    for state_value_index in range(1,len(state_value_options)):
        #state_value_index=1
        Dataframe=pd.DataFrame(columns=Column_value)
#        time.sleep(5)
        #state_value_index=1
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[2]'))).click()
        state_value=Select(d.find_element_by_xpath('//*[@id="states"]'))
        state_value.select_by_index(state_value_index)
        time.sleep(1)
         #print ( state_value.first_selected_option.text)
        #this will click on submit button
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[5]/center/a'))).click()
        #Getting the table data from site
        time.sleep(10)
        
        html=d.page_source
        soup=BeautifulSoup(html,'html.parser')
#        cast_table=soup.findAll("table",{"class":"table"})
        cast_table=soup.find("div",{"class":"table-responsive"})
        cast_table_df=pd.read_html(str(cast_table))
        cast_table_df[0].columns.values
#        for Parameter_value in Parameter:
#            Dataframe_cast['S.NO']=Sr_no
#            Dataframe_cast['State']=state_value.first_selected_option.text
#            Dataframe_cast['Period']=Start_year
#            Dataframe_cast['Parameter']=Parameter_value
            
        #print('caste:table',cast_table_df[k].shape)
        District_table=soup.find("div",{"class":"content table-responsive"})
        District_table_df=pd.read_html(str(District_table))
        District_table_df[0].columns.values
        #print('District table',District_table_df[0].shape)
        #code to put the data in dataframe
        for Parameter_index in range(len(Parameter)):
            Dataframe['District']=District_table_df[0]['District Name']
            Dataframe['Value']=District_table_df[0][Parameter[Parameter_index]]
            Dataframe['Period']=period
            Dataframe['State']=state_value.first_selected_option.text
            Dataframe['Parameter']=Parameter[Parameter_index]
            main_Dataframe=main_Dataframe.append(Dataframe,ignore_index=True)
main_Dataframe.to_excel("E:/Hdfc/Scholarship/res/National_Scholership_District_wise_data.xlsx")
d.close()




import urllib 
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from tqdm import tqdm 
'''----------------------------------------------------------->-----------------------'''
def insert_into_database(Main_DataFrame):
#    Main_DataFrame = pd.read_excel("E:/Hdfc/Scholarship/res/National_Scholership_District_wise_data.xlsx")

    #quoted = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=testDB;UID=developer;PWD=D$pa#2020")
    quoted1 = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=RBI_newDB;UID=developer;PWD=D$pa#2020")
    #engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted)
    engine1 = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted1)
    query = "SELECT * FROM [RBI_newDB].[dbo].[EXT_STATE_DIM_NEW]"
    query1 = "SELECT * FROM [RBI_newDB].[dbo].[EXT_DISTRICT_DIM_NEW]"
    #Main_DataFrame1.read_sql('EMPLOYEES_PROVIDENT_FUND_ORGANISATION',engine,if_exists='append', index=False)
    state_dim = pd.read_sql(query,engine1)
    district_dim = pd.read_sql(query1,engine1)
#    district_merge = pd.merge(state_dim,district_dim,on = ['EXT_STATE_SEQ_ID'] ,how ='left' )
    
    
    Main_DataFrame = Main_DataFrame.fillna(" ")
#    data.columns
    #Main_DataFrame['DISTRICT'] = ''
    
    #len(data.State.unique())
    d_list = list(district_dim.DISTRICT)
    for i,j in tqdm(enumerate(list(Main_DataFrame['District']))):
            name=process.extractOne(j, d_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['District'][i]=name[0]
    
    s_list = list(state_dim.STATE)            
    for i,j in tqdm(enumerate(list(Main_DataFrame['State']))):
            name=process.extractOne(j, s_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['State'][i]=name[0]
            else:
                Main_DataFrame['State'][i]=np.nan
            
    data = pd.merge(Main_DataFrame,district_dim[['EXT_DISTRICT_SEQ_ID', 'DISTRICT']],left_on = ['District'],right_on = ['DISTRICT'] ,how ='left' )
    data = pd.merge(data,state_dim[['EXT_STATE_SEQ_ID', 'STATE']],left_on = ['State'],right_on = ['STATE'] ,how ='inner' )
    
    data = data.drop(columns= ['Unnamed: 0','STATE','DISTRICT'])
    data.dtypes
    data['Period'] = pd.to_datetime(data['Period']).dt.strftime('%m/%d/%Y')
    data = data.fillna(" ")
    data.to_sql('National_Scholership_District_wise_data',engine1,if_exists='append', index=False)
    print('inserted into database')
    
    
Main_DataFrame = pd.read_excel("E:/Hdfc/Scholarship/res/National_Scholership_District_wise_data.xlsx")
insert_into_database(Main_DataFrame)
#data.to_excel("E:/Hdfc/Scholarship/res/National_Scholership_District_wise_data_for_database.xlsx")

