import dash_table
import dash 
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html
from dash_extensions import Download

from graphs import * 

def Homepage():
  HomePage = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Upload(
    id='upload-data',
    children=html.Div([

     html.Button('Select Files',style={'display': 'inline-block','padding': '15px 25px', 'button-radius': '1px', 'cursor': 'pointer', 'text-align':'center', 'cursor': 'pointer',
  'color': 'white', 'font-weight':'bold','border-radius': '15px','box-shadow': '0 2px #999','backgroundColor':'#303030'},),
  
    ],style={'textAlign': 'center'}
    ),
   
    # Allow multiple files to be uploaded
    multiple=True
),
html.Br(),
    html.Br(),
    # html.Div(id='click'),
 
html.Div([
    html.Div([dcc.Loading(children=[  html.Div(id='output-data-upload', style ={ 'display' : 'flex', 'justify-content' : 'center'}),html.Br(),],type='circle'),
],style={'width':'500px'}),

  html.Br(),

html.Div([ html.Button('Clean Data',style={'display': 'inline-block', 'padding': '15px 25px','button-radius': '1px','cursor': 'pointer','text-align':'center',
  'cursor': 'pointer', 'color': 'white', 'font-weight':'bold','border-radius': '15px', 'box-shadow': '0 2px #999', 'backgroundColor':'#303030'},id='btn-1',n_clicks=0)],style={'height':'100px','width':'500px','left':'10%'}),
  


   
html.Div([dcc.Loading(children=[html.Div([html.Div(id='cleaned-data', style ={ 'display' : 'flex', 'justify-content' : 'center'}),])],type='circle')],style={'width':'500px'}),
html.Br(),


html.Div([html.Button("Download csv",style={'display': 'inline-block', 'padding': '15px 25px','button-radius': '1px','cursor': 'pointer','text-align':'center',
  'cursor': 'pointer', 'color': 'white', 'font-weight':'bold','border-radius': '15px', 'box-shadow': '0 2px #999', 'backgroundColor':'#303030'}, id="btnn"), Download(id="download")])
],
style={'position':'absolute','left':'45%','right':'20%','width':'500px'}
),


],style={}

)
  return HomePage


def Charts(cleaned_data):
    try:
        if cleaned_data == 0:
            print("No data")
            Charts = dbc.Container()
    except:        
        output_graph = RunGraph(cleaned_data)
        Charts = dbc.Container([html.Div(children = output_graph)])

    return Charts