#!/usr/bin/env python
# coding: utf-8

# In[24]:


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


# In[32]:


def search_product(strng, group_name, number):
    #########---------------------------setting parameters and conditions for driver------------------------------
    downloadDir = r'C:\Users\dsikotar\Downloads\chromecompleted'
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : downloadDir}
    chrome_options.add_experimental_option('prefs',prefs)
    chrome_options.add_argument("--incognito")
#     options.add_argument('--blink-settings=imagesEnabled=false')

    chromedriver = r"C:\Users\dsikotar\Downloads\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
        
    #####------------------------------------------------------ url to extract data from-------------------------------------------- 
    driver.get('https://www.target.com/')
    driver.maximize_window()
    ####------------------------------searching for products using searchbox from website---------------------------------
    string = strng
    print("SEARCHING FOR: "+string)
    # finding the search box on the webpage and searching for face wash products
    search = driver.find_element_by_id("search")
    search.clear()
    search.send_keys(string)
    search.send_keys(Keys.ENTER)
    print("Loading webpage...")
    # clicking on empty space on webpage to get away from suggestions provided in searchbox
    # driver.find_element_by_xpath("//body").click()
    driver.refresh()
    time.sleep(3)
    driver.save_screenshot(r"C:\Users\dsikotar\Downloads\Web_Scrapping\Search-terms\search__" + strng + ".png")
#     driver.get_screenshot_as_file(r"C:\Users\dsikotar\Downloads\Web_Scrapping\Search-terms\" + strng + ".png")
    
    page = []
    page_no = []
#     thumbnails = []
    list_of_links=[] # to collect all links
    sponsored = [] # collect values in binary format whther products were sponsored or not
    s_tags = [] # store the shop collection tags found directly from webpages
    
    # pulling out total pages for products found based on search item
    driver.execute_script("window.scrollTo(0, 10000)") # scrolling to end of page to load entire webpage
    while True:
        try:
            try:
                time.sleep(1)
                pages = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(@class,'Col-favj32-0 SelectBox__ReactiveTextCol-sc-6gt3w9-0 iXmsJV kTYneT')]"))).text
                num = int(pages[10:])
                print('Landed on first webpage of search term.')
                print('No. of pages: '+str(num))
            except TimeoutException:
                driver.refresh()
                print('Single page for this search term.')
                num = 0
                pass
        except ValueError:
            driver.refresh()
            continue
        break
    
    time.sleep(2)
    # scapping and storing links from landing page
#     driver.execute_script("window.scrollTo(0, 10000)") 
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
    
           
    # to avoid the products that has "shop collection" tag, finding such tags and implemented below two for loops to bypass this products 
    # as these products when opened does not have the same format as others, in short can be said that it opens another list of products instead of opening one product with meta-data

    for t in tags:
        t1 = t.text
        s_tags.append(t1)
    for m in range(0,len(s_tags)):
        if s_tags[m] != "Shop collection":
            pp = productInfoList[m].find_element_by_tag_name('a')
            link = pp.get_property('href')
            list_of_links.append(link)
            page.append(driver.current_url)
            page_no.append(1)
#             time.sleep(1)
#             tb = productInfoList[m].find_element_by_tag_name('picture')
#             thumb = tb.find_element_by_tag_name('img')
#             tl = thumb.get_property('src')
#             thumbnails.append(tl)
    
    # scrapping and storing products links from successive webpages
    
    # In range you can see that I have provide the starting num from 2, thats because to go onto next page have to click element and that elements xpath is 
    # dynamic, putting the class name it did not help so in the last resort have to do this
    
    for i in range(2,num+1):
        s_tags = []
        driver.execute_script("window.scrollTo(0, 10000)") 
        time.sleep(3)
        
        # finding the popup menu where all the pages links are stored and clicking on each page listed 
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(@class,'Button-bwu3xu-0 SelectBox__SelectButtonWithValidation-sc-6gt3w9-1 hUOeWC kCheAN')]"))).click()
        time.sleep(1)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="options"]/li['+str(i)+']/a'))).click()
    
        print('Visiting page '+str(i))
        
        driver.execute_script("window.scrollTo(0, 10000)")
        time.sleep(2)
        productInfoList = driver.find_elements_by_xpath("//*[contains(@class,'Col-favj32-0 iXmsJV h-padding-a-none h-display-flex')]")
        tags = driver.find_elements_by_xpath("//*[contains(@class,'DetailsButtons-sc-1d69i14-0 bmJgSU')]")
        
        # storing the details of first page where we landed
        for l in productInfoList:
                # finding products which are sponsored, if it does not find such tags it except method will be implemented to avoid the error of No such element found
                # outcome will be binary either yes or no  
            try:
                l.find_element_by_xpath("//*[contains(@class,'h-text-xs h-margin-t-tiny')]")
            except NoSuchElementException:
                pass
            if 'sponsored' in l.text:
                sponsored.append('yes')
            else:    
                sponsored.append('no')
    

        for t in tags:
            t1 = t.text
            s_tags.append(t1)
       
        for m in range(0,len(s_tags)):
            # comparing tags to see if there is a product with shop collection buttion andif there is avoid that product and move on to next
            if s_tags[m] != "Shop collection":
                pp = productInfoList[m].find_element_by_tag_name('a')
                link = pp.get_property('href')
                list_of_links.append(link)
                page.append(driver.current_url)
                page_no.append(i)
