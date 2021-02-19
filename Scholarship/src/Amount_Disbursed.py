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
from tqdm import tqdm
d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
d.get("https://nsp.gov.in/dashboard/inner25.jsp?state_name=Maharashtra")
time.sleep(5)
d.maximize_window()
wait=WebDriverWait(d,100)
#table declearation
Column_value=['S.NO','State','Parameter','Period','Male_PRE_Disbursed Amount','Male_Post Matric/Top Class/MCM_Disbursed Amount','Female_PRE_Disbursed Amount','Female_Post Matric/Top Class/MCM_Disbursed Amount','Other_PRE_Disbursed Amount','Other_Post Matric/Top Class/MCM_Disbursed Amount','District_Name','District_value']
dataframe=pd.DataFrame(columns=Column_value)
main_Dataframe=pd.DataFrame()
#to find the year value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[4]'))).click()
Academic_year=Select(d.find_element_by_xpath('//*[@id="academic"]'))
Academic_year_options = [x.text for x in Academic_year.options]
#print(Academic_year)
Sr_no=1
#to find all the state value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[2]'))).click()
state_value=Select(d.find_element_by_xpath('//*[@id="states"]'))
state_value_options=[x.text for x in state_value.options]
Sr_no=1
#for to select the year value
for Academic_year_index in range(1,len(Academic_year_options)):
    #Academic_year_index=2
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calendaryear"]/div/div/div[4]'))).click()
    Academic_year=Select(d.find_element_by_xpath('//*[@id="academic"]'))
    Academic_year.select_by_index(Academic_year_index)
    time.sleep(1)
    Year=Academic_year.first_selected_option.text
    Parameter=Year[:4]
    End_year=Year[5:9]
    Period=datetime.strftime(datetime.strptime('31 03 {}'.format(End_year),'%d %m %Y'),'%d/%m/%Y')

    #print (Academic_year.first_selected_option.text)
    # to print the value
    #print (Academic_year.first_selected_option.get_attribute("value"))

    #this will select the State values
    Parameter='Disbursement Amount'
    for state_value_index in tqdm(range(1,len(state_value_options))):
        dataframe=pd.DataFrame(columns=Column_value)
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
        #print('caste:table',cast_table_df[2].shape)
        District_table=soup.find("div",{"class":"content table-responsive"})
        District_table_df=pd.read_html(str(District_table))
        #print('District table',District_table_df[0].shape)
        #code to put the data in dataframe
        if len(cast_table_df[2])!=2:
            dataframe['District_Name']=District_table_df[0]['District Name']
            dataframe['District_value']=District_table_df[0]['Disbursement Amount']
            dataframe['S.NO']=Sr_no
            dataframe['State']=state_value.first_selected_option.text
            dataframe['Parameter']=Parameter
            dataframe['Period']=Period
            #condition for mail data if PRE value is not present
            if cast_table_df[2]['Unnamed: 1'][0] !='Post Matric/Top Class/MCM':
                dataframe['Male_PRE_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][0]
                dataframe['Male_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][1]
                
                #condition for Female if PRE value is not present
                if cast_table_df[2]['Unnamed: 1'][2] !='Post Matric/Top Class/MCM':
                    dataframe['Female_PRE_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][2]
                    dataframe['Female_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][3]

                    if cast_table_df[2]['Unnamed: 1'][4] =='PRE':
                        dataframe['Other_PRE_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][4]

                        if cast_table_df[2]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                            dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][5]
                             #for the total value
                            
                            
                    elif cast_table_df[2]['Unnamed: 1'][4] == 'Post Matric/Top Class/MCM':
                        dataframe['Other_PRE_Disbursed Amount']=None
                       
                        dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][4]
                        #for the total value
                        dataframe['District_value']=cast_table_df[2]['Disbursed Amount'][5]
                    else:
                        dataframe['Other_PRE_Disbursed Amount']=None
                       
                        dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=None
                        #for the total value
                    main_Dataframe=main_Dataframe.append(dataframe,ignore_index=True,sort=False)
                    #print('main dataframe',main_Dataframe.shape)
                    Sr_no=Sr_no+1
                else:
                    dataframe['Female_PRE_Disbursed Amount']=None
                    dataframe['Female_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][2]

                    if cast_table_df[2]['Unnamed: 1'][3] =='PRE':
                        dataframe['Other_PRE_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][4]
                        if cast_table_df[2]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                            dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][5]
                             #for the total value
                        else:
                            dataframe['District_value']=cast_table_df[2]['Disbursed Amount'][5]
                    elif cast_table_df[2]['Unnamed: 1'][3] == 'Post Matric/Top Class/MCM':
                        dataframe['Other_PRE_Disbursed Amount']=None                        
                        dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][4]                        
                        #for the total value
                    else:
                        dataframe['Other_PRE_Disbursed Amount']=None                        
                        dataframe['Other_Post Matric/Top Class/MCM_Disbursed Amount']=None                        
                        #for the total value
                    main_Dataframe=main_Dataframe.append(dataframe,ignore_index=True,sort=False)
                    #print('main dataframe',main_Dataframe.shape)
                    Sr_no=Sr_no+1

            else:
                    dataframe['Male_PRE_Disbursed Amount']=cast_table_df[2]['Disbursed Amount'][0]
                    Column_value_for_null=['Male_Post Matric/Top Class/MCM_Disbursed Amount','Female_PRE_Disbursed Amount','Female_Post Matric/Top Class/MCM_Disbursed Amount','Other_PRE_Disbursed Amount','Other_Post Matric/Top Class/MCM_Disbursed Amount']
                    dataframe[Column_value_for_null]=None

        else:
            dataframe['District_Name']=District_table_df[0]['District Name']
            dataframe['District_value']=District_table_df[0]['Disbursement Amount']
            dataframe['S.NO']=Sr_no
            dataframe['State']=state_value.first_selected_option.text
            dataframe['Parameter']=Parameter
            dataframe['Period']=Period
            Column_value_for_null=['Male_PRE_Disbursed Amount','Male_Post Matric/Top Class/MCM_Disbursed Amount','Female_PRE_Disbursed Amount','Female_Post Matric/Top Class/MCM_Disbursed Amount','Other_PRE_Disbursed Amount','Other_Post Matric/Top Class/MCM_Disbursed Amount','District_value']
            dataframe[Column_value_for_null]=None
           #a= dataframe.columns.values
            main_Dataframe=main_Dataframe.append(dataframe,ignore_index=True,sort=False)
            Sr_no=Sr_no+1
            #print('main dataframe',main_Dataframe.shape)
        #main_Dataframe.columns.values
d.close()
val=list(main_Dataframe.columns.values)
cpl=val[:4]+val[-2:]
main_df=pd.melt(main_Dataframe,id_vars=cpl,var_name='Combination',value_name='State_value').sort_values('S.NO',axis = 0)
main_df['Gender']=''
main_df['Examination Type']=''
for index ,row in tqdm(main_df.iterrows()):    
     sep=main_df['Combination'][index].split('_')
     main_df['Gender'][index]=sep[0]
     main_df['Examination Type'][index]=sep[1]
     
del main_df['Combination']
main_df.columns.values
main_df=main_df[['S.NO', 'State', 'Parameter', 'Period', 'Gender', 'Examination Type', 'State_value','District_Name', 'District_value']]
main_df.to_csv("E:/Hdfc/Scholarship/res/Amount_Disbursed.csv")




