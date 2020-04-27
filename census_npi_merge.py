import pandas as pd 
import numpy as np
from datetime import datetime
from dateutil import parser

### Author: Jacob Shusko (jws383@cornell.edu) ###
### Date: April 27, 2020 ### 

"""
This script joins together demographic data from the Census with the NPI 
policy data on the fips code.

Links:
	- https://github.com/Keystone-Strategy/covid19-intervention-data/blob/master/complete_npis_raw_policies.csv
	- https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/

The NPI data is updated daily so we this script will pull from the website,
but the Census data is stored in this file's github repository:
	- https://github.com/jshusko/covid19_googleTrends
""" 

# grab and select appropriate columns for npis
url_npi = 'https://raw.githubusercontent.com/Keystone-Strategy/covid19-intervention-data/master/complete_npis_raw_policies.csv'
df = pd.read_csv(url_npi, error_bad_lines=False)
df = df[['fip_code','npi','start_date']]
print(df.head(20))

# create new data frame with a columns for npi types and their values as
# days past mar 12, 2020
npis = np.unique(df['npi']) # list of npi policies 
print(npis)

datetime_str = '03/28/2020'
parser.parse(datetime_str) #creates a datetime object which we can compare with mar 12
print(parser.parse(datetime_str))