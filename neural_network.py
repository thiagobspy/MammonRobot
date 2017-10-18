import random

import numpy

from technical_analysis import TechnicalAnalysis


class NeuralNetwork:
    def predict(self, open, high, low, close, volume):
        technical_analysis = TechnicalAnalysis(open, high, low, close, volume).execute()
        data = self.remove_nan(technical_analysis)
        print(data.shape)
        print(data)

        return random.randint(0,2)

    def remove_nan(self, data):
        return data[~numpy.isnan(data).any(axis=1)]
