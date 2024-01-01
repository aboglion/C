import json,os
import plotly.graph_objs as go
import plotly.offline as offline
from .save_data_to_file import rename_re


def Html_chart(json_file):
    json_data={"":""}
    if not os.path.exists(json_file):
        print(json_file,"not founds")
        return
    with open(json_file, "r") as f:
        json_data = f.read()

    # קריאת הנתונים מהקובץ JSON
    data = json.loads(json_data)
    if not data: 
        print(">>>>>-No data in the file",json_file)
        return
    # הכנת הנתונים לצורת המצג המתאימה לPlotly
    x = list(range(len(data)))
    traces = []
    for key in data[0].keys():
        y = [entry[key] for entry in data]
        trace = go.Scatter(x=x, y=y, mode='lines', name=key)
        traces.append(trace)
    
    # יצירת הגרף
    layout = go.Layout(title="JSON Data Visualization")
    fig = go.Figure(data=traces, layout=layout)
    
    # שמירת הגרף כקובץ HTML
    file=json_file[:-5]
    if os.path.exists(file+".html"):rename_re(file+".html")
    offline.plot(fig, filename=file, auto_open=True)


