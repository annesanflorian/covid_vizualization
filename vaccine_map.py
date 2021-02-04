# -*- coding: utf-8 -*-

#import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


vaccine = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')

vaccine = vaccine[vaccine.location != 'World']


lastday = vaccine['date'].max()
firstday = vaccine['date'].min()
vaccine['date'] = pd.to_datetime(vaccine['date'])


daterange = pd.date_range(start=firstday, end=lastday)

vaccine = vaccine.groupby(['location','iso_code','date']).sum()
vaccinations = vaccine['total_vaccinations']
vaccinations = vaccinations.droplevel('location')


iso_codes = set(vaccinations.index.get_level_values(0))
multi_index = pd.MultiIndex.from_product([iso_codes, daterange], names=['iso_code', 'date'])
vaccinations = vaccinations.reindex(multi_index)

vaccinations = vaccinations.unstack(0)

vaccinations = vaccinations.fillna(0)
vaccinations = vaccinations.replace(to_replace=0, method='ffill')

vaccinations = vaccinations.stack()

vaccinations.index = vaccinations.index.swaplevel(0, 1)
vaccinations = vaccinations.reset_index()
vaccinations['date'] = vaccinations['date'].astype(str)
vaccinations.columns = ['iso_code', 'date','total_vaccinations']




'''aaa
vaccine = vaccine.groupby(['iso_code','date']).sum()
vaccine = vaccine.replace(to_replace=0, method='ffill')

iso_codes = set(vaccine.index.get_level_values(0))

multi_index = pd.MultiIndex.from_product([iso_codes, daterange], names=['iso_code', 'date'])
#vaccine = vaccine.reset_index()
#vaccine = vaccine.set_index(['iso_code', 'date'])
vaccine = vaccine.reindex(multi_index)

#vaccine = vaccine.reindex(daterange,level=2).ffill()

#vaccine = vaccine.sort_values(by='date').reset_index()

#accumulated = vaccine.groupby(['location','iso_code','date']).sum().groupby(level=0).cumsum().reset_index()
#del vaccine
#accumulated = accumulated.sort_values(by='date').reset_index()
print(vaccine.head(60))


aaa'''
#max_value = max(vaccinations['total_vaccinations'])

fig = px.choropleth(vaccinations, locations="iso_code", color='total_vaccinations', hover_name="iso_code", animation_frame="date")


fig.update_layout(
    title_text='Global Vaccination COVID-19 2021',
    coloraxis_colorbar=dict(title="Total Vaccinations"),
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)


fig.show()

