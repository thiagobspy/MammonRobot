from oandapyV20 import API
from oandapyV20.endpoints import positions

from configuration import Configuration
from utils import Utils


class Position:
    def __init__(self):
        self.access_token = Configuration.access_token
        self.account_id = Configuration.account_id
        self.client = API(access_token=self.access_token)

    def has_open_position(self):
        response = self.request()
        obj = Utils.json2obj(response)
        return len(obj.positions) != 0

    def request(self):
        open_position = positions.OpenPositions(self.account_id)
        return self.client.request(open_position)
