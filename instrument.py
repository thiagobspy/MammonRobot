from oandapyV20 import API
from oandapyV20.endpoints import instruments

from configuration import Configuration
from utils import Utils


class Instrument:
    def __init__(self):
        self.access_token = Configuration.access_token
        self.account_id = Configuration.account_id
        self.client = API(access_token=self.access_token)

    def get_candles(self, params):
        params_copy = params.copy()
        instrument = params_copy.pop('instrument')
        response = self.request(instrument, params_copy)
        obj = Utils.json2obj(response)
        return obj.candles

    def request(self, instrument, params):
        instrumentsCandles = instruments.InstrumentsCandles(instrument=instrument, params=params)
        return self.client.request(instrumentsCandles)
