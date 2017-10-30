import abc
import math
import json

import numpy
import pandas
import talib
from keras.models import model_from_json, Sequential

from backtesting.trade import Trade
from technical_analysis import TechnicalAnalysisComplete
from utils import Utils


class Strategy:
    Number = 1

    def __init__(self, **kwargs):
        self.name = "Strategy: {0}".format(Strategy.Number)
        if 'name' in kwargs:
            self.name = "Strategy: {0}".format(kwargs['name'])

        self.data = pandas.DataFrame()
        self.trades = []
        self.open_positions = []
        Strategy.Number += 1

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def execute(self):
        pass

    def input_tick(self, tick):
        self.data = pandas.concat([tick, self.data])

    def order(self, units=0, resistance=0, support=0):
        data = self.data.iloc[0]
        trade = Trade(data=data, units=units, resistance=resistance, support=support)
        self.trades.append(trade)
        self.open_positions.append(trade)

    def profit(self):
        profit = 0
        for trade in self.trades:
            profit += trade.profit()
        return profit

    def finish(self, **kwargs):
        data = self.data.iloc[0]
        for trade in self.open_positions:
            if trade.close(data, **kwargs):
                self.open_positions.remove(trade)


class Momentun(Strategy):
    def execute(self):
        if len(self.open_positions) > 0:
            return

        ema_1, ema_2 = self.get_ema()

        if not (math.isnan(ema_1) or math.isnan(ema_2)):
            if ema_1 > ema_2:
                self.buy()
            else:
                self.sell()

    def get_ema(self):
        closes = self.data.iloc[0:21]['close'].values
        serie_ema_1 = talib.EMA(closes[::-1], 7)
        serie_ema_2 = talib.EMA(closes[::-1], 21)

        return serie_ema_1[-1], serie_ema_2[-1]

    def buy(self):
        price = self.data.iloc[0]['close']
        take_profit = price * (1 + 0.002)
        stop_loss = price * (1 - 0.002)
        self.order(1000, take_profit, stop_loss)

    def sell(self):
        price = self.data.iloc[0]['close']
        take_profit = price * (1 - 0.002)
        stop_loss = price * (1 + 0.002)
        self.order(-1000, stop_loss, take_profit)


class NeuralNetwork(Strategy):
    # [1 0 0] -> buy
    # [0 1 0] -> neutral
    # [0 0 s1] -> sell
    def __init__(self, conf, **kwargs):
        super().__init__()

        model_json = open('backtesting/model_(5,141)_m15.json').read()
        self.model = model_from_json(model_json)
        self.model.load_weights('backtesting/weights_(5,141)_m15.h5')
        self.conf = conf
        self.pred = 1

    def execute(self):
        if len(self.open_positions) > 0:
            self.pred = 1
            return

        if self.pred == 0:
            self.buy()
        elif self.pred == 2:
            self.sell()

        self.pred = 1
        self.pred = self.get_predication(self.conf)

    def get_predication(self, conf):
        open_ = numpy.array(self.data.iloc[0:93]['open'].values, dtype=float)
        high = numpy.array(self.data.iloc[0:93]['high'].values, dtype=float)
        low = numpy.array(self.data.iloc[0:93]['low'].values, dtype=float)
        close = numpy.array(self.data.iloc[0:93]['close'].values, dtype=float)
        volume = numpy.array(self.data.iloc[0:93]['volume'].values, dtype=float)

        technical_analysis = TechnicalAnalysisComplete(open_[::-1], high[::-1], low[::-1], close[::-1], volume[::-1])
        input_data = technical_analysis.execute()
        data = Utils.remove_nan(input_data)

        if data.shape[0] < 5:
            return 1

        predict = self.model.predict(numpy.expand_dims(data, 0))

        if predict[predict > conf].shape[0]:
            return predict.argmax()
        return 1

    def buy(self):
        price = self.data.iloc[0]['open']
        take_profit = price * (1 + 0.001)
        stop_loss = price * (1 - 0.001)
        self.order(10000, take_profit, stop_loss)

    def sell(self):
        price = self.data.iloc[0]['open']
        take_profit = price * (1 - 0.001)
        stop_loss = price * (1 + 0.001)
        self.order(-10000, stop_loss, take_profit)
