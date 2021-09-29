from util.fetch_data import fetch_data


class CoinTracker:
    def __init__(self, coins, comparison_currency):
        self.tracked_coins = coins
        self.comparison_currency = comparison_currency
        self.current_page = 0
        self.current_coin = {}
        self.tracked_metrics = [
            "price",
            "change_1h",
            "change_24h",
            "change_7d",
            "change_30d"
        ]
        self.current_metric_index = 0
        self.fetch_current_coin()

    def change_page(self, dir):
        if dir == "forward":
            self.current_page += 1
            if(self.current_page >= len(self.tracked_coins)):
                self.current_page = 0
        elif dir == "home":
            self.current_page = 0
        else:
            self.current_page -= 1
            if(self.current_page < 0):
                self.current_page = len(self.tracked_coins) - 1

        self.fetch_current_coin()
        print(self.current_page, self.current_coin)

    # Change the shown metric
    def change_metric(self, dir):
        print(dir)
        if dir == "forward":
            self.current_metric_index += 1
            if(self.current_metric_index >= len(self.tracked_metrics)):
                self.current_metric_index = 0
        elif dir == "home":
            self.current_metric_index = 0
        else:
            self.current_metric_index -= 1
            if(self.current_metric_index < 0):
                self.current_metric_index = len(self.tracked_metrics) - 1

    def fetch_current_coin(self):
        self.current_coin = fetch_data(
            self.tracked_coins[self.current_page],
            self.comparison_currency
        )

    def display_text(self):
        return """
        {coin_symbol} - {metric}
        {value}
        """.format(
            coin_symbol=self.current_coin["symbol"],
            metric=self.tracked_metrics[self.current_metric_index],
            value=self.current_coin[self.tracked_metrics[self.current_metric_index]]
        )
