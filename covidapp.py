import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input,Output
from io import StringIO
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

url="https://datahub.io/core/covid-19/r/worldwide-aggregated.csv"

s=requests.get(url, headers= headers).text

df_world=pd.read_csv(StringIO(s)) ## worldwide-aggregated

url="https://datahub.io/core/covid-19/r/countries-aggregated.csv"
s=requests.get(url, headers= headers).text

df_con=pd.read_csv(StringIO(s)) ## countries-aggregated

url="https://datahub.io/core/covid-19/r/key-countries-pivoted.csv"
s=requests.get(url, headers= headers).text

df_key=pd.read_csv(StringIO(s)) ## key-countries-pivoted


url="https://datahub.io/core/covid-19/r/time-series-19-covid-combined.csv"
s=requests.get(url, headers= headers).text

df_t=pd.read_csv(StringIO(s)) ## time series



df_world['Date'] = pd.to_datetime(df_world['Date'])
df_con['Date'] = pd.to_datetime(df_con['Date'])
df_key['Date'] = pd.to_datetime(df_key['Date'])
df_t['Date'] = pd.to_datetime(df_t['Date'])

df_world['Increase rate'].fillna(0, inplace = True)


activ = df_world['Confirmed']-df_world['Recovered']
df_world['Active'] = activ
mot = ((df_world['Deaths']/df_world['Confirmed'])*100)
df_world['Mortality_rate'] = mot

n = df_world.shape[0]
info=df_world.iloc[n-1:]
confirmcase = info['Confirmed'].values[0]
recovercase=info['Recovered'].values[0]
deathcase=info['Deaths'].values[0]



df_c = df_con.copy()
df_c.drop(columns=['Date'],inplace=True)
df_c.drop_duplicates(subset='Country',keep='last',inplace = True)


symp = pd.read_csv('symval.csv')





options=[
    {'label':'Confirmed','value':'Confirmed'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deaths','value':'Deaths'}

]

opt=[
    {'label':'All','value':'All'},
    {'label':'Confirmed','value':'confirmed'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deaths','value':'Deaths'}


]




external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout=html.Div([
    html.Div([
        html.Div([
            html.H1("Covid_19_World_Wide_Analysis",style={'color':'#fff','text-align':'center'}),
        ],className='col-md-12')
    ],className='row'),


    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases :", className='text-light'),
                    html.H4(confirmcase, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered :", className='text-light'),
                    html.H4(recovercase, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths :", className='text-light'),
                    html.H4(deathcase, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-4')
    ], className='row'),








    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options, value='Confirmed'),
                    dcc.Graph(id='map')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='bar-plot',figure={'data':[go.Bar(x=df_world['Date'],y=df_world['Mortality_rate'])],
                                                    'layout':go.Layout(title='Mortality Rate Percentage')})

                ],className='cart-body')
            ],className='card')
        ],className='col-md-12'),
        ],className='row'),










    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='pie-chart',figure={'data':[go.Pie(labels=symp['symptoms'],values=symp['values'])],
                                                     'layout':go.Layout(title='Symtoms Found')})
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='pick',options=opt, value='All'),
                    dcc.Graph(id='line')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ], className='row'),
], className='container')




@app.callback(Output('line','figure'),[Input('pick','value')])
def update_graph(valu):
    if valu == 'All':
        trace1 = go.Scatter(x=df_world['Date'], y=df_world['Confirmed'], mode='lines+markers',
                            marker={'color': '#000000'}, name='Confirmed')
        trace = go.Scatter(x=df_world['Date'], y=df_world['Recovered'], mode='lines+markers',
                           marker={'color': '#FFFF00'}, name='Recovered')
        trace2 = go.Scatter(x=df_world['Date'], y=df_world['Deaths'], mode='lines+markers', marker={'color': '#FF0000'},
                            name='Deaths')


        layout = go.Layout(title='Day By Day Overall Reacords', xaxis={'title': 'Dates'},
                           yaxis={'title': 'No Of Peoples'})
        return {'data': [trace1,trace,trace2],
            'layout': layout}
    elif valu == 'Confirm':
        trace1 = go.Scatter(x=df_world['Date'], y=df_world['Confirmed'], mode='lines+markers',
                            marker={'color': '#000000'}, name='Confirmed')
        layout = go.Layout(title='Day By Day Confirmed Case Reacords', xaxis={'title': 'Dates'},
                           yaxis={'title': 'No Of Peoples'})
        return {'data': [trace1],
                'layout': layout}
    elif valu == 'Recovered':
        trace = go.Scatter(x=df_world['Date'], y=df_world['Recovered'], mode='lines+markers',
                           marker={'color': '#FFFF00'}, name='Recovered')
        layout = go.Layout(title='Day By Day Recovered Case Reacords', xaxis={'title': 'Dates'},
                           yaxis={'title': 'No Of Peoples'})
        return {'data': [trace],
                'layout': layout}
    else:
        trace2 = go.Scatter(x=df_world['Date'], y=df_world['Deaths'], mode='lines+markers', marker={'color': '#FF0000'},
                            name='Deaths')

        layout = go.Layout(title='Day By Day Deaths Reacords', xaxis={'title': 'Dates'},
                           yaxis={'title': 'No Of Peoples'})
        return {'data': [trace2],
                'layout': layout}








@app.callback(Output('map','figure'),[Input('picker','value')])
def update_map(type):
    if type == 'Confirmed':
        trace = dict(type='choropleth',
                     locations=df_c['Country'],
                     locationmode='country names',
                     autocolorscale=False,
                     colorscale='Rainbow',
                     marker=dict(line=dict(color='rgb(255,255,255)', width=1)),
                     z=df_c['Confirmed'], colorbar={'title': 'Colour Range', 'len': 0.5})

        layout = dict(title="Today's View On Confirmed Cases")
        return {'data': [trace],
                'layout': layout}
    elif type == 'Recovered':
        trace = dict(type='choropleth',
                     locations=df_c['Country'],
                     locationmode='country names',
                     autocolorscale=False,
                     colorscale='Rainbow',
                     marker=dict(line=dict(color='rgb(255,255,255)', width=1)),
                     z=df_c['Recovered'], colorbar={'title': 'Colour Range', 'len': 0.5})

        layout = dict(title="Today's View On Recovered")
        return {'data': [trace],
                'layout': layout}
    else:
        trace = dict(type='choropleth',
                     locations=df_c['Country'],
                     locationmode='country names',
                     autocolorscale=False,
                     colorscale='Rainbow',
                     marker=dict(line=dict(color='rgb(255,255,255)', width=1)),
                     z=df_c['Deaths'], colorbar={'title': 'Colour Range', 'len': 0.5})

        layout = dict(title="Today's View On Deaths")
        return {'data': [trace],
                'layout': layout}











if __name__=="__main__":
   app.run_server(debug=False)