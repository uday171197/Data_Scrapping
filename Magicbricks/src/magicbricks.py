# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:10:28 2019

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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def open_link(element,drive,area):
#    alert = drive.switch_to_alert()
#    alert_obj.dismiss()
    try:
        dict_data = {}
        drive.execute_script("arguments[0].click();", element)
        time.sleep(2)
        default_handle = drive.current_window_handle
        window_before = drive.window_handles[0]
        handles = list(drive.window_handles)
        #        time.sleep(2)
        assert len(handles) > 1
        #        window_after = driver.window_handles[1]
        handles.remove(default_handle)
        #        time.sleep(2)
        assert len(handles) > 0

        drive.switch_to.window(handles[0])
        html = drive.page_source
        soup = BeautifulSoup(html,'html.parser')
        val = soup.find_all("div",{"class":"m-srp-card SRCard"})
        data_col = ['Bedrooms','Bathrooms','Balcony','Store Room','Super area','Carpet area','Status','Transaction type','Floor','Car parking','Furnished status','Lift','Type of Ownership','Facing','Address','Landmarks','RERA ID','Overlooking','Flooring','Water Availability','Status of Electricity','Age of Construction','Furnishing','Authority Approval']


        Price = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="priceSv"]'))).get_attribute('innerText')
        Flat_Size =  wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="propertyDetailTabId"]/div[3]/div[1]/div/div[1]/div[3]/h1/span[1]'))).get_attribute('innerText')

        #Bathrooms = re.findall('\d{1,2}',soup.find("div",{"class":"p_infoColumn"}).text)[0]
        #Balcony = re.findall('\d{1,2}',soup.find("div",{"class":"p_infoColumn"}).text)[0]
        #Super_area = re.findall('\d{1,10}',soup.find("span",{"id":"coveredAreaDisplay"}).text)[0]
        #Carpet_area = re.findall('\d{1,10}',soup.find("span",{"id":"carpetAreaDisplay"}).text)[0]
        row_1 = soup.find("div",{"id":"firstFoldDisplay"}).text.split('\n')
        data_1 = [x for x in row_1  if x !='']
        try:
            row_2 = soup.find("div",{"id":"secondFoldDisplay"}).text.split('\n')
            data_2 = [x for x in row_2  if x !='']
        except:
            data_2 = []
        try:
            row_3 = soup.find("div",{"id":"fourthFoldDisplay"}).text.split('\n')
            data_3 = [x for x in row_3  if x !='']
        except:
            data_3 = []
        try:
            row_4 = soup.find("div",{"id":"forthfoldAllRegCounterExt"}).text.split('\n')
            data_4 = [x for x in row_4  if x !='']
        except:
            row_4 = soup.find("div",{"id":"fourthFoldDisplay"}).text.split('\n')
            data_4 = [x for x in row_4  if x !='']

            pass

        description = soup.find("div",{"class":"descriptionCont"}).text.split('\n')
        description_list = [x for x in description  if x !='']
        data_list = data_1 + data_2 + data_3 + data_4 + description_list
        main_list_data = []
        s = ' '
        for i in range(len(data_col)):
    #        i =3
            if data_col[i] in data_list :
                if data_col[i] in ['Super area','Carpet area']:
                    data_ind = data_list.index(data_col[i])
                    main_list_data.append(data_col[i])
                    main_list_data.append(s.join(data_list[data_ind+1:data_ind+3]))
                elif data_col[i] == 'Floor':
                    data_ind = data_list.index(data_col[i])
                    main_list_data.append(data_col[i])
                    main_list_data.append(data_list[data_ind+1].replace('\xa0',' '))
                else:
                    data_ind = data_list.index(data_col[i])
                    main_list_data.append(data_col[i])
                    main_list_data.append(data_list[data_ind+1])
            else:
                if  data_col[i] == 'Bedrooms' and 'Bedroom' in data_list:
                    data_ind = data_list.index('Bedroom')
                    main_list_data.append(data_col[i])
                    main_list_data.append(data_list[data_ind+1])
                elif data_col[i] == 'Bathrooms' and 'Bathroom' in data_list:
                    data_ind = data_list.index('Bathroom')
                    main_list_data.append(data_col[i])
                    main_list_data.append(data_list[data_ind+1])
                elif data_col[i] == 'Balcony' and 'Balconies' in data_list:
                    data_ind = data_list.index('Balconies')
                    main_list_data.append(data_col[i])
                    main_list_data.append(data_list[data_ind+1])
                else:
                    main_list_data.append(data_col[i])
                    main_list_data.append('None')

        ind_dic = 0
        dict_data['Price'] = Price.replace('₹','')
        dict_data['flat Size'] = Flat_Size
        dict_data['Area'] = area

        for col_ind  in range(len(data_col)):
            dict_data[main_list_data[ind_dic]] = main_list_data[ind_dic+1]
            ind_dic = ind_dic+2

    #    data_main = data_main.append(dict_data,ignore_index =True, sort = False)
    #    drive.current_url
        drive.close()
        drive.switch_to.window(default_handle)
