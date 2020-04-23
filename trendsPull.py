### Author: Jacob Shusko (jws383@cornell.edu) ###
### Date: April 22, 2020 ### 
### Refs: https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f

## This script pulls google trends data for US-NY and US-CA metropolitan areas 
## related to Covid-19 symptoms and updates the "covid19_googleTrends.csv" in 
## the following repo: https://github.com/jshusko/covid19_googleTrends.git

import pandas as pd
import matplotlib
from pytrends.request import TrendReq


pytrend = TrendReq(hl='en-US',tz=360,retries=10,backoff_factor=0.5)

symptoms = ['smell', 'taste']
pytrend.build_payload(kw_list=symptoms)

# interest by region
df = pytrend.interest_by_region(resolution='DMA',inc_low_vol=True,inc_geo_code=True)
print(df.head(10))

#parse 
NY_counties = ["Binghamton NY", 'Watertown NY', 'Buffalo NY', 'Utica NY', 
               'Syracuse NY', 'Rochester NY', 'Albany-Schenectady-Troy NY'
               'Elmira NY', 'New York NY', 'Burlington VT-Plattsburgh NY']

# read out to csv
df.to_csv('covid19_googleTrends.csv',encoding='utf-8')