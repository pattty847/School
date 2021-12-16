from os import remove, stat
from requests.api import head
import pepe
import requests
from bs4 import BeautifulSoup, element
import json


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
# This function will take a list of every link on the home page, open it, and extract all the TA information.
def pullTAData(link):
    # We loop through the links
    for statTable in link:
        if statTable != 'https://coinalyze.net/funfair/technical-analysis/':
            # Create a new request
            r = requests.get(statTable)
            # New beautifulsoup
            taSoup = BeautifulSoup(r.content, 'html.parser')
            # with open('ta.txt', 'w') as my_data_file:
            # This contains the data in the "stats" category/class
            data = taSoup.find('div', class_='stats')
            # This will grab all of the coins data
            headers = data.findNext('td').contents[0]
            product = data.findNext('td').contents[0] # we will ignore this data
            price = product.findNext('td')
            statsHeaders = ['Stats', '1 Hour', '24 Hours', '7 Days', '30 Days']
            statsData = price.findNext('table')
            # changesTitles = statsData.find_next() # ignoring
            # changesData = changesTitles.find_next_siblings('tr')[0]
            # highsData = changesTitles.find_next_siblings('tr')[1]
            # lowsData = changesTitles.find_next_siblings('tr')[2]
            # trendHeaders = ['Trend', '5 min', '15 min' '1 hour', '2 hour', '4 hour', '6 hour', '1 day']
            trendTable = statsData.findNext('table')
            # trendTable = str(trendTable.text).strip()

            # Data clean up section
            headers = str(headers.text.replace("/", "-"))
            headers = headers.replace("Current", "").strip() # Headers after removing the "/" and "Current"
            price = str(price.text.lstrip())
            statsData = removeEmptyStrings(statsData.text.lstrip().splitlines())
            trendTable = removeEmptyStrings(trendTable.text.lstrip().splitlines()) # function to remove empty strings in the list
            statsTableHeaders = statsData[0:5] # grabbing the "stats" strings in the list
            statsTableChange = statsData[5:10] # grabbing the "change" strings in the list
            statsTableHigh = statsData[10:15] # grabbing the "high" strings in the list
            statsTableLow = statsData[15:20] # grabbing the "low" strings in the list
            strippedTrendTable = []
            for x in trendTable:
                strippedTrendTable.append(x.strip())
            trendTableSMA10 = strippedTrendTable[9:30]
            trendTableEMA10 = strippedTrendTable[31:52]
            trendTableSMA20 = strippedTrendTable[52:74]
            trendTableEMA20 = strippedTrendTable[74:96]
            trendTableSMA30 = strippedTrendTable[96:118]
            trendTableEMA30 = strippedTrendTable[118:140]
            trendTableSMA50 = strippedTrendTable[140:162]
            trendTableEMA50 = strippedTrendTable[162:184]
            trendTableSMA100 = strippedTrendTable[184:206]
            print(trendTableEMA50)
            # d = json.dumps(fullCoinStats)
            # trendTablesAllLinks.append(fullCoinStats)
            # with open(product + '.json', 'w') as f:
                # json.dump(d, f)


def removeEmptyStrings(l):
    return list(filter(None, l))

def saveToFile():
    trendTablesAllLinksJSON = json.dumps(trendTablesAllLinks)
    with open('ta.json', 'w') as f:
        json.dump(trendTablesAllLinksJSON, f)

def start():
    loadTALinks()


start()


"""
[<tr>
<td>Change %</td>
<td class="green">0.46%</td>
<td class="green">2.67%</td>
<td class="red">-4.54%</td>
<td class="red">-26.22%</td>
</tr>, <tr>
<td>High</td>
<td>48,449.35</td>
<td>48,795.00</td>
<td>51,250.00</td>
<td>66,339.90</td>
</tr>, <tr>
<td>Low</td>
<td>48,077.60</td>
<td>46,344.93</td>
<td>45,727.92</td>
<td>42,333.00</td>
</tr>]
"""