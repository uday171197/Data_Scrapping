# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:14:05 2019

@author: uday.gupta
"""

# -*- coding: utf-8 -*-


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
import os
from tqdm import tqdm,trange

try:
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", "E:\Parivahan\res")
    driver= webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe",firefox_profile=profile)
    #it is the link of the website from which we are going to scrap the data
    driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/")
    time.sleep(5)
    #these all variable is use to store the value of each table and then
    # we are pass this value to dictionary so that we can get the all value together
    #put that value
    #these all are the column of the table
    Top=['Period',
    'State',
    'RTO Name',
    'RTO Transport',
    'RTO Non Transport',
    'Vehicle Category',
    'Vehicle_Class','vehical_class_Total']
    table_data=pd.DataFrame()# we create a empty dataframe
    table_data=pd.DataFrame(columns=Top)#we have a dataframe with columns
    
      #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
    #paginator_bottom=['//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[2]','//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[3]','//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[4]']
    first_week={'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[7]'}
    last_week={'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[7]'}
    wait=WebDriverWait(d,100)
    Type = driver.find_element_by_xpath('//*[@id="j_idt24_label"]').click()
    driver.find_element_by_xpath('//*[@id="j_idt24_3"]').click()
    time.sleep(8)
    for i in range(2019,(datetime.now().year)+1):
        #i=2019
        if i==datetime.now().year:
            for k in range(1,(datetime.now().month)):
                #for upto   k=3
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_uptoDate_input"]'))).click()
                yr=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
                mt.select_by_value(str(k-1))
                last_day=calendar.monthrange(i,k)
                if len(str(k))==1:
                    month='0'+str(k)
                else:
                    month=str(k)
                year=str(i)
                one=str(last_day[1])
                lastday=one+month+year
                lastday=datetime.strptime(str(lastday), "%d%m%Y").date()
                Period=datetime.strftime(lastday,"%d/%m/%Y")
                print(lastday)
                l=lastday.strftime("%A")
                for day in last_week.keys():
                    if day==l:
                        path=last_week[day]
                wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
                time.sleep(10)

#            #for from
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_fromDate_input"]'))).click()
                yr=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
                mt.select_by_value(str(k-1))
                print('from month',k)
                time.sleep(3)

                if len(str(k))==1:
                    month='0'+str(k)
                else:
                    month=str(k)
                year=str(i)
                one='01'
                firstday=one+month+year
                firstday=datetime.strptime(str(firstday), "%d%m%Y").date()
                print(firstday)
                l=firstday.strftime("%A")
                for day in first_week.keys():
                    if day==l:
                        path=first_week[day]
                wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
                time.sleep(10)
                Rdate=month+'-'+year
                print(Rdate)
#                state_op=Select(driver.find_element_by_xpath('//*[@id="j_idt35_input"]'))
#                state_val=[x.text for x in state_op.options ]
#                a='ghfajsfdghad(10000)'
#                p1=re.compile('[(\d)]').sub('',a)
#                for state_val_index in range(1,len(state_val)):
#                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
#                    state_val_xpath='//*[@id="j_idt35_'+str(state_val_index)+'"]'
#                    wait.until(EC.element_to_be_clickable((By.XPATH,state_val_xpath))).click()
#                    time.sleep()
#                
#                
#                    try:
#                       element1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt54"]')))
#                       element1.click()
#                       time.sleep(25)
#                    except:
#                        print('Error')
                
                
                 # Vehical Registration
                # Table data

              #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
              # selecting the district value 
             
                #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
                state_value=Select(driver.find_element_by_xpath('//*[@id="j_idt34_input"]'))
                state_value_options=[x.text for x in state_value.options]
                for state_value_options_index in trange(1,len(state_value_options)):
                    #state_value_options_index=1
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt34_label"]'))).click()
                    st_xpath='//*[@id="j_idt34_'+str(state_value_options_index)+'"]'
                    driver.find_element_by_xpath(st_xpath).click()
                    time.sleep(5)
                    try:
                         element1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt61"]')))
                         element1.click()
                         time.sleep(10)
                    except:
                        print('not able to click') # Vehical Registration
                   
              #loop for the data of states
                    download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
                    rto_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls")
                    #rto_data.columns.values
                    for rto_data_index in range(len(rto_data)):
                        #it is the Xpath for the states 
                        #rto_data_index=1
                        #x=//*[@id="datatable_rtoWise:0:j_idt116:1:j_idt118"]
                        x='//*[@id="datatable_rtoWise:'+str(rto_data_index)+':j_idt116:1:j_idt118"]'
                        try:
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                            time.sleep(10)
                        except:
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_paginator_bottom"]/a[3]'))).click()
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                            time.sleep(10)
                        download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
                        CategoryWise_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls")
                        #classwise_data.columns.values
                        for CategoryWise_data_index in range(len(CategoryWise_data)):
                            #it is the xpath for the Rtos
                            #CategoryWise_data_index=2
                            #//*[@id="datatable_rtoWise:1:j_idt116:1:j_idt118"]
                            
                            dt1={'Period':Period,'State':re.compile('[(\d)]').sub('',state_value_options[state_value_options_index]),
                                 'RTO Name':rto_data[' RTO Name '][rto_data_index],
                                'Transaction Type':CategoryWise_data[' Transaction Type '][CategoryWise_data_index],
                                'Total':CategoryWise_data[' Total '][CategoryWise_data_index]
                                }
                                
                            table_data = table_data.append(dt1,ignore_index=True,sort=False)
                            print(table_data.shape)
                    #        
            
                        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt129"]'))).click()
                        time.sleep(5)
                    os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls') 
                    table_data.to_excel("E:/Hdfc/vahan_parivahan/res/no_of_transaction"+str(Rdate)+".xlsx")
              
                 
                
                


        else:
            for k in range(1,12):
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_uptoDate_input"]'))).click()
                yr=Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
                mt.select_by_value(str(k-1))
                last_day=calendar.monthrange(i,k)
                if len(str(k))==1:
                    month='0'+str(k)
                else:
                    month=str(k)
                year=str(i)
                one=str(last_day[1])
                lastday=one+month+year
                lastday=datetime.strptime(str(lastday), "%d%m%Y").date()
                Period=datetime.strftime(lastday,"%d/%m/%Y")
                print(lastday)
                l=lastday.strftime("%A")
                for day in last_week.keys():
                    if day==l:
                        path=last_week[day]
                wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
                time.sleep(10)

#            #for from
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_fromDate_input"]'))).click()
                yr=Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
                mt.select_by_value(str(k-1))
                print('from month',k)
                time.sleep(3)

                if len(str(k))==1:
                    month='0'+str(k)
                else:
                    month=str(k)
                year=str(i)
                one='01'
                firstday=one+month+year
                firstday=datetime.strptime(str(firstday), "%d%m%Y").date()
                print(firstday)
                l=firstday.strftime("%A")
                for day in first_week.keys():
                    if day==l:
                        path=first_week[day]
                wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
                time.sleep(10)
                Rdate=month+'-'+year
                print(Rdate)
#                state_op=Select(driver.find_element_by_xpath('//*[@id="j_idt35_input"]'))
#                state_val=[x.text for x in state_op.options ]
#                a='ghfajsfdghad(10000)'
#                p1=re.compile('[(\d)]').sub('',a)
#                for state_val_index in range(1,len(state_val)):
#                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
#                    state_val_xpath='//*[@id="j_idt35_'+str(state_val_index)+'"]'
#                    wait.until(EC.element_to_be_clickable((By.XPATH,state_val_xpath))).click()
#                    time.sleep()
#                
#                
#                    try:
#                       element1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt54"]')))
#                       element1.click()
#                       time.sleep(25)
#                    except:
#                        print('Error')
                
                
                 # Vehical Registration
                # Table data

              #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
              # selecting the district value 
             
                #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
                state_value=Select(driver.find_element_by_xpath('//*[@id="j_idt35_input"]'))
                state_value_options=[x.text for x in state_value.options]
                for state_value_options_index in trange(1,len(state_value_options)):
                    #state_value_options_index=1
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
                    st_xpath='//*[@id="j_idt35_'+str(state_value_options_index)+'"]'
                    driver.find_element_by_xpath(st_xpath).click()
                    time.sleep(5)
                    try:
                         element1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt61"]')))
                         element1.click()
                         time.sleep(10)
                    except:
                        print('not able to click') # Vehical Registration
                   
              #loop for the data of states
                    download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
                    rto_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls")
                    #rto_data.columns.values
                    for rto_data_index in range(len(rto_data)):
                        #it is the Xpath for the states 
                        #rto_data_index=1
                        #x=//*[@id="datatable_rtoWise:0:j_idt116:1:j_idt118"]
                        x='//*[@id="datatable_rtoWise:'+str(rto_data_index)+':j_idt116:1:j_idt118"]'
                        try:
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                            time.sleep(10)
                        except:
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_paginator_bottom"]/a[3]'))).click()
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                            time.sleep(10)
                        download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
                        CategoryWise_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls")
                        #classwise_data.columns.values
                        for CategoryWise_data_index in range(len(CategoryWise_data)):
                            #it is the xpath for the Rtos
                            #CategoryWise_data_index=2
                            #//*[@id="datatable_rtoWise:1:j_idt116:1:j_idt118"]
                            
                            dt1={'Period':Period,'State':re.compile('[(\d)]').sub('',state_value_options[state_value_options_index]),
                                 'RTO Name':rto_data[' RTO Name '][rto_data_index],
                                'Transaction Type':CategoryWise_data[' Transaction Type '][CategoryWise_data_index],
                                'Total':CategoryWise_data[' Total '][CategoryWise_data_index]
                                }
                                
                            table_data = table_data.append(dt1,ignore_index=True,sort=False)
                            print(table_data.shape)
                    #        
            
                        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt129"]'))).click()
                        time.sleep(5)
                    os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls') 
                    table_data.to_excel("E:/Hdfc/vahan_parivahan/res/no_of_transaction"+str(Rdate)+".xlsx")

except:

   driver.close()
   print("the execution is intrupted ,so we start the execution again")
   try:
       os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
       os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
   except:
       print('data is deleted from download')

