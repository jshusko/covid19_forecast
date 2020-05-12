#test.py
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/Yu-Group/covid19-severity-prediction/master/data/county_data_abridged.csv")
df.to_csv("Yu-Group Data.csv")