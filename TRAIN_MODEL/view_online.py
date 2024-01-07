import threading
import time
import os,sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, '..'))

from Plugins_funcs.analyze_market import Analyze_market
from Plugins_funcs.cvsChart import cvsChart
from Plugins_funcs.BINANCE_book_data import Binance_book_data

# SYMBOL = "tSOLUSD" #"tBTCUSD"  # all=>https://api-pub.bitfinex.com/v2/tickers?symbols=ALL
# url_symbols = "https://api.binance.com/api/v3/exchangeInfo"

h=60*60
LIFE_TIME = h
JSON_FILE = os.path.join(ROOT_DIR, 'collected_data',f'{os.getlogin()}_data_json.json')
STEPS = 2
long_len_range=100
short_len_range=20

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


    buyed=False
    buycTime_counter,buyc_counter=0,0
    while life_time > 0:
        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                Prediction_price=analyzed_data["Prediction_price"]
                last_price=round(analyzed_data["Last_Price"],3)
                TIME=time.strftime("%H:%M:%S %d.%m.%y", time.localtime())
                date=TIME[9:]
                TIME=TIME[:9]
                

                #cvsChart(f"./{symbol} {date}.cvs")
                #exit(1)
                
                Len__AVG_LIST_last_prices=len(AVG_LIST_last_prices)
                
                AVG_LIST_Prediction.append(Prediction_price)
                AVG_LIST_last_prices.append(last_price)

                if len(AVG_LIST_Prediction)>short_len_range:
                    del AVG_LIST_Prediction[0]
                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]

                    Prediction_avg_now=round((sum(AVG_LIST_Prediction[-short_len_range:])/short_len_range),3)
                    Last_price_avg_now=round((sum(AVG_LIST_last_prices[-short_len_range:])/short_len_range),3)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/Len__AVG_LIST_last_prices),3)
                    #----------#
                    #  BUYING  #
                    #----------#
                    if  Last_price_avg_long>last_price>Prediction_avg_now>Last_price_avg_now and\
                        (Last_price_avg_long-last_price) > (last_price-Prediction_avg_now):
                        if buycTime_counter==0:
                            buycTime_counter=int(time.time())
                            #רצוף מתחת ל 5 שניות יש אותו  שלוש פעמים 
                        if int(time.time())-buycTime_counter<=5:
                            buyc_counter+=1
                        else:
                            buyc_counter=0
                            print("buycTime_counter")
                        buycTime_counter=int(time.time())

                        if buyc_counter>=3 and not buyed:
                            buyed=True
                            buyed_prics=last_price
                            st= (f"{buyed}{buycTime_counter}@{buycTime_counter} BUYING: {TIME} price:{last_price} \n\t#{Last_price_avg_long}#{last_price}#{Prediction_avg_now}#{Last_price_avg_now} \n\t{(Last_price_avg_long-last_price)} > {(last_price-Prediction_avg_now)}\n\t------------------------------\n")
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)

                    #-----------#
                    #  SEELING  #
                    #-----------#
                    if buyed and last_price>Last_price_avg_now>Prediction_avg_now>Last_price_avg_long \
                        ((buyed_prics - last_price) / last_price) * 100>0.1:
                        buyed=False
                        st =f"\n=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                        st+=f"\t#| PROF=> {buyed_prics}-{last_price} => {((buyed_prics - last_price) / last_price) * 100}% |#\n"
                        st+= (f"\t#{last_price}#{Last_price_avg_now}#{Prediction_avg_now}#{Last_price_avg_long} \n\t------------------------------\n\n")
                        with open(f"./{symbol} {date}.log", "+a") as logfile:
                            logfile.write(st)
                    else :
                        print ("\t#",TIME,last_price)



                    output=f'{round(last_price,3)},{Last_price_avg_now},{Prediction_avg_now},{Last_price_avg_long} ,{TIME}\n'
                    with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                        logfile.write(output)

                else:
                    print("collecting data.. :",((Len__AVG_LIST_last_prices+1)/long_len_range)*100,"%")
                    
                    
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
    cvsChart(f"./{symbol} {date}.cvs")
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()
    


