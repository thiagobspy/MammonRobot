class Trade:
    def __init__(self, data, units, resistance=0, support=0):
        self.initial_date = data['date']
        self.initial_price = data['open']
        self.final_date = ''
        self.final_price = 0
        self.resistance = resistance
        self.support = support
        self.units = units

    def __str__(self):
        if self.is_open():
            log = 'Order {0} OPEN:\nStart: {1}\nInitial Price: {2}' \
                .format(self.type(), self.initial_date, self.initial_price)
        else:
            log = 'Order {0} CLOSED:\nStart: {1} - End: {2}\nInitial Price: {3} - Final Price: {4}\nProfit: {5}\n\n' \
                .format(self.type(), self.initial_date, self.final_date, self.initial_price, self.final_price,
                        self.profit())
        return log

    def type(self):
        if self.units > 0:
            return 'Buy'
        elif self.units < 0:
            return 'Sell'
        else:
            return 'Invalid'

    def is_open(self):
        return self.final_price == 0

    def close(self, data, **kwargs):
        if self.is_open():
            self.final_date = data['date']
            if 'use_price' in kwargs:
                self.final_price = data[kwargs['use_price']]
            else:
                self.final_price = data['close']
            kwargs['logger'].close(self)
            return True
        return False

    def automatic_close(self, data, **kwargs):
        if (self.resistance or self.support) and self.is_open():
            price_h = data['high']
            price_c = data['low']
            if price_h >= self.resistance:
                self.close(data, use_price='high', **kwargs)
                return True
            if price_c <= self.support:
                self.close(data, use_price='low', **kwargs)
                return True
        return False

    def prior_profit(self, price):
        return (price - self.initial_price) * self.units

    def profit(self):
        if not self.is_open():
            return (self.final_price - self.initial_price) * self.units
