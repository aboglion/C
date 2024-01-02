import math

def Avg_ord_list(ord_list):
    total_val, total_weight = 0, 0
    for index, order in enumerate(ord_list):
        exp_factor=((len(ord_list)-index)/len(ord_list))*100
        total_val += order["PRICE"] * order["AMOUNT"] * order["COUNT"]* exp_factor
        total_weight += order["AMOUNT"] * order["COUNT"] * exp_factor
    if total_weight == 0:
        return 0

    return total_val / total_weight

def Analyze_market(book):
    bids,asks=book
    # הנחה: רשימת הביקוש ממוינת מהגבוה לנמוך לפי מחיר, ורשימת ההיצע ממוינת מהנמוך לגבוה לפי מחיר
    Last_Price=Avg_ord_list([bids[0],asks[0]])
    REV_price=Avg_ord_list([bids[-1],asks[-1]])
    # spread = asks[0]["PRICE"] - bids[0]["PRICE"]
    avg_bid_price = Avg_ord_list(bids)                                                      
    avg_ask_price = Avg_ord_list(asks)
    avg_price=(avg_bid_price+avg_ask_price)/2
    REV_avg_bid_price=Avg_ord_list(bids[::-1])
    REV_avg_ask_price=Avg_ord_list(asks[::-1])
    REV_avg_price=(REV_avg_bid_price+REV_avg_ask_price)/2

    # חישוב ממוצע משקולל
    AVG_Prediction=(avg_price+REV_avg_price)/2
    # הסטיית תקן
    # bid_std_dev = (sum([(bid["PRICE"] - avg_bid_price)**2 * bid["AMOUNT"] * bid["COUNT"] for bid in bids]) / sum([bid["AMOUNT"] * bid["COUNT"] for bid in bids]))**0.5
    # ask_std_dev = (sum([(ask["PRICE"] - avg_ask_price)**2 * ask["AMOUNT"] * ask["COUNT"] for ask in asks]) / sum([ask["AMOUNT"] * ask["COUNT"] for ask in asks]))**0.5

    return {
        'Last_Price': Last_Price,
        'Prediction_price':AVG_Prediction,
    }

