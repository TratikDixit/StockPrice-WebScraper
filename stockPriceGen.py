# importing libraries
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv

# function to check if the URL is valid


def validURL(soup):
    check = soup.findAll('p')
    for i in check:
        if(i.text == 'No result'):
            return False
    return True

# function that returns the html content for the page


def getHTML(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup


# page counter to iterate through different pages of the website
pagectr = 1
# stores all the data about the stocks
stockData = []
# stock data headers
head = ['StockName', 'CurrentPrice', '%Change',
        'OpeningPrice', 'High', 'Low', 'VolumeCap']

baseURL = "https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_29-us-nyse-stocks--qc_1-alphabetical-order?p="
URL = baseURL + '1'
soup = getHTML(URL)


while validURL(soup):
    print("Loading content at ", URL)

    # storing the data for the current page
    data = soup.find('tbody')
    for t in data.findAll('tr'):
        stock = {}
        ctr = 1
        for c in t.findAll('td'):
            n = c.find('a')
            if(n != None):
                stock['StockName'] = n.text
            for j in c.findAll('span'):
                if(ctr == 7):
                    break
                stock[head[ctr]] = j.text
                ctr += 1

        stockData.append(stock)

    # traversing to the next page
    pagectr += 1
    URL = baseURL + str(pagectr)
    soup = getHTML(URL)

# storing the stock data in a csv file
today = datetime.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_day = today.strftime("%d:%m:%Y")

filename = 'stock-price-data-'+current_day+'-'+current_time+'.csv'

with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, head)
    w.writeheader()
    for quote in stockData:
        w.writerow(quote)
