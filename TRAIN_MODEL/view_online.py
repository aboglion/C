import threading
import time
import os,sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, '..'))
from Plugins_funcs.telgram_ import *
from Plugins_funcs.analyze_market import Analyze_market
from Plugins_funcs.cvsChart import cvsChart,clean_files,Day_chart
from Plugins_funcs.BINANCE_book_data import Binance_book_data
from Plugins_funcs import one_pass
env=one_pass.env()

# SYMBOL = "tSOLUSD" #"tBTCUSD"  # all=>https://api-pub.bitfinex.com/v2/tickers?symbols=ALL
# url_symbols = "https://api.binance.com/api/v3/exchangeInfo"



m=60
h=m*60
LIFE_TIME = h*75
STEPS = 2
long_len_range=45*m
medium_len_range=15*m
short_len_range=5*m
# prediction_len_range=20

# long_len_range=4
# medium_len_range=2
# short_len_range=1


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

    # AVG_LIST_Prediction=[]
    AVG_LIST_last_prices=[]

    TOTAL_PROFET=0
    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[0]
    STATUS="---"
    fee_buy=1.001
    fee_sell=-1.001


    (buyed,UP,UNDER_MaxMin,medium_underLong,short_UNDER_med,price_UNDER_short)=(
        False,False,False,False,False,False )
    Action,buyed_prics,profet=0,0,0 #0 -> nothing 1-> buy  2-> sell
    date=time.strftime("%d.%m.%y_%H", time.localtime())

    
    while life_time > 0:
        if not date==time.strftime("%d.%m.%y_%H", time.localtime()) :
            if os.path.exists(f"./{symbol} {date}.cvs"):
                    Name_chart=cvsChart(f"./{symbol} {date}.cvs")
                    send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],date,Name_chart)

            date=time.strftime("%d.%m.%y_%H", time.localtime())

        TIME=time.strftime("%H:%M:%S", time.localtime())

        #cvsChart(f"./{symbol} {date}.cvs")
        #exit(1)

        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                # Prediction_up=round(analyzed_data["Prediction_up"],3)
                last_price=round(analyzed_data["Last_Price"],3)

                
              
                #----- collect data  part1---------------- 
                AVG_LIST_last_prices.append(last_price)
                # if not(Prediction_up==0):AVG_LIST_Prediction.append(Prediction_up)

                # if len(AVG_LIST_Prediction)>prediction_len_range:
                #      del AVG_LIST_Prediction[0]
                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]
                    short=AVG_LIST_last_prices[-short_len_range:]
                    medium=AVG_LIST_last_prices[-medium_len_range:]

                    Last_price_avg_short=round((sum(short)/short_len_range),3)
                    Last_price_avg_medium=round((sum(medium)/medium_len_range),3)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/long_len_range),3)
                    # Prediction_dir=True if round((sum(AVG_LIST_Prediction)/prediction_len_range),3)>0 else False
                #-------  

                    UP=AVG_LIST_last_prices[-1]>AVG_LIST_last_prices[-2]>AVG_LIST_last_prices[-3]
                    
                    CRISIS=(avg_MaxMin>
                            Last_price_avg_long> 
                            Last_price_avg_medium>
                            Last_price_avg_short>
                            last_price)
                #------
                    #RESET MAX MIN
                    #if (not medium_underLong) and Last_price_avg_medium  < Last_price_avg_long:
                    #    max_price ,avg_MaxMin,min_price= Last_price_avg_long,Last_price_avg_long,Last_price_avg_long
                    #    medium_underLong=True
                    #if medium_underLong and Last_price_avg_medium > Last_price_avg_long:
                    #    min_price ,avg_MaxMin,max_price= Last_price_avg_long,Last_price_avg_long,Last_price_avg_long
                    #   medium_underLong=False
                    #MAX_MIN
                    if AVG_LIST_last_prices[-4] > max_price and\
                    AVG_LIST_last_prices[-4] < AVG_LIST_last_prices[-3] < AVG_LIST_last_prices[-2] < AVG_LIST_last_prices[-1]:
                        max_price = AVG_LIST_last_prices[-4]
                        avg_MaxMin=round((max_price+min_price)/2,3)
                    if AVG_LIST_last_prices[-4] < min_price and \
                    AVG_LIST_last_prices[-4] > AVG_LIST_last_prices[-3] > AVG_LIST_last_prices[-2] > AVG_LIST_last_prices[-1]:
                        min_price = AVG_LIST_last_prices[-4]          
                        avg_MaxMin=round((max_price+min_price)/2,3)
                #--------
                    # print(Prediction_dir,[AVG_LIST_last_prices[-5:]])

                    #----------#
                    #  BUYING  #
                    #----------#
                    # if (not buyed )and UNDER_MaxMin and (
                    #         Last_price_avg_long>last_price>=avg_MaxMin>Last_price_avg_short) \
                    #     and Last_price_avg_medium < Last_price_avg_long :
                        # and Last_price_avg_medium < avg_MaxMin:
                    if False and (not buyed )and Max_OnTop and (
                        last_price>Last_price_avg_short>Last_price_avg_medium and\
                        avg_MaxMin>Last_price_avg_short and \
                        Last_price_avg_long>Last_price_avg_short):
                            Action=1
                            buyed_prics=last_price*fee_buy
                            st="\n[----------------------------------------]"
                            st+= f"\n\t BUYING: {TIME} price:{last_price}\n"
                            print(st)
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
                            send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],st)

                    short_UNDER_med=Last_price_avg_medium>Last_price_avg_short
                    price_UNDER_short=last_price<Last_price_avg_short
                    UNDER_MaxMin=last_price<avg_MaxMin #its shuld be true before main cinditions checks
                    Max_OnTop=avg_MaxMin>Last_price_avg_long>Last_price_avg_medium>Last_price_avg_short
                    #-----------#
                    #  SEELING  #
                    #-----------
                    if buyed :profet=round((((last_price*fee_sell)-buyed_prics) / buyed_prics if buyed_prics>0 else 1) * 100,3) 
                    if False and buyed and profet>0.1\
                        and (last_price 
                                > Last_price_avg_short>avg_MaxMin
                                >Last_price_avg_medium
                                )and(
                                    int(last_price-Last_price_avg_short)
                                    >int(Last_price_avg_medium-Last_price_avg_long))\
                                or False and (buyed and CRISIS):
                            Action=2
                            st =f"=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                            st+=f"\t{'CRISIS ! ' if CRISIS  else'# selling'}\n|buy:{buyed_prics}->sell:{last_price} => profet {profet}% |#"
                            st+="\n[----------------------------------------]\n"
                            print(st)
                            TOTAL_PROFET += profet
                            print("\tTOTAL_PROFET: ",TOTAL_PROFET,"\n=-=-=-=-=-=-=-=-=-=-=-\n")
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
                            send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],st,cvsChart(f"./{symbol} {date}.cvs"))


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
    if os.path(f"./{symbol} {date}.cvs") :
        Name_chart=cvsChart(f"./{symbol} {date}.cvs")
        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS",Name_chart)
    else:send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS - NOfile ")


    # with open("./logfile.log", "+a") as logfile:
    #     logfile.write(output)


if __name__ == "__main__":
    try:
        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"strting ..")
        main()
    except Exception as e:
        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],str(e))

    


