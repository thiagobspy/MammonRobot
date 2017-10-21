import pandas

from backtesting.logger import Logger, GeneralStatistics
from backtesting.strategy import Strategy, Momentun


class Machine:
    def __init__(self):
        self.money = 10000
        self.tick = 0
        self._data = pandas.DataFrame()
        self.strategies = []
        self.logger = Logger()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if {'date', 'open', 'high', 'low', 'close', 'volume'}.issubset(value.columns):
            self._data = value
        else:
            raise

    def run(self):
        dataset_final = self.data.shape[0]
        while self.tick < dataset_final:
            tick = self.data.iloc[self.tick:self.tick + 1]
            for strategy in self.strategies:
                strategy.input_tick(tick)
                strategy.execute()
                for trade in strategy.open_positions:
                    if trade.automatic_close(tick.iloc[0], logger=self.logger):
                        strategy.open_positions.remove(trade)

            self.tick += 1

        for strategy in self.strategies:
            strategy.finish(logger=self.logger)
            if self.logger:
                self.logger.final(strategy.trades)

    def add_strategy(self, strategy):
        if isinstance(strategy, Strategy):
            self.strategies.append(strategy)
        else:
            raise

    def add_logger(self, logger):
        if isinstance(logger, Logger):
            self.logger = logger
        else:
            raise
