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


    for line in lines:
        data = line.strip().split(',')
        if len(data) == 5:
            Last_price.append(float(data[0]))
            price_avg_now.append(float(data[1]))
            Prediction_avg_now.append(float(data[2]))
            price_avg_long.append(float(data[3]))
            TIME.append(data[4])

    # יצירת סדרות נתונים לגרף בעזרת plotly
    trace1 = go.Scatter(x=TIME, y=Last_price, mode='lines', name='Last Price')
    trace2 = go.Scatter(x=TIME, y=price_avg_now, mode='lines', name='Price-Avg')
    trace3 = go.Scatter(x=TIME, y=price_avg_long, mode='lines', name='price-Avg_LONG')
    trace4 = go.Scatter(x=TIME, y=Prediction_avg_now, mode='lines', name='Prediction')

    data = [trace1, trace2, trace3,trace4]

    layout = go.Layout(title=name_, xaxis=dict(title='זמן'), yaxis=dict(title='ערכים'))

    fig = go.Figure(data=data, layout=layout)

    # יצירת קובץ HTML והצגת הגרף בו
    plot(fig, filename=name_+'.html', auto_open=True)


