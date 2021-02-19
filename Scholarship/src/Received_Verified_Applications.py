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
T=True
while T==True:
    try:
        d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
        d.get("https://nsp.gov.in/dashboard/inner25.jsp?state_name=Maharashtra")
        time.sleep(5)
        d.maximize_window()
        wait=WebDriverWait(d,100)
        #table declearation
        Column_value=['S.NO','State','Period','Parameter','Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Male_Post Matric/Top Class/MCM_General','Male_Post Matric/Top Class/MCM_SC','Male_Post Matric/Top Class/MCM_ST','Male_Post Matric/Top Class/MCM_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post Matric/Top Class/MCM_General','Female_Post Matric/Top Class/MCM_SC','Female_Post Matric/Top Class/MCM_ST','Female_Post Matric/Top Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post Matric/Top Class/MCM_General','Others_Post Matric/Top Class/MCM_SC','Others_Post Matric/Top Class/MCM_ST','Others_Post Matric/Top Class/MCM_OBC','District_Name','District_value']
        Dataframe=pd.DataFrame(columns=Column_value)
        data_df=pd.DataFrame()
        
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
                
                for k in range(len(Parameter)-1):    #k=0
                    if len(cast_table_df[k])!=2:
                        Dataframe['District_Name']=District_table_df[0]['District Name']
                        Dataframe['District_value']=District_table_df[0][Parameter[k]]
                        Dataframe['S.NO']=Sr_no
                        Dataframe['State']=state_value.first_selected_option.text
                        Dataframe['Period']=period
                       
                        Dataframe['Parameter']=Parameter[k]   
                        #condition for mail data if PRE value is not present
                        if cast_table_df[k]['Unnamed: 1'][0] !='Post Matric/Top Class/MCM':
                            Dataframe['Male_PRE_General']=cast_table_df[k]['General'][0]
                            Dataframe['Male_PRE_SC']=cast_table_df[k]['SC'][0]
                            Dataframe['Male_PRE_ST']=cast_table_df[k]['ST'][0]
                            Dataframe['Male_PRE_OBC']=cast_table_df[k]['OBC'][0]
                            Dataframe['Male_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][1]
                            Dataframe['Male_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][1]
                            Dataframe['Male_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][1]
                            Dataframe['Male_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][1]
                            #condition for Female if PRE value is not present
                            if cast_table_df[k]['Unnamed: 1'][2] !='Post Matric/Top Class/MCM':
                                Dataframe['Female_PRE_General']=cast_table_df[k]['General'][2]
                                Dataframe['Female_PRE_SC']=cast_table_df[k]['SC'][2]
                                Dataframe['Female_PRE_ST']=cast_table_df[k]['ST'][2]
                                Dataframe['Female_PRE_OBC']=cast_table_df[k]['OBC'][2]
                                Dataframe['Female_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][3]
                                Dataframe['Female_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][3]
                                Dataframe['Female_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][3]
                                Dataframe['Female_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][3]
            
                                if cast_table_df[k]['Unnamed: 1'][4] =='PRE':
                                    Dataframe['Others_PRE_General']=cast_table_df[k]['General'][4]
                                    Dataframe['Others_PRE_SC']=cast_table_df[k]['SC'][4]
                                    Dataframe['Others_PRE_ST']=cast_table_df[k]['ST'][4]
                                    Dataframe['Others_PRE_OBC']=cast_table_df[k]['OBC'][4]
                                    if cast_table_df[k]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                                        Dataframe['Others_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][5]
                                        
                                elif cast_table_df[k]['Unnamed: 1'][4] == 'Post Matric/Top Class/MCM':
                                    Dataframe['Others_PRE_General']=None
                                    Dataframe['Others_PRE_SC']=None
                                    Dataframe['Others_PRE_ST']=None
                                    Dataframe['Others_PRE_OBC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][4]
                                    #for the total value
                    
                                else:
                                    Dataframe['Others_PRE_General']=None
                                    Dataframe['Others_PRE_SC']=None
                                    Dataframe['Others_PRE_ST']=None
                                    Dataframe['Others_PRE_OBC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_General']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_SC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_ST']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_OBC']=None
                                    
                                data_df=data_df.append(Dataframe,ignore_index=True,sort=False)
                                #print('main dataframe',data_df.shape)
                                Sr_no=Sr_no+1
                            else:
                                Dataframe['Female_PRE_General']=None
                                Dataframe['Female_PRE_SC']=None
                                Dataframe['Female_PRE_ST']=None
                                Dataframe['Female_PRE_OBC']=None
                                Dataframe['Female_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][2]
                                Dataframe['Female_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][2]
                                Dataframe['Female_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][2]
                                Dataframe['Female_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][2]
            
                                if cast_table_df[k]['Unnamed: 1'][3] =='PRE':
                                    Dataframe['Others_PRE_General']=cast_table_df[k]['General'][4]
                                    Dataframe['Others_PRE_SC']=cast_table_df[k]['SC'][4]
                                    Dataframe['Others_PRE_ST']=cast_table_df[k]['ST'][4]
                                    Dataframe['Others_PRE_OBC']=cast_table_df[k]['OBC'][4]
                                    if cast_table_df[k]['Unnamed: 1'][5] == 'Post Matric/Top Class/MCM':
                                        Dataframe['Others_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][5]
                                        Dataframe['Others_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][5]
                                         #for the total value
                                        
                                elif cast_table_df[k]['Unnamed: 1'][3] == 'Post Matric/Top Class/MCM':
                                    Dataframe['Others_PRE_General']=None
                                    Dataframe['Others_PRE_SC']=None
                                    Dataframe['Others_PRE_ST']=None
                                    Dataframe['Others_PRE_OBC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][4]
                                    Dataframe['Others_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][4]
                                    #for the total value
                                    
                                else:
                                    Dataframe['Others_PRE_General']=None
                                    Dataframe['Others_PRE_SC']=None
                                    Dataframe['Others_PRE_ST']=None
                                    Dataframe['Others_PRE_OBC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_General']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_SC']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_ST']=None
                                    Dataframe['Others_Post Matric/Top Class/MCM_OBC']=None
                                    
                                data_df=data_df.append(Dataframe,ignore_index=True,sort=False)
                                #print('main dataframe',data_df.shape)
                                Sr_no=Sr_no+1
            
                        else:
                                Dataframe['Male_Post Matric/Top Class/MCM_General']=cast_table_df[k]['General'][0]
                                Dataframe['Male_Post Matric/Top Class/MCM_SC']=cast_table_df[k]['SC'][0]
                                Dataframe['Male_Post Matric/Top Class/MCM_ST']=cast_table_df[k]['ST'][0]
                                Dataframe['Male_Post Matric/Top Class/MCM_OBC']=cast_table_df[k]['OBC'][0]
                                
                                Column_value_for_null=['Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post Matric/Top Class/MCM_General','Female_Post Matric/Top Class/MCM_SC','Female_Post Matric/Top Class/MCM_ST','Female_Post Matric/Top Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post Matric/Top Class/MCM_General','Others_Post Matric/Top Class/MCM_SC','Others_Post Matric/Top Class/MCM_ST','Others_Post Matric/Top Class/MCM_OBC']
                                Dataframe[Column_value_for_null]=None
            
                    else:
                        Dataframe['District_Name']=District_table_df[0]['District Name']
                        Dataframe['District_value']=District_table_df[0][Parameter[k]]
                        Dataframe['S.NO']=Sr_no
                        Dataframe['State']=state_value.first_selected_option.text
                        Dataframe['Period']=period
                       
                        Dataframe['Parameter']=Parameter[0]   
                        Column_value_for_null=['Male_PRE_General','Male_PRE_SC','Male_PRE_ST','Male_PRE_OBC','Male_Post Matric/Top Class/MCM_General','Male_Post Matric/Top Class/MCM_SC','Male_Post Matric/Top Class/MCM_ST','Male_Post Matric/Top Class/MCM_OBC','Female_PRE_General','Female_PRE_SC','Female_PRE_ST','Female_PRE_OBC','Female_Post Matric/Top Class/MCM_General','Female_Post Matric/Top Class/MCM_SC','Female_Post Matric/Top Class/MCM_ST','Female_Post Matric/Top Class/MCM_OBC','Others_PRE_General','Others_PRE_SC','Others_PRE_ST','Others_PRE_OBC','Others_Post Matric/Top Class/MCM_General','Others_Post Matric/Top Class/MCM_SC','Others_Post Matric/Top Class/MCM_ST','Others_Post Matric/Top Class/MCM_OBC']
                        Dataframe[Column_value_for_null]=None
                       #a= Dataframe.columns.values
                        data_df=data_df.append(Dataframe,ignore_index=True,sort=False)
                        Sr_no=Sr_no+1
            #print('main dataframe',data_df.shape)
            #data_df.columns.values
        d.close()
        #data_df.to_excel("E:/Hdfc/Scholarship/res/Received_Applications1.xlsx")
        import pandas as pd
        #data_df=pd.read_excel("E:/Hdfc/Scholarship/res/Received_Applications1.xlsx")
        #del data_df['Unnamed: 0']
#        data_df=data_df.dropna(subset=['     '])
        col=list(data_df.columns)
        columns_val=col[:4]+col[-2:]
        df=pd.melt(data_df,id_vars=columns_val,var_name='combination',value_name='State_value').sort_values('S.NO',axis = 0)
        df['Gender']=''
        df['Examination Type']=''
        df['Category']=''
        for index ,row in tqdm(df.iterrows()):    
             sep=df['combination'][index].split('_')
             df['Gender'][index]=sep[0]
             df['Examination Type'][index]=sep[1]
             df['Category'][index]=sep[2]
        del df['combination']
        cpl1=['S.NO', 'Period', 'State','Gender', 'Examination Type', 'Category','State_value','District_Name','District_value']
        df=df[cpl1]
        df.to_excel("E:/Hdfc/Scholarship/res/National_Scholership_portal.xlsx")
        T=False
    except:
        d.close()
    

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