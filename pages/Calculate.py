import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime as dt
import plotly.figure_factory as ff
import plotly.express as px
from sqlalchemy.orm import sessionmaker
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc
from lifetimes.utils import calibration_and_holdout_data
from zenq.visualizations.plot import Visuals
from zenq.clvmodels.pareto import Model
from zenq.api.prepare_db import db
from zenq.api.endpoints import insert_facts
import dash
import base64
from urllib.parse import quote as urlquote
import io
import os
from flask import Flask 
from dash import callback,Input, Output, State, dcc, html 

UPLOAD_DIRECTORY =  r"zenq/api"

dash.register_page(
    __name__,
     path='/Calculate',
    title='Calculate',
    name='Calculate'
)
 
layout =  html.Div([
    html.Div([
        html.Div([
            dcc.Upload(id='upload_buttom',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text'),
                ),        
           html.Div(id="output"),]),
        html.Div([    
            dcc.Input(
                id='input1',
                type='text',
                placeholder='csv name(globbing.csv)',
            ),
            dcc.Input(
                id='input2',
                type='text',
                placeholder='customer_id',
            ),
            
            # Second input field
            dcc.Input(
                id='input3',
                type='text',
                placeholder='gender',
            ),
            
            # Third input field
            dcc.Input(
                id='input4',
                type='text',
                placeholder='invoice_id',
            ),
            
            # Fourth input field
            dcc.Input(
                id='input5',
                type='text',
                placeholder='date',
            ),
            
            # Fifth input field
            dcc.Input(
                id='input6',
                type='text',
                placeholder='quantity',
            ),
            
            # Sixth input field
            dcc.Input(
                id='input7',
                type='text',
                placeholder='total_price',
            ),],id = 'column_inputs'), 
        
            html.Div([
            html.Button(id='submit_button',  n_clicks=0,
                children=html.Div(['Submit'], id = 'csv_text_1'),
                ),        
           html.Div(id="output"),]),
            html.Div(
            html.Button('Submit', id='submit_button',  n_clicks=0),
            style={'textAlign': 'center' }  # Center the button
        ), 
         
        html.Div(id='output_div')
    ], className = 'black_box33'),
 
    html.Div([          
        html.Div([
                    html.Div(id='time-series')
        ],
                #  className = 'rect1'
                 ),
          
        html.Div([
                html.Div([
                    html.Div(id='gender_price')
                ])
            
            ], 
                #  className = 'rect2'
                 ) ,              
    ],  ),

    html.Div([  
                      
        html.Div([html.Div(id='rfm_treemap')],
                #  className = 'rect3'
                 ),
          
        html.Div([html.Div(id='top_customers_30days')], 
                #  className = 'rect4'
                 ) ,   
                   
    ],className = 'pordz'),
        html.Div([  
                      
        html.Div([html.Div(id='customer_aliveness')],
                #  className = 'rect3'
                 ),
          
        html.Div([html.Div(id='price_distribution')], 
                #  className = 'rect4'
                 ) ,   
                   
    ],className = 'pordz')
    ])

def save_file(name, content):
    """Save a file uploaded with the dcc.Upload component."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

@callback(
    Output("output", "children"),
    Input("upload_buttom", "filename"),
    State("upload_buttom", "contents"),
    prevent_initial_call=True,
)
def upload_files(names, contents):
    """Save uploaded files and return a message to the user."""
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    if isinstance(names, str):
        # user has uploaded a single file
        save_file(names, contents)
        return f"{names} uploaded"

@callback(
    Output('output_div', 'children'),
    # Output('plot2', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('input1', 'value'),
    State('input2', 'value'),
    State('input3', 'value'),
    State('input4', 'value'),
    State('input5', 'value'),
    State('input6', 'value'),
    State('input7', 'value')
)
 
def process_inputs(n_clicks, filename, customer_id, gender, invoice_id, date, quantity, total_price):
    initialize=db()
    initialize.main()
    if n_clicks > 0:
        insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price)
        model=Model()
        model.cltv_df()
        model.rfm_score()
        model.fit_paretonbd()
        model.model_params()
        model.predict_paretonbd()
        model.customer_is_alive()
        visuals = Visuals()
        time_series = visuals.time_series()
        price_distribution = visuals.price_distribution()
        gender_price  = visuals.gender_price()
        rfm_treemap = visuals.rfm_treemap()
        top_customers_30days = visuals.top_customers_30days()
        customer_aliveness = visuals.customer_aliveness()
        
        # return html.P("Data has been inserted into the database."), dcc.Graph(figure=fig) 
        return [
        dcc.Graph(id='time_series', figure=time_series),
        dcc.Graph(id='price_distribution', figure=price_distribution),
        dcc.Graph(id='gender_price', figure=gender_price),
        dcc.Graph(id='rfm_treemap', figure=rfm_treemap),
        dcc.Graph(id='top_customers_30days', figure=top_customers_30days),
        dcc.Graph(id='customer_aliveness', figure=customer_aliveness)
 
        ] 
    
if __name__ == "__main__":
    app.run_server(debug=True, port=8058)
    