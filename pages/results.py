from dash import Input, Output, callback, html
import pandas as pd
import dash_bootstrap_components as dbc
import dash
from assets import Utils


dash.register_page(__name__, path='/results')

layout = dbc.Container([
    dbc.Row([
        html.H1("Results of the application analysis", className="my-4"),
        html.Hr()
    ]),
    dbc.Tabs(
    [
        dbc.Tab(label="Classes of the App", tab_id="classes"),
        dbc.Tab(label="Query a class", tab_id="query"),

    ], id="tabs", active_tab="classes",
    ),
    dbc.Row(id="tab-content", className="p-4"),

])
def getData():
    with open('./UploadedAPKs/apknames.txt', 'r') as f:
        lines = f.readlines()
        apkName = lines[-1].replace("\n", "").replace(".apk","")
    f.close()
    df = pd.read_csv("./UploadedAPKs/classesSummarized_"+apkName+".csv")
    return df

@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab :
        if active_tab == "classes":
            return  [html.H5("You can select a cell with one click and use your keyboard shorcut to copy the content and then paste it on the Query´s Search bar."),
                    Utils.createTable(getData())]

        elif active_tab == "query":
            return renderQueryTab()
    return "No tab selected"
def renderQueryTab():
    body = html.Div([
        dbc.Row([html.Div(["Query a class for the details. "], className="text-dark")]),
        Utils.search_bar, #id="search_class"
        html.Div([],id="class_details")
    ])
    return body

@callback(
    Output("class_details", "children"),
    [Input("search_class", "value")],
    prevent_initial_call=True
)
def update_output(class_):
    df = getData()
    class_=str(class_).replace('"', '').replace(" ", "")
    mask = df['Classes']== class_
    summary = df[mask]["Summaries"]
    if summary.empty:
        return [html.P(["Input Error! - The class introduced <", class_,"> is not in the APK"], className="text-danger")]
    else:
        children = [
        dbc.Row([
            html.H3(["Details of the class: ", html.Span(["{}".format(class_)], className = "text-info")], className=""),
            html.Hr()
        ]),
        dbc.Row([
            html.H5("Summary", className=""),
        ]),
        dbc.Row([
            html.P(summary)
        ]),
        html.Br(),
        html.Br(),
        dbc.Row([
            html.H4(["Methods associated to the class: ", html.Span(["{}".format(class_)], className = "text-info")], className=""),
            html.Hr()
        ]),
        dbc.Row([
            Utils.accordion_with_methods(class_),
        ])
        ]
        return children

