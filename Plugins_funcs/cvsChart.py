import plotly.graph_objs as go
from plotly.offline import plot
import os,time
import glob
import shutil



def cvsChart(csv_file,part_of_day=False):
    name_=os.path.basename(csv_file)[:-4]
    if part_of_day:name_+=time.strftime(" UNTIL %H", time.localtime())
    
         
    # פתח את הקובץ CSV וקרא את הנתונים ישירות
    with open(csv_file, 'r') as file:
        lines = file.readlines()
    
    # יצירת רשימות עבור הנתונים
    TIME = []
    Last_price = []
    AVG_MaxMin = []
    price_avg_short = []
    price_avg_medium=[]
    price_avg_long = []
    BUY_action_prices=[]
    BUY_action_times = []
    SELL_action_prices = []
    SELL_action_times=[]
    prediction_p=[]
    PROFIT_txt=[]

    for line in lines:
        data = line.strip().split(',')
        if len(data) == 7:
            Last_price.append(float(data[0]))
            AVG_MaxMin.append(float(data[1]))
            price_avg_short.append(float(data[2]))
            price_avg_medium.append(float(data[3]))
            price_avg_long.append(float(data[4]))
            prediction_p.append(float(data[5]))
            TIME.append(data[6].strip())
        if len(data) == 2:
                BUY_action_prices.append(float(data[0]))
                BUY_action_times.append(data[1].strip())
        if len(data) == 3:
            SELL_action_prices.append(float(data[0]))
            SELL_action_times.append(data[1].strip())
            PROFIT_txt.append("רווח :"+data[2])
                
    # יצירת סדרות נתונים לגרף בעזרת plotly
    Price = go.Scatter(x=TIME, y=Last_price, mode='lines', name='Price')
    MaxMin = go.Scatter(x=TIME, y=AVG_MaxMin, mode='lines', name='AVG_MaxMin')
    AVG_SHORT = go.Scatter(x=TIME, y=price_avg_short, mode='lines', name='AVG_SHORT')
    AVG_medium = go.Scatter(x=TIME, y=price_avg_medium, mode='lines', name='AVG_medium')
    AVG_LONG = go.Scatter(x=TIME, y=price_avg_long, mode='lines', name='AVG_LONG')
    prediction_price = go.Scatter(x=TIME, y=prediction_p, mode='lines', name='prediction')
    points_buy = go.Scatter(x=BUY_action_times, y=BUY_action_prices, mode='markers', name='קנייה',marker=dict(size=10,))
    points_sell = go.Scatter(x=SELL_action_times, y=SELL_action_prices, mode='markers+text', name='מכירה',text=PROFIT_txt,textposition='top center',marker=dict(size=10,))


    data = [Price,MaxMin,AVG_SHORT,AVG_medium,AVG_LONG,prediction_price,points_buy,points_sell]

    layout = go.Layout(
        title=name_, 
        xaxis=dict(title='זמן',showgrid=False), 
        yaxis=dict(title='ערכים',gridcolor='rgba(128, 128, 128, 0.5)'),
        plot_bgcolor='rgba(127, 128, 129, 0.8)',  # Semi-transparent black
        paper_bgcolor='rgba(229, 244, 247, 0.62)'  # Solid white
    )

    fig = go.Figure(data=data, layout=layout)
    filename=name_+'.html'
    # יצירת קובץ HTML והצגת הגרף בו
    if os.path.exists(filename):
        os.remove(filename)
        time.sleep(0.5)     
    plot(fig, filename=filename, auto_open=True)
    return filename



def Day_chart():
    files=sorted(glob.glob("./*.cvs"))
    print(files)
    # last_price,Last_price_avg_short,Last_price_avg_medium,Last_price_avg_long,prediction_p,TIME
    history_dir = 'history'

    # יצירת התיקייה אם היא לא קיימת
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
            # מעבר על כל הקבצים בתיקייה
    for file in files:
            if 'DAY' not in file:
                print(file)
                output_filename =os.path.basename(file)[:-7]+"_DAY.cvs"
                with open(file, 'r') as csv_file:
                    rows =csv_file.readlines()
                    for row in rows:
                        row=row.split(",")
                        row=",".join(row)
                        with open(output_filename, 'a+') as file_out:
                                file_out.write(row)
                shutil.move(file, history_dir)
    files=sorted(glob.glob("./*.cvs"))
    for file in files:
        print(file)
        cvsChart(file,False)



def clean_files():
    history_dir = 'history'
    
    # יצירת התיקייה אם היא לא קיימת
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    # רשימת סיומות הקבצים לחיפוש
    file_extensions = ['*.html', '*.log', '*.cvs']

    for extension in file_extensions:
        # מציאת כל הקבצים עם הסיומת הנוכחית
        for file in glob.glob(extension):
            # העברת הקובץ לתיקייה 'history'
            shutil.move(file, history_dir)

