import requests


def fetch_data(coin, comparison_currency):
    # Input your own coinlib api key here
    API_KEY = "12456789"

    API_URL = "https://coinlib.io/api/v1/coin?key={API_KEY}&pref={comparison_currency}&symbol={coin}".format(
        API_KEY=API_KEY, comparison_currency=comparison_currency, coin=coin
    )

    response = requests.get(API_URL).json()

    filtered_data = {
        "comparison": response["symbol"] + " to " + comparison_currency,
        "symbol": response["symbol"],
        "name": response["name"],
        "price": int(response["price"]) + comparison_currency,
        "change_1h": response["delta_1h"] + "%",
        "change_24h": response["delta_24h"] + "%",
        "change_7d": response["delta_7d"] + "%",
        "change_30d": response["delta_30d"] + "%"
    }

    return filtered_data
