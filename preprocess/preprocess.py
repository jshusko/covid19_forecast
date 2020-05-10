import pandas as pd  
import numpy as np 
from datetime import datetime 
from dateutil import parser

### Author: Jacob Shusko (jws383@cornell.edu) 
### Date: April 27, 2020 ### 

""" This script joins together demographic data, NPI data and covid-19 data on
    the county level by the FIPS code. 

	Links: 
	- https://github.com/Keystone-Strategy/covid19-intervention-data/blob/master/complete_npis_raw_policies.csv
	- https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
	- https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv

	The NPI and covid19 data is updated daily so this script will pull from 
    the website, but the Census data is stored in this file's github repository 
    with relative path "./co-est2019-alldata-utf8.csv"
""" 

## prepare census data for join
df_census = pd.read_csv("co-est2019-alldata-utf8.csv"); 
df_census['STATE'] = df_census['STATE'].apply(str)
df_census['COUNTY'] = df_census['COUNTY'].apply(str)

def create_fip(row):
    st = row['STATE']
    ct = row['COUNTY']
    if int(st)<10:
    	st_prime = st
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
df_census = df_census.set_index('FIPS')
print("\n\nCensus index: \n",df_census.index)
print("\n\nCensus columns: \n",df_census.columns)
print("\n\nCensus dataset: \n",df_census)
print("\n\n-------------------------------------------------------------------------------------------------------------------\n\n")

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
'4/22/20','4/23/20','4/24/20','4/25/20','4/26/20','4/27/20','4/28/20','4/29/20',
'4/30/20','5/1/20','5/2/20','5/3/20','5/4/20','5/5/20','5/6/20','5/7/20','5/8/20']
df_covid19 = df_covid19[colnames]

# format FIPS, set index, convert to datetime
df_covid19['FIPS'] = ((df_covid19['FIPS'].fillna(0.0)).apply(int)).apply(str)
df_covid19 = df_covid19.set_index('FIPS')
df_covid19 = df_covid19.stack()
df_covid19 = df_covid19.to_frame()
df_covid19 = df_covid19.reset_index()
df_covid19 = df_covid19.set_index('FIPS')
df_covid19.columns = ['DATE','CUMULATIVE DEATHS']
df_covid19['DATE'] = pd.to_datetime(df_covid19['DATE'],infer_datetime_format=True,errors="coerce")
print("\n\nCovid 19 index: \n",df_covid19.index)
print("\n\nCovid 19 columns: \n", df_covid19.columns)
print("\n\nCovid 19 dataset: \n", df_covid19)
print("\n\n-------------------------------------------------------------------------------------------------------------------\n\n")


## prepare NPI data for join
url_npi = 'https://raw.githubusercontent.com/Keystone-Strategy/covid19-intervention-data/master/complete_npis_raw_policies.csv'
df_npi = pd.read_csv(url_npi, error_bad_lines=False) 
df_npi = df_npi[['fip_code','npi','start_date']]
df_npi.columns = ['FIPS','npi','start_date']; 
df_npi['FIPS'] = df_npi['FIPS'].apply(str)  

# convert to datetime, take difference
base_str = "3/1/2020"
end_str = colnames[len(colnames)-1]
print(end_str)

base = pd.to_datetime(base_str)
end = pd.to_datetime(end_str)
df_npi['start_date'] = df_npi['start_date'].fillna(end_str)
df_npi.loc[df_npi['start_date'] == 'None in Place', 'start_date'] = end_str
df_npi.loc[df_npi['start_date'] == 'Start', 'start_date'] = end_str
df_npi['start_date'] = pd.to_datetime(df_npi['start_date'],infer_datetime_format=True,errors="coerce")
#df_npi['days_from_base'] = df_npi.apply(lambda row: (row['start_date'] - base).days, axis=1)

# pivot on npis and fill na with end date
df_npi_pivot = df_npi.pivot(index="FIPS",columns="npi",values='start_date')
u = df_npi_pivot.select_dtypes(include=['datetime'])
df_npi_pivot[u.columns] = u.fillna(end)
print("\n\nNPI index: \n",df_npi_pivot.index)
print("\n\nNPI columns: \n", df_npi_pivot.columns)
print("\n\nNPI dataset: \n",df_npi_pivot)
print("\n\n-------------------------------------------------------------------------------------------------------------------\n\n")


## join together datasets
df_master = df_covid19.join(df_census,how='inner')
df_master = df_master.join(df_npi_pivot,how='inner')
for i in df_npi_pivot.columns:
	df_master[str(i)] = df_master.apply(lambda row: max((row['DATE'] - row[str(i)]).days,0.0), axis=1)
print("\n\nMaster dataset index: \n",df_master.index)
print("\n\nMaster dataset columns: \n",df_master.columns)
print("\n\nMaster dataset: \n",df_master)
df_master.to_csv("".join(["master_",end_str.replace('/','-'),".csv"]))