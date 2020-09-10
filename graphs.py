import plotly.express as px
from clean_module import *
import dash_bootstrap_components as dbc
import dash_core_components as dcc 
import dash_html_components as html
#Numerical
def HistChart(data,colnum):
    title_plot = "Histogram of "+colnum
    fig = px.histogram(data, x = colnum, title=title_plot, labels={colnum:colnum})
    fig.update_xaxes(tickangle=70)
    return fig

def PieChart(data,colcat):
    labels = data[colcat].value_counts().index
    values = data[colcat].value_counts().values
    fig = px.pie(values = values, names = labels, title="Pie Chart of "+ colcat)
    return fig

#Numerical
def ViolinChartsecond(data,colcat,colnum):
    fig = px.violin(data, y=colnum, x=colcat, box=True, color = colcat, points="all", title = "Violin Plot between "+ colcat + " and "+ colnum)
    fig.update_xaxes(tickangle=70)
    return fig

def LineChart(data,colDate,colnum):
    year_name = colDate+'_year'
    data[year_name] = pd.DatetimeIndex(data[colDate]).year
    title = 'Line Chart between ' + str(colDate) + ' and ' + str(colnum)
    fig = px.line(data, x=year_name, y=colnum, title=title)
    return fig

def bivariate(data, data_type, cat_col,  output):
    for i in cat_col:
        for (columnName, columnData) in data.iteritems():
            if (data_type[columnName] == "integer") or (data_type[columnName] == "Float"):
                output.append(ViolinChartsecond(data,i,columnName))
    return output

def bivariate2(data, data_type, date_col,output):
    for i in date_col:
        for (columnName, columnData) in data.iteritems():
            if (data_type[columnName] == "integer") or (data_type[columnName] == "Float"):
                output.append(LineChart(data,i,columnName))
    return output


def graphmain(data):
    output = []
    cat_col = []
    date_col = []
    data_type = Datatype(data)
    for (columnName, columnData) in data.iteritems():
        if (data_type[columnName] == "Integer") or (data_type[columnName] == "Float"):
            output.append(HistChart(data,columnName))  
        if (data_type[columnName] == "String") or (data_type[columnName] == "Boolean"):
            if (data_type[columnName] == "Boolean"):
                output.append(PieChart(data,columnName))
            if (data.shape[0] < 1000) and (data[columnName].nunique() <= data.shape[0]*0.01):
                cat_col.append(columnName)      
                output.append(PieChart(data,columnName))
            elif(data.shape[0] > 1000) and (data[columnName].nunique() <= 20):
                cat_col.append(columnName)
                output.append(PieChart(data,columnName))
        if data_type[columnName] == "DateTime":
            date_col.append(columnName)
    output = bivariate(data, data_type, cat_col, output)
    output = bivariate2(data, data_type,date_col,output)

    return output


def RunGraph(df):
    output_graph = []
    outputs = graphmain(df)
    for output in outputs:
        output_graph.append(dbc.Row([               
                dbc.Col(
                    [
                            dcc.Graph(figure = output)

                    ]
                ),
                
            ]))

    return output_graph