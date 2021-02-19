from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import scrapy
import time
import re
import pandas as pd
from tqdm import trange,tqdm




#PROXY = "61.246.226.112:8080" # IP:PORT or HOST:PORT
#
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % PROXY)
#driver=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe",chrome_options=chrome_options)
driver=webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
driver.get("https://www.swiggy.com/restaurants")
time.sleep(2)
driver.maximize_window()
wait=WebDriverWait(driver,10)
driver.refresh()
time.sleep(2)#click on the location of this pin code
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]'))).click()
time.sleep(2)
#click on the location element
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/header/div/div/div'))).click()
time.sleep(2)
#click on the search menu
search_element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[2]/div[2]/div/input')))
search_element.send_keys(400055)
time.sleep(2)
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="overlay-sidebar-root"]/div/div/div[2]/div/div/div[3]/div/div[1]/div/div'))).click()
time.sleep(3)
T=True
#k=1
while T == True:
   
    #web_scroller()
    driver.refresh()
    time.sleep(3)
    element=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="open_filter"]/div/div/div[1]/div/div/a')))
    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except:
        element.location_once_scrolled_into_view
    element.click()
    time.sleep(5)
    No_res=element.get_attribute('innerText')
    restaurants=int(re.findall('\d{2,4}',No_res)[0])
    try:
        data=pd.read_excel(r'E:\Hdfc\Swiggy\res\swiggy_data.xlsx')
        data = data.drop(['Unnamed: 0'],axis = 1)
    except:
        cols=['Restaurant name','rating','Area','Pincode']
        data=pd.DataFrame(columns=cols)
    time.sleep(5)
#    f=open(r'E:\Hdfc\Swiggy\res\K_val.txt','r')
#    k=f.read()
#    f.close()
    f=open(r'E:\Hdfc\Swiggy\res\J_val.txt','r')
    m=f.read()
    f.close()
    #k=1
#    data1=pd.DataFrame(columns=cols)
    f=open(r'E:\Hdfc\Swiggy\res\K_val.txt','r')
    k=f.read()
    f.close()
    try:
        for i in trange(int(m),int(restaurants)+1):
            #i=int(m)
            if i%4==0:
                k=int(i/4)+1
                j=4
#                data=data.append(data1,ignore_index=True)
#                data1=pd.DataFrame(columns=cols)
            else:
                j=i%4
            #j=1    
            resturants_name=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_restaurants"]/div[2]/div[2]/div[1]/div/div['+str(k)+']/div['+str(j)+']')))
            try:
                f=open(r'E:\Hdfc\Swiggy\res\K_val.txt','r')
                location = f.read()
                f.close()
            except:
                location=resturants_name.location
            try:
                resturants_name.location_once_scrolled_into_view
            except:
                driver.execute_script("arguments[0].scrollIntoView();", resturants_name)
            time.sleep(3)
            resturants_name.click()
            time.sleep(5)
            Rest_name=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]'))).get_attribute('innerText')
            Area=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div[1]/div[3]/div[1]/div/div[2]/div/div[3]/div[2]'))).get_attribute('innerText')
            Rating=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div[1]/div[1]/div[3]/div[1]/div/div[2]/div/div[3]/div[3]/div[1]/div[1]'))).get_attribute('innerText')
        #    Rating= Rating if Rating != '--' else '0.0'
        #    print(Rest_name,Area,Rating)
            data=data.append({'Restaurant name':Rest_name,'rating':Rating,'Area':Area,'Pincode':400055},ignore_index=True)
            driver.back()
            time.sleep(5)
        T = False
    #    f=open(r'E:\Hdfc\Swiggy\res\K_val.txt','w')
    #    f.write('1')
    #    f.close()
    except:
        driver.refresh()
        f=open(r'E:\Hdfc\Swiggy\res\K_val.txt','w')
        f.write(str(k))
        f.close()
        f=open(r'E:\Hdfc\Swiggy\res\J_val.txt','w')
        f.write(str(i))
        f.close()
        
    data.to_excel(r'E:\Hdfc\Swiggy\res\swiggy_data.xlsx')    
   




#PROXY = "61.246.226.112:8080" # IP:PORT or HOST:PORT
#
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % PROXY)
#
#chrome = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe",chrome_options=chrome_options)
#chrome.get("http://google.com") 
    
#element=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_restaurants"]/div[2]/div[2]/div[1]/div/div[8]/div[2]')))
#element.location_once_scrolled_into_view
#element.click()
#


