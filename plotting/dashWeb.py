# dashWeb.py --- 
# 
# Filename: dashWeb.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat Oct  6 22:23:27 2018 (-0500)
# Version: 
# Last-Updated: Sun Oct  7 00:40:11 2018 (-0500)
#           By: yulu
#     Update #: 85
# 

import dash
import os
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

dataPath = './'
dataSubFolders = ['dev1', 'dev2', 'dev3', 'dev4', 'dev5']
deviceColor = {'dev1':'blue', 'dev2': 'red', 'dev3':'green', 'dev4':'black', 'dev5': 'gray'}


def csvDateFile(path):
    if os.path.isdir(path):
        datetime = [x.split('_')[1].split('.')[0] for x in os.listdir(path) if x[-4:] == '.csv']
        files = [x for x in os.listdir(path) if x[-4:] == '.csv']
        return datetime, files
    else:
        print("No data subfolders found !")
        return [], []

    
commonDate = csvDateFile('./dev5')[0]
df_dev1_newest = pd.read_csv(os.path.join(dataPath, 'dev1', 'dev1_%s.csv'%commonDate[-1]))
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)


app.layout = html.Div(
    [
        html.H1("Raizen Lab Temperature / Humidity Interactive DataBase"),
        
        # drop down for multi device selection
        html.Label('Select raspberry pi device: '),
        dcc.Dropdown(
            id = 'device-selector',
            options = [dict([('label', dev), ('value',dev)]) for dev in dataSubFolders],
            value = 'dev1',
            multi = True
        ),

        # drop down for date selection
        html.Label('Select date:'),
        dcc.Dropdown(
            id = 'date-selector',
            options = [dict([('label', date), ('value', date)]) for date in commonDate],
            value = commonDate[-1],
            multi = True
        ),
        
        dcc.Graph(id = 'interactive-graph-humidity'),
        dcc.Graph(id = 'interactive-graph-temperature'),
        
    
        
        
    ]
)


@app.callback(
    dash.dependencies.Output('interactive-graph-temperature', 'figure'),
    [dash.dependencies.Input('device-selector', 'value'),
     dash.dependencies.Input('date-selector', 'value')])
def update_temperature_figure(selected_device, selected_date):
    traces = []
    selected_device = [selected_device] if type(selected_device) == str else selected_device
    selected_date = [selected_date] if type(selected_date) == str else selected_date
    for dev in selected_device:
        for date in selected_date:
            print(dev, date)
            df = pd.read_csv(os.path.join(dataPath, dev, '%s_%s.csv'%(dev, date)))
            traces.append(
                go.Scatter(
                    x = df['time'],
                    y = df['temperature'],
                    name = "Device: %s"%dev, 
                    mode = 'lines+markers',
                    line = {
                        'color': deviceColor[dev],
                        #'shape': 'spline'
                    },
                )
            )
            
    graph = {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'time of the day'},
            yaxis = {'title': 'temperature'}
        )
    }
    return graph 

@app.callback(
    dash.dependencies.Output('interactive-graph-humidity', 'figure'),
    [dash.dependencies.Input('device-selector', 'value'),
     dash.dependencies.Input('date-selector', 'value')])
def update_humidity_figure(selected_device, selected_date):
    traces = []
    selected_device = [selected_device] if type(selected_device) == str else selected_device
    selected_date = [selected_date] if type(selected_date) == str else selected_date
    for dev in selected_device:
        for date in selected_date:
            print(dev, date)
            df = pd.read_csv(os.path.join(dataPath, dev, '%s_%s.csv'%(dev, date)))
            traces.append(
                go.Scatter(
                    x = df['time'],
                    y = df['humidity'],
                    name = "Device: %s"%dev, 
                    mode = 'lines+markers',
                    line = {'color': deviceColor[dev]},
                )
            )
            
    graph = {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'time of the day'},
            yaxis = {'title': 'humidity'}
        )
    }
    return graph 

if __name__ == '__main__':
    app.run_server(debug = True)
