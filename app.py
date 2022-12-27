from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from assets import Utils

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP],suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    Utils.navbar, 
    dbc.Container([    
        dash.page_container
    ])
])

if __name__ == '__main__':
	app.run_server(debug=True)