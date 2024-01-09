import plotly.graph_objs as go
from plotly.offline import plot
import os




def cvsChart(csv_file):
    name_=os.path.basename(csv_file).split('.')[0]
    # פתח את הקובץ CSV וקרא את הנתונים ישירות
    with open(csv_file, 'r') as file:
        lines = file.readlines()
    
    # יצירת רשימות עבור הנתונים
    TIME = []
    Last_price = []
    price_avg_now = []
    Prediction_avg_now = []
    price_avg_long = []
    BUY_action_prices=[]
    BUY_action_times = []
    SELL_action_prices = []
    SELL_action_times=[]
    PROFIT_txt=[]

    for line in lines:
        data = line.strip().split(',')
        if len(data) == 5:
            Last_price.append(float(data[0]))
            price_avg_now.append(float(data[1]))
            Prediction_avg_now.append(float(data[2]))
            price_avg_long.append(float(data[3]))
            TIME.append(data[4].strip())
        if len(data) == 2:
                BUY_action_prices.append(float(data[0]))
                BUY_action_times.append(data[1].strip())
        if len(data) == 3:
            SELL_action_prices.append(float(data[0]))
            SELL_action_times.append(data[1].strip())
            PROFIT_txt.append("רווח :"+data[2])
                
    # יצירת סדרות נתונים לגרף בעזרת plotly
    trace1 = go.Scatter(x=TIME, y=Last_price, mode='lines', name='Last Price')
    trace2 = go.Scatter(x=TIME, y=price_avg_now, mode='lines', name='Price-Avg')
    trace3 = go.Scatter(x=TIME, y=price_avg_long, mode='lines', name='price-Avg_LONG')
    trace4 = go.Scatter(x=TIME, y=Prediction_avg_now, mode='lines', name='Prediction')
    points_buy = go.Scatter(x=BUY_action_times, y=BUY_action_prices, mode='markers', name='קנייה',marker=dict(size=10,))
    points_sell = go.Scatter(x=SELL_action_times, y=SELL_action_prices, mode='markers+text', name='מכירה',text=PROFIT_txt,textposition='top center',marker=dict(size=10,))


    data = [trace1,trace2,trace3,trace4,points_buy,points_sell]

    layout = go.Layout(
        title=name_, 
        xaxis=dict(title='זמן',showgrid=False), 
        yaxis=dict(title='ערכים',gridcolor='rgba(128, 128, 128, 0.5)'),
        plot_bgcolor='rgba(127, 128, 129, 0.8)',  # Semi-transparent black
        paper_bgcolor='rgba(229, 244, 247, 0.62)'  # Solid white
    )

    fig = go.Figure(data=data, layout=layout)

    # יצירת קובץ HTML והצגת הגרף בו
    plot(fig, filename=name_+'.html', auto_open=True)


