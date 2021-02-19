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
    """
    This function written to tranform the list to size of 5 from size of more then 5

    Parameters:
    val(list): It is the list which have size more than 5

    Returns:
    list: It return the list which have the size of 5

    """
#    val='1 ANDAMAN AND NICOBAR ISLANDS 39 36 38'
    q=str(val)
    c=[x for x in q.split(' ') ]
#    print(c)
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
            del c[2]
        if l==4:
            c[1]=c[1]+' '+c[2]+' '+c[3]+' '+c[4]+' '+c[5]
            del c[2]
            del c[2]
            del c[2]
            del c[2]
        
    return(c)


d=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
d.get("https://www.dbtdacfw.gov.in/DashboardHome.aspx?DeptCode=1&FinYear=0")
d.maximize_window
wait=WebDriverWait(d,40)
#year=['2018-19','2017-18','2019-20']
Top=['Period','Short Name','Scheme Name','Scheme Total','State','Total No. of Beneficiary','Total No. of Beneficiary with Aadhar No','Total No. of Beneficiary with bank Account','District','Total No. of Beneficiary of District','Total No. of Beneficiary with Aadhar No of District','Total No. of Beneficiary with bank Account of District']
table_data=pd.DataFrame()# we create a empty dataframe
table_data=pd.DataFrame(columns=Top)#
from datetime import date
from dateutil.parser import parse
today_date = date.today()
todaydate=parse(str(today_date))
value1_of_today=todaydate.strftime(" %d-%m-%Y ,%I:%M%p")
Year_val=Select(d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ddlFinyear"]'))
year=[x.text for x in Year_val.options]
for i in tqdm(range(2,len(year))):
    #i=3
    #click on the the select year   //*[@id="ContentPlaceHolder1_ddlFinyear"]/option[2]
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
    #code for date
    #i=2
    Start=year[i-1][:4]
    End='20'+year[i-1][5:8]
    period=datetime.strftime(datetime.strptime('31 03 {}'.format(End),'%d %m %Y'),'%d/%m/%Y')
    for scheme_table_index in tqdm(range(len(scheme_table[0])-1)):
        #scheme_table_index=9
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
        if len(rows_table_id2)!=0 and scheme_table[0]['Scheme Total'][scheme_table_index] != 0: 
            for scheme_sub_table_index in range(len(rows_table_id2)):
                #scheme_sub_table_index=2
                 #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView7"]/tbody/tr['+str(scheme_sub_table_index)+']/td[2]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_GridView7_LinkButtonStateName_'+str(scheme_sub_table_index)+'"]'))).click()
                time.sleep(10)
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
                    dt1={
                           'Period':period,
                           'Short Name':scheme_table[0]['Short Name'][scheme_table_index],
                          'Scheme Name':scheme_table[0]['Scheme Name'][scheme_table_index],
                           'Scheme Total':scheme_table[0]['Scheme Total'][scheme_table_index],
                          'State':rows_table_id2[scheme_sub_table_index][1],
                          'Total No. of Beneficiary':rows_table_id2[scheme_sub_table_index][2],
                          'Total No. of Beneficiary with Aadhar No':rows_table_id2[scheme_sub_table_index][3],
                          'Total No. of Beneficiary with bank Account':rows_table_id2[scheme_sub_table_index][4],
                          'District':None,
                          'Total No. of Beneficiary of District':None,
                          'Total No. of Beneficiary with Aadhar No of District':None,
                          'Total No. of Beneficiary with bank Account of District':None}
                    table_data = table_data.append(dt1,ignore_index=True,sort=False)
                else:
                     for scheme_sub_table_state_index in range(len(rows_table_id3)):
                         dt1={
                                'Period':period,
                               'Short Name':scheme_table[0]['Short Name'][scheme_table_index],
                              'Scheme Name':scheme_table[0]['Scheme Name'][scheme_table_index],
                               'Scheme Total':scheme_table[0]['Scheme Total'][scheme_table_index],
                              'State':rows_table_id2[scheme_sub_table_index][1],
                              'Total No. of Beneficiary':rows_table_id2[scheme_sub_table_index][2],
                              'Total No. of Beneficiary with Aadhar No':rows_table_id2[scheme_sub_table_index][3],
                              'Total No. of Beneficiary with bank Account':rows_table_id2[scheme_sub_table_index][4],
                              'District':rows_table_id3[scheme_sub_table_state_index][1],
                              'Total No. of Beneficiary of District':rows_table_id3[scheme_sub_table_state_index][2],
                              'Total No. of Beneficiary with Aadhar No of District':rows_table_id3[scheme_sub_table_state_index][3],
                              'Total No. of Beneficiary with bank Account of District':rows_table_id3[scheme_sub_table_state_index][4]}
                         table_data = table_data.append(dt1,ignore_index=True,sort=False)
    #
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_lnkstate"]'))).click()
                time.sleep(5)
        else:
             dt1={
                           'Period':period,
                           'Short Name':scheme_table[0]['Short Name'][scheme_table_index],
                          'Scheme Name':scheme_table[0]['Scheme Name'][scheme_table_index],
                           'Scheme Total':scheme_table[0]['Scheme Total'][scheme_table_index],
                          'State':None,
                          'Total No. of Beneficiary':None,
                          'Total No. of Beneficiary with Aadhar No':None,
                          'Total No. of Beneficiary with bank Account':None,
                          'District':None,
                          'Total No. of Beneficiary of District':None,
                          'Total No. of Beneficiary with Aadhar No of District':None,
                          'Total No. of Beneficiary with bank Account of District':None}
             table_data = table_data.append(dt1,ignore_index=True,sort=False)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ContentPlaceHolder1_lnkscheme"]'))).click()
        time.sleep(5)
    #table_data.to_csv("E:/Direct_benifit_transfer/res/Direct_benifit_transfer1_of_{}.csv".format(str(value1_of_today)))
table_data.to_excel("E:/Hdfc/Direct_benifit_transfer/res/Direct_benifit_transfer_new.xlsx")




import urllib 
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from tqdm import tqdm 
'''----------------------------------------------------------->-----------------------'''
def insert_into_database(Main_DataFrame):
#    Main_DataFrame = pd.read_excel("E:/Hdfc/Direct_benifit_transfer/res/Direct_benifit_transfer_new.xlsx")

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
    district_dim.columns
    #Main_DataFrame['DISTRICT'] = ''
    
    d_list = list(district_dim.DISTRICT)
    for i,j in tqdm(enumerate(list(Main_DataFrame['District']))):
            name=process.extractOne(j, d_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['District'][i]=name[0]
    
    d_list = list(state_dim.STATE)            
    for i,j in tqdm(enumerate(list(Main_DataFrame['State']))):
            name=process.extractOne(j, d_list,scorer=fuzz.token_set_ratio,score_cutoff=80)
        #    x=process.extract(j,d_list)
            if type(name)==tuple:
                Main_DataFrame['State'][i]=name[0]
            else:
                Main_DataFrame['State'][i]=np.nan
                
                
                
    data = pd.merge(Main_DataFrame,district_dim[['EXT_DISTRICT_SEQ_ID', 'DISTRICT']],left_on = ['District'],right_on = ['DISTRICT'] ,how ='left' )
    data = pd.merge(data,state_dim[['EXT_STATE_SEQ_ID', 'STATE']],left_on = ['State'],right_on = ['STATE'] ,how ='left' )
    data = data.fillna(" ")
    data = data.drop(columns= ['Unnamed: 0','STATE','DISTRICT'])
    
    data.dtypes
    
    data['Period'] = pd.to_datetime(data['Period']).dt.strftime('%m/%d/%Y')
    data.to_sql('Direct_benifit_transfer',engine1,if_exists='append', index=False)
    print('inserted into database')

Main_DataFrame = pd.read_excel("E:/Hdfc/Direct_benifit_transfer/res/Direct_benifit_transfer_new.xlsx")
insert_into_database(Main_DataFrame)
