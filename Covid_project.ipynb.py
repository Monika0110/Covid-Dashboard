#!/usr/bin/env python
# coding: utf-8

# ### The idea is to make an interactive dashboard showing COVID cases and population of countries, one can set the variable to compare all the countries. 

# In[ ]:





# In[1]:


import pandas as pd

import numpy as np

import requests

import folium

from bs4 import BeautifulSoup

import plotly.express as px

import plotly.graph_objects as go

import dash

import dash_html_components as html

import dash_core_components as dcc

from dash.dependencies import Input, Output

import requests

import json

from flask import Flask

import os

# #### First get the data using the worldometer website which shows updated data for cases of COVID for each day.

# In[2]:


url="https://www.worldometers.info/coronavirus/?from=groupmessage&isappinstalled=0&nsukey=yt0agaqvkr89bjtpnmm8m9vla/v5edttqdsdc5nug+dpwiyqiztyw/a2kv2kykkhkildmtxxff3fspv4mlgxh14hrlhuhqc5lfpfyov0tsx5mgezbomly6ywn3iyb8lmut2kai5oc79105ep7i4rckdq4j3xbq2nmo6ovqzhzythjnyfndmyuyhmgq/9janotm+ghsxygi6zvo32lbix6g==&__cf_chl_captcha_tk__=b896c97a0f6870fb9662fa9a0541b3d34ab3575c-1584097489-0-ar66lqtkk5u1w0dytl4fjv_gz2qvpld8fkhuznqxfa2nfzmzeqwqhktuxdiom33ccokbmbx7bdp_po_mvsqqshpejjz_s-tlfoug0wdzzxhng_rbmj5gkn_h#countries"

data = requests.get(url).text

soup = BeautifulSoup(data,"html.parser")


# In[3]:


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


# ### Time to clean the data and format each columns. We first remove all the NaN values from the data by dropping the columns containing NaN values because as our countries are rows, and we don't want to remove any country name. And also we will convert the dtype of columns to float/int because if we want to show the data on world_map using folium then it only works for float/int type variables.

# In[5]:


covidData = covidData.replace(r'^\s*$', np.NaN, regex=True)
covidData = covidData.replace('N/A',np.nan,regex=True)
columnName = covidData.columns
# covidData.info()
for col in columnName[1:]:
    covidData[col] = pd.to_numeric(covidData[col])


# columnName[1:]

# covidData.head()


# ### Now as folium requires a json file containing the boundaries of states and countries, to plot our dataset on it, we load that json file. 

# In[6]:


url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'

res = requests.get(url).json()
# res


# In[7]:



# create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

world_map.choropleth(geo_data=res,
                     data = covidData,
                  columns=['Country','Total Cases'],
                  key_on='feature.properties.name',
                  fill_color='YlGn',
                  fill_opacity=0.7,
                  line_opacity=0.2,
                  legend_name='Country vise Covid Report')


# In[8]:


# world_map


# In[23]:


# world_map
covidData.head(20)
# covidData.dtypes


# ### The choropleth map according to the current Total Cases data of each country can be seen.
# ### One can compare this data for the countries using the plotly.express's bubble map which I am gonna show on the dashboard too.

# In[24]:


px.scatter(covidData,x ='Population',y='Total Cases',
          size='Total Cases',color='Country',
          hover_name='Country',log_x=True,size_max=60)


# In[25]:


app = dash.Dash(__name__)
server = app.server

# server = Flask(__name__)
# server.secret_key = os.environ.get('secret_key', 'secret')
# app = dash.Dash(name = __name__, server = server)
# app.config.supress_callback_exceptions = True

app.layout = html.Div(children = [html.H1("Covid Dashboard",style={'textAlign':'center','color':'#503D36','font-size':40}),
                                  html.Div([
                                      html.Div([
                                          html.H2("Covid Report For: ",style={'align-right':'2em'}),
                                      ]),
                                      
                                      dcc.Dropdown(id = 'input-type',
                                                   options = [{'label':i, 'value':i } for i in columnName[1:]],
                                                   value="Total Cases",
                                                   placeholder = "Select type",
                                                   style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                  ], style={'display':'flex'}),
                                  html.Br(),
                                  html.Br(),
                                  html.Div(dcc.Graph(id='fig'))
                                  ])


@app.callback(Output(component_id = 'fig',component_property='figure'),
             Input(component_id='input-type',component_property='value'))
             State('plot','children'))



def get_graph(typec):
    
    
#     df = covidData[typec]
    
    fig = px.scatter(covidData,x ='Population',y='{}'.format(typec),
          size='Population',color='Country',
          hover_name='Country',log_x=True,size_max=60)
    
    return fig
    
#     world_map.choropleth(geo_data=res,
#                          data=covidData,
#                          columns=['Country','{}'.format(typec)],
#                          key_on='feature.properties.name',
#                          fill_color='YlOrRd',
#                          fill_opacity=0.7,
#                          line_opacity=0.4,
#                          legend_name='Country vise Covid Report')
    
#     return world_map

# if __name__=='__main__':
#     app.run_server()
app.run_server()
# In[ ]:




