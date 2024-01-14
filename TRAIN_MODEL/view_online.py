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
LIFE_TIME = h*10
JSON_FILE = os.path.join(ROOT_DIR, 'collected_data',f'{os.getlogin()}_data_json.json')
STEPS = 2
long_len_range=800
medium_len_range=400
short_len_range=100
prediction_len_range=10

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
    date=time.strftime("%d.%m.%y_%H", time.localtime())
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


    buyed,UP,UP_1=False,False,False
    Action,buyed_prics,profet=0,1,0 #0 -> nothing 1-> buy  2-> sell
    date=time.strftime("%d.%m.%y_%H", time.localtime())

    
    while life_time > 0:
        if not date==time.strftime("%d.%m.%y_%H", time.localtime()) :
            if os.path.exists(f"./{symbol} {date}.cvs"):cvsChart(f"./{symbol} {date}.cvs")
            date=time.strftime("%d.%m.%y_%H", time.localtime())

        TIME=time.strftime("%H:%M:%S", time.localtime())

        #cvsChart(f"./{symbol} {date}.cvs")
        #exit(1)

        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                Prediction_price=round(analyzed_data["Prediction_price"],3)
                last_price=round(analyzed_data["Last_Price"],3)

                
              
                #----- collect data ---------------- 
                AVG_LIST_last_prices.append(last_price)

                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]
                #-----------------------data collected -v--
                    
                    Last_price_avg_short=round((sum(AVG_LIST_last_prices[-short_len_range:])/short_len_range),3)
                    Last_price_avg_medium=round((sum(AVG_LIST_last_prices[-medium_len_range:])/medium_len_range),3)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/long_len_range),3)
                    

                    if Last_price_avg_long>last_price and\
                        Last_price_avg_long>Last_price_avg_short and \
                        Last_price_avg_long>Last_price_avg_medium:
                        UP_1=True
                    elif UP_1 and (last_price>Last_price_avg_long ):
                    #                >Last_price_avg_short>Last_price_avg_medium)\
                    #      and (2*(Last_price_avg_short-Last_price_avg_medium)< (Last_price_avg_long-Last_price_avg_short)):
                        UP=True
                    else:
                        UP_1=False
                        UP=False

                    #----------#
                    #  BUYING  #
                    #----------#
                    if (not buyed )and UP  :
                                Action=1
                                buyed_prics=last_price
                                st="\n[----------------------------------------]"
                                st+= f"\n\t BUYING: {TIME} price:{last_price} \n"
                                with open(f"./{symbol} {date}.log", "+a") as logfile:
                                    logfile.write(st)

                    #-----------#
                    #  SEELING  #
                    #-----------#
                    if buyed :profet=round(((last_price-buyed_prics) / buyed_prics) * 100,3) 
                    if buyed and ( profet>0.1 and int(Last_price_avg_short-Last_price_avg_medium)==int(Last_price_avg_medium-Last_price_avg_long) \
                                or 
                                (Last_price_avg_short<Last_price_avg_long 
                                and Last_price_avg_medium<Last_price_avg_long)):
                            
                            Action=2
                            st =f"=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                            st+=f"\t#|buy:{buyed_prics}->sell:{last_price} => profet {profet}% |#"
                            st="\n[----------------------------------------]\n"
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
          

                #==== LOG IT ======#
            
                    output=f'{round(last_price,3)},{Prediction_price},{Last_price_avg_short},{Last_price_avg_medium},{Last_price_avg_long},{TIME}\n'
                    if Action:
                        if Action==1:
                            buyed=True
                            output+=f'{buyed_prics},{TIME}\n'
                        elif Action==2:
                            buyed=False
                            output+=f'{last_price},{TIME},{profet}%\n'
                        Action=0
                    with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                        logfile.write(output)

                else:
                    print("collecting data.. :",((len(AVG_LIST_last_prices)+1)/long_len_range)*100,"%")
                    
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
    cvsChart(f"./{symbol} {date}.cvs")
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()
    