#                 time.sleep(1)
#                 tb = productInfoList[m].find_element_by_tag_name('picture')
#                 thumb = tb.find_element_by_tag_name('img')
#                 tl = thumb.get_property('src')
#                 thumbnails.append(tl)
        
    print('Scrapped all links of products that are listed.')
    print('Total links scrapped: '+str(len(list_of_links)))
    
    ######-------------------------storing the meta-data-------------------
    # while loop tries to scrap all details that are asked and if there is error in finding elements, it will refresh the webpage and try again unitl all details of 
    # every product links are visited and scrapped.
    all_details = []
    # condition = True
    # while condition:
    count = 0
    for i in tqdm(list_of_links):
        if len(list_of_links) < int(number): # if length of links is less than given number (for the products that needs to be scrapped) then still it should scrap the products that are found
            try:
            #    print(i)
                driver.get(i)
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
                    shipping = "Null"
                driver.execute_script("window.scrollTo(0, 10000)")                                                                                     # scrolling to end of page to load more info
                try:
                    ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                except NoSuchElementException:
                    ratings = "Null"
#             try:    
#                 comment_elements = driver.find_elements_by_xpath("//*[contains(@class,'h-margin-t-default')]")
#                 comments = [comment.text for comment in comment_elements]                                                                                 # extracting comments that are displayed
#             except NoSuchElementException:
#                 comments = None
            # storing all scrapped data in a dictionary
                data = {
                    'Group Name': group_name,
                    'Search_term': string,
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
#                 'Comments':comments,
                    'Link': i
                }
                all_details.append(data) 
            except NoSuchElementException:
                driver.refresh()
                time.sleep(3)
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
                    shipping = "Null"
                driver.execute_script("window.scrollTo(0, 10000)")                                                                                     # scrolling to end of page to load more info
                try:
                    ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                except NoSuchElementException:
                    ratings = "Null"
    #             try:    
    #                 comment_elements = driver.find_elements_by_xpath("//*[contains(@class,'h-margin-t-default')]")
    #                 comments = [comment.text for comment in comment_elements]                                                                                 # extracting comments that are displayed
    #             except NoSuchElementException:
    #                 comments = None
                # storing all scrapped data in a dictionary
                data = {
                    'Group Name': group_name,
                    'Search_term': string,
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
    #                 'Comments':comments,
                    'Link': i
                }
                all_details.append(data)
                             
        elif count == int(number):                                                                           # if it reaches the given number of products that are scrapped than it breaks out of the loop
            break
        else: 
            try:
            #    print(i)
                driver.get(i)                                # product name
                time.sleep(3)
                product = driver.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[1]/div[2]/h1/span').text
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
                    shipping = "Null"
                driver.execute_script("window.scrollTo(0, 10000)")                                                                                     # scrolling to end of page to load more info
                try:
                    ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                except NoSuchElementException:
                    ratings = "Null"
#             try:    
#                 comment_elements = driver.find_elements_by_xpath("//*[contains(@class,'h-margin-t-default')]")
#                 comments = [comment.text for comment in comment_elements]                                                                                 # extracting comments that are displayed
#             except NoSuchElementException:
#                 comments = None
            # storing all scrapped data in a dictionary
                data = {
                    'Group Name': group_name,
                    'Search_term': string,
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
#                 'Comments':comments,
                    'Link': i
                }
                all_details.append(data)
                count += 1
            except NoSuchElementException:
                driver.refresh()
                time.sleep(3)
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
                    shipping = "Null"
                driver.execute_script("window.scrollTo(0, 10000)")                                                                                     # scrolling to end of page to load more info
                try:
                    ratings = driver.find_element_by_xpath("//*[contains(@class,'RatingSummary__StyledRating-bxhycp-0 kXLtsm h-text-bold')]").text          # ratings 
                except NoSuchElementException:
                    ratings = "Null"
    #             try:    
    #                 comment_elements = driver.find_elements_by_xpath("//*[contains(@class,'h-margin-t-default')]")
    #                 comments = [comment.text for comment in comment_elements]                                                                                 # extracting comments that are displayed
    #             except NoSuchElementException:
    #                 comments = None
                # storing all scrapped data in a dictionary
                data = {
                    'Group Name': group_name,
                    'Search_term': string,
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
    #                 'Comments':comments,
                    'Link': i
                }
                all_details.append(data)
                count += 1
            
        
    #     condition = False
    
    scrapped_data = pd.DataFrame(all_details)
    scrapped_data['Sponsored']= None                                                         # initializing Sponsored column 
    scrapped_data['Product_order_listing']= None                                             # initializing Product_order_listing column 
    scrapped_data['Page_link'] = None
    scrapped_data['Page_no'] = None
