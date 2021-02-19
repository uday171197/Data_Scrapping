# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 18:38:55 2019

@author: uday.gupta
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import scrapy
import time
import re
import pandas as pd
from tqdm import trange,tqdm
import json
#def Data_fetch(wait,data,i,j,type_res):
#    try:
#        resturants_name = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_restaurants"]/div[2]/div[2]/div[1]/div/div['+str(i)+']/div['+str(j)+']')))
#        driver.execute_script("arguments[0].scrollIntoView();", resturants_name)
#        resturants = resturants_name.get_attribute('innerText').split('\n')  
#    #        print(resturants)
#        if  resturants[0] in type_res:
#            resturants.remove(resturants[0])
#        data_val = {'Restaurant name':resturants[0],'rating':resturants[2] ,'Type_of_food':resturants[1],'Pincode':pincode}
#        time.sleep(1)
#    except Exception as e:
#        print(e)
#        pass
#    return data_val
    
driver=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
driver.get("https://www.swiggy.com/restaurants")
time.sleep(1)
driver.maximize_window()
time.sleep(1)
wait=WebDriverWait(driver,5)
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]'))).click()
time.sleep(2)
#click on the location element

#click on the search menu
data_main =pd.DataFrame()
pincodes = pd.read_excel(r'E:\Hdfc\Pincode data\cleaned_to_search.xlsx')
Branch = pincodes['BRANCH'].tolist()
pincodes = 0
#pincodes = [400001,400002,400003,400004,400005,400006,400007,400008,400009,400010,400011,400012,400013,400014,400015,400016,400017,400018,400050,400051,400052,400053,400054,400055,400056,400057,400058,400059,400060,400070,400061,400062,400063]
#pincodes.columns  Branch = ['SECTOR 40, CHANDIGARH ']
for pincode in Branch:
#for pincode = 'Ferani'  in pincodes:
    try:
        print(pincode)
        driver.refresh()
        time.sleep(1)#click on the location of this pin code
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/header/div/div/div'))).click()
        
        time.sleep(2)
        
        search_element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[2]/div[2]/div/input')))
    
        search_element.send_keys(pincode)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[3]/div/div[1]/div/div'))).click()
        time.sleep(2)
        element=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="open_filter"]/div/div/div[1]/div/div/a')))
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
        except:
            element.location_once_scrolled_into_view
        element.click()
        time.sleep(5)
        No_res=element.get_attribute('innerText')
        restaurants=int(re.findall('\d{2,4}',No_res)[0])
           
        cols=['Restaurant name','rating','Type_of_food','Pincode']
        global data_1
        data=pd.DataFrame(columns=cols)
        
        type_res = ['PROMOTED', 'EXCLUSIVE','NEWLY ADDED','DAILY MENUS']
        print(restaurants)
        last = int(int(restaurants)/4)
        for i in tqdm(range(1,last+2)):
            for j in range(1,5):
                try:
                    resturants_name = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_restaurants"]/div[2]/div[2]/div[1]/div/div['+str(i)+']/div['+str(j)+']')))
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].scrollIntoView();", resturants_name)
                    resturants = resturants_name.get_attribute('innerText').split('\n')
                    
                    if  resturants[0] in type_res:
                        resturants.remove(resturants[0])
                    data = data.append({'Restaurant name':resturants[0],'rating':resturants[2] ,'Type_of_food':resturants[1],'Pincode':pincode},ignore_index=True)
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
                    print(resturants)
                    pass
        data_main = data_main.append(data,ignore_index = True)
        data_main.to_excel(r'E:\Hdfc\Swiggy\res\swiggy_1.xlsx')
    except:
        print('no data')
#            print(pincode)
        data_main = data_main.append({'Restaurant name':None,'rating':None ,'Type_of_food':None,'Area':pincode},ignore_index = True)
        data_main.to_excel(r'E:\Hdfc\Swiggy\res\swiggy_1.xlsx')        


