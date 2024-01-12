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
    # half=len(bids)//2
    # הנחה: רשימת הביקוש ממוינת מהגבוה לנמוך לפי מחיר, ורשימת ההיצע ממוינת מהנמוך לגבוה לפי מחיר
    Last_Price=Avg_ord_list([bids[0],asks[0]])
    
    
    # Sort bids and asks based on AMOUNT in descending order
    sorted_bids = sorted(bids, key=lambda x: x['AMOUNT'], reverse=True)
    sorted_asks = sorted(asks, key=lambda x: x['AMOUNT'], reverse=True)

    # Select top 5 bids and asks
    top_bids = sorted_bids[:10]
    top_asks = sorted_asks[:10]

    # Calculate the moving average for the selected bids and asks
    Prediction_price = Avg_ord_list(top_bids + top_asks)

    return {
        'Last_Price': Last_Price,
        'Prediction_price':Prediction_price,
    }