#     scrapped_data['Thumbnail'] = None
    
    for i in range(0,len(scrapped_data)):
        scrapped_data['Sponsored'][i] = sponsored[i]                                         # setting sponsored values from above that were scrapped
        scrapped_data['Product_order_listing'][i] = i+1                                      # setting product orders, using i+1 so that values start from 1 instead of 0
        scrapped_data['Page_link'][i] = page[i]
        scrapped_data['Page_no'][i] = page_no[i]
#         scrapped_data['Thumbnail'][i] = thumbnails[i]
    
    driver.quit()
    
    return scrapped_data


# In[33]:


def all_search():
    df = pd.DataFrame()
    no = int(input('Enter number of products that needs to be scrapped: '))
    
    search = pd.read_csv('search-terms.csv')           # using the file
    
    for name, group in zip(search.Search_terms, search.Group_name):
        data = search_product(name, group, no)
        df = df.append(data)

#     search1 = pd.read_csv('search_terms1.csv')           # using the file
    
#     for name, group in zip(search1.Search_terms, search1.Group_name):
#         data = search_product(name, group, no)
#         df = df.append(data)

    
    # using regex to pull out below information from specifications column 
    df['TCIN'] = df['Specifications'].str.extract(r'(TCIN:[ 0-9]+)')                                    # TCIN 
    df['TCIN'] = df['TCIN'].str.extract(r'([ 0-9]+)')                                                   # only the numbers
    df['UPC'] = df['Specifications'].str.extract(r'(UPC:[ 0-9]+)')                                      # UPC
    df['UPC'] = df['UPC'].str.extract(r'([ 0-9]+)')                                                     # only the numbers
#     df['DPCI'] = df['Specifications'].str.findall('Item Number [A-Za-z.\-\)\(]+:[ 0-9]+-[0-9]+-[0-9]+') # DPIC
#     for i in range(0,len(df)):                                                                          # only the numbers
#         df['DPCI'][i] = df['DPCI'][i][-1][-11:]
    df['DPCI'] = df['Specifications'].str.extract(r'(Item Number [A-Za-z.\-\)\(]+:[ 0-9]+-[0-9]+-[0-9]+)')
    df['DPCI'] = df['DPCI'].str.extract(r'([ 0-9]+-[0-9]+-[0-9]+)')
    df['Extracted_Date'] = datetime.today().strftime('%Y-%m-%d')
    
    column_names = ['Extracted_Date', 'Group Name', 'Search_term', 'Product_order_listing',  'Product', 'Link', 'Sponsored', 
                    'Brand', 'Price', 'Ratings', 'TCIN', 'UPC', 'DPCI', 'Page_no', 'Page_link', #'Thumbnail', 
                    'Highlights', 'Description', 'Specifications', 'Drug-facts', 'Label-info', 'Shipping & Returns']
    
    df = df.reindex(columns = column_names)
    
    df.to_excel('temp.xlsx', index=False)
    
    df_new = pd.read_excel('temp.xlsx')
    
    df_new['Specifications'] = df_new['Specifications'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    df_new['Description'] = df_new['Description'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    df_new['Highlights'] = df_new['Highlights'].str.replace('\n', ', ')
    df_new['Specifications'] = df_new['Specifications'].str.replace('\n', ', ')
    df_new['Description'] = df_new['Description'].str.replace('\n', ', ')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('\n', ', ').str.replace('Shipping details,', '')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('Shipping options,', '')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.replace('Return details,', 'Return details:')
    df_new['Shipping & Returns'] = df_new['Shipping & Returns'].str.strip()
    
    for i in range(len(df_new)):
        if len(df_new['Brand'][i]) > 4:
            df_new['Brand'][i] = df_new['Brand'][i][9:]
        else:
            df_new['Brand'][i] = df_new['Brand'][i]
            
    
    df_new['Drug-facts'] = df_new['Drug-facts'].str.replace('\n', ', ')
    df_new['Label-info'] = df_new['Label-info'].str.replace('\n', ', ')
    
#     regex_list = ['Features', 'Package Quantity', 'Product Form', 'Suggested Age', 'Primary Active Ingredient','Health Facts', 'Product Warning','Sustainability Claims', 'Origin', ]
    
#     for i in regex_list:
#         df_new[i] = df_new['Specifications'].str.extract(r'('+i+':[ \w]+)')
#         df_new[i] = df_new[i].str.replace(i+': ', '')
    
#     df_new['Capacity (Volume)'] = df_new['Specifications'].str.extract(r'(Capacity [A-Za-z.\-\)\(]+:[ \w.]+)')               # [A-Za-z.\-\)\(]+:[ 0-9]+-[0-9]+-[0-9]+
#     df_new['Capacity (Volume)'] = df_new['Capacity (Volume)'].str[19:].str.strip()
    
    df_new.fillna("Null", inplace=True)
    
    return df_new


# In[34]:


start_time = datetime.now()
detes = all_search()
end_time = datetime.now()
print('-------------------------------------------------------------------------------------------------')
print('Duration: {}'.format(end_time-start_time))


# In[37]:


pd.options.display.max_rows = None
pd.options.display.max_columns = None
detes.head()


# In[ ]:


detes.to_excel('output.xlsx', index=False)
