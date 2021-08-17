import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import calendar
import re
from datetime import datetime

df1 = pd.read_csv('twitter_alldata.csv')



df_symptoms = pd.read_excel('FrequencySymptoms.xlsx')

SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'padding':10,
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'transition': '0.3s',
    'border-radius': '5px',
    'margin-top':'20px',
    'margin-bottom':'20px',
}


LINKS_LIST_STYLE = {
    'height':'750px',
    "background-color":"#f8f9fa",
    'padding':10,
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'transition': '0.3s',
    'border-radius': '5px',
    'margin-top':'20px',
    'margin-bottom':'20px',
    'overflow':'auto'
}

GRAPH_STYLE = {
    "background-color":"#f8f9fa",
    'padding':10,
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'transition': '0.3s',
    'border-radius': '5px',
    'margin-top':'50px'
}


tweet = []

for x in range(len(df1['Tweet'])):
    s ='<br>'.join(re.findall('.{1,50}', df1['Tweet'][x]))
    tweet.append(s)

df1['Tweet'] = tweet

symptoms = []


for i in df_symptoms['Symptoms'].unique():
    symptoms.append(i)

symptoms_dd1 = symptoms[0:26]
symptoms_dd2 = symptoms[26:len(symptoms)-1]

dd1_options = [{'label':i,'value':i} for i in symptoms_dd1]
dd2_options = [{'label':i,'value':i} for i in symptoms_dd2]

df1['Date'] = df1['Date'].astype(str)
df1['Time'] = df1['Time'].astype(str)

df1['Time'] = pd.to_datetime(df1['Time']).dt.strftime('%H:%M')

df1["Date"] = pd.to_datetime(df1["Date"]).dt.strftime('%d/%m/%Y')
df1['Date'] = pd.to_datetime(df1['Date'])
df1['month'] = pd.DatetimeIndex(df1['Date']).month

min1 = min(df1['Date'].astype(str))
max1 = max(df1['Date'].astype(str))

min_date = min1.replace("-",",")
max_date = max1.replace("-",",")

min_y = int(min_date[:4])
min_m = int(min_date[5:7])
min_d = int(min_date[8:10])

max_y = int(max_date[:4])
max_m = int(max_date[5:7])
max_d = int(max_date[8:10])


# Content For tab 1
sidebar = html.Div(
    [
        html.H2("Control Panel", className="display-4"),
        html.Hr(),
        html.P(
            "Adjust the values for dataset", className="lead"
        ),
        dbc.Nav(
            [
            html.Label(['Select Symptom'],style={'font-weight':'bold'}),
            dcc.Dropdown(
                        id="dd1",
                        options=dd1_options,
                        multi=True,
                        value = [],
                        placeholder= "Select a Symptom",
                        style = {'margin-bottom':'20px'}


           ),
           html.Label(['Select Secondary Symptom'],style={'font-weight':'bold'}),
           dcc.Dropdown(
                       id="dd2",
                       options=dd2_options,
                       multi=True,
                       value = [],
                       placeholder= "Select a Symptom",
                       style = {'margin-bottom':'20px'}


          ),
           # html.Label(['Select Month'],style={'font-weight':'bold'}),
           # html.Div([dcc.Slider(
           #          id="slider",
           #          min=1,
           #          max=12,
           #          marks= marks_options,
           #        )
           #        ],style={'margin-bottom':'20px','padding':'20px'}),
            html.Label(['Select Date'],style={'font-weight':'bold'}),
            html.Div(
                     [
                     dcc.DatePickerRange(id='date-range',
                                         min_date_allowed=datetime(min_y,min_m,min_d),
                                         max_date_allowed=datetime(max_y,max_m,max_d),
                                         start_date=datetime(min_y,min_m,min_d),
                                         end_date=datetime(max_y,max_m,max_d)
                                                   )
                     ],style={'margin-bottom':'20px'}
            ),


            dbc.Button(id='submit-button',
            n_clicks=0,
            children='Submit',color="primary", className="mr-1",
            style={'font-size':'24px','margin-bottom':'20px'}),
            dbc.Button(id='clear-button',
            n_clicks=0,
            children='Reset',color="dark", className="mr-1",
            style={'font-size':'24px','margin-bottom':'20px'}),
            dbc.Spinner(color='primary',children=[html.Div(id="loading-output",style={'visibility':'hidden','margin-bottom':'20px'})]),
            ],
            vertical=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


links_list =  html.Div([
              html.H2("Links", className="display-4"),
              html.Hr(),
              html.Div(
                       id="links"
             )
             ],style = LINKS_LIST_STYLE)



content = html.Div([
                    html.H2("Graph", className="display-4",style={'text-align':'center'}),
                    html.Hr(),
                    dcc.Graph(id="plot")
                   ],style=GRAPH_STYLE)


modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Do you want to visit this link?"),
                dbc.ModalBody(id='modal-body'),
                dbc.ModalFooter(children=[
                    dbc.Button(
                        "Close",
                        id="close-centered",
                        className="ml-auto",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        "Yes",
                        id="visit-link",
                        n_clicks=0,
                        target="_blank"
                    ),
                  ],
                ),
            ],
            id="modal-centered",
            centered=True,
            is_open=False,
        ),
    ]
)


tab_1_layout = dbc.Row(
        [
        dbc.Col(
                [
                sidebar
                ]
        ),
        dbc.Col(
                [
                modal,
                content
                ],md=8
        ),
        dbc.Col(
                [
                links_list
                ]
        ),
        ]
)
