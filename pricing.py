from oandapyV20 import API
from oandapyV20.endpoints import pricing

from configuration import Configuration
from utils import Utils


class Pricing:
    def __init__(self):
        self.access_token = Configuration.access_token
        self.account_id = Configuration.account_id
        self.client = API(access_token=self.access_token)

    def get_prices(self, instrument):
        response = self.request(instrument)
        obj = Utils.json2obj(response)
        bid = obj.prices[0].bids[0].price
        ask = obj.prices[0].asks[0].price
        return (float(bid), float(ask))

    def request(self, instrument):
        params = {'instruments': instrument}
        pricingInfo = pricing.PricingInfo(self.account_id, params=params)
        return self.client.request(pricingInfo)
