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
    
    
    # Calculate the total AMOUNT for top bids
    total_amount_bids = sum(b['AMOUNT'] for b in bids)

    # Calculate the total AMOUNT for top asks
    total_amount_asks = sum(a['AMOUNT'] for a in asks)


    
    if total_amount_asks-total_amount_bids*2>0 :
        Prediction_price =Last_Price*1.01
    elif total_amount_bids-total_amount_asks*2>0 :
        Prediction_price =Last_Price*0.09
    elif total_amount_asks-total_amount_bids>0:
        Prediction_price =Last_Price*1.003
    elif total_amount_bids-total_amount_asks>0 :
        Prediction_price =Last_Price*0.007
    else : Prediction_price=Last_Price

   
    return {
        'Last_Price': Last_Price,
        'Prediction_price':Prediction_price,
    }

