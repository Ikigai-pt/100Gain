from bs4 import BeautifulSoup
from iexfinance import Stock

def fetchStock(symbol):
    try:
        quote = Stock(symbol, output_format="json")
        stock = {}
        if quote is not None:
            stock['symbol'] = quote.get_quote()["symbol"]
            stock['name'] = quote.get_quote()["companyName"]
            stock['sector'] = quote.get_quote()["sector"]
            stock[ 'price' ] = quote.get_price()
            stock[ 'avgVolume' ] = quote.get_quote()["avgTotalVolume"]
            stock[ 'change' ] = quote.get_quote()["change"]
            stock[ 'changePercent' ] = quote.get_quote()["changePercent"]
            stock[ 'marketCap' ] = quote.get_quote()["marketCap"]
            stock[ 'week52High' ] = quote.get_quote()["week52High"]
            stock[ 'week52Low' ] = quote.get_quote()["week52Low"]
            return stock
        else:
            print('symbol not found in Exchange')
            return None
    except Exception as err:
        print(err)
        return None
