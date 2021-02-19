# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:03:33 2019

@author: uday.gupta
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 20:59:48 2019

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
    d = webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe",firefox_profile=profile)
    #it is the link of the website from which we are going to scrap the data
    d.get("https://vahan.parivahan.gov.in/vahan4dashboard/")
    time.sleep(5)
    #these all variable is use to store the value of each table and then
    # we are pass this value to dictionary so that we can get the all value together
    #put that value
    #these all are the column of the table
    Top=['Serial No',' State Name', 
       ' Rto Name', 'Fee(Cash)', ' Fee(Internet) ',
       ' Fee(Other)', ' Tax(Cash) ', ' Tax(Internet)', ' Tax(Other)',
       'Total Revenue ',' Transaction Type ', ' Total Revenue']
    table_data=pd.DataFrame()# we create a empty dataframe
    table_data=pd.DataFrame(columns=Top)#we have a dataframe with columns
    
      #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
    #paginator_bottom=['//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[2]','//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[3]','//*[@id="datatable_moreInfo13_paginator_bottom"]/span[2]/a[4]']
    first_week={'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[7]'}
    last_week={'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[7]'}
    wait=WebDriverWait(d,100)
    d.find_element_by_xpath('//*[@id="j_idt25_label"]').click()
    d.find_element_by_xpath('//*[@id="j_idt25_3"]').click()
    time.sleep(8)
    for i in range(2019,(datetime.now().year)+1):
        #i=2019
        if i==datetime.now().year:
            for k in range(1,(datetime.now().month)):
                #for upto   k=3
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_uptoDate_input"]'))).click()
                yr=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
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
                yr=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
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
#                state_op=Select(d.find_element_by_xpath('//*[@id="j_idt35_input"]'))
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
#                       element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt54"]')))
#                       element1.click()
#                       time.sleep(25)
#                    except:
#                        print('Error')
                
                
                 # Vehical Registration
                # Table data

              #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
              # selecting the district value 
             
                #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
                try:
                   WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                   time.sleep(10)
                except:
                    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                    time.sleep(5)
                    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                    time.sleep(10)# Vehical Registration     
                # Table data
                
                  #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
                  #loop for the data of states
                download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_moreInfo13:csv"]'))).click()
                state_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/state.xls")
                #state_data.columns.values
                for state_data_index in trange(len(state_data)):
                    #it is the Xpath for the states 
                    #state_data_index=1
                    #//*[@id="datatable_moreInfo13:1:j_idt101:1:j_idt103"]
                    x='//*[@id="datatable_moreInfo13:'+str(state_data_index)+':j_idt101:1:j_idt103"]'
                    try:
                        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13:0:j_idt101:1:j_idt103"]'))).click()
                        time.sleep(10)
                    except:
                        WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_paginator_bottom"]/a[3]'))).click()
                        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_data"]/tr[1]/td[2]'))).click()
                        time.sleep(10)
                    download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
                    RTO_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls")
                    #CategoryWise_data.columns.values
                    
                    for RTO_data_index in range(len(RTO_data)):
                        #it is the xpath for the Rtos
                        #RTO_data_index=6
                        #//*[@id="datatable_rtoWise:1:j_idt116:1:j_idt118"]
                        y='//*[@id="datatable_rtoWise:'+str(RTO_data_index)+':j_idt116:1:j_idt118"]'
                        try:
                            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
                            time.sleep(10)
                        except:
                            WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise_paginator_bottom"]/a[3]'))).click()
                            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
                            time.sleep(10)
                        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
                        CategoryWise_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls")
                #        table_data=pd.DataFrame(columns=Top)
                #        #this loop for the data of Vehical category
                #        table_data[' Transaction Type ']=CategoryWise_data[' Transaction Type '] 
                #        table_data[' Total Revenue']:CategoryWise_data[' Total Revenue']
                #        table_data['Serial No']:state_data['Serial No'][state_data_index]
                #        table_data[' State Name']:state_data[' State Name'][state_data_index]
                #        table_data['Fee(Cash)']:state_data['Fee(Cash)'][state_data_index]
                #        table_data[' Fee(Internet) ']:state_data[' Fee(Internet) '][state_data_index]
                #        table_data[' Fee(Other)']:state_data['Fee(Cash)'][state_data_index]
                #        table_data[' Tax(Cash) ']:state_data[' Tax(Cash) '][state_data_index]
                #        table_data[' Tax(Internet)']:state_data[' Tax(Internet)'][state_data_index]
                #        table_data[' Tax(Other)']:state_data[' Tax(Other)'][state_data_index]
                #        table_data['Total Revenue ']:state_data['Total Revenue '][state_data_index]
                #        table_data[' Rto Name']:RTO_data[' Rto Name'][RTO_data_index]
                #        table_data['Fee(Cash)']:RTO_data['Fee(Cash)'][RTO_data_index]
                #        table_data[' Fee(Internet) ']:RTO_data[' Fee(Internet) '][RTO_data_index]
                #        
                #        table_data[' Fee(Other)']:RTO_data[' Fee(Other)'][RTO_data_index]
                #        table_data[' Tax(Cash) ']:RTO_data[' Tax(Cash) '][RTO_data_index]
                #        table_data[' Tax(Internet)']:RTO_data[' Tax(Internet)'][RTO_data_index]
                #        table_data[' Tax(Other)']:RTO_data[' Tax(Other)'][RTO_data_index]
                #        table_data['Total Revenue ']:RTO_data['Total Revenue '][RTO_data_index]
                #        
                #        main_table_data=main_table_data.append(table_data,ignore_index=True,sort=False)
                        
                        for CategoryWise_index in range(len(CategoryWise_data)):
                            #link for the 
                            
                            dt1={'Serial No':state_data['Serial No'][state_data_index],' State Name':state_data[' State Name'][state_data_index],
                       ' Rto Name':RTO_data[' Rto Name'][RTO_data_index], 'Fee(Cash)':RTO_data['Fee(Cash)'][RTO_data_index], ' Fee(Internet) ':RTO_data[' Fee(Internet) '][RTO_data_index],
                       ' Fee(Other)':RTO_data[' Fee(Other)'][RTO_data_index], ' Tax(Cash) ':RTO_data[' Tax(Cash) '][RTO_data_index], ' Tax(Internet)':RTO_data[' Tax(Internet)'][RTO_data_index], ' Tax(Other)':RTO_data[' Tax(Other)'][RTO_data_index],
                       'Total Revenue ':RTO_data['Total Revenue '][RTO_data_index],' Transaction Type ':CategoryWise_data[' Transaction Type '][CategoryWise_index], ' Total Revenue':CategoryWise_data[' Total Revenue'][CategoryWise_index]}
                                
                            table_data = table_data.append(dt1,ignore_index=True,sort=False)
                            print(table_data.shape)
                #        
                        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt129"]'))).click()
                        time.sleep(5)
                    os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise:j_idt114"]'))).click()
                    time.sleep(5)
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/state.xls') 
                table_data.to_excel("E:/Hdfc/vahan_parivahan/res/Vehical_Month_wise_reviewof"+str(Rdate)+".xlsx")

        else:
            for k in range(1,12):
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_uptoDate_input"]'))).click()
                yr=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
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
                yr=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
                yr.select_by_value(str(i))
                mt=Select(d.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
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
#                print(Rdate)
#                state_op=Select(d.find_element_by_xpath('//*[@id="j_idt35_input"]'))
#                state_val=[x.text for x in state_op.options ]
#                p1=re.compile(r'( *?)').sub('',state_val[0])
#                for state_val_index in range(1,len(state_val)):
#                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
#                    state_val_xpath='//*[@id="j_idt35_'+str(state_val_index)+'"]'
#                    wait.until(EC.element_to_be_clickable((By.XPATH,state_val_xpath))).click()
#                    time.sleep()
#                
#                
#                    try:
#                       element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt54"]')))
#                       element1.click()
#                       time.sleep(25)
#                    except:
#                        print('Error')
                
                
                 # Vehical Registration
                # Table data

              #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
              # selecting the district value 
             
                #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt35_label"]'))).click()
                try:
                   WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                   time.sleep(10)
                except:
                    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                    time.sleep(5)
                    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
                    time.sleep(10)# Vehical Registration     
                # Table data
                
                  #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
                  #loop for the data of states
                download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_moreInfo13:csv"]'))).click()
                state_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/state.xls")
                #state_data.columns.values
                for state_data_index in trange(len(state_data)):
                    #it is the Xpath for the states 
                    #state_data_index=1
                    #//*[@id="datatable_moreInfo13:1:j_idt101:1:j_idt103"]
                    x='//*[@id="datatable_moreInfo13:'+str(state_data_index)+':j_idt101:1:j_idt103"]'
                    try:
                        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13:0:j_idt101:1:j_idt103"]'))).click()
                        time.sleep(10)
                    except:
                        WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_paginator_bottom"]/a[3]'))).click()
                        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_data"]/tr[1]/td[2]'))).click()
                        time.sleep(10)
                    download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
                    RTO_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls")
                    #CategoryWise_data.columns.values
                    
                    for RTO_data_index in range(len(RTO_data)):
                        #it is the xpath for the Rtos
                        #RTO_data_index=6
                        #//*[@id="datatable_rtoWise:1:j_idt116:1:j_idt118"]
                        y='//*[@id="datatable_rtoWise:'+str(RTO_data_index)+':j_idt116:1:j_idt118"]'
                        try:
                            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
                            time.sleep(10)
                        except:
                            WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise_paginator_bottom"]/a[3]'))).click()
                            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
                            time.sleep(10)
                        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
                        CategoryWise_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls")
                #        table_data=pd.DataFrame(columns=Top)
                #        #this loop for the data of Vehical category
                #        table_data[' Transaction Type ']=CategoryWise_data[' Transaction Type '] 
                #        table_data[' Total Revenue']:CategoryWise_data[' Total Revenue']
                #        table_data['Serial No']:state_data['Serial No'][state_data_index]
                #        table_data[' State Name']:state_data[' State Name'][state_data_index]
                #        table_data['Fee(Cash)']:state_data['Fee(Cash)'][state_data_index]
                #        table_data[' Fee(Internet) ']:state_data[' Fee(Internet) '][state_data_index]
                #        table_data[' Fee(Other)']:state_data['Fee(Cash)'][state_data_index]
                #        table_data[' Tax(Cash) ']:state_data[' Tax(Cash) '][state_data_index]
                #        table_data[' Tax(Internet)']:state_data[' Tax(Internet)'][state_data_index]
                #        table_data[' Tax(Other)']:state_data[' Tax(Other)'][state_data_index]
                #        table_data['Total Revenue ']:state_data['Total Revenue '][state_data_index]
                #        table_data[' Rto Name']:RTO_data[' Rto Name'][RTO_data_index]
                #        table_data['Fee(Cash)']:RTO_data['Fee(Cash)'][RTO_data_index]
                #        table_data[' Fee(Internet) ']:RTO_data[' Fee(Internet) '][RTO_data_index]
                #        
                #        table_data[' Fee(Other)']:RTO_data[' Fee(Other)'][RTO_data_index]
                #        table_data[' Tax(Cash) ']:RTO_data[' Tax(Cash) '][RTO_data_index]
                #        table_data[' Tax(Internet)']:RTO_data[' Tax(Internet)'][RTO_data_index]
                #        table_data[' Tax(Other)']:RTO_data[' Tax(Other)'][RTO_data_index]
                #        table_data['Total Revenue ']:RTO_data['Total Revenue '][RTO_data_index]
                #        
                #        main_table_data=main_table_data.append(table_data,ignore_index=True,sort=False)
                        
                        for CategoryWise_index in range(len(CategoryWise_data)):
                            #link for the 
                            
                            dt1={'Serial No':state_data['Serial No'][state_data_index],' State Name':state_data[' State Name'][state_data_index],
                       ' Rto Name':RTO_data[' Rto Name'][RTO_data_index], 'Fee(Cash)':RTO_data['Fee(Cash)'][RTO_data_index], ' Fee(Internet) ':RTO_data[' Fee(Internet) '][RTO_data_index],
                       ' Fee(Other)':RTO_data[' Fee(Other)'][RTO_data_index], ' Tax(Cash) ':RTO_data[' Tax(Cash) '][RTO_data_index], ' Tax(Internet)':RTO_data[' Tax(Internet)'][RTO_data_index], ' Tax(Other)':RTO_data[' Tax(Other)'][RTO_data_index],
                       'Total Revenue ':RTO_data['Total Revenue '][RTO_data_index],' Transaction Type ':CategoryWise_data[' Transaction Type '][CategoryWise_index], ' Total Revenue':CategoryWise_data[' Total Revenue'][CategoryWise_index]}
                                
                            table_data = table_data.append(dt1,ignore_index=True,sort=False)
                            print(table_data.shape)
                #        
                        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt129"]'))).click()
                        time.sleep(5)
                    os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise:j_idt114"]'))).click()
                    time.sleep(5)
                os.remove('C:/Users/uday.gupta/Desktop/Parivahan/state.xls') 
                table_data.to_excel("E:/Hdfc/vahan_parivahan/res/Vehical_Month_wise_reviewof"+str(Rdate)+".xlsx")

except:

   
   print("the execution is intrupted ,so we start the execution again")
   try:
       os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
       os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
       os.remove('C:/Users/uday.gupta/Desktop/Parivahan/state.xls')
       d.close()
   except:
       d.close()
   










#
#profile = webdriver.FirefoxProfile()
#profile.set_preference("browser.download.panel.shown", False)
#profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
#profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.dir", "E:/vahan_parivahan/res")
#d = webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe",firefox_profile=profile)
##it is the link of the website from which we are going to scrap the data
#d.get("https://vahan.parivahan.gov.in/vahan4dashboard/")
#time.sleep(5)
#wait=WebDriverWait(d,40)
##these all variable is use to store the value of each table and then
## we are pass this value to dictionary so that we can get the all value together
##these all are the column of the table
#Top=['Serial No',' State Name', 
#       ' Rto Name', 'Fee(Cash)', ' Fee(Internet) ',
#       ' Fee(Other)', ' Tax(Cash) ', ' Tax(Internet)', ' Tax(Other)',
#       'Total Revenue ',' Transaction Type ', ' Total Revenue']
#main_table_data=pd.DataFrame(columns=Top)# we create a empty dataframe
#table_data=pd.DataFrame(columns=Top)#we have a dataframe with columns
#table_data.set_index('Serial No')#we make the serial no as index
#
##Select_date_function(d,wait)
#try:
#   WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
#   time.sleep(10)
#except:
#    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
#    time.sleep(5)
#    WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt68"]'))).click()
#    time.sleep(10)# Vehical Registration     
## Table data
#
#  #  all_table_xpath=['//*[@id="datatable_moreInfo13"]/div[2]/table','//*[@id="datatable_rtoWise"]/div[2]/table','//*[@id="datatableCategoryWise"]/div[2]/table','//*[@id="datatableVehicleClsssWise"]/div[2]/table']
#  #loop for the data of states
#download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_moreInfo13:csv"]'))).click()
#state_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/state.xls")
##state_data.columns.values
#for state_data_index in trange(len(state_data)):
#    #it is the Xpath for the states 
#    #state_data_index=1
#    #//*[@id="datatable_moreInfo13:1:j_idt101:1:j_idt103"]
#    x='//*[@id="datatable_moreInfo13:'+str(state_data_index)+':j_idt101:1:j_idt103"]'
#    try:
#        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13:0:j_idt101:1:j_idt103"]'))).click()
#        time.sleep(10)
#    except:
#        WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_paginator_bottom"]/a[3]'))).click()
#        element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_moreInfo13_data"]/tr[1]/td[2]'))).click()
#        time.sleep(10)
#    download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
#    RTO_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls")
#    #CategoryWise_data.columns.values
#    
#    for RTO_data_index in range(len(RTO_data)):
#        #it is the xpath for the Rtos
#        #RTO_data_index=6
#        #//*[@id="datatable_rtoWise:1:j_idt116:1:j_idt118"]
#        y='//*[@id="datatable_rtoWise:'+str(RTO_data_index)+':j_idt116:1:j_idt118"]'
#        try:
#            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
#            time.sleep(10)
#        except:
#            WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise_paginator_bottom"]/a[3]'))).click()
#            element1=WebDriverWait(d,5).until(EC.element_to_be_clickable((By.XPATH,y))).click()
#            time.sleep(10)
#        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
#        CategoryWise_data=pd.read_excel("C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls")
##        table_data=pd.DataFrame(columns=Top)
##        #this loop for the data of Vehical category
##        table_data[' Transaction Type ']=CategoryWise_data[' Transaction Type '] 
##        table_data[' Total Revenue']:CategoryWise_data[' Total Revenue']
##        table_data['Serial No']:state_data['Serial No'][state_data_index]
##        table_data[' State Name']:state_data[' State Name'][state_data_index]
##        table_data['Fee(Cash)']:state_data['Fee(Cash)'][state_data_index]
##        table_data[' Fee(Internet) ']:state_data[' Fee(Internet) '][state_data_index]
##        table_data[' Fee(Other)']:state_data['Fee(Cash)'][state_data_index]
##        table_data[' Tax(Cash) ']:state_data[' Tax(Cash) '][state_data_index]
##        table_data[' Tax(Internet)']:state_data[' Tax(Internet)'][state_data_index]
##        table_data[' Tax(Other)']:state_data[' Tax(Other)'][state_data_index]
##        table_data['Total Revenue ']:state_data['Total Revenue '][state_data_index]
##        table_data[' Rto Name']:RTO_data[' Rto Name'][RTO_data_index]
##        table_data['Fee(Cash)']:RTO_data['Fee(Cash)'][RTO_data_index]
##        table_data[' Fee(Internet) ']:RTO_data[' Fee(Internet) '][RTO_data_index]
##        
##        table_data[' Fee(Other)']:RTO_data[' Fee(Other)'][RTO_data_index]
##        table_data[' Tax(Cash) ']:RTO_data[' Tax(Cash) '][RTO_data_index]
##        table_data[' Tax(Internet)']:RTO_data[' Tax(Internet)'][RTO_data_index]
##        table_data[' Tax(Other)']:RTO_data[' Tax(Other)'][RTO_data_index]
##        table_data['Total Revenue ']:RTO_data['Total Revenue '][RTO_data_index]
##        
##        main_table_data=main_table_data.append(table_data,ignore_index=True,sort=False)
#        
#        for CategoryWise_index in range(len(CategoryWise_data)):
#            #link for the 
#            
#            dt1={'Serial No':state_data['Serial No'][state_data_index],' State Name':state_data[' State Name'][state_data_index],
#       ' Rto Name':RTO_data[' Rto Name'][RTO_data_index], 'Fee(Cash)':RTO_data['Fee(Cash)'][RTO_data_index], ' Fee(Internet) ':RTO_data[' Fee(Internet) '][RTO_data_index],
#       ' Fee(Other)':RTO_data[' Fee(Other)'][RTO_data_index], ' Tax(Cash) ':RTO_data[' Tax(Cash) '][RTO_data_index], ' Tax(Internet)':RTO_data[' Tax(Internet)'][RTO_data_index], ' Tax(Other)':RTO_data[' Tax(Other)'][RTO_data_index],
#       'Total Revenue ':RTO_data['Total Revenue '][RTO_data_index],' Transaction Type ':CategoryWise_data[' Transaction Type '][CategoryWise_index], ' Total Revenue':CategoryWise_data[' Total Revenue'][CategoryWise_index]}
#                
#            table_data = table_data.append(dt1,ignore_index=True,sort=False)
#            print(table_data.shape)
##        
#        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/CategoryWise.xls')
#        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt129"]'))).click()
#        time.sleep(5)
#    os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
#    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise:j_idt114"]'))).click()
#    time.sleep(5)
#os.remove('C:/Users/uday.gupta/Desktop/Parivahan/state.xls') 
#table_data.to_csv("E:/Hdfc/vahan_parivahan/res/Vehical_Month_wise_review.csv")
