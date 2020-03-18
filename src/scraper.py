#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


# In[2]:


_dict = {}


# In[3]:


url = 'https://www.worldometers.info/coronavirus/'
today = str(date.today())


# In[4]:


page = requests.get(url)
soup = BeautifulSoup(page.content)


# In[5]:


print(soup.prettify())


# In[6]:


for _tr_list in soup.tbody.find_all('tr'):
    _td_list = _tr_list.find_all('td')
    for i, _td in enumerate(_td_list):        
        # Recuperar el nombre del pais cuando es un enlace
        if i%9 == 0:
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
                _dict[country_name][today] = []
        # Recuperar los datos del pais
        else:
            if len(_td.contents) > 0:
                data = _td.contents[0].replace('+','').replace(',','').strip()
                if data:
                    _dict[country_name][today].append(float(data))
                else:
                    _dict[country_name][today].append(0)
            else:
                _dict[country_name][today].append(0)


# https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary

# In[7]:


df = pd.concat({k: pd.DataFrame(v).T for k, v in _dict.items()}, axis=0)
df.columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases', 'servious_critical', 'total_cases_1M_pop']
display(df.head())


# In[8]:


df.loc['spain'].loc['2020-03-18']['total_cases']


# In[9]:


df.to_csv('out.csv', index=True) 



# %%
