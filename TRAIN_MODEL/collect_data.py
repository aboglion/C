import threading
import time
import os,sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT_DIR, '..'))

# from Plugins_funcs.bitfinex_book_data import Bitfinex_book_data
from Plugins_funcs.analyze_market import Analyze_market
from Plugins_funcs.save_data_to_file import Save_data_to_file
from Plugins_funcs.html_chart import Html_chart
# from Plugins_funcs.bitfinex_book_data import Bitfinex_book_data
from Plugins_funcs.BINANCE_book_data import Binance_book_data

# SYMBOL = "tSOLUSD"import threading
import time
import os,sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT_DIR, '..'))

# from Plugins_funcs.bitfinex_book_data import Bitfinex_book_data
from Plugins_funcs.analyze_market import Analyze_market
from Plugins_funcs.save_data_to_file import Save_data_to_file
from Plugins_funcs.html_chart import Html_chart
# from Plugins_funcs.bitfinex_book_data import Bitfinex_book_data
from Plugins_funcs.BINANCE_book_data import Binance_book_data
 #"tBTCUSD"  # all=>https://api-pub.bitfinex.com/v2/tickers?symbols=ALL
# url_symbols = "https://api.binance.com/api/v3/exchangeInfo"

h=60*60
LIFE_TIME = 1*h
JSON_FILE = os.path.join(ROOT_DIR, 'collected_data',f'{os.getlogin()}_data_json.json')
STEPS = 2
top_10_binance_symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "USDTBUSD",
    "USDCUSDT",
    "SOLUSDT",
    "BUSDUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "LUNAUSDT",
]

# Semaphore for limiting the threads
# מותר 1600 בקשות ב 24 שעות אז כל התליכון 2 שניות אז מקסמום 3 ביחד אפשר להריץ
semaphore = threading.Semaphore(3)
save_data_lock = threading.Lock() #נעילת שמירת הקובץ שלא יווצר התנגשות

def Hart(symbol, life_time, STEPS, json_file):
    with semaphore:
        print(symbol, "=> start")
        records = []
        total_life = life_time
        while life_time > 0:
            with save_data_lock:
                book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                records.append(analyzed_data)
            
            time.sleep(STEPS)
            life_time -= STEPS
            print(total_life - life_time, "/", total_life, symbol, "\n", analyzed_data, "\n     -------------\n")
        
        with save_data_lock:
            Save_data_to_file(records, json_file)
        print("DONE..=>", symbol)

def main():
    while True:
        threads = []
        for SYMBOL in top_10_binance_symbols:
            thread = threading.Thread(target=Hart, args=(SYMBOL, LIFE_TIME, STEPS, JSON_FILE))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            time.sleep(1)
        # המתנה לסיום כל התהלכונים
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()

