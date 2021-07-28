import pandas as pd

import numpy as np

import requests

from bs4 import BeautifulSoup

import plotly.express as px

import plotly.graph_objects as go

import dash

import dash_html_components as html

import dash_core_components as dcc

from dash.dependencies import Input, Output

import requests

import json


# First get the data using the worldometer website which shows updated data for cases of COVID for each day.


url="https://www.worldometers.info/coronavirus/?from=groupmessage&isappinstalled=0&nsukey=yt0agaqvkr89bjtpnmm8m9vla/v5edttqdsdc5nug+dpwiyqiztyw/a2kv2kykkhkildmtxxff3fspv4mlgxh14hrlhuhqc5lfpfyov0tsx5mgezbomly6ywn3iyb8lmut2kai5oc79105ep7i4rckdq4j3xbq2nmo6ovqzhzythjnyfndmyuyhmgq/9janotm+ghsxygi6zvo32lbix6g==&__cf_chl_captcha_tk__=b896c97a0f6870fb9662fa9a0541b3d34ab3575c-1584097489-0-ar66lqtkk5u1w0dytl4fjv_gz2qvpld8fkhuznqxfa2nfzmzeqwqhktuxdiom33ccokbmbx7bdp_po_mvsqqshpejjz_s-tlfoug0wdzzxhng_rbmj5gkn_h#countries"

data = requests.get(url).text

soup = BeautifulSoup(data,"html.parser")


table = soup.find("table")

covidData = pd.DataFrame(columns = ['Country','Total Cases','New Cases','Total Deaths',
                                    'New Deaths','Total Recovered','New Recovered','Active Cases','Serious Cases',
                                    'Total Cases/1M pop','Deaths/1M pop','Total Tests','Tests/1M pop','Population'],dtype="float")
for row in table.find_all('tr'):
    col = row.find_all('td')
    
    if(col != [] and row.find_all('a',href=True)):
        col_1 = col[1].text
        col_2 = col[2].text.replace(',','').replace('+','')
        col_3 = col[3].text.replace('+','').replace(',','')
        col_4 = col[4].text.replace(',','').replace('+','')
        col_5 = col[5].text.replace(',','').replace('+','')
        col_6 = col[6].text.replace(',','').replace('+','')
        col_7 = col[7].text.replace(',','').replace('+','')
        col_8 = col[8].text.replace(',','').replace('+','')
        col_9 = col[9].text.replace(',','').replace('+','')
        col_10 = col[10].text.replace(',','').replace('+','')
        col_11 = col[11].text.replace(',','').replace('+','')
        col_12 = col[12].text.replace(',','').replace('+','')
        col_13 = col[13].text.replace(',','').replace('+','')
        col_14 = col[14].text.replace(',','').replace('+','')
        
        covidData = covidData.append({'Country':col_1,'Total Cases':col_2,'New Cases':col_3,'Total Deaths':col_4,
                                    'New Deaths':col_5,'Total Recovered':col_6,'New Recovered':col_7,'Active Cases':col_8,
                                    'Serious Cases':col_9,'Total Cases/1M pop':col_10,'Deaths/1M pop':col_11,
                                    'Total Tests':col_12,'Tests/1M pop':col_13,'Population':col_14}, ignore_index=True)
        
# covidData


# Time to clean the data and format each columns. We first remove all the NaN values from the data by dropping the columns containing NaN values because as our countries are rows, and we don't want to remove any country name. And also we will convert the dtype of columns to float/int because if we want to show the data on world_map using folium then it only works for float/int type variables.

covidData = covidData.replace(r'^\s*$', np.NaN, regex=True)
covidData = covidData.replace('N/A',np.nan,regex=True)
columnName = covidData.columns
# covidData.info()
for col in columnName[1:]:
    covidData[col] = pd.to_numeric(covidData[col])


# columnName[1:]

# covidData.head()

#Now as folium requires a json file containing the boundaries of states and countries, to plot our dataset on it, we load that json file. 

url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'

res = requests.get(url).json()
# res


# covidData.head(20)
# covidData.dtype

# countryName = list(covidData['Country'])
# test=covidData[covidData['Country']=='India']
copyData = covidData
copyData.replace(0.0,np.nan,inplace=True)
# data=copyData.dropna(subset=['Total Cases'],axis=0)
# data.sort_values('Total Cases',ascending=False,inplace=True)
# datause=data.tail()
# data

# fig=px.pie(covidData, values='Total Recovered',names='Country')
# data=copyData.dropna(subset=['Active Cases'],axis=0,inplace=True)
# data.sort_values('Active Cases',ascending=False,inplace=True)
# fig = px.sunburst(datause,path=['Country'],values='Total Cases',color='Country')
# # fig.show()
# data.tail()
# copyData.tail()
# covidData['New Cases'].head()


#The choropleth map according to the current Total Cases data of each country can be seen.
# One can compare this data for the countries using the plotly.express's bubble map which I am gonna show on the dashboard too.

# px.scatter(covidData,x ='Population',y='Total Cases',
#           size='Total Cases',color='Country',
#           hover_name='Country',log_x=True,size_max=60)

animData = covidData.melt(id_vars=covidData.columns[0:1],
                         value_vars=covidData.columns[1:],
                         var_name='Var',value_name='Value')

# # animData.head()
# fig=px.choropleth(animData,locations='Country',locationmode='country names',
#                  color='Value',animation_frame='Var',
#                  basemap_visible=False,
#                  color_continuous_scale='mint',
#                     title=('Country Wise COVID Report')
#                  )
# fig.update_layout(height=600)
# fig.show()

