import selenium
from selenium import webdriver
from tqdm import tqdm
import time
import pandas as pd

url = 'https://cm.theisn.org/cmPortal/searchable/WCN2021/config/normal#!sessionlist'

# give path of your webdriver below:
# for example webdriver.{Your browser_name 'capitalized'}(executable_path = r"{drivers path\driver_name.exe}")

driver = webdriver.Chrome(executable_path= r'C:\Users\amnj1\.wdm\drivers\chromedriver\win32\88.0.4324.96\chromedriver.exe')
driver.get(url)
driver.implicitly_wait(10) #pass time attribute according to your network speed
driver.maximize_window()
time.sleep(5)

# print(driver.title)
# session_info_list = driver.find_elements_by_class_name('cmspg-session-listitem-context')
# print(len(session_info_list))
# session_info = session_info_list[0]
# print(session_info.text)
# session = session_info.find_element_by_tag_name('a')
# print(session.text)
# print(session.get_property('href'))
# next_page = driver.find_element_by_xpath('//*[@id="cmspg-session-list-pager"]/a[3]').click

print("Collecting all links...")
list_of_links = []
condition = True
while condition:
    time.sleep(1)
    session_info_list = driver.find_elements_by_class_name('cmspg-session-listitem-context')
    for element in session_info_list:
        session = element.find_element_by_tag_name('a')
        list_of_links.append(session.get_property('href'))
    try :
        driver.find_element_by_xpath('//*[@id="cmspg-session-list-pager"]/a[3]').click()
    except:
        condition = False
print(f"There are {len(list_of_links)} links to process")

print("Please wait while scraping data")

            # paths of all elements
all_details = []
for link in tqdm(list_of_links):
    driver.get(link)
    try:
        source_code = driver.find_element_by_css_selector('#cmspg-sessiondetails > div.media > div.media-body > div:nth-child(1) > span:nth-child(2)').text
    except:
        source_code = ''
    time.sleep(1)
    try:
        article_title = '[virtual],'+ driver.find_element_by_css_selector('#cmspg-sessiondetails > div.media > div.media-body > div:nth-child(2) > span:nth-child(2)').text
    except:
        article_title = ''
    time.sleep(1)
    # url = driver.find_element_by_css_selector().text
    try:
        author_1 = driver.find_element_by_css_selector('#cmspg-session-details-presentation-list > div:nth-child(1) > blockquote > div > div.media-body > div:nth-child(1) > div > span').text
        author_1=author_1.split(',')
        author_1=author_1[0]
    except:
        author_1 = ''
    time.sleep(1)
    try:
        author_2 = driver.find_element_by_css_selector('#cmspg-session-details-presentation-list > div:nth-child(2) > blockquote > div > div.media-body > div:nth-child(1) > div > span').text
        author_2=author_2.split(',')
        author_2=author_2[0]
    except:
        author_2 = ''
    time.sleep(1)
    try:
        author_1_affi = driver.find_element_by_css_selector('#cmspg-session-details-presentation-list > div:nth-child(1) > blockquote > div > div.media-body > div:nth-child(1) > div > span').text
        author_1_affi=author_1_affi.split(',')
        author_1_affiliation=''
        for x in author_1_affi[1:]:
            author_1_affiliation=author_1_affiliation+x
    except:
        author_1_affiliation = "Not Provided"
    time.sleep(1)
    try:
        author_2_affi = driver.find_element_by_css_selector('#cmspg-session-details-presentation-list > div:nth-child(2) > blockquote > div > div.media-body > div:nth-child(1) > div > span').text
        author_2_affi=author_2_affi.split(',')
        author_2_affiliation=''
        for x in author_2_affi[1:]:
            author_2_affiliation=author_2_affiliation+x
    except:
        author_2_affiliation = "Not Provided"
    time.sleep(1)
    try:
        d = driver.find_element_by_css_selector('#cmspg-sessiondetails > div:nth-child(1) > div > span:nth-child(1)').text
        d=d.split(',')
        date=d[1]+'2021'

    except:
        date = "Not Provided"
    time.sleep(1)
    try:
        start = driver.find_element_by_css_selector('#cmspg-sessiondetails > div:nth-child(1) > div > span:nth-child(1)').text
        start=start.split(',')
        start_=start[-1].split('-')
        start_time=start_[0]
    except:
        start_time = "Not Provided"
    time.sleep(1)
    try:
        end = driver.find_element_by_css_selector('#cmspg-sessiondetails > div:nth-child(1) > div > span:nth-child(1)').text
        end=end.split(',')
        e=end[-1].split('-')
        end_time=e[-1]

    except:
        end_time = "Not Provided"
    time.sleep(1)
    try:
        location = driver.find_element_by_css_selector('#cmspg-sessiondetails > div:nth-child(1) > div > span:nth-child(2)').text
    except:
        location = "Not Provided"
    time.sleep(1)
    try:
        session_title = driver.find_element_by_css_selector('#cmspg-sessiondetails > div.media > div.media-body > div:nth-child(2) > span:nth-child(2)').text
    except:
        session_title = "Not Provided"
    time.sleep(1)
    try:
        session_type = driver.find_element_by_css_selector('#cmspg-sessiondetails > div.media > div.media-body > div:nth-child(3) > span:nth-child(2)').text
    except:
        session_type = "Not Provided"

    id = {
        'source_id': source_code,
        'manual_id':' ',
        'article_title': article_title,
         'url': link,
        'authors': author_1+';'+author_2,
        'author_affiliation':author_1_affiliation+';'+author_2_affiliation,
        'abstract_text':'',
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'location': location,
        'session_title': session_title,
        'session_type': session_type,
        'category':'',
        'subcategory':'',
        'disclosure':'',
        'Image_Table':''
        }
    all_details.append(id)
    time.sleep(1)

df = pd.DataFrame(all_details)
print(df.head())  #shows first five rows of the dataframe
df.to_csv("confrence_details_1.csv")

driver.close()