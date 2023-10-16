import yfinance as yf
import finplot as fplt
from datetime import datetime


user_input = input("Please enter a ticker: ")
ticker = yf.Ticker(user_input)


df = ticker.history(interval='1d',period='1y')

info = ticker.info
print(info.keys())

total_rev = info['lastFiscalYearEnd']
print(f"{total_rev:,}")

#fplt.candlestick_ochl(df[['Open','Close','High','Low']])
#fplt.show()