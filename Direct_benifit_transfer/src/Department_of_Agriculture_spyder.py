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

def transformation5(val):
    q=str(val)
    c=[]
    for i in q.split(' '):
        c.append(i)
        val=c
    if len(c)>5:
        l= len(c)-5
        if l==1:
            c[1]=c[1]+' '+c[2]
            del c[2]
        if l==2:
            c[1]=c[1]+' '+c[2]+' '+c[3]
            del c[2]
            del c[2]
        if l==3:
            c[1]=c[1]+' '+c[2]+' '+c[3]+' '+c[4]
            del c[2]
            del c[2]
            del c[3]
        val=c
    return(val)
d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
d.get("https://www.dbtdacfw.gov.in/DashboardHome.aspx?DeptCode=1&FinYear=0")
wait=WebDriverWait(d,40)
Top=['S.No','Short Name','Scheme Name','Scheme Total','State','Total No. of Beneficiary','Total No. of Beneficiary with Aadhar No','Total No. of Beneficiary with bank Account','District','Total No. of Beneficiary','Total No. of Beneficiary with Aadhar No','Total No. of Beneficiary with bank Account']
table_data=pd.DataFrame()# we create a empty dataframe
table_data=pd.DataFrame(columns=Top)#
from datetime import date
from dateutil.parser import parse
today_date = date.today()
todaydate=parse(str(today_date))
value1_of_today=todaydate.strftime(" %d-%m-%Y ,%I:%M%p")
for i in tqdm(range(2,5)):
    #click on the the select year
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_ddlFinyear"]'))).click()
    time.sleep(2)
    #select the year value i=2
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_ddlFinyear"]/option['+str(i)+']'))).click()
    time.sleep(2)
    #click on the search button
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_btnSearch"]'))).click()
    time.sleep(2)
    html_string1=d.page_source
    scheme_table = pd.read_html(html_string1)
    #scheme_table[0].columns.values
    #scheme_table = pd.read_html('https://www.dbtdacfw.gov.in/DashboardHome.aspx?DeptCode=1&FinYear=0')
    
    for scheme_table_index in tqdm(range(len(scheme_table[0])-1)):
        #scheme_table_index=3
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView6_lbltest_'+str(scheme_table_index)+'"]'))).click()
        #html_string=d.page_source
        #scheme_sub_table = pd.read_html(html_string)
        time.sleep(2)
        table_id2=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView7"]')))
        rows_table_id2=[]#it stote the all the value of the 
        rows_table_id2_webelement=table_id2.find_elements_by_tag_name('tr')
        for dt2 in range(1,len(rows_table_id2_webelement)-1):
            #print(rows_table_id2_webelement[dt2].text)
            dtt2=transformation5(rows_table_id2_webelement[dt2].text)
            rows_table_id2.append(dtt2)
        #scheme_sub_table[0].columns.values
        for scheme_sub_table_index in range(len(rows_table_id2)):
            #scheme_sub_table_index=2
             #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView7"]/tbody/tr['+str(scheme_sub_table_index)+']/td[2]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView7_LinkButtonStateName_'+str(scheme_sub_table_index)+'"]'))).click()
            time.sleep(2)
            table_id3=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView8"]')))
            rows_table_id3=[]#it stote the all the value of the 
            rows_table_id3_webelement=table_id3.find_elements_by_tag_name('tr')
            for dt3 in range(1,len(rows_table_id3_webelement)-1):
                #print(rows_table_id3_webelement[dt3].text)
                dtt3=transformation5(rows_table_id3_webelement[dt3].text)
                rows_table_id3.append(dtt3)
             #html_string_state=d.page_source
#             soup = BeautifulSoup(html_string_state,features="lxml")
#             dt=soup.find("table", { "id":"ContentPlaceHolder1_GridView8"})
             #scheme_sub_table_state = pd.read_html(html_string_state)
             #scheme_sub_table_state[0].columns.values
            if len(rows_table_id3) ==0:
                #putiing the None value
                dt1={'S.No':scheme_table[0]['S.No'][scheme_table_index],
                       'Short Name':scheme_table[0]['Short Name'][scheme_table_index],
                      'Scheme Name':scheme_table[0]['Scheme Name'][scheme_table_index],
                       'Scheme Total':scheme_table[0]['Scheme Total'][scheme_table_index],
                      'State':rows_table_id2[scheme_sub_table_index][1],
                      'Total No. of Beneficiary':rows_table_id2[scheme_sub_table_index][2],
                      'Total No. of Beneficiary with Aadhar No':rows_table_id2[scheme_sub_table_index][3],
                      'Total No. of Beneficiary with bank Account':rows_table_id2[scheme_sub_table_index][4],
                      'District':None,
                      'Total No. of Beneficiary':None,
                      'Total No. of Beneficiary with Aadhar No':None,
                      'Total No. of Beneficiary with bank Account':None}
                table_data = table_data.append(dt1,ignore_index=True,sort=False)
            else:   
                 for scheme_sub_table_state_index in range(len(rows_table_id3)):
                     dt1={'S.No':scheme_table[0]['S.No'][scheme_table_index],
                           'Short Name':scheme_table[0]['Short Name'][scheme_table_index],
                          'Scheme Name':scheme_table[0]['Scheme Name'][scheme_table_index],
                           'Scheme Total':scheme_table[0]['Scheme Total'][scheme_table_index],
                          'State':rows_table_id2[scheme_sub_table_index][1],
                          'Total No. of Beneficiary':rows_table_id2[scheme_sub_table_index][2],
                          'Total No. of Beneficiary with Aadhar No':rows_table_id2[scheme_sub_table_index][3],
                          'Total No. of Beneficiary with bank Account':rows_table_id2[scheme_sub_table_index][4],
                          'District':rows_table_id3[scheme_sub_table_state_index][1],
                          'Total No. of Beneficiary':rows_table_id3[scheme_sub_table_state_index][2],
                          'Total No. of Beneficiary with Aadhar No':rows_table_id3[scheme_sub_table_state_index][3],
                          'Total No. of Beneficiary with bank Account':rows_table_id3[scheme_sub_table_state_index][4]}
                     table_data = table_data.append(dt1,ignore_index=True,sort=False)
#             
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_lnkstate"]'))).click()
            time.sleep(2)            
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_lnkscheme"]'))).click()
        time.sleep(2)
    #table_data.to_csv("E:/Direct_benifit_transfer/res/Direct_benifit_transfer1_of_{}.csv".format(str(value1_of_today)))
table_data.to_csv("E:/Direct_benifit_transfer/res/Direct_benifit_transfer.csv")
      