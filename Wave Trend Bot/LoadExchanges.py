from configparser import ConfigParser
import ccxt
import pandas as pd
import pprint
import os

class Exchange:
    # Initialize the Exchange() with a list of exchanges and a config file containing api key pairs
    def __init__(self, exchange_, config_, pair_, timeframe_):
        self.exchange = exchange_
        self.connection = None
        self.config = config_
        self.pair = pair_
        self.timeframe = timeframe_
        self.bars = None


    def saveNewHistory(self):
        pass
        # add the timeframe (rows) that haven't been saved to the ohlc/file.csv
        # subtract the csv file rows from self.bars then append those to the end of the csv


    def fetchLastTF(self):
        lastTF = pd.DataFrame(self.connection.fetch_ohlcv(self.pair, self.timeframe, limit=1))
        self.bars.append(lastTF)

    def loadHistory(self):
        file = 'ohlc/' + self.pair.replace('/', '-') + '.csv'
        if(os.path.isfile(file)):
            self.bars = pd.read_csv(file)
        else:
            self.bars = pd.DataFrame(self.connection.fetch_ohlcv(self.pair, self.timeframe))
            self.bars.to_csv(file)
        print(self.bars.head)


    def connectExchange(self):
        exchange_class = getattr(ccxt, self.exchange)
        if(self.exchange.upper() in self.config):
            try:
                self.connection = exchange_class({
                    'apiKey': self.config[self.exchange.upper()]['apiKey'],
                    'secret': self.config[self.exchange.upper()]['secret'],
                })
                self.loadHistory()
                print(self.exchange + " - Connected")
            except ccxt.NetworkError as e:
                print(e)
            except ccxt.ExchangeError as e:
                print(e)
            except Exception as e:
                print(e)