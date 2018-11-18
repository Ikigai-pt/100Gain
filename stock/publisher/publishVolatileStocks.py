import pandas_datareader.data as web
from bs4 import BeautifulSoup
import requests
from stock.tasks.recordVolatileStock import stockInfo
losers_url= "https://finance.yahoo.com/losers?offset=0&count=100"

def gatherStocks(category):
    base_url = "https://finance.yahoo.com/"+category+"?offset=0&count=100"
    r  = requests.get(base_url)
    data = r.text
    soup = BeautifulSoup(data,"html.parser")
    for row in soup.find_all('td'):
        link = row.a
        if link is not None:
            symbol = link['href'].split('=')[1]
            stockInfo.delay(symbol,category)

if __name__ == '__main__':
    print("Top Gainers")
    gatherStocks('gainers')
    print("Top Losers")
    gatherStocks('losers')
