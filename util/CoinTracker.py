from util.fetch_data import fetch_data


class CoinTracker:
    def __init__(self, coins, comparison_currencies):
        self.tracked_coins = coins
        self.comparison_currencies = comparison_currencies
        self.current_page = 0
        self.current_coin = {}
        self.fetch_current_coin()

    def switch_page(self, dir):
        if(dir == "forward"):
            self.current_page += 1
            if(self.current_page >= len(self.tracked_coins)):
                self.current_page = 0
        else:
            self.current_page -= 1
            if(self.current_page < 0):
                self.current_page = len(self.tracked_coins) - 1

        self.fetch_current_coin()

    def fetch_current_coin(self):
        self.current_coin = fetch_data(
            self.tracked_coins[self.current_page], self.comparison_currencies[0]
        )
