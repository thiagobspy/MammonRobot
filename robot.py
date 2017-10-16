import json
import random

import numpy
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
from oandapyV20.endpoints import pricing, positions, instruments, trades, orders
from oandapyV20.endpoints.pricing import PricingStream

from technical_analysis import TechnicalAnalysis


def get_price():
    accountID = '101-004-6614323-001'
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)
    instrument = 'EUR_USD'
    params = {'instruments': instrument}
    pricingInfo = pricing.PricingInfo(accountID, params=params)
    rv = client.request(pricingInfo)

    bids = float(rv['prices'][0]['bids'][0]['price'])
    asks = float(rv['prices'][0]['asks'][0]['price'])

    return bids, asks


def get_position():
    accountID = '101-004-6614323-001'
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)
    positionList = positions.OpenPositions(accountID)
    rv = client.request(positionList)

    return rv


def get_trade():
    accountID = '101-004-6614323-001'
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)
    positionList = trades.OpenTrades(accountID)
    rv = client.request(positionList)

    return rv


def get_order():
    accountID = '101-004-6614323-001'
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)
    positionList = orders.OrdersPending(accountID)
    rv = client.request(positionList)

    return rv


def get_datas():
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)
    instrument = 'EUR_USD'
    params = {
        'granularity': 'M5',
        'count': 170
    }
    instrumentsCandles = instruments.InstrumentsCandles(instrument=instrument, params=params)
    rv = client.request(instrumentsCandles)

    return rv


def transform_input():
    candles = get_datas()['candles']
    open = []
    high = []
    low = []
    close = []
    volume = []

    for candle in candles:
        mid = candle['mid']
        open.append(mid['o'])
        high.append(mid['h'])
        low.append(mid['l'])
        close.append(mid['c'])
        volume.append(candle['volume'])

    return numpy.array(open, dtype=float), numpy.array(high, dtype=float), numpy.array(low, dtype=float), numpy.array(
        close, dtype=float), numpy.array(volume, dtype=float)


def execute_technical_analysis():
    open, high, low, close, volume = transform_input()
    technical_analysis = TechnicalAnalysis(open, high, low, close, volume)
    return technical_analysis.execute()


def remove_nan(data):
    return data[~numpy.isnan(data).any(axis=1)]


def call_neural(data):
    return random.randint(0, 2)


def create_order(unit, tk, sl):
    accountID = '101-004-6614323-001'
    access_token = '435fc89e4fec6d2c1fa46de985e6ab6f-2b4e3458cb268aac64666f37d10ac0ee'
    client = API(access_token=access_token)

    mktOrder = MarketOrderRequest(
        instrument="EUR_USD",
        units=unit,
        takeProfitOnFill=TakeProfitDetails(price=tk).data,
        stopLossOnFill=StopLossDetails(price=sl).data)

    r = orders.OrderCreate(accountID, data=mktOrder.data)
    return client.request(r)


order = call_neural(2)


def comprar():
    b, a = get_price()
    tk = a * 1 + 0.002
    sl = a * 1 - 0.002
    create_order(1, tk, sl)


def vender():
    b, a = get_price()
    tk = b * 1 - 0.002
    sl = b * 1 + 0.002
    create_order(-1, tk, sl)


if order == 1:
    comprar()
elif order == 2:
    vender()
else:
    pass


print(order)
