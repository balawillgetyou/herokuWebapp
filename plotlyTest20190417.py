import os
import re
import pandas as pd
#import numpy as np
#from datetime import datetime as dt
import requests# to pull data from gitHub

#import plotly
#import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



#read file and extract useful info into a DF
url = 'https://github.com/balawillgetyou/herokuWebapp/raw/master/WhatsAppCRPP20190409.txt'
page = requests.get(url)
chatLog = page.text
page.close()
strings = re.findall(r'(\d+/\d+/\d+,\s+\d+:\d+)\s+-\s+(.*):(.*)', chatLog)

#os.chdir('/media/sf_ForVirtualBox/CRPP')
#f = open("WhatsAppCRPP20190409.txt", 'r', encoding='utf8') 
#strings = re.findall(r'(\d+/\d+/\d+,\s+\d+:\d+)\s+-\s+(.*):(.*)', f.read())
#f.close()

MsgTable= pd.DataFrame(strings,columns =['DateTime', 'Sender', 'Message'])
MsgTable['DateTime'] = MsgTable['DateTime'].str.replace(',','')
MsgTable['DateTime'] = pd.to_datetime(MsgTable['DateTime'], format='%d/%m/%Y %H:%M')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('Crpp','')
MsgTable['Message'] = MsgTable['Message'].str.replace(':','')
MsgTable.set_index(keys='DateTime', inplace=True)

#exclude organizers
#MsgTable = MsgTable[~MsgTable['Sender'].str.contains('Badri|Sree|Subashini|Karthik', regex=True)]

#Dates
MsgTable.reset_index(level=0, inplace=True)#to convert index to 'PostDateTime' column
MsgTable['PostDate'] = [d.date() for d in MsgTable.DateTime]
                    
#replacing phone numbers with names, as needed
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 99406 66025', 'Usha')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98408 40466', 'S Kumar')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98408 22288', 'Uma')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 99761 47435', 'Javid')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 99625 84326', 'RDX')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98405 42076', 'Captain Ganesh')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98847 21714', 'Vikram')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 95662 18287', 'WineGuy')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98403 57510', 'S Mohan')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 93804 14631', 'Ramganesh')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98414 31419', 'Sudhakar S')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 97901 39602', 'Sabitha')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 98848 88836', 'V Vijayan')
MsgTable['Sender'] = MsgTable['Sender'].str.replace('91 97899 78077', 'Nandini')


app.layout = html.Div([
    html.H1(children='WhatsApp group usage'),
    html.Br(),
    dcc.Input(id='myid', value='Replace with your name', type='text'),
    html.Br(),
    html.Div(id='MsgTableShape'),
    html.Br(),
    html.Div(id='my-div')

],style = dict(width = '40%')
)


@app.callback(
    [#Output('output-container-date-picker-range', 'children'),
     Output(component_id='MsgTableShape', component_property='children'),
     Output(component_id='my-div', component_property='children'),
    #Output('fig3', 'figure')
    ],
    [#Input('my-date-picker-range', 'start_date'),
     #Input('my-date-picker-range', 'end_date'),
     Input(component_id='myid', component_property='value'),
     #Input('pics', 'value'),
     ]
)
def update_output_div(myid):
    MsgTableShape = MsgTable.shape
    return myid, MsgTableShape
#
if __name__ == '__main__':
    app.run_server(debug=True)

