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
    # Calculate the demand-supply ratio
    ratio = total_amount_bids / total_amount_asks

      # Determine the maximum change allowed (5% of the current price)
    max_change = Last_Price * 0.01
    
    # Calculate the desired change based on the ratio
    # If ratio > 1 (more demand), price increase up to 5%
    # If ratio < 1 (more supply), price decrease up to -5%
    # The change is proportional to the difference from 1, limited by max_change
    if ratio > 1:
        price_change = min((ratio - 1) * Last_Price, max_change)
    else:
        price_change = max((ratio - 1) * Last_Price, -max_change)
    
    # Apply the calculated change to the current price
    Prediction_P = Last_Price + price_change

   
    return {
        'Last_Price': Last_Price,
        'Prediction_up':Prediction_P,
    }

