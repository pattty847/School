from configparser import ConfigParser
from datetime import datetime
import ccxt
import pandas as pd
import pprint
import os


class Exchange:
    def __init__(self, exchange_, config_, pair_, timeframe_):
        self.exchange = exchange_
        self.config = config_
        self.pair = pair_
        self.timeframe = timeframe_
        self.bars = None
        self.api = None


    def saveNewHistory(self):
        pass
        # add the timeframe (rows) that haven't been saved to the ohlc/file.csv
        # subtract the csv file rows from self.bars then append those to the end of the csv


    def fetchLastTF(self):
        lastTF = pd.DataFrame(self.api.fetch_ohlcv(self.pair, self.timeframe, limit=1))
        self.bars.append(lastTF)


    # 1642386240000
    # This function checks if we have a file with ohlc history and updates the timeframes we missed since last update
    def loadHistoryOnStartup(self):
        file = 'ohlc/' + self.pair.replace('/', '-') + '.csv'
        if(os.path.isfile(file)):
            history = pd.read_csv(file)
            new_data = pd.DataFrame(self.api.fetch_ohlcv(self.pair, self.timeframe, since=history.iloc[-1, 1]))
            new_data.to_csv(file, mode='a', index=True, header=False)
        else:
            self.bars = pd.DataFrame(self.api.fetch_ohlcv(self.pair, self.timeframe))
            self.bars.to_csv(file)


    # This is called first to make a connection to the exchange from the CONFIG file
    def connectExchange(self):
        exchange_class = getattr(ccxt, self.exchange)
        if(self.exchange.upper() in self.config):
            try:
                self.api = exchange_class({
                    'apiKey': self.config[self.exchange.upper()]['apiKey'],
                    'secret': self.config[self.exchange.upper()]['secret'],
                })
                # function explained above
                self.loadHistoryOnStartup()
                print(self.exchange + " - Connected")
            except ccxt.NetworkError as e:
                print(e)
            except ccxt.ExchangeError as e:
                print(e)
            except Exception as e:
                print(e)