from jupyter_dash import JupyterDash

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div(children = [html.H1("Covid Dashboard",style={'textAlign':'center','color':'#503D36',
                                                                   'font-size':40,'font-family': 'cursive',
                                                                  }),
                                  html.Div([
                                      html.Div([
                                          html.H2("Covid Report For:  ",style={'margin-left':'50px','font-size':'30px','margin-top':'42px'})
                                      ]),
                                      
                                      dcc.Dropdown(id = 'input-type',
                                                   options = [{'label':i, 'value':i } for i in columnName[1:]],
                                                   value='Total Cases',
                                                   placeholder = "Select Factor",
                                                   style={'width':'60%', 'padding':'3px', 
                                                          'font-size': '18px',
                                                          'font-family': 'cursive','margin-left':'10px','margin-top':'20px'})
                                  ], style={'display':'flex'}),
                                  html.Br(),
                                  html.Br(),
                                  html.Div(dcc.Graph(id='fig')),
                                  html.Br(),
                                  html.Br(),
                                  html.H2("Country Wise COVID Report", style={'align-right':'1.5em','font-family':'cursive'}),
                                  html.Div(dcc.Graph(id='map')),
                                  html.Br(),
                                  html.Br(),
                                  html.Div([
                                      html.Div(dcc.Graph(id='sun')),
                                      html.Br(),
                                      html.Br(),
                                      html.Div(dcc.Graph(id='sund'))
                                      
                                  ],style={'display':'flex','flex-direction':'row','margin-left':'8px'})
                                  
                                  ])

@app.callback([Output(component_id = 'fig',component_property='figure'),
               Output(component_id='map',component_property='figure'),
              Output(component_id='sun',component_property='figure'),
              Output(component_id='sund',component_property='figure')],
             Input(component_id='input-type',component_property='value'))
#              Input(component_id='country',component_property='value')
#              State('plot','children'))



def get_graph(value):
    
    fig = px.scatter(covidData,x ='Population',y='{}'.format(value),
          size='Population',color='Country',
          hover_name='Country',log_x=True,size_max=60)
#     fig.update_yaxes(rangemode="tozero")
    fig.update_layout(height=500,
                       font_family="cursive",
                      font_size=20,
                       font_color="black",)
    
    fig2=px.choropleth(animData,locations='Country',locationmode='country names',
                 color='Value',animation_frame='Var',
                 basemap_visible=False,
                 color_continuous_scale='mint'
                 )
    fig2.update_layout(height=600,
                       font_family="cursive",
                       font_size=20,
                       font_color="black",)
    
    if(value=='Total Cases' or value=='Total Tests' or value=='New Cases'):
        data=copyData.dropna(subset=['{}'.format(value)],axis=0)
        data['{} Rate'.format(typec)]=(data['{}'.format(value)]/data['Population'])*100
        data.sort_values('{} Rate'.format(value),ascending=False,inplace=True)
        useDataHead=data.head()
        useDataTail=data.tail()
        fig3 = px.sunburst(useDataHead,path=['Country'],
                       values='{} Rate'.format(value),color='Country',
                       hover_data={'Population','{}'.format(value)},
                       title="{} As Factor-> Top Five Performer Countries".format(value),
                      )
        
        fig4 = px.sunburst(useDataTail,
                       path=['Country'],
                       values='{} Rate'.format(value),
                       hover_data={'Population','{}'.format(value)},
                       color='Country',title="{} As Factor-> Bottom Five Performer Countries".format(value),
                      )
    elif(value=='Total Deaths' or value=='Total Recovered' or 
            value=='New Deaths' or value=='New Recovered' or value=='Active Cases' or value=='Serious Cases'):
        data=copyData.dropna(subset=['{}'.format(value)],axis=0)
        data['{} Rate'.format(value)]=(data['{}'.format(value)]/data['Total Cases'])*100
        data.sort_values('{} Rate'.format(value),ascending=False,inplace=True)
        useDataHead=data.head()
        useDataTail=data.tail()
        fig3 = px.sunburst(useDataHead,path=['Country'],
                       values='{} Rate'.format(value),color='Country',
                       hover_data={'Total Cases','{}'.format(value)},
                       title="{} As Factor-> Top Five Performer Countries".format(value),
                      )
        
        fig4 = px.sunburst(useDataTail,
                       path=['Country'],
                       values='{} Rate'.format(value),
                       hover_data={'Total Cases','{}'.format(value)},
                       color='Country',title="{} As Factor-> Bottom Five Performer Countries".format(value),
                      )
    else:
        data=copyData.dropna(subset=['{}'.format(value)],axis=0)
        data.sort_values('{}'.format(value),ascending=False,inplace=True)
        useDataHead=data.head()
        useDataTail=data.tail()
        fig3 = px.sunburst(useDataHead,path=['Country'],
                       values='{}'.format(value),color='Country',
                       hover_data={'Population','{}'.format(value)},
                       title="{} As Factor-> Top Five Performer Countries".format(value),
                      )
        
        fig4 = px.sunburst(useDataTail,
                       path=['Country'],
                       values='{}'.format(value),
                       hover_data={'Population','{}'.format(value)},
                       color='Country',title="{} As Factor-> Bottom Five Performer Countries".format(value),
                      )
    
    fig3.update_layout(height=600,
                       font_family="cursive",
                       font_color="black",
                       font_size=16,
                       title_font_family="cursive",
                       title_font_color="black")
    
    fig4.update_layout(height=600,
                       font_family="cursive",
                       font_color="black",
                       font_size=16,
                       title_font_family="cursive",
                       title_font_color="black")
    
    
    return fig,fig2,fig3,fig4

if __name__=='__main__':
    app.run_server(debug=True, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')

