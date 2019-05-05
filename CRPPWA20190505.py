import os
import re
import pandas as pd
import numpy as np
from datetime import datetime as dt
#import requests# to pull data from gitHub
import base64
import io

import plotly
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output#, State
#import dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1(children='WhatsApp group usage'),
    html.Br(),
    html.Div(children='''Load the .txt file that is exported by WhatsApp'''),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
#    dcc.DatePickerRange(
#        id='my-date-picker-range',
#        min_date_allowed=MsgTable['PostDate'].min(),
#        max_date_allowed=MsgTable['PostDate'].max(),
#        #initial_visible_month=MsgTable['PostDate'].min(),
#        start_date=MsgTable['PostDate'].min(),
#        end_date=MsgTable['PostDate'].max()
#    ),
    html.Br(),
    html.Div(children='''Pick message type'''),
    html.Div([
              dcc.Dropdown(
                 id='pics',
                 options=[{'label': i, 'value': i} for i in ['All', 'Only with media (like selfies)', 'Only without media']], 
                 value = 'All'
                 ),
              dcc.Graph(id='fig3'),
              dcc.Input(id='myid', value='Replace with your name', type='text'),
              html.Div(id='my-div')]
              ),
    html.Div(id='output-data-upload')

],style = dict(width = '40%')
)

def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        #WhatsApp chat log is a .txt file
        df1 = pd.read_csv(io.StringIO(decoded.decode('utf-8')),header=None, error_bad_lines=False, skiprows=1)
#        df = df1    
#to knock out just the message text that wraps to 1+ lines
        df1.iloc[:,0] = pd.to_datetime(df1.iloc[:,0], format='%d/%m/%Y', errors='coerce')
        df1.dropna(inplace=True)
        df1['Full'] = df1.iloc[:,0].map(str)+df1.iloc[:,1].map(str)
        df1['FullStr'] = df1['Full'].str.strip()
#        df = df1    
        df = df1['FullStr'].str.extract(r'(?P<Date>\d+-\d+-\d+)\s+(?P<Time1>\d+:\d+:\d+)\s+(?P<Time2>\d+:\d+)\s+-\s+(?P<Sender>.*):(?P<Message>.*)') #        #Dates
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df.set_index(keys='Date', inplace=True)
        df.reset_index(level=0, inplace=True)#to convert index to 'Date' column
#think through how to deal with exception path
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return df
        
@app.callback(
    [#Output('output-container-date-picker-range', 'children'),
#     Output('output-data-upload', 'children'),
     Output('fig3', 'figure'),
     Output(component_id='my-div', component_property='children'),

    ],
    [
#     Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date'),
    Input('upload-data', 'contents'),
    Input(component_id='myid', component_property='value'),
    Input('pics', 'value'),
     ]
)
def update_output_div(list_of_contents, myid, pics):
    if list_of_contents is not None:
        for c in list_of_contents:
            MsgTable1a = parse_contents(c)
    if pics == 'All': 
        MsgTable1 = MsgTable1a
    if pics == 'Only with media (like selfies)': 
        MsgTable1 = MsgTable1a[MsgTable1a['Message'].str.contains("<Media omitted>", na=False)]
    if pics == 'Only without media': 
        MsgTable1 = MsgTable1a[-MsgTable1a['Message'].str.contains("<Media omitted>", na=False)]
    TopWAMsgWriters = MsgTable1.groupby('Sender').count().sort_values(by='Message', ascending=False)
    TopWAMsgWriters = TopWAMsgWriters.iloc[0:5,]
    TopWAMsgWriters.reset_index(level=0, inplace=True)#to convert index back to 'Sender' column
    TopWAMsgWriters.Sender = TopWAMsgWriters.Sender.astype(str).apply(lambda x: '.'+x[0:3]+'.'+x[3:9]+'.'+x[9:15])
    return {
                'data': [{
                          'x': TopWAMsgWriters.Sender, 
                          'y': TopWAMsgWriters.Message, 
                          'type': 'bar'
                          }],
                'layout': {'title': 'WA message posters by count'}
            }, 'Reguester name: {}'.format(myid)
#
if __name__ == '__main__':
    app.run_server(debug=True)

