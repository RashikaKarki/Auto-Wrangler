
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import base64
import dash_table
import pandas as pd
import io
import numpy as mp

from visions.functional import cast_to_inferred, detect_type, infer_type
from visions.typesets import StandardSet

import plotly.express as px
from dash_extensions.snippets import send_data_frame


from data_cleaner import Main_func
from pages import Homepage, Charts
from graphs import *
from parse_data import  parse_data_nohead, parse_data


typeset = StandardSet()
typeset.types

global cleaned_data

cleaned_data = 0

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "1rem 1rem",
    "background-color": "#303030",
    
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    
}

sidebar = html.Div(
    [
        html.P("Data Analysis", className="display-4",style={'font-size':'1.2em','font-weight':'bold','color':'white','text-align':'center'}),
        html.Hr(style={'border':'1px solid white'}),
        
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/homepage", id="page-1-link", style={'text-align':'center','color':'white'}),
                dbc.NavLink("Data Overview", href="/overview", id="page-2-link", style={'text-align':'center','color':'white'}),
                dbc.NavLink("Charts", href="/charts", id="page-3-link", style={'text-align':'center','color':'white'}),
            ],
            vertical=True,
            # pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


homepage = Homepage()

Overview =  html.Div([
    html.H1("This is overview")
])




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)


homepage = html.Div([sidebar,homepage],style=CONTENT_STYLE)
overview = html.Div([sidebar,Overview],style=CONTENT_STYLE)


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
    elif pathname == "/overview":
        return overview
    elif pathname == "/charts":
        return html.Div([sidebar,Charts(cleaned_data)],style=CONTENT_STYLE)
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
      Input('upload-data', 'filename')]
      )

def update_table(contents, filename):
 table = html.Div()

 if contents:
    contents = contents[0]
    filename = filename[0]

    df = parse_data(contents, filename)


# button click garera chai yo call hunu paryo ani spinner chalnu paryo ani table aaunu paryo
    # df = Main_func(df, df_nohead)  

    table = html.Div([
        html.H5(filename,style={'color':'black'}),
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
        html.Br(),
   
    ],style={'color':'green','text-align':'center'} ),

 return table

    
@app.callback(Output('cleaned-data', 'children'),
              [Input('btn-1', 'n_clicks'),
              Input('upload-data', 'contents'),
           Input('upload-data', 'filename')]
              )

def click(btn,contents,filename):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-1' in changed_id:
       x=2
      
       table_2 = html.Div()

       if contents:
         contents = contents[0]
         filename = filename[0]
     
# yo df lai initially print garnu paryo
         df = parse_data(contents, filename)

        #  df_nohead = parse_data_nohead(contents, filename)

# button click garera chai yo call hunu paryo ani spinner chalnu paryo ani table aaunu paryo
         
         df = Main_func(df)  
         global cleaned_data
         cleaned_data = df

         table_2 = html.Div([
         html.Br(),
        
        
        
        html.Hr(),
       
        html.Br(),
        html.P("Cleaned Data: ",style={'font-size':'1.2em','font-weight':'bold','color':'black','text-align':'left'}),

        html.H5(filename,style={'color':'black'}),
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
 
       return table_2   




     
@app.callback(Output("download", "data"), [Input("btnn", "n_clicks"), Input('upload-data', 'contents'),
           Input('upload-data', 'filename')])

def download(btn,contents,filename):
    global df
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btnn' in changed_id:

       if contents:
         contents = contents[0]
         filename = filename[0]
     

         df = parse_data(contents, filename)
         df = Main_func(df)  

       return send_data_frame(df.to_csv, filename=filename)     


         


if __name__ == "__main__":
    app.run_server()