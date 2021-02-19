# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 16:53:39 2019

@author: uday.gupta
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 20:30:42 2019

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
Column_value=['State','Period','Parameter','Gender','Examination Type','Category','Value']
main_dataframe=pd.DataFrame(columns=Column_value)
data_df=pd.DataFrame()



#to find the year value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[4]'))).click()
Academic_year=Select(d.find_element_by_xpath('//*[@id="academic"]'))
Academic_year_options = [x.text for x in Academic_year.options]
#print(Academic_year)

#to find all the state value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[2]'))).click()
state_value=Select(d.find_element_by_xpath('//*[@id="states"]'))
state_value_options=[x.text for x in state_value.options]

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
        main_dataframe=pd.DataFrame(columns=Column_value)
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
        time.sleep(5)
        
        html=d.page_source
        soup=BeautifulSoup(html,'html.parser')
    #        cast_table=soup.findAll("table",{"class":"table"})
        cast_table=soup.find("div",{"class":"table-responsive"})
        cast_table_df=pd.read_html(str(cast_table))
        #cast_table_df[0].columns.values
    #        for Parameter_value in Parameter:
    #            Dataframe_cast['S.NO']=Sr_no
    #            Dataframe_cast['State']=state_value.first_selected_option.text
    #            Dataframe_cast['Period']=Start_year
    #            Dataframe_cast['Parameter']=Parameter_value
            
        #main_dataframe['Gender']=1
        for k in range(len(Parameter)):
            #k=2
            value_dict=dict()  
            if k!=2:
                
                #condition for mail data if PRE value is not present
                #cast_table_df[0]
                if len(cast_table_df[k]) > 2:
                    for i in range(len(cast_table_df[k][:len(cast_table_df[k])])):
                        #i=2
                        cast_val=['General','SC','ST','OBC']
                        for cast_index in range(len(cast_val)):
#                            
                             if  str(cast_table_df[k]['Unnamed: 1'][i]) !='Total' and type(cast_table_df[k]['Unnamed: 1'][i]) == str:
                                 value_dict={'State':state_value.first_selected_option.text,'Period':period ,'Parameter':Parameter[k],'Gender':cast_table_df[0]['Unnamed: 0'][i],'Examination Type':cast_table_df[k]['Unnamed: 1'][i],'Category':cast_val[cast_index],'Value':cast_table_df[k][cast_val[cast_index]][i]}
                                 data_df=data_df.append(value_dict,ignore_index=True)
                else:
                    value_dict={'State':state_value.first_selected_option.text,'Period':period ,'Parameter':Parameter[k],'Gender':None,'Examination Type':None,'Category':None,'Value':None}

                    data_df=data_df.append(value_dict,ignore_index=True)
            else:
                
                if len(cast_table_df[k]) > 2:
                    for i in range(len(cast_table_df[k][:len(cast_table_df[k])-2])):
                        #i=0 
                        if  str(cast_table_df[k]['Unnamed: 1'][i]) != 'Total' and type(cast_table_df[k]['Unnamed: 1'][i]) == str :
                            value_dict={'State':state_value.first_selected_option.text,'Period':period ,'Parameter':Parameter[k],'Gender':cast_table_df[k]['Unnamed: 0'][i],'Examination Type':cast_table_df[k]['Unnamed: 1'][i],'Value':cast_table_df[k]['Disbursed Amount.2'][i]}
                            data_df=data_df.append(value_dict,ignore_index=True)
                else:
                    value_dict={'State':state_value.first_selected_option.text,'Period':period ,'Parameter':Parameter[k],'Gender':None,'Examination Type':None,'Value':None}
                    data_df=data_df.append(value_dict,ignore_index=True)
 
#data=pd.read_excel("E:/Hdfc/Scholarship/res/National_Scholership_cast_wise_value.xlsx")
data_df=data_df.dropna()         
data_df.to_excel("E:/Hdfc/Scholarship/res/National_Scholership_cast_wise_value.xlsx")

#a='Others_PRE_SC'
#a.split('_')
#
# 
# 
#for i in tqdm(range(len(df[:1000]))):
#   sep=df['combination'][i].split('_')
#   df['Gender'][i]=sep[0]
#   df['Examination Type'][i]=sep[1]
#   df['Category'][i]=sep[2]

import urllib 
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from tqdm import tqdm
import smtplib 

def insert_into_database(Main_DataFrame):
#        Main_DataFrame = pd.read_excel("E:/Hdfc/Scholarship/res/National_Scholership_cast_wise_value.xlsx")
    quoted = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=testDB;UID=developer;PWD=D$pa#2020")

    quoted1 = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=RBI_newDB;UID=developer;PWD=D$pa#2020")
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted)
    engine1 = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted1)
    query = "SELECT * FROM [RBI_newDB].[dbo].[EXT_STATE_DIM_NEW]"
    query1 = "SELECT * FROM [RBI_newDB].[dbo].[EXT_DISTRICT_DIM_NEW]"
    #Main_DataFrame1.read_sql('EMPLOYEES_PROVIDENT_FUND_ORGANISATION',engine,if_exists='append', index=False)
    state_dim = pd.read_sql(query,engine1)
    district_dim = pd.read_sql(query1,engine1)
    Main_DataFrame = Main_DataFrame.fillna(" ")
#    data.columns
    #Main_DataFrame['STATE'] = ''
    
    #len(data.State.unique())
    d_list = list(state_dim.STATE)
    for i,j in tqdm(enumerate(list(Main_DataFrame['State']))):
            name=process.extractOne(j, d_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['State'][i]=name[0]
            else:
                Main_DataFrame['State'][i]=np.nan
        
    data = pd.merge(Main_DataFrame,state_dim[['EXT_STATE_SEQ_ID', 'STATE']],left_on =['State'],right_on = ['STATE'] ,how ='inner' )
    data = data.drop(columns= ['Unnamed: 0', 'STATE'])
    data.dtypes
    data['Period'] = pd.to_datetime(data['Period']).dt.strftime('%m/%d/%Y')
    data = data.fillna(" ")
#    data.to_sql('National_Scholership_cast_wise_value',engine,if_exists='append', index=False)
#    print('inserted into database')

Main_DataFrame = pd.read_excel("E:/Hdfc/Scholarship/res/National_Scholership_cast_wise_value.xlsx")
insert_into_database(Main_DataFrame)

def send_mail():
    conn=smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
    conn.ehlo() # call this to start the connection
    conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
    conn.login('aratoengbot@gmail.com', 'dpa@1234')
    subject='Error Occured while running National_Scholership_cast_wise_value Bot'
    body='Please check the Bot '
    msg= f'subject: {subject}\n\n{body}'
    conn.sendmail('aratoengbot@gmail.com','uday.gupta@decimalpointanalytics.com',msg)
    conn.quit()



