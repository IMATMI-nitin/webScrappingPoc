# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:37:49 2021

@author: DSikotar
"""

#####--------------------- -------------------------------importing libraries-------------------------------
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def browser():
    """
    Setting the properties for the chromedriver that providing the necessary directories
    and finally returning the driver with set conditions and opening target.com site when called upon.
    """
    downloadDir = r'/home/nitin/webDevelopment/webScrappingPythonServer/download'
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : downloadDir}
    chrome_options.add_experimental_option('prefs',prefs)
    chrome_options.add_argument("--incognito")
    #    options.add_argument('--blink-settings=imagesEnabled=false')
    chromedriver = r"/home/nitin/webDevelopment/webScrappingPythonServer/chromedriver"
    driver_1 = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
    return driver_1

def lazy_scroll(dr):
    """
    Function takes in chromedriver as an input and it return nothing but performs scrolling across
    the webpage in a way how human would slowly scroll the webpage. This is done to load the images 
    on the webpage that driver is visiting as to pull out the product thumbnail URL.
    """
    y = 100
    for _ in range(0,18):
        dr.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 500
        time.sleep(1)
        
        
def search_product(strng, group_name, number):
    
    driver = browser()
        
    #####------------------------------------------------------ url to extract data from-------------------------------------------- 
    driver.get('https://www.target.com/')
    driver.maximize_window()
    ####------------------------------searching for products using searchbox from website---------------------------------
    string = strng
    # finding the search box on the webpage and searching for face wash products
    search = driver.find_element_by_id("search")
    search.clear()
    search.send_keys(string)
    search.send_keys(Keys.ENTER)
    # clicking on empty space on webpage to get away from suggestions provided in searchbox
    # driver.find_element_by_xpath("//body").click()
    driver.refresh()
    time.sleep(3)
#     driver.save_screenshot(r"C:\Users\dsikotar\Downloads\stage -3 Collection-flag\Product-pictures\search__" + string + ".png")
    #driver.get_screenshot_as_file(r"C:\Users\dsikotar\Downloads\Thumbnail\Product-pictures\search__" + string + ".png")
        
    page = []
    page_no = []
    collections = []
    list_of_links=[] # to collect all links
    sponsored = [] # collect values in binary format whther products were sponsored or not
    options = []
    s_tags = [] # store the shop collection tags found directly from webpages
    
    lazy_scroll(driver)
        
    # pulling out total pages for products found based on search item
    #    driver.execute_script("window.scrollTo(0, 20000)") # scrolling to end of page to load entire webpage
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        try:
            try:
                time.sleep(1)
                pages = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(@class,'Col-favj32-0 SelectBox__ReactiveTextCol-sc-6gt3w9-0 iXmsJV kTYneT')]"))).text
                num = int(pages[10:])
            except TimeoutException:
                driver.execute_script("window.scrollTo(0, 20000)")
                num = 0
                pass
        except ValueError:
            driver.refresh()
            continue
        break
        
    # scapping and storing links from landing page
    #    driver.execute_script("window.scrollTo(0, 20000)") 
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    productInfoList = driver.find_elements_by_xpath("//*[contains(@class,'Col-favj32-0 iXmsJV h-padding-a-none h-display-flex')]")
    tags = driver.find_elements_by_xpath("//*[contains(@class,'DetailsButtons-sc-1d69i14-0 bmJgSU')]")
    
    # storing the details of first page where we landed
    while True:
        for l in productInfoList:
            # finding products which are sponsored, if it does not find such tags it except method will be implemented to avoid the error of No such element found
            # outcome will be binary either yes or no  
            try:
                try:
                    l.find_element_by_xpath("//*[contains(@class,'h-text-xs h-margin-t-tiny')]")
                except NoSuchElementException:
                    pass
                if 'sponsored' in l.text:
                    sponsored.append('yes')
                else:    
                    sponsored.append('no')
            except StaleElementReferenceException:
                driver.refresh()
                continue
        break
        
           
    #  products that has "shop collection" tag, finding such tags and implemented below two for loops  
    # as these products when opened does not have the same format as others, in short can be said that it opens another list of products instead of opening one product with meta-data
    
    try:
        for t in tags:
            t1 = t.text
            s_tags.append(t1)
    except StaleElementReferenceException:
        driver.refresh()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        tags = driver.find_elements_by_xpath("//*[contains(@class,'DetailsButtons-sc-1d69i14-0 bmJgSU')]")
        for t in tags:
            t1 = t.text
            s_tags.append(t1)
    
    try:
        for m in range(0,len(s_tags)):
            pp = productInfoList[m].find_element_by_tag_name('a')
            link = pp.get_property('href')
            list_of_links.append(link)
            page.append(driver.current_url)
            page_no.append(1)
            if s_tags[m] == "Shop collection":
                collections.append('yes')
            else:
                collections.append('no')
            if s_tags[m] == "Choose options":
                options.append('yes')
            else:
                options.append('no')
    except StaleElementReferenceException:
        driver.refresh()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        productInfoList = driver.find_elements_by_xpath("//*[contains(@class,'Col-favj32-0 iXmsJV h-padding-a-none h-display-flex')]")
        for m in range(0,len(s_tags)):
            pp = productInfoList[m].find_element_by_tag_name('a')
            link = pp.get_property('href')
            list_of_links.append(link)
            page.append(driver.current_url)
            page_no.append(1)
            if s_tags[m] == "Shop collection":
                collections.append('yes')
            else:
                collections.append('no')
            if s_tags[m] == "Choose options":
                options.append('yes')
            else:
                options.append('no')
        
    # scrapping and storing products links from successive webpages
    
    # In range you can see that I have provide the starting num from 2, thats because to go onto next page have to click element and that elements xpath is 
    # dynamic, putting the class name it did not help so in the last resort have to do this
    
    # products that normally are there on first landing page are 28 (usually its upto 28)
    # suppose the user asks for 30 products that he needs for each search term then there is no use for sceapping products that are listed on 3rd page
    p = 28
    for i in range(2,num+1):
        if p >= number:
            break
        else:
            s_tags = []
        #        driver.execute_script("window.scrollTo(0, 20000)") 
        #        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #        time.sleep(3)
            
            # finding the popup menu where all the pages links are stored and clicking on each page listed 
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(@class,'Button-bwu3xu-0 SelectBox__SelectButtonWithValidation-sc-6gt3w9-1 hUOeWC kCheAN')]"))).click()
            time.sleep(1)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="options"]/li['+str(i)+']/a'))).click()
            
            lazy_scroll(driver)
                
        #        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #        time.sleep(3)
            productInfoList = driver.find_elements_by_xpath("//*[contains(@class,'Col-favj32-0 iXmsJV h-padding-a-none h-display-flex')]")
            tags = driver.find_elements_by_xpath("//*[contains(@class,'DetailsButtons-sc-1d69i14-0 bmJgSU')]")
                
            # storing the details of first page where we landed
            # finding products which are sponsored, if it does not find such tags it except method will be implemented to avoid the error of No such element found
            # outcome will be binary either yes or no
            
            for l in productInfoList:  
                try:
                    l.find_element_by_xpath("//*[contains(@class,'h-text-xs h-margin-t-tiny')]")
                except NoSuchElementException:
                    pass
                if 'sponsored' in l.text:
                    sponsored.append('yes')
                else:    
                    sponsored.append('no')     
            
            # storing the text that whether product listed for search term has text such as 'shop collection', 'add to cart' or anything like that
            # this is done because, the product which are listed and having shop collection tag, when opend results into opening a product listing page.
            try:
                for t in tags:
                    t1 = t.text
                    s_tags.append(t1)
            except StaleElementReferenceException:
                driver.refresh()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                tags = driver.find_elements_by_xpath("//*[contains(@class,'DetailsButtons-sc-1d69i14-0 bmJgSU')]")
                for t in tags:
                    t1 = t.text
                    s_tags.append(t1)
                
            # comparing tags to see if there is a product with shop collection buttion and if there is then appending the value of yes in collection list
            # and finding the product link from productInfoList and appending them in separate list, which later will be used for scrapping meta-data
            # lastly, appending the page no on which the product was mentioned and that particular page-url as well
            
            try:
                for m in range(0,len(s_tags)):
                    pp = productInfoList[m].find_element_by_tag_name('a')
                    link = pp.get_property('href')
                    list_of_links.append(link)
                    page.append(driver.current_url)
                    page_no.append(1)
                    if s_tags[m] == "Shop collection":
                        collections.append('yes')
                    else:
                        collections.append('no')
                    if s_tags[m] == "Choose options":
                        options.append('yes')
                    else:
                        options.append('no')
            except StaleElementReferenceException:
                driver.refresh()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                productInfoList = driver.find_elements_by_xpath("//*[contains(@class,'Col-favj32-0 iXmsJV h-padding-a-none h-display-flex')]")
                for m in range(0,len(s_tags)):
                    pp = productInfoList[m].find_element_by_tag_name('a')
                    link = pp.get_property('href')
                    list_of_links.append(link)
                    page.append(driver.current_url)
                    page_no.append(1)
                    if s_tags[m] == "Shop collection":
                        collections.append('yes')
                    else:
                        collections.append('no')
                    if s_tags[m] == "Choose options":
                        options.append('yes')
                    else:
                        options.append('no')
            p += 28
            
    
    ######-------------------------scrapping and storing the meta-data---------------------------------------------
    # below for loop, has a driver method of get that will open the browser and open every link that exists in list_of_links list
        # if-elif-else loop scrapes the meta data based on number of products that user has asked to scrape, if the products are less tha
        # number provide, it shall scrape those available products, elif there are more products than the user has asked for it, shall only scrape 
        # products till the number that user provided, and come out of the loop
            # with if-elif-else there is a main try-except condition
            # it basically looks for products meta-data
                # if the product belongs to shop collection tag, then it shall have info related to product name, and it opens a new list of products (like a nested product listing page)
                # if above is found then with nosuchelementexception error, it will try the next block of codes that properly scrapes the meta-data
                # sometimes this opened product meta-data page slightly varies and there is another nosuchelementexception error triggered, so to avoid there is another block of codes that
                # will be executed to scrape the data and to avoid that error
    
    all_details = []
    count = 0
    
        
    for i in tqdm(list_of_links):
        if len(list_of_links) < int(number): # if length of links is less than given number (for the products that needs to be scrapped) then still it should scrap the products that are found
            try:
                driver.get(i)
                # if the product listed is of "shop collection" class
                product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div/h1').text
                brand = product.split()[0]
                price = None
                highlights = None
                description = None
                specs = None
                drug = None
                label = None
                shipping = None
                ratings = None
            except NoSuchElementException:
                try:
                    time.sleep(3)
                    product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[1]/div[2]/h1/span').text                                # product name
                    brand = driver.find_element_by_xpath("//*[contains(@class,'Link__StyledLink-sc-4b9qcv-0 fUrQXY')]").text                            # product's brand
                    try:
                        price = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div').text              # price of product
                    except NoSuchElementException:
                        price = "Null"
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/button').click()                                                 # clicks on show more info button 
                    try:
                        highlights = driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div/div/ul').text             # captures highligths
                    except NoSuchElementException:
                        highlights = "Null"
                    description = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-l-default')]").text                                    # description of product
                    specs = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-h-tight')]").text               # specifications 
                    try:                                                                                          
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                       # clicks on drugs tab
                        drug = driver.find_element_by_xpath('//*[@id="tabContent-tab-Drugfacts"]').text                                                       # drugs information
                    except NoSuchElementException:
                        drug = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-Labelinfo"]').click()                                                                     # clicks on label tab
                        label = driver.find_element_by_xpath('//*[@id="tabContent-tab-Labelinfo"]/div/div/div[1]/div').text                                  # label information
                    except NoSuchElementException:
                        label = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-ShippingReturns"]').click()                                                               # clicks on shipping and returns tab
                        shipping = driver.find_element_by_xpath('//*[@id="tabContent-tab-ShippingReturns"]/div').text                                      # shipping information
                    except NoSuchElementException:
                        shipping = "Null"                                                                                     # scrolling to end of page to load more info
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                    except NoSuchElementException:
                        ratings = "Null"
                except NoSuchElementException:
                    product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[2]/div/h1/span').text
                    brand = driver.find_element_by_xpath("//*[contains(@class,'Link__StyledLink-sc-4b9qcv-0 fUrQXY')]").text                            # product's brand
                    try:
                        price = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[4]/div[1]/div[1]/div/div[1]/div').text              # price of product
                    except NoSuchElementException:
                        price = "Null"
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/button').click()                                                 # clicks on show more info button 
                    try:
                        highlights = driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div/div/ul').text             # captures highligths
                    except NoSuchElementException:
                        highlights = "Null"
                    description = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-l-default')]").text                                    # description of product
                    specs = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-h-tight')]").text               # specifications 
                    try:                                                                                          
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                       # clicks on drugs tab
                        drug = driver.find_element_by_xpath('//*[@id="tabContent-tab-Drugfacts"]/div/div').text                                                       # drugs information
                    except NoSuchElementException:
                        drug = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                     # clicks on label tab
                        label = driver.find_element_by_xpath('//*[@id="tabContent-tab-Labelinfo"]/div/div/div[1]/div').text                                  # label information
                    except NoSuchElementException:
                        label = "Null"   
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-ShippingReturns"]').click()                                                               # clicks on shipping and returns tab
                        shipping = driver.find_element_by_xpath('//*[@id="tabContent-tab-ShippingReturns"]/div/div').text                                      # shipping information
                    except NoSuchElementException:
                        shipping = "Null"                                                                                   # scrolling to end of page to load more info
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                    except NoSuchElementException:
                        ratings = "Null"
        elif count == int(number):                                                                           # if it reaches the given number of products that are scrapped than it breaks out of the loop
                break
        else:
            try:
                driver.get(i)
                product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div/h1').text
                brand = product.split()[0]
                price = None
                highlights = None
                description = None
                specs = None
                drug = None
                label = None
                shipping = None
                ratings = None
                count += 1
            except NoSuchElementException:
                try:
                    time.sleep(3)
                    product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[1]/div[2]/h1/span').text                                # product name
                    brand = driver.find_element_by_xpath("//*[contains(@class,'Link__StyledLink-sc-4b9qcv-0 fUrQXY')]").text                            # product's brand
                    try:
                        price = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div').text              # price of product
                    except NoSuchElementException:
                        price = "Null"
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/button').click()                                                 # clicks on show more info button 
                    try:
                        highlights = driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div/div/ul').text             # captures highligths
                    except NoSuchElementException:
                        highlights = "Null"
                    description = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-l-default')]").text                                    # description of product
                    specs = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-h-tight')]").text               # specifications 
                    try:                                                                                          
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                       # clicks on drugs tab
                        drug = driver.find_element_by_xpath('//*[@id="tabContent-tab-Drugfacts"]').text                                                       # drugs information
                    except NoSuchElementException:
                        drug = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-Labelinfo"]').click()                                                                     # clicks on label tab
                        label = driver.find_element_by_xpath('//*[@id="tabContent-tab-Labelinfo"]/div/div/div[1]/div').text                                  # label information
                    except NoSuchElementException:
                        label = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-ShippingReturns"]').click()                                                               # clicks on shipping and returns tab
                        shipping = driver.find_element_by_xpath('//*[@id="tabContent-tab-ShippingReturns"]/div').text                                      # shipping information
                    except NoSuchElementException:
                        shipping = "Null"                                                                                    # scrolling to end of page to load more info
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                    except NoSuchElementException:
                        ratings = "Null"
                    count += 1
                except NoSuchElementException:
                    product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[2]/div/h1/span').text
                    brand = driver.find_element_by_xpath("//*[contains(@class,'Link__StyledLink-sc-4b9qcv-0 fUrQXY')]").text                            # product's brand
                    try:
                        price = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[2]/div[4]/div[1]/div[1]/div/div[1]/div').text              # price of product
                    except NoSuchElementException:
                        price = "Null"
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/button').click()                                                 # clicks on show more info button 
                    try:
                        highlights = driver.find_element_by_xpath('//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div/div/ul').text             # captures highligths
                    except NoSuchElementException:
                        highlights = "Null"
                    description = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-l-default')]").text                                    # description of product
                    specs = driver.find_element_by_xpath("//*[contains(@class,'styles__StyledCol-ct8kx6-0 kxIdUL h-padding-h-tight')]").text               # specifications 
                    try:                                                                                          
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                       # clicks on drugs tab
                        drug = driver.find_element_by_xpath('//*[@id="tabContent-tab-Drugfacts"]/div/div').text                                                       # drugs information
                    except NoSuchElementException:
                        drug = "Null"
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()                                                                     # clicks on label tab
                        label = driver.find_element_by_xpath('//*[@id="tabContent-tab-Labelinfo"]/div/div/div[1]/div').text                                  # label information
                    except NoSuchElementException:
                        label = "Null"   
                    try:
                        driver.find_element_by_xpath('//*[@id="tab-ShippingReturns"]').click()                                                               # clicks on shipping and returns tab
                        shipping = driver.find_element_by_xpath('//*[@id="tabContent-tab-ShippingReturns"]/div/div').text                                      # shipping information
                    except NoSuchElementException:
                        shipping = "Null"                                                                                     # scrolling to end of page to load more info
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                    except NoSuchElementException:
                        ratings = "Null"   
                    count += 1
        data = {
               'Group Name': group_name,
               'Search Term': string,
               'Product': product,
               'Brand': brand,
               'Price': price,
               'Highlights': highlights,
               'Description': description,
               'Specifications': specs,
               'Drug-facts': drug,
               'Label-info': label,
               'Shipping & Returns': shipping,
               'Ratings': ratings,
               'Product Link': i
               }
        all_details.append(data)
                    
    scrapped_data = pd.DataFrame(all_details)
    scrapped_data['Sponsored']= None                                                         # initializing Sponsored column 
    scrapped_data['Product Order Listing']= None                                             # initializing Product_order_listing column 
    scrapped_data['Page Link'] = None
    scrapped_data['Page No'] = None
    scrapped_data['Collection'] = None
    scrapped_data['Multiple Options'] = None
        
    for i in range(0,len(scrapped_data)):
        scrapped_data['Sponsored'][i] = sponsored[i]                                         # setting sponsored values from above that were scrapped
        scrapped_data['Product Order Listing'][i] = i+1                                      # setting product orders, using i+1 so that values start from 1 instead of 0
        scrapped_data['Page Link'][i] = page[i]                                              # setting page link values
        scrapped_data['Page No'][i] = page_no[i]                                             # setting the page no
        scrapped_data['Collection'][i] = collections[i]
        scrapped_data['Multiple Options'][i] = options[i]
        
    driver.quit()

    return scrapped_data

def regex(dataframe):
    df = dataframe
     #----------------cleaning the data------------------------------
    # using regex to pull out below information from specifications column 
    df['TCIN'] = df['Specifications'].str.extract(r'(TCIN:[ 0-9]+)')                                    # TCIN 
    df['TCIN'] = df['TCIN'].str.extract(r'([ 0-9]+)')                                                   # only the numbers
    df['UPC'] = df['Specifications'].str.extract(r'(UPC:[ 0-9]+)')                                      # UPC
    df['UPC'] = df['UPC'].str.extract(r'([ 0-9]+)')                                                     # only the numbers
    df['DPCI'] = df['Specifications'].str.extract(r'(Item Number [A-Za-z.\-\)\(]+:[ 0-9]+-[0-9]+-[0-9]+)')
    df['DPCI'] = df['DPCI'].str.extract(r'([ 0-9]+-[0-9]+-[0-9]+)')
    df['Extracted Date'] = datetime.today().strftime('%Y-%m-%d')
      
    df.to_excel('temp.xlsx', index=False)
    
    df_new = pd.read_excel('temp.xlsx') # temporarily saving file 
    
    regex_list = ['Features', 'Material', 'Package Quantity', 'Product Form', 'Suggested Age', 'Primary Active Ingredient', 
                  'Health Facts', 'Product Warning','Sustainability Claims', 'Origin']
    
    for i in regex_list:
        df_new[i] = df_new['Specifications'].str.extract(r'('+i+':[ \w,-]+)')
        df_new[i] = df_new[i].str.replace(i+': ', '')
    
    df_new['Capacity (Volume)'] = df_new['Specifications'].str.extract(r'(Capacity [A-Za-z.\-\)\(]+:[ \w.]+)')               
    df_new['Capacity (Volume)'] = df_new['Capacity (Volume)'].str[19:].str.strip()
    
    df_new['Brand'] = df_new['Brand'].str.replace('Shop all', '')
    df_new['Highlights'] = df_new['Highlights'].str.replace('\n', ', ')
    df_new['Specifications'] = df_new['Specifications'].str.replace('\n', ', ') #[16:]
    df_new['Description'] = df_new['Description'].str.replace('\n', ', ')
    df_new['Specifications'] = df_new['Specifications'].str.replace('Specifications,', '')
    df_new['Description'] = df_new['Description'].str.replace('Description,', '')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('\n', ', ').str.replace('Shipping details,', '')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('Shipping options,', '')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('Return details,', 'Return details:')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.strip()
    df_new['Highlights'] = df_new['Highlights'].str.strip()
    df_new['Specifications'] = df_new['Specifications'].str.strip()
    df_new['Description'] = df_new['Description'].str.strip()
    
    df_new['Brand'] = df_new['Brand'].str.strip()
    df_new['Drug-facts'] = df_new['Drug-facts'].str.replace('\n', ', ')
    df_new['Label-info'] = df_new['Label-info'].str.replace('\n', ', ')
    
    # adding the duplicate column for the products that have the same Product link in the form of boolean values
    df_new['Duplicates'] = df_new.duplicated(['Product Link']) 
    
    # rearranging the column names
    column_names = ['Extracted Date', 'Group Name', 'Search Term', 'Product Order Listing',  'Product', 'Brand', 
                    'Sponsored', 'Price', 'Ratings', 'TCIN', 'UPC', 'DPCI', 'Collection', 'Multiple Options', 'Duplicates', 'Page No', 'Product Link','Page Link', 'Thumbnail Link',
                    'Features', 'Material', 'Package Quantity', 'Product Form', 'Suggested Age', 'Primary Active Ingredient', 'Health Facts', 
                    'Product Warning','Sustainability Claims', 'Origin', 'Capacity (Volume)',
                    'Highlights', 'Description', 'Specifications', 'Drug-facts', 'Label-info', 'Shipping & Returns']
    df_new = df_new.reindex(columns = column_names)
    
    # filling all the null values with string value represented as null
    df_new.fillna("Null", inplace=True)
    
    return df_new

# function that opens the search term file and calls search_product function to scrape all the products as asked by user 
# the called function returns a dataframe which is uncleaned, thereby cleaning this data and returning the cleansed dataframe

def all_search(no):
    df = pd.DataFrame()
    
    
    search = pd.read_excel(r'/home/nitin/webDevelopment/webScrappingPythonServer/static/files/search.xlsx')           # opening the file 
    
    for name, group in zip(search.Search_terms, search.Group_name):  
        data = search_product(name, group, no) # calling the function to scrape products meta data for each search term  
        df = df.append(data) # output obtained from the called function 
        
    cleaned_data = regex(df)
    cleaned_data.to_csv(r'/home/nitin/webDevelopment/webScrappingPythonServer/download/output.csv')
    
    return cleaned_data

#start_time = datetime.now()
#detes = all_search()
#end_time = datetime.now()
#print('Duration: {}'.format(end_time-start_time))
