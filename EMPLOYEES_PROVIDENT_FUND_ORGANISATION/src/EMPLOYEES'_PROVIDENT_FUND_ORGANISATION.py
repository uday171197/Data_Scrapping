
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 19:41:33 2019

@author: uday.gupta
"""

""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time
import calendar
from datetime import datetime,date,timedelta
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import os
import shutil
import schedule
from pyexcel.cookbook import merge_all_to_a_book
import glob
import pandas as pd


def Job_ckeck_status():
    """

    This function is used to Scrap the data from 'EMPLOYEES_PROVIDENT_FUND_ORGANISATION' this site.  I am also monitor that if the data is updated in the website then it will download the scrap the data and store that into excel sheet.
    If the data is will not update then we don't store the data.

    """
    try:
        browser=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
        browser.get("https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/dashboard")
        time.sleep(5)
        wait=WebDriverWait(browser,100)
        time.sleep(5)
        last=browser.find_element_by_xpath('//*[@id="displayTime"]')
        last_string=last.text
        Today_update=last_string[27:len(last_string)-9]
        try:
            Period=datetime.strftime(datetime.strptime(Today_update,'%d-%m-%Y'),'%d/%m/%Y')
            try:
                f=open('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/date.text','r')
                Last_Update_date=f.read()
                f.close()
            except:
                Last_Update_date=last_string[27:len(last_string)-9]
                #print(Last_Update_date)
                f=open('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/date.text','w+')
                f.write(Last_Update_date)
                f.close()
                #Creating the dataframe
                col=['Zone','Period', ' Office', ' Estb. with at least one member',
                   ' UAN Alloted', ' AADHAAR', ' PAN', ' Bank', ' AADHAAR & Bank',
                   ' Others', ' Total', ' AADHAAR %', ' PAN %', ' Bank %',
                   ' AADHAAR & Bank %', ' Others %', ' Contributory Establishments',
                   ' Contributory Members', ' UAN Activated on Portal',
                   ' KYC Approved W/o Bank']
                Main_DataFrame=pd.DataFrame(columns=col)
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="exportToExcel"]'))).click()
                time.sleep(5)
        #        os.rename('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.csv','C:/Users/uday.gupta/Desktop/Parivahan/UAN_Dashboard.csv')
        #        shutil.move('C:/Users/uday.gupta/Desktop/Parivahan/UAN_Dashboard.csv','E:/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.csv')
                merge_all_to_a_book(glob.glob('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.csv'),'C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx')
                data_dataframe=pd.read_excel('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx')
                data_dataframe['Period']=''
                data_dataframe['Period']=Period
                Main_DataFrame=Main_DataFrame.append(data_dataframe,ignore_index=True,sort=False)
                #os.remove('E:/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx')
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.csv')
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx')
                Main_DataFrame.to_excel('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx')
           #tinding today date
    
            print(Today_update)
            if Today_update != Last_Update_date:
                f=open('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/date.text','w+')
                f.write(Today_update)
                f.close()
    
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="exportToExcel"]'))).click()
                time.sleep(5)
                Main_DataFrame=pd.read_excel('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx',ignore_index=True)
                d=Main_DataFrame.columns
                #d[:8]
                Main_DataFrame=Main_DataFrame.drop(columns=d[0],axis=0)
                merge_all_to_a_book(glob.glob('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.csv'),'C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx')
                data_dataframe=pd.read_excel('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx',index =False)
                #data_dataframe.columns.values
                data_dataframe['Period']=''
                data_dataframe['Period']=Period
                Main_DataFrame=Main_DataFrame.append(data_dataframe,ignore_index=True,sort=False)
                os.remove('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx')
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.csv')
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/UAN Dashboard.xlsx')
                Main_DataFrame.to_excel('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx')
                print('Updated')
    
            else:
                print('Not Updated')
            browser.close()
        except:
            print('there is a null date value')
            browser.close()
    except Exception as e :
        print(e)
        print('problem in the website loading')
        browser.close()

schedule.every().day.at('10:47').do(Job_ckeck_status)

while True:
    schedule.run_pending()
    time.sleep(1)



import urllib 
from fuzzywuzzy import process
from sqlalchemy import create_engine
import pandas as pd

Main_DataFrame = pd.read_excel('E:/Hdfc/EMPLOYEES_PROVIDENT_FUND_ORGANISATION/res/UAN_Dashboard.xlsx',usecols = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])
mapping_data = pd.read_excel(r'C:\Users\uday.gupta\Desktop\Parivahan\final_mapped_data1.csv')

Main_DataFrame['Period'] = pd.to_datetime(Main_DataFrame['Period'])
Main_DataFrame.dtypes
Main_DataFrame.columns = ['Zone', 'Period', 'Office', 'Estb_with_at_least_one_member',
       'UAN_Alloted', 'AADHAAR', 'PAN', 'Bank', 'AADHAAR_and_Bank',
       'Others', 'Total', 'AADHAAR_pct', 'PAN_pct', 'Bank_pct',
       'AADHAAR_and_Bank_pct', 'Others_pct', 'Contributory_Establishments',
       'Contributory_Members', 'UAN_Activated_on_Portal',
       'KYC_Approved_W/o_Bank']
[Zone]
      ,[Period]
      ,[Office]
      ,[Estb_with_at_least_one_member]
      ,[UAN_Alloted]
      ,[AADHAAR]
      ,[PAN]
      ,[Bank]
      ,[AADHAAR_and_Bank]
      ,[Others]
      ,[AADHAAR_pct]
      ,[PAN_pct]
      ,[Bank_pct]
      ,[AADHAAR_and_Bank_pct]
      ,[Others_pct]
      ,[Contributory_Establishments]
      ,[Contributory_Members]
      ,[UAN_Activated_on_Portal]
      ,[KYC_Approved_W/o_Bank]
      ,[Total]

quoted = urllib.parse.quote_plus("Driver={SQL Server Native Client 11.0};Server=192.168.2.6\MSSQLSERVERDEV,1490;Database=testDB;UID=sa;PWD=admin@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quoted)

Main_DataFrame.to_sql('EMPLOYEES_PROVIDENT_FUND_ORGANISATION',engine,if_exists='append', index=False)

Main_DataFrame.reset_index(inplace = True) 
