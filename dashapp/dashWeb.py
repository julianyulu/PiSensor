#!/usr/bin/python3

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
# Last-Updated: Sun Oct  7 17:45:23 2018 (-0500)
#           By: yulu
#     Update #: 198
# 
import sys
sys.path.insert(0, '/usr/local/lib/python3.5/dist-packages')

import dash
import os
import datetime
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


dataPath = '/home/yulu/SyncRaspberryPi/'
dataSubFolders = ['dev1', 'dev2', 'dev3', 'dev4', 'dev5']
deviceColor = {'dev1':'#E1AF35', 'dev2': '#3277DC', 'dev3':'#DC76E1', 'dev4':'#43A95C', 'dev5': '#787878'}


def csvDateFile(path):
    if os.path.isdir(path):
        datetime = sorted([x.split('_')[1].split('.')[0] for x in os.listdir(path) if x[-4:] == '.csv'])
        files = [x for x in os.listdir(path) if x[-4:] == '.csv']
        return datetime, files

    else:
        print("No data subfolders found !")
        return 0, 0

    
commonDate = csvDateFile(os.path.join(dataPath, 'dev1'))[0]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)


app.config.requests_pathname_prefix = ''

server = app.server


app.layout = html.Div(
    [
        # drop down for multi device selection
        html.Div(
            [
                html.H1("Raizen Lab Temperature / Humidity Interactive Database"),
                # Device selection drop down 
                html.Div(
                    [
                        html.H2("Plot Config:"),
                        html.Label('Select raspberry pi device: '),
                        dcc.Dropdown(
                            id = 'device-selector',
                            options = [dict([('label', dev), ('value',dev)]) for dev in dataSubFolders],
                            value = ['dev1'],
                            multi = True
                        ),
                    ],
                    style = {'width': '60%',
                             'display': 'block',
                             'padding': '2em 0',
                             'margin': '0 0 0 0',
                             }
                ),

                # Date selection drop down
                html.Div(
                    [
                        html.Label('Select date:'),
                        dcc.Dropdown(
                            id = 'date-selector',
                            options = [dict([('label', date), ('value', date)]) for date in commonDate],
                            #value = commonDate[-1],
                            value = [str(datetime.date.today())],
                            multi = True
                        )
                    ],
                    style = {'width': '60%',
                             'display': 'block',
                             'padding': '2em 0 ',
                             'margin': '0 0 0 0',
                             }
                )
            ],

            style = {'width': '30%',
                     'display': 'inline-block',
                     'vertical-align': 'top',
                     'padding': '2em',
                     'margin': '0',
                     }

        ),

        html.Div(
            [
                dcc.Graph(id = 'interactive-graph-humidity'),
                dcc.Graph(id = 'interactive-graph-temperature')
            ],
            style = {'width': '65%',
                     'display': 'inline-block',
                     'height': '100%',
                     'padding': '0',
                     'margin': '0',
                     'backgroundColor': '#e6f0ff'
            }
            )

        
    ],
    style = {'height': '100vh',
             'width': '100%',
             'padding': '0',
             'margin': '0',
             'backgroundColor': '#e6f0ff'
    }
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
            title = 'Temperature',
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
            title = 'Relative Humidity',
            xaxis = {'title': 'time of the day'},
            yaxis = {'title': 'humidity [%]'}
        )
    }
    return graph 

if __name__ == '__main__':
    app.run_server(debug = True)
