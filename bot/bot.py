from binance.client import Client
from binance.enums import *
api_key = ''
api_secret = ''
timeFrame = '4h'
client =Client(api_key,api_secret)
exchange_info = client.get_exchange_info()
symbols = [symbol['symbol'] for symbol in exchange_info['symbols']]
for symbol in symbols:
    klines = client.get_klines(symbol=symbol, interval=timeFrame)
    close_prices = [float(kline[4]) for kline in klines]
    macd, signal, _ = talib.MACD(np.array(close_prices))
    if macd[-1] < 0:
        print(f"{symbol} 在 {timeFrame} 周期级别下的MACD在零轴下方")
