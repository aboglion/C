import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import logging

# Setting up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def Binance_book_data(symbol):
    # Adjusting the URL for the Binance API
    url_book = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"

    # Dynamic retry strategy
    retries = Retry(total=10, backoff_factor=2, status_forcelist=[500, 502, 503, 504], allowed_methods=frozenset(['GET', 'POST']))
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {"accept": "application/json"}

    try:
        response = session.get(url_book, headers=headers)
        response.raise_for_status()  # Throws an error if an error code was received

        re_data = response.json()
        bids_book = []
        asks_book = []

        # Loops for converting the data
        for bid in re_data['bids']:
            bids_book.append({
                "PRICE": float(bid[0]),
                "COUNT": 1,
                "AMOUNT": float(bid[1])
            })

        for ask in re_data['asks']:
            asks_book.append({
                "PRICE": float(ask[0]),
                "COUNT": 1,
                "AMOUNT": float(ask[1])
            })

        return [bids_book, asks_book]
    except requests.exceptions.RequestException as e:
        logging.error("Failed in Binance_book_data: %s", e)
        return None
