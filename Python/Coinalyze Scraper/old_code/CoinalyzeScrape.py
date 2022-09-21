from os import remove, stat
from requests.api import head
from coin import coin
import old_code.pepe as pepe
import requests
from bs4 import BeautifulSoup, element
import pandas as pd
import json
import lxml
import os
pepe = pepe

# This contains all pairs in list format
allCoinPairs = []

# This contains all coins, stats, and trend stats in list of DataFrame objects
coinObjects = []

# This function will grab all of the 'technical analysis' links for all coins on the front page
def getNewTaData():
    URL = "https://coinalyze.net"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    # Load the figure elements with class 'gallery-item'
    getCoinsDiv = soup.find_all("div", class_='coins')
    allCoinsURL = []
    for coin in getCoinsDiv:
        links = coin.findAll('a')
        for a in links:
            l = URL + a["href"]
            allCoinsURL.append(l)
    getTAData(allCoinsURL)


# This function will take a list of every link on the home page, open it, and extract all the TA information.
def getTAData(link):
    for l in link:
        if(l != 'https://coinalyze.net/funfair/technical-analysis/'):
            # We loop through the links
            # Create a new request
            r = requests.get(l)
            # New beautifulsoup
            taSoup = BeautifulSoup(r.content, 'html.parser')
            # with open('ta.txt', 'w') as my_data_file:
            # This contains the data in the "stats" category/class
            data = taSoup.find('div', class_='stats')
            # This will grab all of the coins data
            product = data.findNext('td').contents[0]
            price = product.findNext('td')
            statsData = price.findNext('table')

            trendTable = statsData.findNext('table')
            statsDF = pd.read_html(str(statsData))[0]
            trendDF = pd.read_html(str(trendTable))[0]
            product = str(product.text.replace('Current ', ''))
            product = product.replace(' / ', '')
            allCoinPairs.append(product)
            cwd = os.getcwd()
            path = cwd + "/TA/"
            statsDF.to_csv(path+product + " STATS.csv", index=False, header=False)
            trendDF.to_csv(path+product + " TRENDS.csv", index=False, header=False)


def getNewFuturesData():
    URL = "https://coinalyze.net/futures-data/coins/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
        
    table_wrapper = soup.find('div', class_='table-wrapper')
    table = table_wrapper.findNext('table')
    futuresDF = pd.read_html(str(table))[0]
    futuresDF = futuresDF.drop(columns=["Unnamed: 0"])
    print(futuresDF)



# This function will load all coins from the file below, loop through, and create a dictionary of the {name:dataframe} from the 
# associated file in the 'ta' folder
def importCoins():
    cwd = os.getcwd()
    path = cwd + "/TA/"
    ta_files = os.listdir(path=path)
    for f in ta_files:
        # need to check for f being 'TREND' file or 'STAT' file before proceeding
        if(f.endswith("TRENDS.csv")):
            coin = f.split(' ')[0]
            coin_obj = {coin : pd.read_csv(path + f)}
            coinObjects.append(coin_obj)
            
# After loading the 'csv' files you can call these 'summary' functions + the coin name to lookup its stats
def getTrendSummary(df, coin):
    for each in df:
        for key in each.keys():
            if(key == coin):
                # print(each[key].loc[12])
                z = each[key].loc[12]
                print(z)


def getSummary(df, coin):
    for each in df:
        for key in each.keys():
            if(key == coin):
                # print(each[key].loc[12])
                z = each[key]
                print(z)

def getSummaryAllCoins(df):
    for each in df:
        print(df[each])


def start():
    #getNewTaData(coin='BTCUSD')
    #importCoins()
    #getTrendSummary(coinObjects, "BTCUSD")
    #getSummary(coinObjects, "BTCUSD")
    #getNewFuturesData()

    
    pass