#        print(dict_data)
    except Exception as e:
        print(e)
        drive.close()
        drive.switch_to.window(default_handle)
        pass

    return dict_data




T = True

while T == True:
    try:
        try:
            log=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\log_Magicbricks.text','a',encoding='utf-8')
        except:
            log=open(r'E:\Hdfc\Magicbricks\res\log_Magicbricks.text','a',encoding='utf-8')

        try:
            drive = webdriver.Chrome(executable_path=r"D:\Hdfc_Scrapping_data\Uday\driver\chromedriver.exe")
        except:
            drive = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
        drive.get('https://www.magicbricks.com/')
        time.sleep(5)
        drive.maximize_window()
        time.sleep(2)
        wait = WebDriverWait(drive ,10)

        try:
            data_main = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\Magicbricks.csv')
            data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
        except:
            data_main =pd.DataFrame()

        try:
            pincodes = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Pincode data\final_data.csv',usecols=[3,6,7,8,9])
        except:
            pincodes = pd.read_csv(r'E:\Hdfc\Pincode data\final_data.csv',usecols=[3,6,7,8,9])
        period=datetime.strftime(datetime.strptime('{} {} {}'.format(calendar.monthrange(date.today().year  ,date.today().month)[1],date.today().month,date.today().year),'%d %m %Y'),'%d/%m/%Y')
        try:
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\index.text','r')
                start_ind = f.read()
                f.close()
            except:
                f=open(r'E:\Hdfc\Magicbricks\res\index.text','r')
                start_ind = f.read()
                f.close()
        except:
            try:
                start_ind = 0
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\index.text','w+',encoding='utf-8')
                f.write('0')
                f.close()
            except:
                start_ind = 0
                f=open(r'E:\Hdfc\Magicbricks\res\index.text','w+',encoding='utf-8')
                f.write('0')
                f.close()
        # Area =['Kalina','Versova']#4,'J B Nagar','Marol','Khar East']
        for state_index_i in range(int(start_ind),len(pincodes.STATE.unique())):
    #        print(i) state_index_i = 1
            print(pincodes.STATE.unique()[state_index_i])
            Branch = pincodes[pincodes['STATE'] == pincodes.STATE.unique()[state_index_i] ]['BRANCH'].tolist()
    #    Branch = pincodes['STATE'].unique()
            print(len(Branch))
            try:

                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\index.text','w+',encoding='utf-8')
                f.write(str(state_index_i))
                f.close()
            except:
                f=open(r'E:\Hdfc\Magicbricks\res\index.text','w+',encoding='utf-8')
                f.write(str(state_index_i))
                f.close()

            try:
                try:
                    data_main = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\Magicbricks_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
                    data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
                except:
                    data_main = pd.read_csv(r'E:\Hdfc\Magicbricks\res\Magicbricks_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
                    data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
            except:
                data_main =pd.DataFrame()
            try:
                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\area_index.text','r')
                    start_area_index = f.read()
                    f.close()
                except:
                    f=open(r'E:\Hdfc\Magicbricks\res\area_index.text','r')
                    start_area_index = f.read()
                    f.close()
            except:
                try:
                    start_area_index = 0
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\area_index.text','w+',encoding='utf-8')
                    f.write('0')
                    f.close()
                except:
                    start_area_index = 0
                    f=open(r'E:\Hdfc\Magicbricks\res\area_index.text','w+',encoding='utf-8')
                    f.write('0')
                    f.close()
            for area_index,area in tqdm(enumerate(Branch[int(start_area_index):])):
            #    area = Branch[int(start_area_index)]
            #area_index = 1
                try:

                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\area_index.text','w+',encoding='utf-8')
                    f.write(str(int(start_area_index) + area_index))
                    f.close()
                except:
                    f=open(r'E:\Hdfc\Magicbricks\res\area_index.text','w+',encoding='utf-8')
                    f.write(str(int(start_area_index) + area_index))
                    f.close()
                print(str(int(start_area_index) + area_index) +' : '+ str(area))
                search = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="keyword"]')))
                search.clear()
                search.send_keys(area)
                #time.sleep(5)
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchWrap"]/div[4]'))).click()
                    time.sleep(3)
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchWrap"]/div[4]'))).click()
                    time.sleep(3)
                except:
                    pass

                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\area_index.text','w+',encoding='utf-8')
                    f.write(str(int(start_area_index) + area_index))
                    f.close()
                except:
                    f=open(r'E:\Hdfc\Magicbricks\res\area_index.text','w+',encoding='utf-8')
                    f.write(str(int(start_area_index) + area_index))
                    f.close()
                vald ='https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&Locality'

                if fuzz.ratio(drive.current_url, vald) >= 85 :

                #total_prop = int(re.findall('\d{1,7}',wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="resultDiv"]/div[1]/div[2]/div[1]/div[1]/div[3]'))).get_attribute('innerText'))[0])
                    ind = 0
                    html = drive.page_source
                    soup = BeautifulSoup(html,'html.parser')
                    val = soup.find_all("div",{"class":"m-srp-card SRCard"})
                    ids = [str(x)[int(re.search('resultBlockWrappe',str(x)).start()):int(re.search('resultBlockWrappe',str(x)).start())+26] for x in val ]
                    print(len(ids))

                    print('Loading the code..........')
                    for i in tqdm(range(0,200000,1000)):
                        drive.execute_script('window.scrollTo({}, {});'.format(0, i))
                        ind = 0
                        html = drive.page_source
                        soup = BeautifulSoup(html,'html.parser')
                        val = soup.find_all("div",{"class":"m-srp-card SRCard"})
                        ids1 = [str(x)[int(re.search('resultBlockWrappe',str(x)).start()):int(re.search('resultBlockWrappe',str(x)).start())+26] for x in val ]
                        ids1 = list(set(ids + ids1))
                        print(len(ids1))
                        time.sleep(0.5)




                    ids1 = ids+ids1
                    print(len(set(ids1)))

                        #v = re.search('resultBlockWrappe',str(val[0])).start()
                    #id = str(val[0])[int(v.start()):int(v.start())+26]

                #    //*[@id="resultBlockWrapper45733217"]/div[4]/div[3]/div[1]/h3/span
                    data_main1 = pd.DataFrame()
                    for index ,value in tqdm(enumerate(list(set(ids1)))):
                    #        print(index,value = ids[1])
                #        element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="{}"]/div[4]/div[3]/div[1]/h3/span'.format(ids[index]))))

                #//*[@id="resultBlockWrapper45733217"]    //*[@id="resultBlockWrapper45733217"]/div[4]/div[3]/div[1]/h3/span
                        element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="{}"]'.format(ids1[index]))))
                        try:
                            drive.execute_script("arguments[0].scrollIntoView();", element)
                        except:
                            element.location_once_scrolled_into_view

                    #    val_1 = value
                        ret_val = open_link(element,drive,area)
                #        print(ret_val)
                        if ret_val != {}:
                            data_main = data_main.append(ret_val,ignore_index = True )
                        print(data_main.shape)
                    log.write("\n have data at location : {}".format(area))
                    drive.back()
                    try:
                        data_main.to_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\Magicbricks_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))

                    except:
                        data_main.to_csv(r'E:\Hdfc\Magicbricks\res\Magicbricks_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))

                    print(data_main.shape)
            #        data_main.columns

                else:
                    print('no data at {}'.format(area))
            #            print(pincode)
                    data_main = data_main.append({'Address':None, 'Age of Construction':None, 'Area':area, 'Authority Approval':None,
                   'Balcony':None, 'Bathrooms':None, 'Bedrooms':None, 'Car parking':None, 'Carpet area':None,
                   'Facing':None, 'Floor':None, 'Flooring':None, 'Furnished status':None, 'Furnishing':None,
                   'Landmarks':None, 'Lift':None, 'Overlooking':None, 'Price':None, 'RERA ID':None, 'Status':None,
                   'Status of Electricity':None, 'Store Room':None, 'Super area':None, 'Transaction type':None,
                   'Type of Ownership':None, 'Water Availability':None, 'flat Size':None},ignore_index = True)

                    log.write("\n doesn't have data at location : {} ".format(area))
                    try:
                        data_main.to_csv(r'E:\Hdfc\Magicbricks\res\data.csv')
                    except:
                        data_main.to_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\data.csv')
                    print(data_main.shape)
                    if drive.current_url != 'https://www.magicbricks.com/':
                        drive.back()
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\area_index.text','w+',encoding='utf-8')
                f.write('0')
                f.close()
            except:
                f=open(r'E:\Hdfc\Magicbricks\res\area_index.text','w+',encoding='utf-8')
                f.write('0')
                f.close()
        log.close()
        drive.close()
        T == False
    except Exception as e:
        print(e)
        log.write(str(e))
        log.write("\n some issue in code or site ")
        log.close()
        # Daily_Mail()
        drive.close()
        time.sleep(100)


    #drive.refresh()
