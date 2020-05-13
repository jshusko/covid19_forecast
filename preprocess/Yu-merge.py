import pandas as pd  
import numpy as np 
from datetime import datetime 
from dateutil import parser

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

# format FIPS, set index
df_covid19['FIPS'] = ((df_covid19['FIPS'].fillna(0.0)).apply(int)).apply(str)
df_covid19 = df_covid19.set_index('FIPS')

print("\n\nCovid 19 index: \n",df_covid19.index)
print("\n\nCovid 19 columns: \n", df_covid19.columns)
print("\n\nCovid 19 dataset: \n", df_covid19)
print("\n\n-------------------------------------------------------------------------------------------------------------------\n\n")


### County Level Demographics Data ### 
df_yu = pd.read_csv("Yu-Group Data.csv")
df_yu= df_yu.set_index('countyFIPS')

print("\n\nDemographic index: \n",df_yu.index)
print("\n\nDemographic columns: \n", df_yu.columns)
print("\n\nDemographic dataset: \n", df_yu)

### Merge ### 
df_master = df_covid19.join(df_yu,how='inner')
df_master['death_rate'] = df_master.apply(lambda row: (row['5/8/20']/row['PopulationEstimate2018'])*100000, axis=1)
print("\n\nMaster dataset index: \n",df_master.index)
print("\n\nMaster dataset columns: \n",df_master.columns)
print("\n\nMaster dataset: \n",df_master)
df_master.to_csv("master_yu.csv")