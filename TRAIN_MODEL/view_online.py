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
LIFE_TIME = h*4
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




def check_contenuation(last_time,counter,buyed,symbol,times=20):
    date=time.strftime("%d.%m.%y", time.localtime())
    timeing=time.strftime("%H:%M:%S %d.%m.%y", time.localtime())

    if int(time.time())-last_time<=6:
        counter+=1
        st=f'\n{"BUYING" if not buyed else "SELL"}:[0k] {timeing} | CONUTER:{counter} time_diff =>{int(int(time.time())-last_time)}'
        with open(f"./{symbol} {date}.log", "+a") as logfile:
            logfile.write(st)
    else: 
        counter=0
        st=f'\n{"BUYING" if not buyed else "SELL"}:[X] {timeing} | CONUTER:{counter} time_diff =>{int(int(time.time())-last_time)}'
        with open(f"./{symbol} {date}.log", "+a") as logfile:
            logfile.write(st)

    last_time=int(time.time())

    if counter>times:
        counter=0
        return True,last_time,counter
    else: return False,last_time,counter


                            



def main():


    AVG_LIST_Prediction=[]
    AVG_LIST_last_prices=[]
    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[0]
    STATUS="---"


    counter=0
    last_time=time.time()  
    res_contenuation=False  
    buyed=False

    while life_time > 0:
        TIME=time.strftime("%H:%M:%S %d.%m.%y", time.localtime())
        date=TIME[9:]
        TIME=TIME[:9]

        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                Prediction_price=analyzed_data["Prediction_price"]
                last_price=round(analyzed_data["Last_Price"],3)

                
              
                Len__AVG_LIST_last_prices=len(AVG_LIST_last_prices)
                
                AVG_LIST_Prediction.append(Prediction_price)
                AVG_LIST_last_prices.append(last_price)
                Action=0  #0 -> nothing 1-> buy  2-> sell
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
                    if not buyed and\
                        last_price>Last_price_avg_long and \
                        last_price>Last_price_avg_now and \
                        last_price>Prediction_avg_now and\
                        (Prediction_avg_now-Last_price_avg_long) > 2.5*(last_price-Prediction_avg_now):
                            res_contenuation,last_time,counter=check_contenuation(last_time,counter,buyed,symbol,5)
                            if res_contenuation :
                                buyed=True
                                Action=1
                                buyed_prics=last_price
                                st= f"\n{buyed} BUYING: {TIME} price:{last_price} \n\t#{Last_price_avg_long}#{last_price}#{Prediction_avg_now}#{Last_price_avg_now} \n\t{(Last_price_avg_long-last_price)} > {(last_price-Prediction_avg_now)}\n\t------------------------------\n"
                                with open(f"./{symbol} {date}.log", "+a") as logfile:
                                    logfile.write(st)

                            

                    #-----------#
                    #  SEELING  #
                    #-----------#
                    if buyed and \
                    last_price<Last_price_avg_long and \
                    last_price<Last_price_avg_now and \
                    last_price<Prediction_avg_now and\
                    (Last_price_avg_long-Prediction_avg_now) > (Prediction_avg_now-last_price):
                        #and ((last_price - buyed_prics) / buyed_prics) * 100>0.1:
                        res_contenuation,last_time,counter=check_contenuation(last_time,counter,buyed,symbol,6)
                        
                        if res_contenuation:
                            buyed=False
                            Action=2
                            profet=round(((last_price-buyed_prics) / buyed_prics) * 100,4)
                            st =f"\n=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                            st+=f"\t#| PROF=>{last_price} - {buyed_prics}=> {((last_price-buyed_prics) / buyed_prics) * 100}% |#\n"
                            st+= (f"\t#{last_price}#{Last_price_avg_now}#{Prediction_avg_now}#{Last_price_avg_long} \n\t------------------------------\n\n")
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
                        else :
                            print ("\t#",TIME,last_price)



                    output=f'{round(last_price,3)},{Last_price_avg_now},{Prediction_avg_now},{Last_price_avg_long} ,{TIME}\n'
                    if Action:
                        output+=f'{buyed_prics},{TIME}\n' if Action==1 else f'{buyed_prics},{TIME},{profet}%\n'
                        Action=0
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
    


