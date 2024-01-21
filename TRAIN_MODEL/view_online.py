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
LIFE_TIME = h*8
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
    UP=False
    min_point=False

    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[0]
    STATUS="---"


    buyed,UP,UP_1=False,False,False
    Action,buyed_prics,profet=0,0,0 #0 -> nothing 1-> buy  2-> sell
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
                Prediction_up=round(analyzed_data["Prediction_up"],3)
                last_price=round(analyzed_data["Last_Price"],3)

                
              
                #----- collect data  part1---------------- 
                AVG_LIST_last_prices.append(last_price)
                AVG_LIST_Prediction.append(Prediction_up)

                if len(AVG_LIST_Prediction)>prediction_len_range:
                     del AVG_LIST_Prediction[0]
                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]
                    short=AVG_LIST_last_prices[-short_len_range:]
                    medium=AVG_LIST_last_prices[-medium_len_range:]

                    Last_price_avg_short=round((sum(short)/short_len_range),3)
                    Last_price_avg_medium=round((sum(medium)/medium_len_range),3)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/long_len_range),3)
                    Prediction_dir=True if round((sum(AVG_LIST_Prediction)/prediction_len_range),3)>0 else False
                #-------  COLLECT UP DIRCTION data part2------

                    UP=AVG_LIST_last_prices[-1]>AVG_LIST_last_prices[-2]>AVG_LIST_last_prices[-3]
                    
                    CRISIS=(Last_price_avg_long<=buyed_prics 
                            >Last_price_avg_medium>Last_price_avg_short
                            and UP)
                    if last_price < Last_price_avg_long:
                        max_price = Last_price_avg_long
                    if last_price > Last_price_avg_long:
                        min_price = Last_price_avg_long

                    if AVG_LIST_last_prices[-4] > max_price and AVG_LIST_last_prices[-4] > Last_price_avg_long and \
                    AVG_LIST_last_prices[-4] < AVG_LIST_last_prices[-3] < AVG_LIST_last_prices[-2] < AVG_LIST_last_prices[-1]:
                        max_price = AVG_LIST_last_prices[-4]
                        avg_MaxMin=round((max_price+min_price)/2,3)

                    if AVG_LIST_last_prices[-4] < min_price and AVG_LIST_last_prices[-4] < Last_price_avg_long and \
                    AVG_LIST_last_prices[-4] > AVG_LIST_last_prices[-3] > AVG_LIST_last_prices[-2] > AVG_LIST_last_prices[-1]:
                        min_price = AVG_LIST_last_prices[-4]          
                        avg_MaxMin=round((max_price+min_price)/2,3)

                    print(Prediction_dir,[AVG_LIST_last_prices[-5:]])

                    #----------#
                    #  BUYING  #
                    #----------#
                    if ((not buyed )and (not UP)and last_price <
                        Last_price_avg_short
                        <Last_price_avg_medium
                        <Last_price_avg_long
                            )and(
                        int(Last_price_avg_long-((Last_price_avg_medium+Last_price_avg_short)/2))
                        ==int(((Last_price_avg_medium+Last_price_avg_short)/2)-last_price)
                                ) :min_point=True
                    elif (
                           Last_price_avg_short>Last_price_avg_medium
                            or
                            Last_price_avg_medium>Last_price_avg_long
                        ):min_point=False


                    if (not buyed )and min_point and (
                            last_price>Last_price_avg_short):
                                Action=1
                                buyed_prics=last_price
                                st="\n[----------------------------------------]"
                                st+= f"\n\t BUYING: {TIME} price:{last_price} \n"
                                print(st)
                                with open(f"./{symbol} {date}.log", "+a") as logfile:
                                    logfile.write(st)

                    #-----------#
                    #  SEELING  #
                    #-----------#                            round(((last_price-buyed_prics) / buyed_prics) * 100,3)<0.01  and int(Last_price_avg_short-Last_price_avg_medium)==int(Last_price_avg_medium-Last_price_avg_long) \

                    if buyed :profet=round(((last_price-buyed_prics) / buyed_prics if buyed_prics>0 else 1) * 100,3) 
                    if buyed and profet>0.11\
                        and (last_price
                                > Last_price_avg_short
                                >Last_price_avg_medium
                                )and(
                                    int(last_price-Last_price_avg_short)
                                    ==int(Last_price_avg_short-Last_price_avg_medium))\
                                or (buyed and CRISIS):
                            Action=2
                            st =f"=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                            st+=f"\t{'CRISIS' if CRISIS  else'#'}Prediction_dir: {Prediction_dir}|buy:{buyed_prics}->sell:{last_price} => profet {profet}% |#"
                            st+="\n[----------------------------------------]\n"
                            print(st)
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
        

                #==== LOG IT ======#
            
                    output=f'{round(last_price,3)},{avg_MaxMin},{Last_price_avg_short},{Last_price_avg_medium},{Last_price_avg_long},{TIME}\n'
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

                #======DATA NOT COLLECTED YET ====xxx
                else:
                    Data_collection_progress=((len(AVG_LIST_last_prices)+1)/long_len_range)*100
                    if Data_collection_progress<=100:print("collecting data.. :",((len(AVG_LIST_last_prices)+1)/long_len_range)*100,"%")
                    else:print("DONE collection data. NOW IT'S START ..")
                    max_price,min_price,avg_MaxMin = last_price,last_price,last_price
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
    cvsChart(f"./{symbol} {date}.cvs")
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()
    


