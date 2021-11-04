from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import re
from bs4 import BeautifulSoup
import requests
import time

site = input("please input domain:")
site_h = site.split(".")[0]
# bing
driver = webdriver.Edge()
webpage_list = []
driver.get("https://cn.bing.com/") 
driver.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys("site:"+site)  
driver.find_element_by_xpath('//*[@id="search_icon"]').click()
for _ in range(30):  #page number 30
    webpage_list_curr = WebDriverWait(driver, 20, 0.5).until(lambda driver:driver.find_elements_by_xpath('//*[@class="sh_favicon"]')) #wait
    for webpage in webpage_list_curr:
        tmp1 = webpage.get_attribute('href')
        tmp2 = re.search("\/\/.*"+site_h+".*?\/",tmp1)[0][2:-1] #regex
        webpage_list.append(tmp2)
    try:
        driver.find_elements_by_xpath('//*[@id="bnp_hfly_cta2"]')[-1].click() 
    except:
        pass
    driver.find_elements_by_xpath('//*[@class="sb_pagN sb_pagN_bp b_widePag sb_bp "]')[-1].click() #click next button
# baidu
driver.get("https://www.baidu.com/") 
driver.find_element_by_xpath('//*[@id="kw"]').send_keys("site:"+site)  
driver.find_element_by_xpath('//*[@id="su"]').click()
for _ in range(10):  #page number 10
    webpage_list_curr = WebDriverWait(driver, 20, 0.5).until(lambda driver:driver.find_elements_by_xpath('//*[@class="result c-container new-pmd"]/h3/a'))
    for webpage in webpage_list_curr:
        tmp1 = requests.get(str(webpage.get_attribute('href'))).url #get url
        #print(tmp1)
        tmp2 = re.search("\/\/.*"+site_h+".*?\/",tmp1)[0][2:-1] #regex
        webpage_list.append(tmp2)
    address = driver.find_elements_by_xpath('//*[@class="n"]')[-1].get_attribute('href') #get next page
    driver.get(address) # get
    #print(address)


#crt.sh
req = requests.get("https://crt.sh/?q="+site)
text_list = BeautifulSoup(req.text).text.split("\n")
for s in text_list:
    if s != '':
        if s[0] != '*' and s[0:6] != "crt.sh" and s[0:4] != "Type":
            if re.match('.*'+site+'$',s):
                webpage_list.append(s)

# site.ip138
driver.get("https://site.ip138.com/"+site+"/domain.htm") 
tmp3 = driver.find_elements_by_xpath('//*[@class="panel"]')[0].text.split("\n")[2:-1]
webpage_list.extend(tmp3)

# chaziyu.com
driver.get("https://chaziyu.com/"+site) 
js="var q=document.documentElement.scrollTop=100000"  
driver.execute_script(js)  
time.sleep(3) 

tmp4 = driver.find_elements_by_xpath('//*[@class="result"]')[0].text.split("\n")
for s in tmp4:
    if re.match('.*'+site+'$',s):
        webpage_list.append(s.split(" ")[-1])


driver.close()
domain = list(set(webpage_list)) # delete duplicate
#print(domain)
f = open('domain.txt','w') #write domain.txt
for s in domain:
    f.write(s+'\n')
f.close()