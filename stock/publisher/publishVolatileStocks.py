import pandas_datareader.data as web
from bs4 import BeautifulSoup
import requests
from celery import chain
from stock.tasks.manageStock import stockInfo, registerStock
losers_url= "https://finance.yahoo.com/losers?offset=0&count=100"

def gatherStocks(category):
    base_url = "https://finance.yahoo.com/"+category+"?offset=0&count=100"
    r  = requests.get(base_url)
    data = r.text
    soup = BeautifulSoup(data,"html.parser")
    count = 0
    for row in soup.find_all('td'):
        link = row.a
        # if link is not None and count < 1:
        if link is not None :
            symbol = link['href'].split('=')[1]
            result = stockInfo.delay(symbol,category)
            registered = registerStock.delay(result.get(),category)
            print('result')
            print(registered.get())
            count = 1

if __name__ == '__main__':
    print("Top Gainers/Losers")
    gatherStocks('Gainers')
    gatherStocks('Losers')
