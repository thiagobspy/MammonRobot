import pandas

from backtesting.logger import GeneralStatistics
from backtesting.machine import Machine
from backtesting.strategy import Momentun

s = Momentun(name='Neural')
l = GeneralStatistics()
m = Machine()
m.data = pandas.read_csv('eur_usd_m5.csv')[0:3000]
m.add_strategy(s)
m.add_logger(l)
m.run()
