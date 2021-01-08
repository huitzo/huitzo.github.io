#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from plotly import graph_objects as  go
from matplotlib import pyplot as plt
from datetime import datetime
from os.path import basename
import numpy as np
import requests
np.seterr(divide='ignore', invalid='ignore')


# In[ ]:


day_mean = 10
today = datetime.now()
#URL =  " https://opendata.ecdc.europa.eu/covid19/casedistribution/csv-{0:%Y}-{0:%m}-{0:%d}.csv" #https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{0:%Y}-{0:%m}-{0:%d}.csv".format(today)
#FILE = "/home/lev/Dropbox/ScriptsLCS-Mesura/Coronavirus/LATAM/Data/"+basename(URL)

#with open(FILE, 'wb') as f:
#    f.write(requests.get(URL, allow_redirects=False).content)
#    print('DONE')

#dataglobal = pd.read_csv(FILE)
print (today)


# In[ ]:


dataglobal = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
dataglobal.columns = ['daterep', 'year_week', 'cases_weekly', 'deaths_weekly', 'countries', 'geoid','gedoid1','pop','continentExp','notification_rate_per_100000_population_14-days']
dataglobal[dataglobal['countries'] == 'Panama']


# In[ ]:


dataglobal['daterep'] =pd.to_datetime(dataglobal.daterep, format = "%d/%m/%Y")


# In[ ]:





# In[ ]:


datalatam = dataglobal[dataglobal['countries'].isin(['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa_Rica', 'Cuba',
                                           'Ecuador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Paraguay', 'Peru', 'Dominican_Republic', 'Uruguay', 'Venezuela'])]
mask = (datalatam['daterep'] > '02/28/2020') & (datalatam['daterep'] <= today.strftime('%m-%d-%Y'))
datalatam = datalatam.loc[mask]


# In[ ]:


datalatam = datalatam[['daterep', 'cases_weekly', 'countries', 'pop','deaths_weekly',]]


# In[ ]:


datalatam[datalatam['countries'] == 'Argentina']


# In[ ]:


idx = pd.date_range('2020-02-28', today.strftime('%Y-%m-%d'))

for rdate in idx:
    for country in ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa_Rica', 'Cuba',
                                           'Ecuador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Paraguay', 'Peru', 'Dominican_Republic', 'Uruguay', 'Venezuela']:
        dlt = datalatam[datalatam['countries'] == country]
        pop_country = dlt['pop'].iloc[0]
        death_country = dlt['deaths_weekly'].iloc[0]
        if rdate in set(dlt.daterep):
            value = dlt['cases_weekly'].loc[dlt['daterep'] == rdate]
            val = value.values[0]
        else:
            print(country)
            print(rdate)
            df2 = pd.DataFrame({"daterep": [rdate], "cases_weekly": [0], "countries": country, "deaths_weekly": [0], "pop": pop_country})
            datalatam = datalatam.append(df2, ignore_index = True, sort=True)
datalatam[datalatam['countries'] == 'Argentina']


# In[ ]:
# changed

datalatam = datalatam.sort_values(by=['countries', 'daterep'], ascending=True)
datalatam


# In[ ]:


datalatam['cumsum'] = datalatam.groupby(['countries'])['cases_weekly'].cumsum()
datalatam['cumnorm']=(datalatam['cumsum']/datalatam['pop'])*100000
datalatam['cumsumdeath'] = datalatam.groupby(['countries'])['deaths_weekly'].cumsum()
datalatam['cumdeathnorm']=(datalatam['cumsumdeath']/datalatam['pop'])*100000
datalatam['letalidad'] = (datalatam['cumsumdeath']/datalatam['cumsum'])*100
datalatam


# In[ ]:


fig = px.line(datalatam, x="daterep", y="cumsum", color="countries", line_shape = "linear", line_group="countries", hover_name="countries")
#fig.update_traces(textposition='top center')
fig.update_layout(
    title="COVID-19 en LATAM "+today.strftime('%Y-%m-%d'),
    xaxis_title="Fecha",
    yaxis_title="Casos acumulados",
    yaxis_type = "log",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ),
    images= [dict(
                    source="https://raw.githubusercontent.com/sydmizar/datacovid19mx/master/images/csl.png",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=0.2, sizey=0.4,
                    sizing="stretch",
                    opacity = 0.4,
                    layer="below")],
    annotations=[
            dict(
                text='Fuente: @ECDC_EU Gráfica: CSL UPIITA',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.16,
                bordercolor='black',
                borderwidth=1
            )
        ]
)
fig.show()


