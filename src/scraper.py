#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import numpy as np


# In[2]:


url = 'https://www.worldometers.info/coronavirus/'
now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
_dict = {}
save_csv = True
append_csv = False
percentile = 97


# In[3]:


page = requests.get(url)
soup = BeautifulSoup(page.content)


# In[4]:


for _tr_list in soup.tbody.find_all('tr'):
    _td_list = _tr_list.find_all('td')
    for i, _td in enumerate(_td_list):  
        # Recuperar el nombre del pais cuando es un enlace
        if i%10 == 0:
            _a = _td.find('a')
                # Recuperar el nombre del pais cuando es un enlace
            if _a:
                country_name = _a['href'].split('/')[1]
            else:
                _span = _td.find('span')
                if _span:
                    # Recuperar el nombre del cuando ocupa dos filas
                    country_name = _span.contents[0]
                else:
                     # Recuperar el nombre del pais cuando no es un enlace
                    country_name = _td.contents[0]
            if country_name:
                country_name = country_name.strip()
                if country_name not in list(_dict.keys()):
                    _dict[country_name] = {} 
                _dict[country_name][now] = []
        # Recuperar los datos del pais
        else:
            if len(_td.contents) > 0:
                # Limipiar el dato de cualquier símbolo para poder convertirlo en un valor numérico
                data = _td.contents[0].replace('+','').replace(',','').strip()
                if data:
                    _dict[country_name][now].append(float(data))
                else:
                    _dict[country_name][now].append(0)
            else:
                _dict[country_name][now].append(0)


# In[5]:


# https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
df = pd.concat({k: pd.DataFrame(v).T for k, v in _dict.items()}, axis=0)
df.columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases', 'servious_critical', 'total_cases_1M_pop', 'total_deaths_1M_pop']
df.index.names = ['country', 'timestamp']
display(df.head())


# In[6]:


if save_csv:
    if append_csv:
        print('Adding data to csv...')
        df.to_csv('covid-19_2020.csv', mode='a', header=False, index=True) 
    else:
        print('Creating csv...')
        df.to_csv('covid-19_2020.csv', index=True)    
else:
    print('Save csv not needed')


# In[7]:


df = pd.read_csv('covid-19_2020.csv')


# In[8]:


df.head()


# In[9]:


# Solo paises más significativos
df_significant = df[(df['total_cases'] > np.percentile(df['total_cases'], percentile))].sort_values(by = ['total_cases'], ascending=False)

# Se muestra el número de casos según el país ("country") para la última muestra
last_timestamp = list(df_significant['timestamp'])[0]
df_last_timestamp = df_significant[(df_significant['timestamp'] == last_timestamp)]
display(df_last_timestamp)


# In[11]:


# Se representan gráficamente los resultados
# https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot
plot = sns.barplot(x="country", y="total_cases", data=df_last_timestamp)


# In[12]:


plot = sns.barplot(x="country", y="total_deaths", data=df_last_timestamp)


# In[13]:


# Añadir dia (date)
df_significant['date'] = [timestamp.split()[0] for timestamp in df_significant['timestamp']]

# Agrupar por dia (date) utilizando el valor máximo del día
df_by_date = df_significant.groupby(['country','date']).max().round()
df_by_date = df_by_date.sort_values(by = ['date', 'total_cases'], ascending=False)

display(df_by_date.head())


# In[14]:


# Se muestra la evolución en el tiempo para cada país ("country")
# Se representan gráficamente los resultados
# 
plot = sns.barplot(x="country", y="total_cases", hue = "date", data=df_by_date.reset_index())


# In[15]:


plot = sns.barplot(x="country", y="total_deaths", hue = "date", data=df_by_date.reset_index())


# In[16]:


df_spain = df_by_date.loc['spain']


# In[17]:


plot = sns.barplot(x='date', y="total_cases", data=df_spain.reset_index())


# In[18]:


plot = sns.barplot(x='date', y="total_deaths", data=df_spain.reset_index())


# In[ ]:




