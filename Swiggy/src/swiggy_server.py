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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import re
import glob, os
import logging
from datetime import date,datetime
import calendar

def Daily_Mail():
    """
    Daily_Mail():

    This function is written to  send the Google alert data from aratoengbot@gmail.com to respected  recipients by mail  and at the end it will show whether the mail is send or not  .

    This function will call by job function after creating the dataset of google alert

    """

    sender = 'aratoengbot@gmail.com'
    gmail_password = 'dpa@1234'
    recipients = ['uday.gupta@decimalpointanalytics.com']
    COMMASPACE = ', '
#    recipients = ['uday.gupta@decimalpointanalytics.com']
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Problem in swiggy data scrapping'
    outer['From'] = 'swiggy site'
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'



    # List of attachment
    try:
        os.chdir(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy")
    except:
       os.chdir(r"E:\Hdfc\Swiggy\res")
    intresting_files = glob.glob('log_swiggy.text')
    # Add the attachments to the message
    for file in intresting_files:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)

        except:
#            logging.error("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise



    composed = outer.as_string()



    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            """It is going to login by the given id and password"""
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
#        logging.info("Email sent!")
    except:
#        logging.error("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


#Daily_Mail()









try:
    try:
        log=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\log_swiggy.text','a',encoding='utf-8')
    except:
       log=open(r'E:\Hdfc\Swiggy\res\log_swiggy.text','a',encoding='utf-8')


#    try:
#        driver = webdriver.Firefox(executable_path=r"D:\Hdfc_Scrapping_data\Uday\driver\geckodriver.exe")
#    except:
#        driver = webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe")
    try:
        driver = webdriver.Chrome(executable_path=r"D:\Hdfc_Scrapping_data\Uday\driver\chromedriver.exe")
    except:
        driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
    driver.get('https://www.swiggy.com/')
    time.sleep(5)
    driver.maximize_window()
    time.sleep(1)
    wait = WebDriverWait(driver,10)
    wait1 = WebDriverWait(driver,50)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]'))).click()
    time.sleep(2)
    #click on the location element

    #click on the search menu


    try:
        pincodes = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Pincode data\final_data.csv.xlsx',usecols=[3,6,7,8,9])
    except:
        pincodes = pd.read_csv(r'E:\Hdfc\Pincode data\final_data.csv',usecols=[3,6,7,8,9])
    period=datetime.strftime(datetime.strptime('{} {} {}'.format(calendar.monthrange(date.today().year  ,date.today().month)[1],date.today().month,date.today().year),'%d %m %Y'),'%d/%m/%Y')
    try:
        try:
            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\state_index.text','r')
        except:
            f=open(r'E:\Hdfc\Swiggy\res\state_index.text','r')
        state_index = f.read()
        f.close()
    except:
        state_index = 0
        try:
            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\state_index.text','w+',encoding='utf-8')
        except:
            f=open(r'E:\Hdfc\Swiggy\res\state_index.text','w+',encoding='utf-8')
        f.write('0')
        f.close()
    for state_index_i in range(int(state_index),len(pincodes.STATE.unique())):
#        print(i) state_index_i = 1
        # print(pincodes.STATE.unique()[state_index_i])
        Branch = pincodes[pincodes['STATE'] == pincodes.STATE.unique()[state_index_i] ]['BRANCH'].tolist()
