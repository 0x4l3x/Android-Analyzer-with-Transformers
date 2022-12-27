import dash_bootstrap_components as dbc
from dash import dash_table, html
import pandas as pd

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("About", href="/results")),
    ],
    brand="Transformers",
    brand_href="/",
    color="primary",
    dark=True,
)

search_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Input(type="search", placeholder="Search", id="search_class", debounce=True)
        ),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="m-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 m-auto flex-nowrap",
    align="center",
)

def logTheProgress(counter, totalMethods, file=""):
    with open("./UploadedAPKs/progresslog"+file+"T5.log", "w") as f:
        f.write(str(counter)+"/"+str(totalMethods))
    f.close()

def createTable(df):
    table= dash_table.DataTable(
    data=df[["Classes", "Summaries"]].to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df[["Classes", "Summaries"]].columns],
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'textAlign': 'left',
    },
    tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        }   
        for row in df[["Classes", "Summaries"]].to_dict('records')
    ],
    tooltip_duration=None,

    id='tbl'
) 
    return table
def getHeader(method):
    index = method.find('{')
    header = method[:index]
    return header

def methodDescription(summary, method):
    return html.Div([
    dbc.Row(dbc.Col([
        html.H6("Method summary:"),
        html.Div([summary], className="bg-light border rounded-3 p-2 mb-2")
        ]), className="mx-2 "
    ),
    dbc.Row(dbc.Col([
        html.H6("Method code:"),
        html.Div([method], className="border rounded-3", style={'fontFamily': 'monospace','whiteSpace': 'pre-wrap','backgroundColor': '#2B2B2B','color': '#FFFFFF','padding': '20px','fontSize': '14px'})
        ]), className="mt-2, mx-2"
    )
    ], ) 
def accordion_with_methods(class_):
    with open('./UploadedAPKs/apknames.txt', 'r') as f:
        lines = f.readlines()
        apkName = lines[-1].replace(".apk","").replace("\n", "")
    f.close() #cambiar apkName
    df = pd.read_csv("./UploadedAPKs/"+apkName+".csv")
    mask = df['Path']== class_
    data = df[mask]
    items=[]
    for i in range(len(data)):
        header = getHeader(data.iloc[i]["Method"])
        method = data.iloc[i]["Method"]
        summary = data.iloc[i]["Summary"]
        items.append(dbc.AccordionItem([methodDescription(summary, method)], title="Method {}".format(header), ))

    accordion = html.Div([
                        dbc.Accordion(
                            items,
                            flush=True,
                            start_collapsed=True,
                        ),
                ])
    return accordion

