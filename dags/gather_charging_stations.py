#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
import requests
from io import StringIO


# In[27]:


# Constants
CSV_URL = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister.csv"
TABLE_NAME = "ladesaeulenregister"


# In[28]:


def download_csv_data():
    """Download CSV data and return a pandas DataFrame"""
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        data = StringIO(response.text)
        df = pd.read_csv(data, sep=";", skiprows=9, header=1)  # Adjusting the header row to 0 based on structure
        #rename straße to strasse
        df = df.rename(columns={"Straße": "Strasse"})
        #rename all columns to lowercase
        df.columns = df.columns.str.lower()
        return df
    else:
        raise Exception(f"Failed to download CSV: {response.status_code}")


# In[29]:


df = download_csv_data()

