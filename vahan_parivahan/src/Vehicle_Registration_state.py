# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:30:07 2019

@author: bot_user
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
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def Starting_date(wait,k,driver,i):
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_fromDate_input"]'))).click()
    yr=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[2]'))
    yr.select_by_value(str(i))
    mt=Select( driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]'))
    mt.select_by_value(str(k-1))

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
        if day == l:
            path=first_week[day]
    wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
    time.sleep(10)
    Rdate=month+'-'+year
    print(Rdate)
    return Rdate


def Ending_date(wait,k,driver,i):
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
    print(' month :',k)
    print(lastday)
    l=lastday.strftime("%A")
    try:
        for day in last_week2.keys():
            if day==l:
                path=last_week2[day]
        wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
    except:
        for day in last_week1.keys():
            if day==l:
                path=last_week1[day]
        wait.until(EC.element_to_be_clickable((By.XPATH,path))).click()
    time.sleep(10)
    return Period

T = True

count = 0
while T == True:
    try:
        try:
           try:
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\tacPendingForApproval.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\CategoryWise.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\Classwise.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\state.xls")
           except:
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\tacPendingForApproval.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\CategoryWise.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Classwise.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\state.xls")
        except:
           pass

        try:
            log=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\log.text','a',encoding='utf-8')
        except:
           log=open(r'E:\Hdfc\vahan_parivahan\res\log.text','a',encoding='utf-8')

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.panel.shown", False)
        profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
        profile.set_preference("browser.download.folderList", 2)
        try:
            profile.set_preference("browser.download.dir", r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration")
        except:
            profile.set_preference("browser.download.dir", r"C:\Users\uday.gupta\Desktop\Parivahan")

        try:
            driver = webdriver.Firefox(executable_path=r"C:\Drivers\geckodriver.exe",firefox_profile = profile)
        except:
            driver = webdriver.Firefox(executable_path=r"D:\Hdfc_Scrapping_data\Uday\driver\geckodriver.exe",firefox_profile = profile)
        #it is the link of the website from which we are going to scrap the data   D:\Hdfc_Scrapping_data\Uday\driver
        driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/dashboardview.xhtml")
        time.sleep(5)
        #these all variable is use to store the value of each table and then
        # we are pass this value to dictionary so that we can get the all value together
        #put that value
        #these all are the column of the table
        wait = WebDriverWait(driver,10)
        driver.maximize_window()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt17"]'))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt17_2"]'))).click()
        time.sleep(10)
        Top = ['Period',
        'State',
        'RTO Name',
        'RTO Transport',
        'RTO Non Transport',
        'Vehicle Category',
        'Vehicle_Class','vehical_class_Total']
        first_week = {'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[7]'}
        last_week1 = {'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[7]'}
        last_week2 = {'Sunday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[1]','Monday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[2]','Tuesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[3]','Wednesday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[4]','Thursday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[5]','Friday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[6]','Saturday':'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[7]'}

        try:
            Type = driver.find_element_by_xpath('//*[@id="j_idt24_label"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="j_idt24_3"]').click()
            time.sleep(2)
        except:
            pass


        try:
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\index.text','r')
            except:
                f=open(r'E:\Hdfc\vahan_parivahan\res\year.text','r')
            start_year = f.read()
            f.close()
        except:
            start_year = '2018'
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\index.text','w+',encoding='utf-8')
            except:
                f=open(r'E:\Hdfc\vahan_parivahan\res\year.text','w+',encoding='utf-8')
            f.write(start_year)
            f.close()
        for i in range(int(start_year),2020):
            #i=2018
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\index.text','w+',encoding='utf-8')
            except:
                f=open(r'E:\Hdfc\vahan_parivahan\res\year.text','w+',encoding='utf-8')
            f.write(str(i))
            f.close()
            try:
                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\month.text','r')
                except:
                    f=open(r'E:\Hdfc\vahan_parivahan\res\month.text','r')
                start_month = f.read()
                f.close()
            except:
                start_month = '0'
                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\index.text','w+',encoding='utf-8')
                except:
                    f=open(r'E:\Hdfc\vahan_parivahan\res\month.text','w+',encoding='utf-8')
                f.write(start_month)
                f.close()

            for k in range(int(start_month),13):
                #for upto   k=1
                Period = Ending_date(wait,k,driver,i)


#            #for from
                Rdate = Starting_date(wait,k,driver,i)
                log.write('Fetching the data of of month : {} \n '.format(Rdate))
                try:
                    try:
                        table_main_data = pd.read_csv("E:/Hdfc/vahan_parivahan/res/Vehical_Registration_{}.csv".format(Rdate))
                        table_main_data = table_main_data.drop(columns = table_main_data.columns[0])
