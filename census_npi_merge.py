import pandas as pd 

### Author: Jacob Shusko (jws383@cornell.edu) ###
### Date: April 27, 2020 ### 

"""
This script joins together demographic data from the Census with the NPI 
policy data on the fips code.

Links:
https://github.com/Keystone-Strategy/covid19-intervention-data/blob/master/complete_npis_raw_policies.csv
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/

The NPI data is updated daily so we this script will pull from the website,
but the Census data is stored in this file's github repository:


""" 