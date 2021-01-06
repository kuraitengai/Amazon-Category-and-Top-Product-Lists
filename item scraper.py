# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:16:44 2018

@author: test
"""

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn

#Creating url list
url_list = ['https://www.amazon.com/best-sellers-books-Amazon/zgbs/books',
            'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Literature-Fiction/zgbs/books/17',
            'https://www.amazon.com/Best-Sellers-Books-Literature-Fiction/zgbs/books/17/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Southern-Fiction/zgbs/books/17745819011',
            'https://www.amazon.com/Best-Sellers-Books-Southern-Fiction/zgbs/books/17745819011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Small-Town-Rural-Fiction/zgbs/books/13922576011',
            'https://www.amazon.com/Best-Sellers-Books-Small-Town-Rural-Fiction/zgbs/books/13922576011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Womens-Domestic-Life-Fiction/zgbs/books/542656',
            'https://www.amazon.com/Best-Sellers-Books-Womens-Domestic-Life-Fiction/zgbs/books/542656/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Family-Life-Fiction/zgbs/books/11047977011',
            'https://www.amazon.com/Best-Sellers-Books-Family-Life-Fiction/zgbs/books/11047977011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Religious-Literature-Fiction/zgbs/books/12489',
            'https://www.amazon.com/Best-Sellers-Books-Religious-Literature-Fiction/zgbs/books/12489/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Christian-Literature-Fiction/zgbs/books/172806',
            'https://www.amazon.com/Best-Sellers-Books-Christian-Literature-Fiction/zgbs/books/172806/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Christian-Romance/zgbs/books/332930011',
            'https://www.amazon.com/Best-Sellers-Books-Christian-Romance/zgbs/books/332930011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
            'https://www.amazon.com/Best-Sellers-Books-Religious-Romance/zgbs/books/12500',
            'https://www.amazon.com/Best-Sellers-Books-Religious-Romance/zgbs/books/12500/ref=zg_bs_pg_2?_encoding=UTF8&pg=2']

#Declaring the lists to store data
titles = []
authors = []
lists = []

#Preparing the monitoring of the loop
start_time = time()
requests = 0

#For each link in url list
for link in url_list:
    #Make a get request
    response = get(link, headers = {"Accept-Language": "en-US, en;q=0.5"})
    #print(response.text)
    
    # Pause the loop
    sleep(randint(8,15))
    
    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    
    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    
    # Break the loop if the number of requests is greater than expected
    if requests > 72:
        warn('Number of requests was greater than expected.')  
        break 
    
    #Parse the content of the request with BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    
    book_lists = html_soup.find_all('span', class_ = 'category')
    for container in book_lists:
        list = container.text.strip()
    
    #Select all the containers from a single page
    book_containers = html_soup.find_all('li', class_ = 'zg-item-immersion')
    #print(type(book_containers))
    #print(len(book_containers))
    
    #first_book = book_containers[0]
    #print(first_book.a.text)
    
    #first_author = first_book.find('div', class_ = 'a-row a-size-small')
    #print(first_author.text)
    
    #For each of the containers on the page
    for container in book_containers:
        #Scrape the title
        title = container.a.text.strip()
        titles.append(title)
        
        #Scrape the author
        author = container.find('div', class_ = 'a-row a-size-small').text
        authors.append(author)
        
        lists.append(list)
        
#Store data in dataframe
bestseller_list = pd.DataFrame({'list': lists,
                                'author': authors,
                                'title': titles})

#Display dataframe results
print(bestseller_list.info())
#print(bestseller_list)

#Populate csv with results
bestseller_list.to_csv('output_list.csv', sep=',', encoding='utf-8', index=False)
