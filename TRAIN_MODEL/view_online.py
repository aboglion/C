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
prediction_len_range=5 
direction_LenPart=12

if long_len_range<24:
     print("exit long_len_range must be > 4 for UP len")
     exit(1)

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
    UP_medium_list=[]
    UP_short_list=[]
    UP_collected=False

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

                
              
                #----- collect data  part1---------------- 
                AVG_LIST_last_prices.append(last_price)
                AVG_LIST_Prediction.append(Prediction_price)

                if len(AVG_LIST_Prediction)>prediction_len_range:
                    del AVG_LIST_Prediction[0]
                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]
                    short=AVG_LIST_last_prices[-short_len_range:]
                    medium=AVG_LIST_last_prices[-medium_len_range:]

                    Last_price_avg_short=round((sum(short)/short_len_range),3)
                    Last_price_avg_medium=round((sum(medium)/medium_len_range),3)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/long_len_range),3)
                    # Prediction_AVG=round((sum(AVG_LIST_Prediction)/prediction_len_range),3)
                #-------  COLLECT UP DIRCTION data part2------
                    UP_medium_list.append(Last_price_avg_medium)
                    UP_short_list.append(Last_price_avg_short)
                    if len(UP_medium_list)>(direction_LenPart*2):
                        UP_collected=True
                #-----------==STARTED=----------------------------
                    if UP_collected:
                        # price -> 24 =>[12,12]
                        price_PART1_avg=round((sum(AVG_LIST_last_prices[-(direction_LenPart*2):-direction_LenPart]) / direction_LenPart),3)
                        price_PART2_avg=round((sum(AVG_LIST_last_prices[-direction_LenPart:]) / direction_LenPart),3)
                        #  short 24 =>[12,12]
                        UP_short_list=UP_short_list[-(direction_LenPart*2):]
                        short_PART1_avg=round((sum(UP_short_list[:direction_LenPart]) / direction_LenPart),3)
                        short_PART2_avg=round((sum(UP_short_list[direction_LenPart:]) / direction_LenPart),3)
                        #medium->  30 =>[15,15]
                        UP_medium_list=UP_medium_list[-(direction_LenPart*2):]
                        medium_PART1_avg=round((sum(UP_medium_list[:direction_LenPart]) / direction_LenPart),3)
                        medium_PART2_avg=round((sum(UP_medium_list[direction_LenPart:]) / direction_LenPart),3)

                        UP_price=price_PART2_avg>price_PART1_avg
                        UP_short=short_PART2_avg>short_PART1_avg
                        UP_medium=medium_PART2_avg>medium_PART1_avg
                        CRISIS=(Last_price_avg_short<Last_price_avg_medium 
                                and Last_price_avg_medium<Last_price_avg_long
                                and last_price<Last_price_avg_short)

                        #----------#
                        #  BUYING  #
                        #----------#
                        if (not buyed )and UP_price and UP_short and UP_medium and (
                            last_price>Last_price_avg_short
                            and last_price<Last_price_avg_long ):
                                    Action=1
                                    buyed_prics=last_price
                                    st="\n[----------------------------------------]"
                                    st+=f"\n price_PART2:{price_PART2_avg} > price_PART1:{price_PART1_avg}=>{UP_price} "
                                    st+=f"\n short_PART2:{short_PART2_avg} > short_PART1:{short_PART1_avg}=>{UP_short} "
                                    st+=f"\n medium_PART2:{medium_PART2_avg} > medium_PART1:{medium_PART1_avg}=>{UP_medium} "
                                    st+= f"\n\t BUYING: {TIME} price:{last_price} \n"
                                    with open(f"./{symbol} {date}.log", "+a") as logfile:
                                        logfile.write(st)

                        #-----------#
                        #  SEELING  #
                        #-----------#
                        if buyed :profet=round(((last_price-buyed_prics) / buyed_prics) * 100,3) 
                        if buyed and not UP_price and not UP_short and profet>0.1\
                            and int(Last_price_avg_short-Last_price_avg_medium)==int(Last_price_avg_medium-Last_price_avg_long) \
                        or (buyed and CRISIS):
                                
                                Action=2
                                st =f"=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                                st+=f"\t{'CRISIS' if CRISIS else'#'}|buy:{buyed_prics}->sell:{last_price} => profet {profet}% |#"
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

                #======DATA NOT COLLECTED YET ====xxx
                    else:
                        print("collect data for UP dirctions",(len(UP_medium_list)/(direction_LenPart*2))*100,"%")
                else:
                    Data_collection_progress=((len(AVG_LIST_last_prices)+1)/long_len_range)*100
                    if Data_collection_progress<=100:print("collecting data.. :",((len(AVG_LIST_last_prices)+1)/long_len_range)*100,"%")
                    else:print("DONE collection data. NOW IT'S START ..")
                
                time.sleep(STEPS)
                life_time -= STEPS
        except KeyboardInterrupt:
            life_time = 0
    cvsChart(f"./{symbol} {date}.cvs")
        
    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    main()
    


