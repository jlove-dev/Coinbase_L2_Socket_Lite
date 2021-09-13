import threading
import websocket
import json
import pandas as pd
import time
import itertools
import collections


class Coin:

    def __init__(self, name):
        self.name = name
        self.bids = {}
        self.asks = {}

    def set_dicts(self, result):
        if result['type'] == 'snapshot':
            for price, size in result['bids']:
                self.bids[float(price)] = {'side': 'bids', 'size': float(size)}

            for price, size in result['asks']:
                self.asks[float(price)] = {'side': 'asks', 'size': float(size)}

        elif result['type'] == 'l2update':
            if result['changes'][0][0] == 'buy':
                if float(result['changes'][0][1]) in self.bids:
                    if float(result['changes'][0][2]) == 0.0:
                        del self.bids[float(result['changes'][0][1])]
                    else:
                        self.bids[float(result['changes'][0][1])]['size'] = float(result['changes'][0][2])
                else:
                    self.bids[float(result['changes'][0][1])] = {'side': 'bids', 'size': float(result['changes'][0][2])}

            elif result['changes'][0][0] == 'sell':
                if float(result['changes'][0][1]) in self.asks:
                    if float(result['changes'][0][2]) == 0.0:
                        del self.asks[float(result['changes'][0][1])]
                    else:
                        self.asks[float(result['changes'][0][1])]['size'] = float(result['changes'][0][2])
                else:
                    self.asks[float(result['changes'][0][1])] = {'side': 'asks', 'size': float(result['changes'][0][2])}

    def get_df(self):
        bids = self.bid_sort()
        asks = self.ask_sort()
        bids_df = pd.DataFrame.from_dict(data=dict(itertools.islice(bids.items(), 500)), orient='index')
        bids_df.reset_index(level=0, inplace=True)
        bids_df = bids_df.rename(columns={'index': 'price'})
        #
        asks_df = pd.DataFrame.from_dict(data=dict(itertools.islice(asks.items(), 500)), orient='index')
        asks_df.reset_index(level=0, inplace=True)
        asks_df = asks_df.rename(columns={'index': 'price'})
        return bids_df, asks_df

    def bid_sort(self):
        ordered_dict = collections.OrderedDict(sorted(self.bids.items(), reverse=True))
        return ordered_dict

    def ask_sort(self):
        ordered_dict = collections.OrderedDict(sorted(self.asks.items()))
        return ordered_dict


class CbSocket:

    def __init__(self, limit):
        self.socket = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
                                             on_message=lambda ws, msg: self.on_message(ws, msg),
                                             on_open=lambda ws: self.on_open(ws))
        self.book = None
        self.limit = limit
        self.bids = {}
        self.asks = {}
        self.best_bid = 0.0
        self.best_ask = 0.0
        self.coins = {
            'ETH-USD': Coin('ETH-USD'),
            'BTC-USD': Coin('BTC-USD'),
            'ADA-USD': Coin('ADA-USD'),
            'SOL-USD': Coin('SOL-USD'),
            'XTZ-USD': Coin('XTZ-USD'),
            'ALGO-USD': Coin('ALGO-USD'),
            'ATOM-USD': Coin('ATOM-USD'),
            'MATIC-USD': Coin('MATIC-USD'),
            'DOT-USD': Coin('DOT-USD'),
            'AAVE-USD': Coin('AAVE-USD')
        }

        '''
        dict format --
        {
            price:
                {'side': 'bids', 'size': 0.1111},
        }
        '''

    def get_df(self, _id):
        book = self.coins.get(_id)
        return book.get_df()

    def on_message(self, ws, message):
        result = json.loads(message)
        if result['product_id'] == 'ETH-USD':
            ethBook = self.coins.get('ETH-USD')
            ethBook.set_dicts(result)
        elif result['product_id'] == 'BTC-USD':
            btcBook = self.coins.get('BTC-USD')
            btcBook.set_dicts(result)
        elif result['product_id'] == 'ADA-USD':
            adaBook = self.coins.get('ADA-USD')
            adaBook.set_dicts(result)
        elif result['product_id'] == 'SOL-USD':
            solBook = self.coins.get('SOL-USD')
            solBook.set_dicts(result)
        elif result['product_id'] == 'XTZ-USD':
            xtzBook = self.coins.get('XTZ-USD')
            xtzBook.set_dicts(result)
        elif result['product_id'] == 'ALGO-USD':
            algoBook = self.coins.get('ALGO-USD')
            algoBook.set_dicts(result)
        elif result['product_id'] == 'ATOM-USD':
            atomBook = self.coins.get('ATOM-USD')
            atomBook.set_dicts(result)
        elif result['product_id'] == 'MATIC-USD':
            maticBook = self.coins.get('MATIC-USD')
            maticBook.set_dicts(result)
        elif result['product_id'] == 'DOT-USD':
            dotBook = self.coins.get('DOT-USD')
            dotBook.set_dicts(result)
        elif result['product_id'] == 'AAVE-USD':
            aaveBook = self.coins.get('AAVE-USD')
            aaveBook.set_dicts(result)
        else:
            print('key not found')

    def on_open(self, ws):
        ws.send(open('subscribe.json').read())

    def run(self):
        t_run = threading.Thread(target=self.socket.run_forever)
        t_run.start()


if __name__ == "__main__":

    new = CbSocket(10)
    new.run()

    while True:
        bids, asks = new.get_df('ETH-USD')
        print(bids)
        time.sleep(1)
        bids, asks = new.get_df('BTC-USD')
        print(bids)
        time.sleep(1)
        bids, asks = new.get_df('DOT-USD')
        print(bids)
        time.sleep(1)
        bids, asks = new.get_df('ADA-USD')
        print(bids)
        time.sleep(1)