# In[ ]:


plot(fig, filename='../LATAM/acumulados_latam.html')


# In[ ]:


fig = px.line(datalatam, x="daterep", y="cumsumdeath", color="countries", line_shape = "linear", line_group="countries", hover_name="countries")
#fig.update_traces(textposition='top center')
fig.update_layout(
    title="COVID-19 en LATAM "+today.strftime('%Y-%m-%d'),
    xaxis_title="Fecha",
    yaxis_title="Decesos acumulados",
    yaxis_type = "log",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ),
    images= [dict(
                    source="https://raw.githubusercontent.com/sydmizar/datacovid19mx/master/images/csl.png",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=0.2, sizey=0.4,
                    sizing="stretch",
                    opacity = 0.4,
                    layer="below")],
    annotations=[
            dict(
                text='Fuente: @ECDC_EU Gráfica: CSL UPIITA',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.16,
                bordercolor='black',
                borderwidth=1
            )
        ]
)
fig.show()


# In[ ]:


plot(fig, filename='../LATAM/decesosacumulados_latam.html')


# In[ ]:


fig = px.scatter(datalatam, x="daterep", y="letalidad",  color="countries", hover_name="countries") #color="countries", line_shape = "linear", line_group="countries", hover_name="countries")
#fig.update_traces(textposition='top center')
fig.update_layout(
    title="COVID-19 en LATAM "+today.strftime('%Y-%m-%d'),
    xaxis_title="Fecha",
    yaxis_title="Letalidad (decesos/confirmados x100)",
    yaxis_type = "log",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ),
    images= [dict(
                    source="https://raw.githubusercontent.com/sydmizar/datacovid19mx/master/images/csl.png",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=0.2, sizey=0.4,
                    sizing="stretch",
                    opacity = 0.4,
                    layer="below")],
    annotations=[
            dict(
                text='Fuente: @ECDC_EU Gráfica: CSL UPIITA',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.16,
                bordercolor='black',
                borderwidth=1
            )
        ]
)
fig.show()


# In[ ]:


plot(fig, filename='../LATAM/letalidad_latam.html')


# In[ ]:


fig = px.scatter(datalatam, x="daterep", y="cumnorm", color="countries", hover_name="countries")
#fig.update_traces(textposition='top center')
fig.update_layout(
    title="COVID-19 per 10^5 "+today.strftime('%Y-%m-%d'),
    xaxis_title="Fecha",
    yaxis_title="(Casos acumulados / población) x 10^5",
    yaxis_type = "log",
    #xaxis_type = "log",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ),
    images= [dict(
                    source="https://raw.githubusercontent.com/sydmizar/datacovid19mx/master/images/csl.png",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=0.2, sizey=0.4,
                    sizing="stretch",
                    opacity = 0.4,
                    layer="below")],
    annotations=[
            dict(
                text='Fuente: @ECDC_EU Gráfica: CSL UPIITA',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.16,
                bordercolor='black',
                borderwidth=1
            )
        ]
)
fig.show()


# In[ ]:


plot(fig, filename='../LATAM/scatter_latam.html')


# In[ ]:


fig = px.scatter(datalatam, x="daterep", y="cumdeathnorm", color="countries", hover_name="countries")
#fig.update_traces(textposition='top center')
fig.update_layout(
    title="Decesos/Pob. per 10^5 "+today.strftime('%Y-%m-%d'),
    xaxis_title="Fecha",
    yaxis_title="(Decesos acumulados / población) x 10^5",
    yaxis_type = "log",
    #xaxis_type = "log",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ),
#fig.update_traces(mode='markers', marker_symbol=diamond),
    images= [dict(
                    source="https://raw.githubusercontent.com/sydmizar/datacovid19mx/master/images/csl.png",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=0.2, sizey=0.4,
                    sizing="stretch",
                    opacity = 0.4,
                    layer="below")],
    annotations=[
            dict(
                text='Fuente: @ECDC_EU Gráfica: CSL UPIITA',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.16,
                bordercolor='black',
                borderwidth=1
            )
        ]
)
fig.show()


# In[ ]:


plot(fig, filename='../LATAM/mortality_latam.html')
