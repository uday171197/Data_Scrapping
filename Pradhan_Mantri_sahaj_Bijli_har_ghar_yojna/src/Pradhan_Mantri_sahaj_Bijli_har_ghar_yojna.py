# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:56:41 2019

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
from datetime import datetime,date,timedelta
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from tqdm import tqdm
d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
d.get("https://saubhagya.gov.in/")
time.sleep(1)
d.maximize_window()
wait=WebDriverWait(d,100)
#table declearation
last_day=date.today()-timedelta(days=1)
last=last_day.strftime('%d %b,%Y')
col=['Sr_No.','State','District','Total Households','Electrified Households as on 10th Oct,2017','Balance Unelectrified Households as on 10th Oct,2017', 'Household Progress from 10th Oct,2017 to '+last_day.strftime(' %b,%Y')+' (a)','Additional Households electrifed from 1st Feb,2019 onwards due to Saubhagya Rath Campaigns, Camps, Control Centre, etc to till date (b)','Total Progress (a+b)','Progress on '+last+' day (last)','Balance Un-electrified Households','Household Electrification (%)']
#state_table=pd.DataFrame(columns=['District','Total Households','Electrified Households as on 10th Oct,2017','Balance Unelectrified Households as on 10th Oct,2017', 'Household Progress from 10th Oct,2017 to 31th Jan,2019 (a)','Additional Households electrifed from 1st Feb,2019 onwards due to Saubhagya Rath Campaigns, Camps, Control Centre, etc to till date (b)','Total Progress (a+b)','Progress on last day (20-08-2019)','Balance Un-electrified Households','Household Electrification (%)'])
main_Dataframe=pd.DataFrame(columns=col)

#to find all the state value
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="myfilters"]/div[1]'))).click()
state_value=Select(d.find_element_by_xpath('//*[@id="state"]'))
state_value_options = [x.text for x in state_value.options]
state_value.select_by_index(2)
#print(state_value_options)
Sr_no=1
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="myfilters"]/div[2]'))).click()
#District_value=Select(d.find_element_by_xpath('//*[@id="district"]'))
#District_value_options=[x.text for x in District_value.options]
#print(District_value_options)

#element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="monthlyhhp"]/div[1]/canvas')))
#element.location_once_scrolled_into_view
#d.execute_script("arguments[0].scrollIntoView();", element)
#action = webdriver.common.action_chains.ActionChains(d)
#action.move_to_element_with_offset(element, 0, 5)
#action.click()
#action.perform()

for state_value_index in tqdm(range(1,len(state_value_options))):
    state_value.select_by_index(state_value_index)
    time.sleep(1)
    html=d.page_source
    soup=BeautifulSoup(html,'html.parser')
    try:
        show_entries=Select(d.find_element_by_xpath('//*[@id="maintable_length"]/label/select'))
        show_entries.select_by_index(3)
        cast_table=soup.find("div",{"class":"dataTables_scrollBody"})
        table_d=pd.read_html(str(cast_table))
        table_data=table_d[0][:len(table_d[0])-1]
        table_data[0]['Sr_No.']=''
        table_data[0]['State']=''
        table_data[0]['Sr_No.']=Sr_no
        table_data[0]['State']=state_value.first_selected_option.text
        main_Dataframe=main_Dataframe.append(table_data,ignore_index=True,sort=False)
        Sr_no=Sr_no+1
    except:
#        table_data=pd.DataFrame(columns=['Total Households','Electrified Households as on 10th Oct,2017','Balance Unelectrified Households as on 10th Oct,2017', 'Household Progress from 10th Oct,2017 to 31th Jan,2019 (a)','Additional Households electrifed from 1st Feb,2019 onwards due to Saubhagya Rath Campaigns, Camps, Control Centre, etc to till date (b)','Total Progress (a+b)','Progress on last day (20-08-2019)','Balance Un-electrified Households','Household Electrification (%)'])
        None_table={}
        for i in col:
            if i== 'Sr_No.':
                None_table[i]=Sr_no
            elif i== 'State':
                None_table[i]=state_value.first_selected_option.text
            else:
                None_table[i]=None

        main_Dataframe=main_Dataframe.append(None_table,ignore_index=True,sort=False)
        Sr_no=Sr_no+1
d.close()
main_Dataframe.to_csv('E:/Pradhan_Mantri_sahaj_Bijli_har_ghar_yojna/res/Pradhan_Mantri_sahaj_Bijli_har_ghar_yojna.csv')
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe")
driver.get("https://saubhagya.gov.in/")

element_to_hover_over = driver.find_element_by_xpath('//*[@id="monthlyhhp"]/div[1]')

hover = ActionChains(driver).move_to_element(element_to_hover_over)
hover.perform()
#import  robot from 