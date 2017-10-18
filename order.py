from oandapyV20 import API
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
from oandapyV20.endpoints import orders

from configuration import Configuration


class CreateOrder:
    def __init__(self):
        self.access_token = Configuration.access_token
        self.account_id = Configuration.account_id
        self.client = API(access_token=self.access_token)

    def execute(self, params):
        instrument = params['instrument']
        take_profit = params['take_profit']
        stop_loss = params['stop_loss']
        units = params['units']

        mktOrder = MarketOrderRequest(
            instrument=instrument,
            units=units,
            takeProfitOnFill=TakeProfitDetails(price=take_profit).data,
            stopLossOnFill=StopLossDetails(price=stop_loss).data)

        response = orders.OrderCreate(self.account_id, data=mktOrder.data)
        return self.client.request(response)
