### Author: Jacob Shusko (jws383@cornell.edu) ###
### Date: April 25, 2020 ### 
### Refs: https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f

"""
This script pulls google trends data for x countries related to Covid-19 symptoms
and updates the "covid19_googleTrends.csv" in the following repository:
		https://github.com/jshusko/covid19_googleTrends.git
"""

import pandas as pd 
from pytrends.request import TrendReq #https://github.com/GeneralMills/pytrends


pytrend = TrendReq(hl='en-US',tz=360,retries=20,backoff_factor=0.5)

# have to perform pull in batches due to google trends limit of 5 terms
symptoms_topic = ['Anosmia','Sore Throat','Diarrhea','Appetite','Shortness of breath']

symptoms = ['smell', 'taste', 'sore', 'throat', 'upset stomach', 'diarrhea', 
       'no appetite', 'difficulty breathing', 'fever', 'sore eyes', 
       'runny nose', 'fatigue', 'dry cough', 'chest pain', 'blue face']
symptoms_1 = symptoms[0:5]
symptoms_2 = symptoms[5:10]
symptoms_3 = symptoms[10:len(symptoms)]

# batch 1 
pytrend.build_payload(kw_list=symptoms_1)
pytrends.interest_over_time()
print(df1.head(20))

# # batch 2 
# pytrend.build_payload(kw_list=symptoms_2)
# df2 = pytrend.interest_by_region(resolution='DMA',inc_low_vol=True,inc_geo_code=True)
# print(df2.head(10))

# # batch 3
# pytrend.build_payload(kw_list=symptoms_3)
# df3 = pytrend.interest_by_region(resolution='DMA',inc_low_vol=True,inc_geo_code=True)
# print(df3.head(10))

# # combine batches
# result = (pd.concat([df1,df2,df3], axis=1, sort=False)).drop(['geoCode'],axis=1)
# print(result.head(10))

# # select NY county data
# print(result.index)

# read out to csv
# result_NY.to_csv('covid19_googleTrends.csv',encoding='utf-8')