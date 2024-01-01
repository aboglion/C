import requests
import time

def Bitfinex_book_data(symbol):

    # url_book = "https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0?len=50"
    url_book = f"https://api-pub.bitfinex.com/v2/book/{symbol}/P0?len=100"

    try:
        headers = {"accept": "application/json"}
        book = requests.get(url_book, headers=headers)
        if book.status_code != 200:
            return 0
        re_data= book.json()
        pids_book=[]
        asks_book=[]
# [0]	PRICE		Price level
# [1]	COUNT		Number of ordershttps://api-pub.bitfinex.com/v2/book/tBTCUSD/P0?len=50 at that price level
# [2]	AMOUNT		Total amount available at that price level (if AMOUNT > 0 then bid else ask)
        for i in re_data:
            ord={"PRICE":i[0],"COUNT":i[1],"AMOUNT":i[2]}
            # ביקוש  
            if ord["AMOUNT"]<0:
                ord["AMOUNT"]*=(-1)
                asks_book.append(ord)
            else:pids_book.append(ord)

        return [pids_book[:50],asks_book[:50]]
    except Exception as e:
        time.sleep(5)
        print("FAILD IN bitfinex_book_data\n",e)
        return 0
    