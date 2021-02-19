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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import re
import glob, os
import logging

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
    outer['Subject'] = 'Problem in Magicbricks data scrapping' 
    outer['From'] = 'Magicbricks site'
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'



    # List of attachment
    try:
        os.chdir(r"D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks")
    except:
       
       os.chdir(r"E:\Hdfc\Magicbricks\res\Magicbricks")
    intresting_files = glob.glob('log_Magicbricks.text')
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

def open_link(element,drive,area):
    """
    open_link(element,drive,area):

    This function is used to scrap the data from the magicbricks site.we are passing 3 parameter into this function .
     
    Parameters:
    element(str): It is the webelement of a property.
    
    drive(str): It is instance of selenium driver
    
    area(str): It is name of Area
        
    Returns:
    dict_data: It return dictionary of all the data of the site

    """
    
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
        pass
        
    return dict_data





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
wait = WebDriverWait(drive ,20) 

#data_main = pd.DataFrame()
#Area = ['Vakola','Kalina','Versova','J B Nagar','Marol','Khar East']
try:
    data_main = pd.read_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\Magicbricks.csv')
    data_main = data_main.drop(columns = data_main.columns[:1], axis = 0 )
except:
    data_main =pd.DataFrame()
    
try:
    pincodes = pd.read_excel(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Pincode data\cleaned_to_search.xlsx')
except:
    pincodes = pd.read_excel(r'E:\Hdfc\Pincode data\cleaned_to_search.xlsx')

Branch = pincodes['BRANCH'].tolist()
pincodes = 0
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

for index1 , area in tqdm(enumerate(Branch[int(start_ind):10])):
#    area = Branch[0]
    try:
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
        if drive.current_url != 'https://www.magicbricks.com/':
            
        
        #total_prop = int(re.findall('\d{1,7}',wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="resultDiv"]/div[1]/div[2]/div[1]/div[1]/div[3]'))).get_attribute('innerText'))[0])
            print('Loading the code..........')
            for i in tqdm(range(0,200000,2000)):
                drive.execute_script('window.scrollTo({}, {});'.format(0, i))
        #        print(i)
                time.sleep(1)
            
            
            
            
            ind = 0
            html = drive.page_source
            soup = BeautifulSoup(html,'html.parser')
            val = soup.find_all("div",{"class":"m-srp-card SRCard"})
            ids = [str(x)[int(re.search('resultBlockWrappe',str(x)).start()):int(re.search('resultBlockWrappe',str(x)).start())+26] for x in val ] 
            print(len(ids))
            
                #v = re.search('resultBlockWrappe',str(val[0])).start()
            #id = str(val[0])[int(v.start()):int(v.start())+26]
           
        #    //*[@id="resultBlockWrapper45733217"]/div[4]/div[3]/div[1]/h3/span
            for index ,value in tqdm(enumerate(ids)):
            #        print(index,value = ids[1])
        #        element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="{}"]/div[4]/div[3]/div[1]/h3/span'.format(ids[index]))))
                
        #//*[@id="resultBlockWrapper45733217"]    //*[@id="resultBlockWrapper45733217"]/div[4]/div[3]/div[1]/h3/span
                try:
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="{}"]'.format(ids[index]))))
                except:
                    continue
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
            try:
                data_main.to_csv(r'E:\Hdfc\Magicbricks\res\data.csv')
            except:
                data_main.to_csv(r'D:\Hdfc_Scrapping_data\Uday\Scrapping_data\Magicbricks\data.csv')
            drive.back()
            time.sleep(2)
        else:
            print('no data')
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
            
    except:
        print('no data')
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
drive.close()           
#        drive.back()
    #            time.sleep(1) val_1 = ids[5] value = ids[2]
    #    print('index:',index,len(ids))
    #    y = y+10000
    ##        coordinates = element.location_once_scrolled_into_view # returns dict of X, Y coordinates
    #    drive.execute_script('window.scrollTo({}, {});'.format(1, y))
    #    time.sleep(5)
        
    #    html1 = drive.page_source
    #    soup = BeautifulSoup(html1,'html.parser')
    #    val = soup.find_all("div",{"class":"m-srp-card SRCard"})
    #    ids = [str(x)[int(re.search('resultBlockWrappe',str(x)).start()):int(re.search('resultBlockWrappe',str(x)).start())+26] for x in val ] 
    #    ind = ids.index(val_1)+1
    #data_main = data_main.str        
    #data_main.to_csv(r'E:\Hdfc\Magicbricks\res\data.csv')
    #drive.back()                
    #to handle the control of windows
    
#logging.basicConfig(filename="newfile.log", 
#                    format='%(asctime)s %(message)s', 
#                    filemode='w') 
#  
##Creating an object 
#logger=logging.getLogger() 
#  
##Setting the threshold of logger to DEBUG 
#logger.setLevel(logging.DEBUG) 
#  
##Test messages 
#logger.debug("Harmless debug Message") 
#logger.info("Just an information") 
#logger.warning("Its a Warning") 
#logger.error("Did you try to divide by zero") 
#logger.critical("Internet is down") 
    
    
    
    
    #drive.refresh()
