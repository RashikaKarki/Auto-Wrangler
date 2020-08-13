
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import dash_table
import pandas as pd
import io
import numpy as mp
from visions.functional import detect_series_type, infer_series_type
from visions.typesets import StandardSet
from visions.typesets import StandardSet
from upload_file import *
from func import Main_func

typeset = StandardSet()
typeset.types


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#303030",
    
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    
}

sidebar = html.Div(
    [
        html.P("Data Analysis", className="display-4",style={'font-size':'1.2em','font-weight':'bold','color':'white','text-align':'center'}),
        html.Hr(style={'border':'1px solid white'}),
        
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/homepage", id="page-1-link", style={'text-align':'center','color':'white'}),
                dbc.NavLink("Data Overview", href="/page-2", id="page-2-link", style={'text-align':'center','color':'white'}),
                dbc.NavLink("Charts", href="/page-3", id="page-3-link", style={'text-align':'center','color':'white'}),
            ],
            vertical=True,
            # pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)





HomePage = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Upload(
    id='upload-data',
    children=html.Div([

        html.Button('Select Files',style={
  'display': 'inline-block',
  'padding': '15px 25px',
  'button-radius': '1px',
  'cursor': 'pointer',
  'text-align':'center',
  'cursor': 'pointer',
  'color': 'white',
  'font-weight':'bold',
  'border-radius': '15px',
  'box-shadow': '0 2px #999',
  'backgroundColor':'#303030'},
  
  
  )
    ],style={'textAlign': 'center'}
    ),
   
    # Allow multiple files to be uploaded
    multiple=True
),
html.Br(),
    html.Br(),
html.Div(id='output-data-upload', style ={ 'display' : 'flex', 'justify-content' : 'center'}),
# html.Div(id='handel_data_type)', style ={ 'display' : 'flex', 'justify-content' : 'center'}),

]
)


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)



homepage = html.Div([sidebar,HomePage],style=CONTENT_STYLE)
# content = html.Div(sidebar, style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), html.Div(id='page-content')])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/homepage" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    if pathname in ["/", "/homepage"]:
        return homepage
    elif pathname == "/page-2":
        return html.P("This is the content of page 2. Yay!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(Output('output-data-upload', 'children'),
      [Input('upload-data', 'contents'),
      Input('upload-data', 'filename')])

def update_table(contents, filename):
 table = html.Div()

 if contents:
    contents = contents[0]
    filename = filename[0]
    
# yo df lai initially print garnu paryo
    df= parse_data(contents, filename)

    df_nohead= parse_data_nohead(contents, filename)

# button click garera chai yo call hunu paryo ani spinner chalnu paryo ani table aaunu paryo
    df = Main_func(df, df_nohead)  

    table = html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns],
             style_table={
                            'padding':'15px',
                            'maxWidth':'900px',
                            'overflowX': 'scroll',
                            'maxHeight': '400px',
                            'overflowY': 'scroll',
                            'color' : 'black',
                           
                            
                            },
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[
                                {'if': {'column_id': 'comments'},
                                        'width': '30%'},]

        ),
       
    ],style={'color':'green'} )
 
 return table


if __name__ == "__main__":
    app.run_server(port=8888)