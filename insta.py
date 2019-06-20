
# coding: utf-8

# In[385]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import json


# In[386]:


search = input("검색 :")
URL = "https://www.instagram.com/explore/tags/{search}/".format(search=search)
driver = webdriver.Chrome("./chromedriver")  
driver.get(URL)

urllists = []
down_key = driver.find_element_by_tag_name("body") 
for n in range(1,4):
    down_key.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    for url in driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a"):
        urllists.append(url.get_attribute("href"))
        
url_list = list(set(urllists))

for url in url_list:
    html = requests.get(url) 
    bs = BeautifulSoup(html.content,"html.parser")  

    hashtag = bs.findAll("script",type="application/ld+json")
    try:
        if hashtag == []:
            hashtag_count = len(bs.findAll("script",type="text/javascript"))
            hashtags = bs.findAll("script",type="text/javascript")
            index_script = []
            for no in range(hashtag_count):
                index_script.append(len(bs.findAll("script",type="text/javascript")[no].text))

            hashtags_json = hashtags[index_script.index(max(index_script))].text
            hashtags_json_start = hashtags_json.find("{")
            content_json = json.loads(hashtags_json[hashtags_json_start:-1])
            print(content_json["caption"])
            print("====================================================================")
        else:
            #hashtag = bs.findAll("script",type="application/ld+json")
            content_json = json.loads(hashtag[0].text)
            print(content_json["caption"])
            print("====================================================================")
    except KeyError:
        content_json = json.loads(hashtags_json[hashtags_json_start:-1])
        print(content_json["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
        print("====================================================================")
    except json.JSONDecodeError:
        hashtag_count = len(bs.findAll("script",type="text/javascript"))
        hashtags = bs.findAll("script",type="text/javascript")
        index_script = []
        for no in range(hashtag_count):
            index_script.append(len(bs.findAll("script",type="text/javascript")[no].text))

        index_script[index_script.index(max(index_script))] = 0
        max(index_script) 
        hashtags_json = hashtags[index_script.index(max(index_script))].text
        hashtags_json_start = hashtags_json.find("{")
        content_json = json.loads(hashtags_json[hashtags_json_start:-1])
        print(content_json["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
        print("====================================================================")

    except:
        print("oooooooooooooooooooooooooooooooo")
        print("oooooooooooooooo",url)
        print("oooooooooooooooooooooooooooooooo")
        pass

