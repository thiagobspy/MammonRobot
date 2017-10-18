import numpy

from instrument import Instrument
from neural_network import NeuralNetwork
from positions import Position
from trader import Buy, Sell


class StrategyNeural:
    def __init__(self):
        self.position = Position()
        self.instrument = Instrument()
        self.neural_network = NeuralNetwork()

    def execute(self):
        if not self.position.has_open_position():
            params = self.builder_params()
            candles = self.instrument.get_candles(params)
            open, high, low, close, volume = self.candles2array(candles)

            operation = self.neural_network.predict(open, high, low, close, volume)

            self.execute_trade(operation)

    def builder_params(self):
        return {'instrument': 'EUR_USD', 'granularity': 'M5', 'count': 170}

    def candles2array(self, candles):
        open = []
        high = []
        low = []
        close = []
        volume = []

        for candle in candles:
            mid = candle.mid
            open.append(mid.o)
            high.append(mid.h)
            low.append(mid.l)
            close.append(mid.c)
            volume.append(candle.volume)

        return numpy.array(open, dtype=float), \
               numpy.array(high, dtype=float), \
               numpy.array(low, dtype=float), \
               numpy.array(close, dtype=float), \
               numpy.array(volume, dtype=float)

    def execute_trade(self, operation):
        params = {}
        params['instrument'] = 'EUR_USD'
        params['take_profit'] = 0.002
        params['stop_loss'] = 0.002
        if operation == 1:
            Buy().execute(params)
        elif operation == 2:
            Sell().execute(params)


str = StrategyNeural()
str.execute()
