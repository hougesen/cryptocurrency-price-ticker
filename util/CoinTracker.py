import requests


# Used for keeping track of currecy related data
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
            "change_30d",
            "market_cap",
            "volume_24h",
            "low_24h",
            "high_24h"
        ]
        self.current_metric_index = 0
        self.fetch_current_coin()

    # Changes the current coin
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

    # Changes the shown metric

    def change_metric(self, dir):
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

    # Fetches coin data for current page
    def fetch_current_coin(self):
        # Input your own coinlib api key here
        API_KEY = None

        if API_KEY == None:
            print("Missing coinlib api key")

        API_URL = "https://coinlib.io/api/v1/coin?key={API_KEY}&pref={comparison_currency}&symbol={coin}".format(
            API_KEY=API_KEY,
            comparison_currency=self.comparison_currency,
            coin=self.tracked_coins[self.current_page],
        )

        response = requests.get(API_URL).json()

        self.current_coin = {
            "symbol": response["symbol"],
            "name": response["name"],
            "price": int(float(response["price"])) if int(float(response["price"])) > 20 else round(float(response["price"]), 2),
            "change_1h": response["delta_1h"],
            "change_24h": response["delta_24h"],
            "change_7d": response["delta_7d"],
            "change_30d": response["delta_30d"],
            "market_cap": int(float(response["market_cap"])),
            "volume_24h": int(float(response["total_volume_24h"])),
            "low_24h": int(float(response["low_24h"])) if int(float(response["low_24h"])) > 20 else round(float(response["low_24h"]), 2),
            "high_24h": int(float(response["high_24h"])) if int(float(response["high_24h"])) > 20 else round(float(response["high_24h"]), 2)
        }

    # Returns the text used by the display
    def display_text(self):
        print(
            "Current coin:", self.current_coin["symbol"],
            "Current metric:", self.tracked_metrics[self.current_metric_index]
        )

        if self.tracked_metrics[self.current_metric_index] == "price":
            return "1 {coin_symbol}:\n{value}{currency}".format(
                coin_symbol=self.current_coin["symbol"],
                value=self.current_coin["price"],
                currency=self.comparison_currency
            ).upper()
        elif "change" in self.tracked_metrics[self.current_metric_index]:
            return "{coin_symbol} {metric}:\n{value}%".format(
                coin_symbol=self.current_coin["symbol"],
                metric=self.tracked_metrics[self.current_metric_index].replace(
                   "_", " "
                ),
                value=self.current_coin[self.tracked_metrics[self.current_metric_index]]
            ).upper()
        else:
            return "{coin_symbol} {metric}:\n{value}".format(
                coin_symbol=self.current_coin["symbol"],
                metric=self.tracked_metrics[self.current_metric_index].replace(
                   "_", " "
                ),
                value=self.current_coin[self.tracked_metrics[self.current_metric_index]]
            ).upper()
