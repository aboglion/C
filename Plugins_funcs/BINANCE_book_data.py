import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

def Binance_book_data(symbol):
    # התאמת ה-URL ל-API של Binance
    url_book = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"

    try:
        # הגדרת ניסיונות חוזרים עם backoff factor
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {"accept": "application/json"}
        response = session.get(url_book, headers=headers)

        # בדיקה אם התקבל קוד תגובה שאינו 200
        response.raise_for_status()

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
        print("Failed in Binance_book_data:", e)
        time.sleep(10)
        return None


