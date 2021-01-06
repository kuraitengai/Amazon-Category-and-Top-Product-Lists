# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:16:44 2018

@author: test
"""

import requests
import json
import threading
from bs4 import BeautifulSoup
import re

def GetSoupResponseFromURL(url):
    response = requests.get(url, timeout=180)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup;

def GetSubCategories(categoryURL):

    subCategory = []

    soup = GetSoupResponseFromURL(categoryURL)

    try:
        ul = soup.find('span', {'class':'zg_selected'}).parent.parent.find('ul')

        if ul is not None:
            subCategories = ul.find_all('a')

            for category in subCategories:
                catTitle =  category.text                
                url = category.get('href')

                lists = soup.find('ul', {'id':'zg_browseRoot'}).find_all('ul')

                del lists[-1]
                global  titleList
                titleList = []

                for ulist in lists:
                    text = re.sub(r'[^\x00-\x7F]+','', ulist.find('li').text)
                    titleList.append(text.strip(' \t\n\r'))            

                fullTitle = (' > '.join(map(str, titleList)) + ' > ' + catTitle)

                soup = GetSoupResponseFromURL(url)
                title = soup.find('span', {'class':'category'})

                if title is not None:
                    title = title.text
                else:
                    title = soup.find('div', {'id':'zg_rssLinks'}).find_all('a')[-1].text
                    title = title[title.index('>') + 2:]

                print('Complete Title: ' + fullTitle)
                print('Title: ' + title)
                print('URL: ' + url)
                print('-----------------------------------')

                data = {}
                data['completeTitle'] = fullTitle
                data['title'] = title
                data['url'] = url

                data['subCategory'] = GetSubCategories(url)         
                subCategory.append(data)
    except Exception as e:
        pass

    return subCategory      

class myThread (threading.Thread):
    def __init__(self, threadID, url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
    def run(self):
        print("Starting Thread " + str(self.threadID))
        array = []
        array = GetSubCategories(self.url)

        with open('Category ' + str(self.threadID) + '.json', 'w') as outfile:
            json.dump(array, outfile)

        print("Exiting Thread " + str(self.threadID))  


mainURL = 'https://www.amazon.com/Best-Sellers-Books-Genre-Literature-Fiction/zgbs/books/10134/ref=zg_bs_nav_b_2_17'
soup = GetSoupResponseFromURL(mainURL)

mainCategories = soup.find('ul', {'id':'zg_browseRoot'}).find_all('a')
print(mainCategories)

counter = 1
for category in mainCategories[1:2]:
    thread = myThread(counter, category.get('href'))
    thread.start()
    counter+=1

#Populate csv with results
mainCategories.to_csv('categories.csv', sep=',', encoding='utf-8', index=False)
