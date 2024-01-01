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

# SYMBOL = "tSOLUSD" #"tBTCUSD"  # all=>https://api-pub.bitfinex.com/v2/tickers?symbols=ALL
# url_symbols = "https://api.binance.com/api/v3/exchangeInfo"

h=60*60
LIFE_TIME = h*5
JSON_FILE = os.path.join(ROOT_DIR, 'collected_data',f'{os.getlogin()}_data_json.json')
STEPS = 2
SP_len_AVG_LIST_POWERS=10 #500

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


def main():
    AVG_LIST_POWERS=[]
    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[0]
    STATUS="---"
    while life_time > 0:
        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                power_price=analyzed_data["power_price"]
                last_price=analyzed_data["Last_Price"]
                PV_len_AVG_LIST_POWERS=len(AVG_LIST_POWERS)
                TIME=time.strftime("%H:%M:%S %d.%m.%y", time.localtime())
                date=TIME[9:]
                TIME=TIME[:9]

                
                if PV_len_AVG_LIST_POWERS>0:old_av=sum(AVG_LIST_POWERS)/PV_len_AVG_LIST_POWERS
                AVG_LIST_POWERS.append(analyzed_data["power_price"])

                if PV_len_AVG_LIST_POWERS>=SP_len_AVG_LIST_POWERS:
                    AVG_LIST_POWERS.pop(0) 
                    new_av=sum(AVG_LIST_POWERS)/PV_len_AVG_LIST_POWERS
                    if new_av>old_av :
                        STATUS="UP"
                    else : 
                        STATUS="DOWN"
                    output=f'{STATUS},{last_price} ,{analyzed_data["power_price"]},{new_av} , {TIME}\n'
                    print(str((life_time/LIFE_TIME)*100) + "\n" + output + "-"*20)
                    with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                        logfile.write(output)
    
                else:print("collecting data.. :",(PV_len_AVG_LIST_POWERS/SP_len_AVG_LIST_POWERS)*100,"%")
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()


