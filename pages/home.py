import dash
from dash import html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc

import shutil
import os
import base64
from assets.Decompile import decompileAPK
from assets.Utils import logTheProgress

dash.register_page(__name__, path='/')


layout =  dbc.Container([
    dbc.Row([
        html.H1("Upload your apk file to analyze", className="text-primary m-auto p-5 text-center"),
        html.Hr(),
        html.P(["Analyse android applications to understand its internal components.",html.Br(), "Use it as support to detect malware and privacy breaches"], 
                className="col-8 m-auto text-center p-5 text-dark"
        ),
    ]),
    dbc.Row([
        dcc.Upload(id="apk-uploaded", children=[
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '300px',
            'lineHeight': '300px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
            },
            className="d-none d-md-block",
        ),
        dcc.Upload(id="apk-uploaded2", children=[
             dbc.Button("Upload a file", color="warning", className="me-1"),
        ],  style={'textAlign': 'center'}, 
            className="d-block d-md-none",
        ),
    ]),
    html.Div(id='loading'),
])
# all logic related to the upload of content
def saveAPKFile(content, filename):
    data = content.encode("utf8").split(b";base64,")[1]
    with open("./UploadedAPKs/"+filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
    fp.close()
    with open('./UploadedAPKs/apknames.txt', 'a') as f:
        f.write(filename+"\n")
    f.close()
    

def parse_content(content, filename, displayClass):
    _, extension = os.path.splitext(filename)

    if extension == '.apk' :
        saveAPKFile(content, filename)
        output = html.Div([
                        dbc.Row(dbc.Col([
                                    dbc.Button("Begin the analysis", color="info", className="me-1", href="/analyzer", id="button")
                        ],  style={'textAlign': 'center'})
                        ),
                ], className = displayClass)
    else:
        output= dbc.Row([dbc.Col([ 
                            dbc.Alert("Ooops! It seems like you didn´t upload an apk file. Please try submitting again.", color="danger", className="col-8 m-auto text-center")
                        ])
                ], className = displayClass)
    return output
    


@callback(Output('loading', 'children'),

            [Input('apk-uploaded', 'contents'),
            State('apk-uploaded', 'filename'),],

            [Input('apk-uploaded2', 'contents'),
            State('apk-uploaded2', 'filename')],
            prevent_initial_call=True
        )      
def update_output(content, name, c2, n2):
    clearOlderAnalysis()
    triggered_id = ctx.triggered_id
    children = []
    if triggered_id == "apk-uploaded" and content is not None:
        children = [ parse_content(content, name, "m-3 d-none d-md-block") ]

    elif triggered_id == "apk-uploaded2" and c2 is not None:
        children = [ parse_content(c2, n2, "m-3 d-block d-md-none") ]

    return  children

def clearOlderAnalysis():
    logTheProgress("0", "0") 
    logTheProgress("0","0","Code")#clear the process log if we want to analyze more than one apk
    dir = "./UploadedAPKs/decompiledAPK/resources"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    dir = "./UploadedAPKs/decompiledAPK/sources"
    if os.path.exists(dir):
        shutil.rmtree(dir)
