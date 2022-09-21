from os import remove, stat
from requests.api import head
import old_code.pepe as pepe
import requests
from bs4 import BeautifulSoup, element
import pandas as pd
import json
from coin import *
import lxml

pepe = pepe
URL = "https://coinalyze.net"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


def loadTALinks():
    # Load the figure elements with class 'gallery-item'
    getCoinsDiv = soup.find_all("div", class_='coins')
    allCoinsURL = []
    for coin in getCoinsDiv:
        links = coin.findAll('a')
        for a in links:
            l = URL + a["href"]
            allCoinsURL.append(l)
    pullTAData(allCoinsURL)


trendTablesAllLinks = []
fullListOfCoinObjects = []


# This function will take a list of every link on the home page, open it, and extract all the TA information.
def pullTAData(link):
    # We loop through the links
    # Create a new request
    r = requests.get(link)
    # New beautifulsoup
    taSoup = BeautifulSoup(r.content, 'html.parser')
    # with open('ta.txt', 'w') as my_data_file:
    # This contains the data in the "stats" category/class
    data = taSoup.find('div', class_='stats')
    # This will grab all of the coins data
    headers = data.findNext('td').contents[0]
    product = data.findNext('td').contents[0]  # we will ignore this data
    price = product.findNext('td')
    statsTableHeaders = ['1 Hour', '24 Hours', '7 Days', '30 Days']
    statsData = price.findNext('table')
    df = pd.read_html(str(statsData))[0]
    print(df)
    # changesTitles = statsData.find_next() # ignoring
    # changesData = changesTitles.find_next_siblings('tr')[0]
    # highsData = changesTitles.find_next_siblings('tr')[1]
    # lowsData = changesTitles.find_next_siblings('tr')[2]
    trendHeaders = ['5 min', '15 min', '1 hour', '2 hour', '4 hour', '6 hour', '1 day']
    trendTable = statsData.findNext('table')
    # trendTable = str(trendTable.text).strip()

    # Data clean up section
    productPair = str(headers.replace("Current", ""))  # Headers after removing the "/" and "Current"
    coinPair = productPair.replace(' / ', '')
    price = str(price.text.lstrip())
    statsData = removeEmptyStrings(statsData.text.lstrip().splitlines())
    trendTable = removeEmptyStrings(trendTable.text.lstrip().splitlines())  # function to remove empty strings in the list
    # statsTableHeaders = statsData[0:5] # grabbing the "stats" strings in the list
    statsTableChange = statsData[6:10]  # grabbing the "change" strings in the list
    statsTableHigh = statsData[11:15]  # grabbing the "high" strings in the list
    statsTableLow = statsData[16:20]  # grabbing the "low" strings in the list

    strippedTrendTable = []
    for x in trendTable:
        strippedTrendTable.append(x.strip())

    trendTableSMA10 = strippedTrendTable[9:30]
    trendTableEMA10 = strippedTrendTable[31:52]

    trendTableSMA20 = strippedTrendTable[53:74]
    trendTableEMA20 = strippedTrendTable[75:96]

    trendTableSMA30 = strippedTrendTable[97:118]
    trendTableEMA30 = strippedTrendTable[119:140]

    trendTableSMA50 = strippedTrendTable[141:162]
    trendTableEMA50 = strippedTrendTable[163:184]

    trendTableSMA100 = strippedTrendTable[185:206]
    trendTableEMA100 = strippedTrendTable[207:228]

    trendTableSMA200 = strippedTrendTable[229:250]
    trendTableEMA200 = strippedTrendTable[251:272]

    trendTableSummary = strippedTrendTable[273:294]

    sma = [trendTableSMA10, trendTableSMA20, trendTableSMA30, trendTableSMA50, trendTableSMA100, trendTableSMA200]
    ema = [trendTableEMA10, trendTableEMA20, trendTableEMA30, trendTableEMA50, trendTableEMA100, trendTableEMA200]

    createStatsTable(statsTableHeaders, statsTableChange, statsTableHigh, statsTableLow)
    createTrendTable(coinPair, trendHeaders, sma, ema, trendTableSummary)
    # d = json.dumps(fullCoinStats)
    # trendTablesAllLinks.append(fullCoinStats)
    # with open(product + '.json', 'w') as f:
    # json.dump(d, f)


def createStatsTable(headers, change, high, low):
    changeStats = dict(zip(headers, change))
    highStats = dict(zip(headers, high))
    lowStats = dict(zip(headers, low))
    #print(changeStats)
    #print(highStats)
    #print(lowStats)

def createTrendTable(coin, headers, sma, ema, summary):
    maTableHead = ["Price", "Change", "Up"]
    sumTableHead = ['Up', 'Down', 'Neutral']

    smaDF = pd.DataFrame(sma, index=['SMA10', 'SMA20', 'SMA30', 'SMA50', 'SMA100', 'SMA200'], 
        columns=["Price", "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", "Price", 
        "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", ])
    emaDF = pd.DataFrame(ema, index=['SMA10', 'SMA20', 'SMA30', 'SMA50', 'SMA100', 'SMA200'],

        columns=["Price", "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", "Price", 
        "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", "Price", "Change", "Rating", ])
    sumDF = pd.DataFrame(summary)
    smaDF.to_json(coin + '.json', orient='table')

def removeEmptyStrings(l):
    return list(filter(None, l))




def start():
    pullTAData("https://coinalyze.net/bitcoin/technical-analysis")