#                            table_main_data =table_main_data.dropna()
                    except:
                        table_main_data = pd.read_csv(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Vehical_Registration_{}.csv".format(Rdate))
                        table_main_data = table_main_data.drop(columns = table_main_data.columns[0])
                except:
                    table_main_data = pd.DataFrame()
                print('read data from excel have size of {} \n'.format(table_main_data.shape))
                # wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt39"]'))).click()
                # html_list = wait.until(EC.presence_of_element_located((By.ID,'j_idt39_items')))
                # items = html_list.find_elements_by_tag_name("li")
                # for item in items:
                #     text = item.text
                    # print(text)
                print('the state data is fetching')
                try:
                    try:
                        f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\states_index.text','r')
                    except:
                        f=open(r'E:\Hdfc\vahan_parivahan\res\states_index.text','r')
                    states_index = f.read()
                    f.close()
                except:
                    states_index = '0'
                    try:
                        f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\states_index.text','w+',encoding='utf-8')
                    except:
                        f=open(r'E:\Hdfc\vahan_parivahan\res\states_index.text','w+',encoding='utf-8')
                    f.write(states_index)
                    f.close()
                print(states_index)
                # ==================================================================
                # for state_value_options_index in tqdm(range(int(states_index),len(items))):
                #     # state_value_options_index=1
                #     table_data = pd.DataFrame()
                #     try:
                #         f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\states_index.text','w+',encoding='utf-8')
                #     except:
                #         f=open(r'E:\Hdfc\vahan_parivahan\res\states_index.text','w+',encoding='utf-8')
                #     f.write(str(state_value_options_index))
                #     f.close()
                #     wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt39_label"]'))).click()
                #     time.sleep(5)
                #     # //*[@id="j_idt39_4"]
                #     st_xpath='//*[@id="j_idt39_'+str(state_value_options_index)+'"]'
                #     stt_v = wait.until(EC.element_to_be_clickable((By.XPATH,st_xpath)))
                #     state_name = stt_v.get_attribute('innerText').split('(')[0]
                #     stt_v.click()
                #     time.sleep(2)
                    # try:
                    #      wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt58"]'))).click()
                    #      time.sleep(5)
                    # except:
                    #     print('not able to click on Vehical registration link') # Vehical Registration
                try:
                     wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j_idt58"]'))).click()
                     time.sleep(30)
                except:
                    print('not able to click on Vehical registration link') # Vehical Registration

                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_moreInfo13:csv"]'))).click()
                print('Downloaded state file')
                time.sleep(3)
                try:
                    download_st = pd.read_excel(r"C:\Users\uday.gupta\Desktop\Parivahan\state.xls")
                except:
                    download_st = pd.read_excel(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\state   .xls")

                for st_in in range(int(states_index),len(download_st)):
                    # st_in = 2
                    state_name = download_st[' State '][st_in]
                    try:
                        f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\states_index.text','w+',encoding='utf-8')
                    except:
                        f=open(r'E:\Hdfc\vahan_parivahan\res\states_index.text','w+',encoding='utf-8')
                    f.write(str(st_in))
                    f.close()
                    st_xpath_n = '//*[@id="datatable_moreInfo13:'+str(st_in)+':j_idt121:1:j_idt123"]'

                    try:
                        element1=wait.until(EC.element_to_be_clickable((By.XPATH,st_xpath_n))).click()
                        time.sleep(30)

                    except:
                        try:
                            wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div[3]/a[3]'))).click()
                            time.sleep(3)
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,st_xpath_n))).click()
                            time.sleep(30)
                        except Exception as ex:
                            print(ex)
                            continue

                    download_rto = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatable_rtoWise:csv"]'))).click()
                    print('Downloaded rto file')
                    time.sleep(1)
                    try:
                        rto_data = pd.read_excel(r"C:\Users\uday.gupta\Desktop\Parivahan\tacPendingForApproval.xls")
                    except:
                        rto_data = pd.read_excel(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\tacPendingForApproval.xls")

                    #rto_data.columns.values
                    try:
                        try:
                            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\rto_index.text','r')
                        except:
                            f=open(r'E:\Hdfc\vahan_parivahan\res\rto_index.text','r')
                        rto_index = f.read()
                        f.close()
                    except:
                        rto_index = '0'
                        try:
                            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\rto_index.text','w+',encoding='utf-8')
                        except:
                            f=open(r'E:\Hdfc\vahan_parivahan\res\rto_index.text','w+',encoding='utf-8')
                        f.write(rto_index)
                        f.close()

                        print('No of rtos are : {}'.format(str(len(rto_data))))
                    for rto_data_index in range(int(rto_index),len(rto_data)):
                        #it is the Xpath for the states
                        #rto_data_index=0
                        #x=//*[@id="datatable_rtoWise:0:j_idt131:1:j_idt133"]
                        table_data = pd.DataFrame()
                        try:
                            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\rto_index.text','w+',encoding='utf-8')
                        except:
                            f=open(r'E:\Hdfc\vahan_parivahan\res\rto_index.text','w+',encoding='utf-8')
                        f.write(str(rto_data_index))
                        f.close()
                        log.write('RTO no.: {} \n'.format(rto_data_index))
                        print(rto_data_index)
#                            //*[@id="datatable_rtoWise:0:j_idt136:1:j_idt138"]
                        x='//*[@id="datatable_rtoWise:'+str(rto_data_index)+':j_idt136:1:j_idt138"]'
                        try:
                            element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                            time.sleep(30)

                        except:
                            try:
                                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise_paginator_bottom"]/a[3]'))).click()
                                time.sleep(10)
                                element1=wait.until(EC.element_to_be_clickable((By.XPATH,x))).click()
                                time.sleep(30)
                            except Exception as ex:
                                print(ex)
                                continue
                        download=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableCategoryWise:csv"]'))).click()
                        time.sleep(3)
                        try:
                            CategoryWise_data=pd.read_excel(r"C:\Users\uday.gupta\Desktop\Parivahan\CategoryWise.xls")
                        except:
                            CategoryWise_data=pd.read_excel(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\CategoryWise.xls")
                        #classwise_data.columns.values
                        for CategoryWise_data_index in range(len(CategoryWise_data)):
                            #it is the xpath for the Rtos
                            #CategoryWise_data_index=0
                            #//*[@id="datatableCategoryWise:0:j_idt156"]
                            y='//*[@id="datatableCategoryWise:'+str(CategoryWise_data_index)+':j_idt156"]'
                            try:
                                element1=wait.until(EC.element_to_be_clickable((By.XPATH,y))).click()
                                time.sleep(30)
                            except:
                                try:
                                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise_paginator_bottom"]/a[3]'))).click()
                                    time.sleep(10)
                                    element1=wait.until(EC.element_to_be_clickable((By.XPATH,y))).click()
                                    time.sleep(10)
                                except:
                                    continue
                            downlosd3 = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="datatableVehicleClsssWise:csv"]'))).click()
                            time.sleep(2)
                            try:
                                classwise_data=pd.read_excel(r"C:\Users\uday.gupta\Desktop\Parivahan\Classwise.xls")
                            except:
                                classwise_data=pd.read_excel(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Classwise.xls")
# classwise_data.columns
                            dt1={}
                            for classwise_data_index in range(len(classwise_data)):
                                #link for the      classwise_data_index=0
                                dt1={'Period':Period,'State':download_st[' State '][st_in],
                                     'RTO Name':rto_data[' RTO Name '][rto_data_index],
                                    'RTO Transport':rto_data[' Transport '][rto_data_index],
                                    'RTO Non Transport':rto_data[' Non Transport '][rto_data_index],
                                    'Vehicle Category':CategoryWise_data[' Vehicle Category '][CategoryWise_data_index],
                                    'Vehicle_Class':classwise_data[' Vehicle Class '][classwise_data_index],
                                    'vehical_class_Total':classwise_data[' Total'][classwise_data_index]}

                                table_data = table_data.append(dt1,ignore_index=True,sort=False)

#                                print(table_data.shape)

                            try:
                                os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\Classwise.xls")
                            except:
                                os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Classwise.xls")
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableVehicleClsssWise:j_idt169"]'))).click()
                            time.sleep(5)
                        try:
                            os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\CategoryWise.xls")
                        except:
                            os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\CategoryWise.xls")

                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatableCategoryWise:j_idt149"]'))).click()
                        time.sleep(10)
                        table_main_data = table_main_data.append(table_data, ignore_index = True)
                        print(table_main_data.shape)
                        try:
                            table_main_data.to_csv("E:/Hdfc/vahan_parivahan/res/Vehical_Registration_{}.csv".format(Rdate))
                        except:
                            table_main_data.to_csv(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Vehical_Registration_{}.csv".format(Rdate))
                    try:
                        f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\rto_index.text','w+',encoding='utf-8')
                    except:
                        f=open(r'E:\Hdfc\vahan_parivahan\res\rto_index.text','w+',encoding='utf-8')
                    f.write('0')
                    f.close()
                    try:
                        os.remove('C:/Users/uday.gupta/Desktop/Parivahan/tacPendingForApproval.xls')
                    except:
                        os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\tacPendingForApproval.xls")
#                        table_main_data = table__main_data.append(table_data, ignore_index = True)
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datatable_rtoWise:j_idt134"]'))).click()
                    time.sleep(5)
                    log.write('Fetch the data of state: {} \n'.format(state_name))

                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\index.text','w+',encoding='utf-8')
                except:
                    f=open(r'E:\Hdfc\vahan_parivahan\res\month.text','w+',encoding='utf-8')
                f.write(str(k))
                f.close()
                log.close()





        T = False
    except Exception as e:

       driver.close()
       print(e)
       count = count + 1
       print(count)
       log.write("the execution is intrupted ,so we start the execution again after 15 min \n")
       log.close()
       print("the execution is intrupted ,so we start the execution again")
       try:
           try:
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\tacPendingForApproval.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\CategoryWise.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\Classwise.xls")
               os.remove(r"C:\Users\uday.gupta\Desktop\Parivahan\state.xls")
           except:
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\tacPendingForApproval.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\CategoryWise.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\Classwise.xls")
               os.remove(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\vahan_parivahan\Vehgical_registration\state.xls")
       except:
           print('file deleted from downloadfile')
       time.sleep(300)
