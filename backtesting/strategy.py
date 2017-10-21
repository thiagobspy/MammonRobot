import abc
import math

import pandas
import talib

from backtesting.trade import Trade


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