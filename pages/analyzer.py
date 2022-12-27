import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

import subprocess
from assets.Decompile import getNumberOfMethods, decompileAPK
import threading

dash.register_page(__name__, path='/analyzer')

modalAnalysisFinished = dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Success!")),
                dbc.ModalBody("Thanks for waiting. Finally your APK has been analyzed."),
                dbc.ModalFooter(
                    dbc.Button("Click to check the results", color="success", className="me-1", href="/results")
                ), ],is_open=True,)

methodProgress = dbc.Col(
        html.Div([
            html.H3("Explaining the purpose of each method on the apk..."),
            html.Hr(),
            dcc.Interval(id="progress-interval", interval=500),
            dbc.Progress(id="progress", color="success", animated=True, striped=True, className="border border-info", style={"height": "30px", 'backgroundColor': '#FFFFFF'}),
        ]   ,className="h-100 p-5 bg-light border rounded-3",
        ), className="my-2 col-12 col-lg-6")

classProgress =dbc.Col(
        html.Div([
        html.H3("Making a summary of all the methods of each class contained on the apk..."),
        html.Hr(),
        dcc.Interval(id="progress-interval2", interval=600),
        dbc.Progress(id="progress2", color="success", animated=True, striped=True, className="border border-info", style={"height": "30px", 'backgroundColor': '#FFFFFF'}),
            ]  , className="h-100 p-5 bg-light border rounded-3",
        ), className="my-2 col-12 col-lg-6")

layout =  dbc.Container([
    dbc.Row(dbc.Col([
        dbc.Button("Decompile the app", color="warning", className="me-1", id="jadx", n_clicks=0),
    ],  style={'textAlign': 'center'}), className="m-3"
    ),
    dbc.Row(dbc.Col([
        dbc.Button("Compute the analysis", color="danger", outline=True, className="me-1", id="start-analysis", n_clicks=0),
    ],  style={'textAlign': 'center'}), className="m-3"
    ),
    dbc.Row(
        [methodProgress, classProgress],
        className="align-items-md-stretch justify-content-center ",
    ),
    html.Div(id="jadx-output"),
    html.Div(id="done"),

    dbc.Row(dbc.Col(
        id="a",  style={'textAlign': 'center'} ),
    ),
    html.Div(id="hidden-div", style={"display":"none"}),
])

def getAPKName():
    with open('./UploadedAPKs/apknames.txt', 'r') as f:
        lines = f.readlines()
        apkName = lines[-1].replace("\n", "")
    f.close()
    return apkName

@callback(
    Output("jadx-output", "children"), [Input("jadx", "n_clicks")],
        prevent_initial_call=True
)
def jadxOutput(n):
    if n == 1:
        decompileAPK(getAPKName())
    with open('./UploadedAPKs/JadxOutput.log', 'r') as f:
            file_content = f.readlines()
    f.close()
    return [
            dbc.Row(dbc.Col([
                    html.H4("The output produced by JADX on the decompiled APK is:"),
                        html.Hr(className="my-2"),    
                    ]), className="mx-4 my-3"
            ),
            dbc.Row(dbc.Col([
                html.Div(file_content)
                ], style={'fontFamily': 'monospace','whiteSpace': 'pre-wrap','backgroundColor': '#2B2B2B','color': '#FFFFFF','padding': '20px','fontSize': '14px'}
                ), className="mx-5")
        ]     
@callback(
    Output("hidden-div", "children"), [Input("start-analysis", "n_clicks")],
    prevent_initial_call=True
)
def startAnalysis(n):
    if n==1:
        thread = threading.Thread(target=subprocess.call(["python3", "./assets/codeT5.py", getAPKName(), str(getNumberOfMethods())], shell=True))
        thread.start()
    return []

@callback(
    [Output("progress", "value"), Output("progress", "label")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    try:
        with open("./UploadedAPKs/progresslogCodeT5.log", mode='r', encoding='utf-8') as plog: 
            progressFormated=plog.readline()
        plog.close()
        if "Done" in progressFormated:
            return 100, "100 %"
        else:
            progressFormated = progressFormated.split("/")
            progress = int(progressFormated[0])*100//int(progressFormated[1])
            return progress, "{} %".format(progress)
    except Exception as e:
        return 0, "0 %"

@callback(
    [Output("progress2", "value"), Output("progress2", "label"), Output("done", "children")],
    [Input("progress-interval2", "n_intervals")],
)
def update_progress(n):
    try:
        with open("./UploadedAPKs/progresslogT5.log", mode='r', encoding='utf-8') as plog: 
            progressFormated=plog.readline()
        plog.close()
        if "Done" in progressFormated:
            return 100, "100 %", modalAnalysisFinished
        else:
            progressFormated = progressFormated.split("/")
            progress = int(progressFormated[0])*100//int(progressFormated[1])
            return progress, "{} %".format(progress), []
    except Exception as e:
        return 0, "0 %", []
