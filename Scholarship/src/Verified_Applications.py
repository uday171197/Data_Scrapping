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
Column_value=['S.NO','State','Start_Year','End_Year','Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Male_Post_Matric/Top_Class/MCM_General','Male_Post_Matric/Top_Class/MCM_SC','Male_Post_Matric/Top_Class/MCM_ST','Male_Post_Matric/Top_Class/MCM_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post_Matric/Top_Class/MCM_General','Female_Post_Matric/Top_Class/MCM_SC','Female_Post_Matric/Top_Class/MCM_ST','Female_Post_Matric/Top_Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post_Matric/Top_Class/MCM_General','Others_Post_Matric/Top_Class/MCM_SC','Others_Post_Matric/Top_Class/MCM_ST','Others_Post_Matric/Top_Class/MCM_OBC','General_Total','SC_Total','ST_Total','OBC_Total','District_Name','Verified_Applications']
Verified_Applications_Dataframe=pd.DataFrame(columns=Column_value)
Verified_Applications_main_Dataframe=pd.DataFrame()
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
    Start_year=Year[:4]
    End_year=Year[5:9]
    #print (Academic_year.first_selected_option.text)
    # to print the value
    #print (Academic_year.first_selected_option.get_attribute("value"))

    #this will select the State values
    for state_value_index in tqdm(range(1,len(state_value_options))):
        Verified_Applications_Dataframe=pd.DataFrame(columns=Column_value)
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
        #print('caste:table',cast_table_df[1].shape)
        District_table=soup.find("div",{"class":"content table-responsive"})
        District_table_df=pd.read_html(str(District_table))
        #print('District table',District_table_df[0].shape)
        #code to put the data in dataframe
        if len(cast_table_df[1])!=2:
            Verified_Applications_Dataframe['District_Name']=District_table_df[0]['District Name']
            Verified_Applications_Dataframe['Verified_Applications']=District_table_df[0]['Verified Applications']
            Verified_Applications_Dataframe['S.NO']=Sr_no
            Verified_Applications_Dataframe['State']=state_value.first_selected_option.text
            Verified_Applications_Dataframe['Start_Year']=Start_year
            Verified_Applications_Dataframe['End_Year']=End_year
            #condition for mail data if PRE value is not present
            if cast_table_df[1]['Unnamed: 1'][0] !='Post Matric/Top Class/MCM':
                Verified_Applications_Dataframe['Male_PRE_General']=cast_table_df[1]['General'][0]
                Verified_Applications_Dataframe['Male_PRE_SC']=cast_table_df[1]['SC'][0]
                Verified_Applications_Dataframe['Male_PRE_ST']=cast_table_df[1]['ST'][0]
                Verified_Applications_Dataframe['Male_PRE_OBC']=cast_table_df[1]['OBC'][0]
                Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][1]
                Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][1]
                Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][1]
                Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][1]
                #condition for Female if PRE value is not present
                if cast_table_df[1]['Unnamed: 1'][2] !='Post Matric/Top Class/MCM':
                    Verified_Applications_Dataframe['Female_PRE_General']=cast_table_df[1]['General'][2]
                    Verified_Applications_Dataframe['Female_PRE_SC']=cast_table_df[1]['SC'][2]
                    Verified_Applications_Dataframe['Female_PRE_ST']=cast_table_df[1]['ST'][2]
                    Verified_Applications_Dataframe['Female_PRE_OBC']=cast_table_df[1]['OBC'][2]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][3]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][3]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][3]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][3]

                    if cast_table_df[1]['Unnamed: 1'][4] =='PRE':
                        Verified_Applications_Dataframe['Others_PRE_General']=cast_table_df[1]['General'][4]
                        Verified_Applications_Dataframe['Others_PRE_SC']=cast_table_df[1]['SC'][4]
                        Verified_Applications_Dataframe['Others_PRE_ST']=cast_table_df[1]['ST'][4]
                        Verified_Applications_Dataframe['Others_PRE_OBC']=cast_table_df[1]['OBC'][4]
                        if cast_table_df[1]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][5]
                             #for the total value
                            Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][6]
                            Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][6]
                            Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][6]
                            Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][6]
                        else:
                            Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][5]
                            Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][5]
                            Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][5]
                            Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][5]
                    elif cast_table_df[1]['Unnamed: 1'][4] == 'Post Matric/Top Class/MCM':
                        Verified_Applications_Dataframe['Others_PRE_General']=None
                        Verified_Applications_Dataframe['Others_PRE_SC']=None
                        Verified_Applications_Dataframe['Others_PRE_ST']=None
                        Verified_Applications_Dataframe['Others_PRE_OBC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][4]
                        #for the total value
                        Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][5]
                        Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][5]
                        Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][5]
                        Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][5]
                    else:
                        Verified_Applications_Dataframe['Others_PRE_General']=None
                        Verified_Applications_Dataframe['Others_PRE_SC']=None
                        Verified_Applications_Dataframe['Others_PRE_ST']=None
                        Verified_Applications_Dataframe['Others_PRE_OBC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=None
                        Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][4]
                        Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][4]
                        Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][4]
                        Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][4]
                    Verified_Applications_main_Dataframe=Verified_Applications_main_Dataframe.append(Verified_Applications_Dataframe,ignore_index=True,sort=False)
                    #print('main dataframe',Verified_Applications_main_Dataframe.shape)
                    Sr_no=Sr_no+1
                else:
                    Verified_Applications_Dataframe['Female_PRE_General']=None
                    Verified_Applications_Dataframe['Female_PRE_SC']=None
                    Verified_Applications_Dataframe['Female_PRE_ST']=None
                    Verified_Applications_Dataframe['Female_PRE_OBC']=None
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][2]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][2]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][2]
                    Verified_Applications_Dataframe['Female_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][2]

                    if cast_table_df[1]['Unnamed: 1'][3] =='PRE':
                        Verified_Applications_Dataframe['Others_PRE_General']=cast_table_df[1]['General'][4]
                        Verified_Applications_Dataframe['Others_PRE_SC']=cast_table_df[1]['SC'][4]
                        Verified_Applications_Dataframe['Others_PRE_ST']=cast_table_df[1]['ST'][4]
                        Verified_Applications_Dataframe['Others_PRE_OBC']=cast_table_df[1]['OBC'][4]
                        if cast_table_df[1]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][5]
                            Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][5]
                             #for the total value
                            Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][6]
                            Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][6]
                            Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][6]
                            Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][6]
                        else:
                            Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][5]
                            Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][5]
                            Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][5]
                            Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][5]
                    elif cast_table_df[1]['Unnamed: 1'][3] == 'Post Matric/Top Class/MCM':
                        Verified_Applications_Dataframe['Others_PRE_General']=None
                        Verified_Applications_Dataframe['Others_PRE_SC']=None
                        Verified_Applications_Dataframe['Others_PRE_ST']=None
                        Verified_Applications_Dataframe['Others_PRE_OBC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][4]
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][4]
                        #for the total value
                        Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][5]
                        Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][5]
                        Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][5]
                        Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][5]
                    else:
                        Verified_Applications_Dataframe['Others_PRE_General']=None
                        Verified_Applications_Dataframe['Others_PRE_SC']=None
                        Verified_Applications_Dataframe['Others_PRE_ST']=None
                        Verified_Applications_Dataframe['Others_PRE_OBC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_General']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_SC']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_ST']=None
                        Verified_Applications_Dataframe['Others_Post_Matric/Top_Class/MCM_OBC']=None
                        Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][3]
                        Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][3]
                        Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][3]
                        Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][3]
                    Verified_Applications_main_Dataframe=Verified_Applications_main_Dataframe.append(Verified_Applications_Dataframe,ignore_index=True,sort=False)
                    #print('main dataframe',Verified_Applications_main_Dataframe.shape)
                    Sr_no=Sr_no+1

            else:
                    Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_General']=cast_table_df[1]['General'][0]
                    Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_SC']=cast_table_df[1]['SC'][0]
                    Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_ST']=cast_table_df[1]['ST'][0]
                    Verified_Applications_Dataframe['Male_Post_Matric/Top_Class/MCM_OBC']=cast_table_df[1]['OBC'][0]
                    Verified_Applications_Dataframe['General_Total']=cast_table_df[1]['General'][2]
                    Verified_Applications_Dataframe['SC_Total']=cast_table_df[1]['SC'][2]
                    Verified_Applications_Dataframe['ST_Total']=cast_table_df[1]['ST'][2]
                    Verified_Applications_Dataframe['OBC_Total']=cast_table_df[1]['OBC'][2]
                    Column_value_for_null=['Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post_Matric/Top_Class/MCM_General','Female_Post_Matric/Top_Class/MCM_SC','Female_Post_Matric/Top_Class/MCM_ST','Female_Post_Matric/Top_Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post_Matric/Top_Class/MCM_General','Others_Post_Matric/Top_Class/MCM_SC','Others_Post_Matric/Top_Class/MCM_ST','Others_Post_Matric/Top_Class/MCM_OBC','General_Total','SC_Total','ST_Total','OBC_Total']
                    Verified_Applications_Dataframe[Column_value_for_null]=None

        else:
            Verified_Applications_Dataframe['District_Name']=District_table_df[0]['District Name']
            Verified_Applications_Dataframe['Verified_Applications']=District_table_df[0]['Verified Applications']
            Verified_Applications_Dataframe['S.NO']=Sr_no
            Verified_Applications_Dataframe['State']=state_value.first_selected_option.text
            Verified_Applications_Dataframe['Start_Year']=Start_year
            Verified_Applications_Dataframe['End_Year']=End_year
            Column_value_for_null=['Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Male_Post_Matric/Top_Class/MCM_General','Male_Post_Matric/Top_Class/MCM_SC','Male_Post_Matric/Top_Class/MCM_ST','Male_Post_Matric/Top_Class/MCM_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post_Matric/Top_Class/MCM_General','Female_Post_Matric/Top_Class/MCM_SC','Female_Post_Matric/Top_Class/MCM_ST','Female_Post_Matric/Top_Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post_Matric/Top_Class/MCM_General','Others_Post_Matric/Top_Class/MCM_SC','Others_Post_Matric/Top_Class/MCM_ST','Others_Post_Matric/Top_Class/MCM_OBC','General_Total','SC_Total','ST_Total','OBC_Total']
            Verified_Applications_Dataframe[Column_value_for_null]=None
           #a= Verified_Applications_Dataframe.columns.values
            Verified_Applications_main_Dataframe=Verified_Applications_main_Dataframe.append(Verified_Applications_Dataframe,ignore_index=True,sort=False)
            Sr_no=Sr_no+1
            #print('main dataframe',Verified_Applications_main_Dataframe.shape)
        #Verified_Applications_main_Dataframe.columns.values
d.close()
Verified_Applications_main_Dataframe.to_csv("E:/Scholarship/res/Verified_Applications.csv")
