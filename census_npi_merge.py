import pandas as pd  
import numpy as np 
from datetime import datetime 
from dateutil import parser

### Author: Jacob Shusko (jws383@cornell.edu) 
### Date: April 27, 2020 ### 

""" This script joins together demographic data from the Census with the NPI 
policy data on the fips code.

Links: 
- https://github.com/Keystone-Strategy/covid19-intervention-data/blob/master/complete_npis_raw_policies.csv
- https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
- https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv

The NPI and covid19 data is updated daily so we this script will pull from the
website, but the Census data is stored in this file's github repository: 
- https://github.com/jshusko/covid19_googleTrends 
""" 

## prepare census data for join
df_census = pd.read_csv("co-est2019-alldata-utf8.csv"); 
df_census['STATE'] = df_census['STATE'].apply(str)
df_census['COUNTY'] = df_census['COUNTY'].apply(str)

def create_fip(row):
    st = row['STATE']
    ct = row['COUNTY']
    if int(st)<10:
    	st_prime = "0" + st
    else:
    	st_prime = st
    if int(ct)>99:
    	new = st_prime + ct
    elif (int(ct)>9)&(int(ct)<100):
    	new = st_prime + "0" + ct
    else:
    	new = st_prime + "00" + ct
    return new

df_census['FIPS'] = df_census.apply(lambda row: create_fip(row), axis=1)
print(df_census.head(20))

## prepare covid 19 data for join
url_covid19 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
df_covid19 = pd.read_csv(url_covid19, error_bad_lines=False) 
colnames = [ 'FIPS',
'1/22/20','1/23/20','1/24/20','1/25/20','1/26/20','1/27/20','1/28/20','1/29/20',
'1/30/20','1/31/20','2/1/20','2/2/20','2/3/20','2/4/20','2/5/20','2/6/20','2/7/20',
'2/8/20','2/9/20', '2/10/20','2/11/20','2/12/20','2/13/20','2/14/20','2/15/20',
'2/16/20','2/17/20','2/18/20','2/19/20','2/20/20','2/21/20','2/22/20','2/23/20',
'2/24/20','2/25/20','2/26/20','2/27/20','2/28/20','2/29/20','3/1/20','3/2/20',
'3/3/20','3/4/20','3/5/20','3/6/20','3/7/20','3/8/20','3/9/20','3/10/20','3/11/20',
'3/12/20','3/13/20','3/14/20','3/15/20','3/16/20','3/17/20','3/18/20','3/19/20',
'3/20/20','3/21/20','3/22/20','3/23/20','3/24/20','3/25/20','3/26/20','3/27/20',
'3/28/20','3/29/20','3/30/20','3/31/20','4/1/20','4/2/20','4/3/20','4/4/20',
'4/5/20','4/6/20','4/7/20','4/8/20','4/9/20','4/10/20','4/11/20','4/12/20','4/13/20',
'4/14/20','4/15/20','4/16/20','4/17/20','4/18/20','4/19/20','4/20/20','4/21/20',
'4/22/20','4/23/20','4/24/20','4/25/20','4/26/20','4/27/20','4/28/20','4/29/20']
df_covid19 = df_covid19[colnames]
df_covid19['FIPS'] = ((df_covid19['FIPS'].fillna(0.0)).apply(int)).apply(str)
print(df_covid19.head(20))

## prepare NPI data for join
url_npi = 'https://raw.githubusercontent.com/Keystone-Strategy/covid19-intervention-data/master/complete_npis_raw_policies.csv'
df_npi = pd.read_csv(url_npi, error_bad_lines=False) 
df_npi = df_npi[['fip_code','npi','start_date']]
df_npi.columns = ['FIPS','npi','start_date']; 
df_npi['FIPS'] = df_npi['FIPS'].apply(str)  

# convert to datetime
base_str = "3/1/2020"; print("\n\n base date: ",base_str)
end_str = "4/29/2020"; print("\n\n end date: ",end_str)
base = pd.to_datetime(base_str)
end = pd.to_datetime(end_str)
df_npi['start_date'] = df_npi['start_date'].fillna(end_str)
df_npi.loc[df_npi['start_date'] == 'None in Place', 'start_date'] = end_str
df_npi.loc[df_npi['start_date'] == 'Start', 'start_date'] = end_str
df_npi['start_date'] = pd.to_datetime(df_npi['start_date'],infer_datetime_format=True,errors="coerce"); print(df_npi.head(20))
print(df_npi.head(20))

# take difference 
df_npi['days_in_effect'] = df_npi.apply(lambda row: (end - row['start_date']).days, axis=1)
#df_npi['days_from_base'] = df_npi.apply(lambda row: (row['start_date'] - base).days, axis=1)
print(df_npi.head(20))

# pivot on npis
df_npi_pivot = df_npi.pivot(index="FIPS",columns="npi",values='days_in_effect') 
print(df_npi_pivot.head(20))