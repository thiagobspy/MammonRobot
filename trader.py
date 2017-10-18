from order import CreateOrder
from pricing import Pricing


class Buy:
    def __init__(self):
        self.pricing = Pricing()
        self.create_order = CreateOrder()

    def execute(self, params):
        instrument = params['instrument']
        take_profit_percentage = params['take_profit']
        stop_loss_percentage = params['stop_loss']

        bid, ask = self.pricing.get_prices(instrument)

        params_create_order = {}
        params_create_order['instrument'] = instrument
        params_create_order['take_profit'] = ask * (1 + take_profit_percentage)
        params_create_order['stop_loss'] = ask * (1 - stop_loss_percentage)
        params_create_order['units'] = 1

        return self.create_order.execute(params_create_order)


class Sell:
    def __init__(self):
        self.pricing = Pricing()
        self.create_order = CreateOrder()

    def execute(self, params):
        instrument = params['instrument']
        take_profit_percentage = params['take_profit']
        stop_loss_percentage = params['stop_loss']

        bid, ask = self.pricing.get_prices(instrument)

        params_create_order = {}
        params_create_order['instrument'] = instrument
        params_create_order['take_profit'] = bid * (1 - take_profit_percentage)
        params_create_order['stop_loss'] = bid * (1 + stop_loss_percentage)
        params_create_order['units'] = -1

        return self.create_order.execute(params_create_order)
