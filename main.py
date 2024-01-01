
import threading
import time,os
import joblib
from Plugins_funcs.analyze_market import Analyze_market
from Plugins_funcs.save_data_to_file import Save_data_to_file
from Plugins_funcs.html_chart import Html_chart
# from Plugins_funcs.bitfinex_book_data import Bitfinex_book_data
from Plugins_funcs.BINANCE_book_data import Binance_book_data

# Constants
# SYMBOL = "tSOLUSD" # all=>https://api-pub.bitfinex.com/v2/tickers?symbols=ALL  
SYMBOL = "BTCUSDT"     #    url_symbols = "https://api.binance.com/api/v3/exchangeInfo"
h = 60 * 60
LIFE_TIME = h/2
STEPS = 2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(ROOT_DIR, "retrained_random_forest_model_local.pkl")  # Assuming the model is in this path
JSON_FILE = os.path.join(ROOT_DIR, 'Predicted_OUT','Predicted_json.json')
# Load the trained model

try:
    # טעינת המודל באמצעות memory-mapping לקריאה בלבד
    rf_model = joblib.load(MODEL_PATH, mmap_mode='r')
except MemoryError:
    print("MemoryError: לא ניתן לטעון את המודל בגלל בעיות זיכרון")

def Hart(symbol, life_time, STEPS, json_file):
    records = []
    total_life = life_time
    while life_time > 0:
        print("--"*10)
        book_data = Binance_book_data(symbol)
        if book_data:
            analyzed_data = Analyze_market(book_data)
            # Predict using the model
            features = [[analyzed_data['Bid Standard Deviation'],analyzed_data['Ask Standard Deviation'],analyzed_data['Spread']]]
            try:predicted_last_price = rf_model.predict(features)[0]
            except Exception as e:
                print(">>>predict model faild |>>>[X]<<<|")
                print(e)
                predicted_last_price = None
            analyzed_data["Predicted_CHANGE_Price"] = predicted_last_price
            records.append(analyzed_data)

        time.sleep(STEPS)
        life_time -= STEPS
        print(total_life - life_time, "/", int(total_life), "|  =>",analyzed_data["Last_Price"] ,int(analyzed_data["Predicted_CHANGE_Price"]))

    Save_data_to_file(records, json_file)


def main():
    
    try:
        print("start_main")
        thread = threading.Thread(target=Hart, args=(SYMBOL, LIFE_TIME, STEPS, JSON_FILE))
        thread.daemon = True
        thread.start()
        print("starting now the thread ")
        thread.join()
    except Exception as e:
        print(e)
        # TODO: Enhance error handling if needed

    print("-=-=-=----DONE")
    Html_chart(JSON_FILE)


if __name__ == "__main__":
    main()
