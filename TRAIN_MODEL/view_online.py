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
SP_len_AVG_LIST=500 #500

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
    AVG_LIST_Prediction=[]
    AVG_LIST_last_prices=[]
    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[0]
    STATUS="---"
    while life_time > 0:
        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                Prediction_price=analyzed_data["Prediction_price"]
                last_price=analyzed_data["Last_Price"]
                TIME=time.strftime("%H:%M:%S %d.%m.%y", time.localtime())
                date=TIME[9:]
                TIME=TIME[:9]

                
                Len__AVG_LIST_Prediction=len(AVG_LIST_Prediction)
                Len__AVG_LIST_last_prices=len(AVG_LIST_last_prices)
                
                # if Len__AVG_LIST_Prediction>0:
                #     old_av=sum(AVG_LIST_Prediction)/Len__AVG_LIST_Prediction
                AVG_LIST_Prediction.append(Prediction_price)
                AVG_LIST_last_prices.append(last_price)

                if Len__AVG_LIST_Prediction>SP_len_AVG_LIST:
                    del AVG_LIST_Prediction[0]
                    del AVG_LIST_last_prices[0]

                    Prediction_avg_now=int(sum(AVG_LIST_Prediction)/Len__AVG_LIST_Prediction)
                    Last_price_avg_now=int(sum(AVG_LIST_last_prices)/Len__AVG_LIST_Prediction)
                    p=int(((3*Prediction_price)+Last_price_avg_now+Prediction_avg_now)/4)
                    if last_price>p:STATUS="UP"
                    elif last_price<p:STATUS="DOWN"
                    else:STATUS="natural"
                     
                    output=f'{STATUS:8},{int(last_price)} ,{p},{Last_price_avg_now},{Prediction_avg_now} , {TIME}\n'
                    with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                        logfile.write(output)

                else:
                    print("collecting data.. :",((Len__AVG_LIST_Prediction+1)/SP_len_AVG_LIST)*100,"%")
                    
                     
                    # if new_av>old_av :
                    # new_av=
                    #     STATUS="UP"
                    # else : 
                    #     STATUS="DOWN"
                    # output=f'{STATUS},{last_price} ,{Prediction_price},{new_av} , {TIME}\n'
                    # print(str((life_time/LIFE_TIME)*100) + "\n" + output + "-"*20)
                    # with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                    #     logfile.write(output)
    
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()


