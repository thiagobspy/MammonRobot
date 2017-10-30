import pandas

from backtesting.logger import GeneralStatistics
from backtesting.machine import Machine
from backtesting.strategy import Momentun, NeuralNetwork

for i in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    s = NeuralNetwork(i, name='Neural')
    l = GeneralStatistics()
    m = Machine()
    m.data = pandas.read_csv('backtesting/eur_usd_m15_.csv')
    m.add_strategy(s)
    m.add_logger(l)
    m.run()
