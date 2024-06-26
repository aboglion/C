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


dot_point_round=4
m=60
h=m*60
LIFE_TIME = h*999
STEPS = 2
# long_len_range=45*m
# medium_len_range=17*m
# short_len_range=10*m
# prediction_len_range=20*m

long_len_range=60*m
medium_len_range=25*m
short_len_range=10*m
prediction_len_range=15*m


report_hours_steps=1.15



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
    "DOTUSDT"
]




def main():

    AVG_LIST_Prediction=[]
    AVG_LIST_last_prices=[]

    TOTAL_PROFET=0
    life_time = LIFE_TIME
    symbol=top_10_binance_symbols[7]
    STATUS="---"
    fee_buy=1.001
    fee_sell=0.009

    buyed_time=0
    buyed=False 
    Action,buyed_prics,profet=0,0,0 #0 -> nothing 1-> buy  2-> sell
    date=time.strftime("%d.%m.%y", time.localtime())
    time_start=time.localtime()
    
    while life_time > 0:
        try:
            book_data = Binance_book_data(symbol)
            if book_data:
                analyzed_data = Analyze_market(book_data)
                Prediction_up=round(analyzed_data["Prediction_up"],dot_point_round)
                last_price=round(analyzed_data["Last_Price"],dot_point_round)

                
              
                #----- collect data  part1---------------- 
                AVG_LIST_last_prices.append(last_price)
                AVG_LIST_Prediction.append(Prediction_up)

                if len(AVG_LIST_Prediction)>prediction_len_range:
                    del AVG_LIST_Prediction[0]
                if len(AVG_LIST_last_prices)>long_len_range:
                    del AVG_LIST_last_prices[0]
                    short=AVG_LIST_last_prices[-short_len_range:]
                    medium=AVG_LIST_last_prices[-medium_len_range:]

                    Last_price_avg_short=round((sum(short)/short_len_range),dot_point_round)
                    Last_price_avg_medium=round((sum(medium)/medium_len_range),dot_point_round)
                    Last_price_avg_long=round((sum(AVG_LIST_last_prices)/long_len_range),dot_point_round)
                    prediction_p=round((sum(AVG_LIST_Prediction)/prediction_len_range),dot_point_round)
                #-------  

                    UP=AVG_LIST_last_prices[-1]>AVG_LIST_last_prices[-2]>AVG_LIST_last_prices[-3]
                    loop_time= time.localtime()
                    TIME=time.strftime("%H:%M:%S",loop_time)


                    CRISIS=False#(avg_MaxMin>
                    #         Last_price_avg_long> 
                    #         Last_price_avg_medium>
                    #         Last_price_avg_short>
                    #         last_price)
         
                    if AVG_LIST_last_prices[-4] > max_price and\
                        AVG_LIST_last_prices[-4] < AVG_LIST_last_prices[-3] and  AVG_LIST_last_prices[-2] > AVG_LIST_last_prices[-1]:
                                max_price = AVG_LIST_last_prices[-4]
                                avg_MaxMin=round((max_price+min_price)/2,dot_point_round)
                    if AVG_LIST_last_prices[-4] < min_price and \
                        AVG_LIST_last_prices[-4] > AVG_LIST_last_prices[-3] and AVG_LIST_last_prices[-2] < AVG_LIST_last_prices[-1]:
                                min_price = AVG_LIST_last_prices[-4]          
                                avg_MaxMin=round((max_price+min_price)/2,dot_point_round)
     
                    #----------#
                    #  BUYING  #
                    #----------#
                    dif_max_long=avg_MaxMin-Last_price_avg_long
                    dif_long_mid=Last_price_avg_long-Last_price_avg_medium
                    dif_mid_short=Last_price_avg_medium-Last_price_avg_short
                    dif_short_prics=Last_price_avg_short-last_price
                    raising=dif_max_long>4*dif_long_mid>2*dif_mid_short>dif_short_prics>=0 
                    if (not buyed ) and raising:
                        Action=1
                        buyed_prics=last_price*fee_buy
                        st="\n[----------------------------------------]"
                        st+= f"\n\t BUYING: {TIME} price:{last_price}\n"
                        print(st)
                        with open(f"./{symbol} {date}.log", "+a") as logfile:
                            logfile.write(st)
                        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],st)

                    if last_price>Last_price_avg_short:dif_eq=False

                    #-----------#
                    #  SEELING  #
                    #-----------# profet>0.1\
                    if buyed :
                        profet=round((((last_price*fee_sell)-buyed_prics) / buyed_prics if buyed_prics>0 else 1) * 100,dot_point_round) 
                        reup=Last_price_avg_short>Last_price_avg_medium>Last_price_avg_long and Last_price_avg_medium>avg_MaxMin
                        dif_up_biger=(last_price-Last_price_avg_medium)>((Last_price_avg_medium-Last_price_avg_long)*1.5)
                    if buyed and reup and dif_up_biger\
                        or  (buyed and CRISIS):
                            print(int(time.time())-buyed_time)
                            Action=2
                            st =f"=======<><><><><><><><><><><><><><><><><>======\n    SELLING: {TIME} price:{last_price}\n"
                            st+=f"\t{'CRISIS ! ' if CRISIS  else'# selling'}\n|buy:{buyed_prics}->sell:{last_price} => profet {profet}% |#"
                            st+="\n[----------------------------------------]\n"
                            print(st)
                            TOTAL_PROFET += profet
                            print("\tTOTAL_PROFET: ",TOTAL_PROFET,"\n=-=-=-=-=-=-=-=-=-=-=-\n")
                            with open(f"./{symbol} {date}.log", "+a") as logfile:
                                logfile.write(st)
                            send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],st,cvsChart(f"./{symbol} {date}.cvs",True))


                    #==== LOG IT ======#
            
                    output=f'{round(last_price,dot_point_round)},{avg_MaxMin},{Last_price_avg_short},{Last_price_avg_medium},{Last_price_avg_long},{prediction_p},{TIME}\n'
                    if Action:
                        if Action==1:
                            buyed=True
                            buyed_time=int(time.time())
                            output+=f'{buyed_prics},{TIME}\n'
                        elif Action==2:
                            buyed=False
                            output+=f'{last_price},{TIME},{profet}%\n'        

                    with open(f"./{symbol} {date}.cvs", "+a") as logfile:
                        logfile.write(output)

                    Action=0
                    
                    #==== SEND REPORT: report evrey 2 h ======#
                            # time.mktime=>Convert both times to seconds since the epoch
                    if time.mktime(loop_time)-time.mktime(time_start)>=(report_hours_steps*60*60):
                            time_start=time.localtime()
                            if os.path.exists(f"./{symbol} {date}.cvs") :
                                Name_chart=cvsChart(f"./{symbol} {date}.cvs", True)
                                send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS",Name_chart)
                            else:send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS - NOfile ")

                #======DATA NOT COLLECTED YET ====xxx
                else:
                    Data_collection_progress=((len(AVG_LIST_last_prices)+1)/long_len_range)*100
                    if Data_collection_progress<=100:print("collecting data.. :",((len(AVG_LIST_last_prices)+1)/long_len_range)*100,"%")
                    else:
                        t="DONE collection data. NOW IT'S START .."
                        print(t)
                        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],t)

                    max_price,min_price,avg_MaxMin = last_price,last_price,last_price
                
                time.sleep(STEPS)
                life_time -= STEPS
            else:
                ERR=f"יש בעיה בחיבור האינטרניט \n{TIME} {symbol}\n"
                send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],ERR)

        except KeyboardInterrupt:
            life_time = 0
    if os.path.exists(f"./{symbol} {date}.cvs") :
        Name_chart=cvsChart(f"./{symbol} {date}.cvs", True)
        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS",Name_chart)
    else:send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"LIFE ENDS - NOfile ")


if __name__ == "__main__":
    try:
        time.sleep(3)
        send_via_telegram(env["tel_CHAT_ID"] ,env["tel_TOKEN"],"strting ..")
        main()
    except Exception as e:
        ERR=f"TRY MAIN ERR\n {e}"
        print(ERR)

    


