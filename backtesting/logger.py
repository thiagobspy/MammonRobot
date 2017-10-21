class Logger:
    def final(self, trades):
        pass

    def close(self, trade):
        pass


class GeneralStatistics(Logger):
    def final(self, trades):
        win = 0
        loser = 0
        all = 0
        profit = 0
        for trade in trades:
            all += 1
            p = trade.profit()

            if p > 0:
                win += 1
            else:
                loser += 1

            profit += p

        logger = 'Total trader: {0}\nWin: {1}\nLoser: {2}\nFinal Profit: {3}\n\n'.format(all, win, loser, profit)
        print(logger)

    def close(self, trade):
        print(trade)
