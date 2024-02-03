import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import logging

# הגדרת ה-logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def Binance_book_data(symbol):
    # התאמת ה-URL ל-API של Binance
    url_book = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"

    # ניסיון חוזר דינמי
    retries = Retry(total=10, backoff_factor=2, status_forcelist=[500, 502, 503, 504], method_whitelist=frozenset(['GET', 'POST']))
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {"accept": "application/json"}

    try:
        response = session.get(url_book, headers=headers)
        response.raise_for_status()  # זורק שגיאה אם התקבל קוד שגיאה

        re_data = response.json()
        bids_book = []
        asks_book = []

        # לולאות להמרת הנתונים
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

