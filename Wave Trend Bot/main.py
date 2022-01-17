import ccxt
import time
from configparser import ConfigParser
from LoadExchanges import Exchange

config_file = ConfigParser()
config_file.read('C:\\Users\\pattt\\Desktop\\exchanges.config')


def mainBotThread(seconds, exchange):
    while(True):
        try:

            time.sleep(seconds)
        except ccxt.NetworkError as e:
            print(exchange.id, 'fetch_order_book failed due to a network error:', str(e))
        except ccxt.ExchangeError as e:
            print(e)
        except Exception as e:
            print(e)


def startBot():
    exchanges = ['gateio']
    coin = 'BTC'
    currency = 'USDT'
    pairs = [coin + '/' + currency]
    timeframe = '1m'
    # 30% of account balance to be used / trade
    trade_ratio_to_balance = .3
    if __name__ == "__main__":
        for exchange in exchanges:
            for pair in pairs:
                e = Exchange(exchange, config_file, pair, timeframe)
                e.connectExchange()
                

startBot()