#    Branch = pincodes['STATE'].unique()
#    Branch.index()
        try:
            try:
                data_main = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\swiggy_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
                data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
            except:
                data_main = pd.read_csv(r'E:\Hdfc\Swiggy\res\swiggy_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
                data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
        except:
            data_main =pd.DataFrame()
        try:
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\index.text','r')
            except:
                f=open(r'E:\Hdfc\Swiggy\res\index.text','r')
            start_ind = f.read()
            f.close()
        except:
            start_ind = 0
            try:
                f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\index.text','w+',encoding='utf-8')
            except:
                f=open(r'E:\Hdfc\Swiggy\res\index.text','w+',encoding='utf-8')
            f.write('0')
            f.close()

        for index1 , pincode in tqdm(enumerate(Branch[int(start_ind):5])):
        #    pincode = 'Vakola' index1 = 0
            try:
                driver.refresh()
                try:
                    f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\index.text','w+',encoding='utf-8')
                except:
                    f=open(r'E:\Hdfc\Swiggy\res\index.text','w+',encoding='utf-8')
                print(index1 + int(start_ind))
                f.write(str(index1 + int(start_ind)))
                f.close()

                time.sleep(1)#click on the location of this pin code
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/header/div/div/div'))).click()

                time.sleep(1)

                search_element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[2]/div[2]/div/input')))

                search_element.send_keys(pincode)


                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[3]/div/div[1]/div/div'))).click()
                time.sleep(2)




                element=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="open_filter"]/div/div/div[1]/div/div/a')))
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                except:
                    element.location_once_scrolled_into_view
                element.click()
                time.sleep(3)
                No_res=element.get_attribute('innerText')
                restaurants=int(re.findall('\d{2,4}',No_res)[0])
                cols=['Restaurant name','rating','Type_of_food','Area','Delivery_Time','Cost_For_Two','Period']
                global data
                data= pd.DataFrame(columns=cols)


                type_res = ['PROMOTED', 'EXCLUSIVE','NEWLY ADDED','DAILY MENUS']
                print(restaurants)
                last = int(int(restaurants)/4)
                for i in tqdm(range(1,last+1)):
                    for j in range(1,5):
                        # i =1 j =1
                        try:
                            resturants_name = wait1.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_restaurants"]/div[2]/div[2]/div[1]/div/div['+str(i)+']/div['+str(j)+']')))
                            time.sleep(3)

                            driver.execute_script("arguments[0].scrollIntoView();", resturants_name)

                            resturants = resturants_name.get_attribute('innerText').split('\n')
    #                        resturants = ['Shiv Sagar ( Authentic Pav Bhaji )', 'South Indian, Snacks, Beverages', '--', '•', '38 MINS', '•', '₹1 FOR TWO']
                            try:
                                if  resturants[0] in type_res:
                                    resturants.remove(resturants[0])
                                data = data.append({'Restaurant name':resturants[0],'rating': resturants[2] if resturants[2] != '--' else None  ,'Type_of_food':resturants[1],'Area':pincode,'Delivery_Time':int(re.findall('\d{2,4}',resturants[4])[0]),'Cost_For_Two':int(re.findall('\d{1,4}',resturants[6])[0]),'Period':period},ignore_index=True)
                                time.sleep(1)
                            except IndexError as error:
                                print(error)
                                print(resturants)
                                pass
                        except Exception as e:
                            print(e)
                            pass
    #                    location = resturants_name.location
    ##                    size = resturants_name.size
    #                    driver.execute_script('window.scrollTo({}, {});'.format(location['y'], location['x']+5000))
                data_main = data_main.append(data,ignore_index = True)
                print(pincode)
                log.write("\n {} have data at location : {}".format(pincodes.STATE.unique()[state_index_i],pincode))
            except :
                print('no data')
                print(pincode)
                data_main = data_main.append({'Restaurant name':None,'rating':None ,'Type_of_food':None,'Area':pincode,'Delivery_Time':None,'Cost_For_Two':None,'Period':period},ignore_index = True)

                log.write("\n {} doesn't have data at location : {} ".format(pincodes.STATE.unique()[state_index_i],pincode))

        try:
            data_main.to_csv(r'E:\Hdfc\Swiggy\res\swiggy_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
        except:
            data_main.to_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\swiggy_of_{}.csv'.format(pincodes.STATE.unique()[state_index_i]))
        try:
            f=open(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Swiggy\index.text','w+',encoding='utf-8')
        except:
            f=open(r'E:\Hdfc\Swiggy\res\index.text','w+',encoding='utf-8')
        f.write('0')
        f.close()
        data_main = pd.DataFrame()
    driver.close()
    log.close()
except Exception as e:
    print(e)
    log.write(str(e))
    log.write("\n some issue in code or site ")
    log.close()
    Daily_Mail()
    driver.close()

#last_day=calendar.monthrange(date.today().year  ,date.today().month)
#
# period=datetime.strftime(datetime.strptime('{} {} {}'.format(calendar.monthrange(date.today().year  ,date.today().month)[1],date.today().month,date.today().year),'%d %m %Y'),'%d/%m/%Y')
#
#
#
#data = pd.read_excel(r'E:\Hdfc\Pincode data\68774_Cleaned1.xlsm',sheet_name='Final')
#data.columns
#data  = data[data['BRANCH'] != data['CITY']]
#data = data.drop_duplicates(['BRANCH','PINCODE'],keep= 'last')
#data.to_csv(r'E:\Hdfc\Pincode data\final_data.csv')
