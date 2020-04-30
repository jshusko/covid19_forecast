import pandas as pd  
import numpy as np 
from datetime import datetime 
from dateutil import parser

### Author: Jacob Shusko (jws383@cornell.edu) ### Date: April 27, 2020 ### 

""" This script joins together demographic data from the Census with the NPI 
policy data on the fips code.

Links: -
https://github.com/Keystone-Strategy/covid19-intervention-data/blob/master/complete_npis_raw_policies.csv
-
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
-
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv
The NPI and covid19 data is updated daily so we this script will pull from the
website, but the Census data is stored in this file's github repository: -
https://github.com/jshusko/covid19_googleTrends """ 

# grab and select appropriate columns for covid 19 data
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
df_covid19 = df_covid19[colnames]; print(df_covid19.head(20))

# grab and select appropriate columns for NPI data
url_npi = 'https://raw.githubusercontent.com/Keystone-Strategy/covid19-intervention-data/master/complete_npis_raw_policies.csv'
df_npi = pd.read_csv(url_npi, error_bad_lines=False) 
df_npi = df_npi[['fip_code','npi','start_date']]; print(df_npi.head(20))

# create new data frame with a columns for npi types and their values as days
# past mar 12, 2020
npis = np.unique(df_npi['npi']); print("\n\n npis:",npis) # list of npi policies 

# first: calculate days past
base = parser.parse('03/12/2020'); print("\n\n base date",base)
#df['start_date'] = pd.datetime(df['start_date']) print(df.head(20))
