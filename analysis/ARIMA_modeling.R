library(dplyr)
library(ggplot2)
library(forecast)

### PREPROCESS ### 
df_full <- read.csv("./preprocess/master_5-8-20.csv") %>% as_tibble() 
df_full

## New York City subset 
la_county_fips = 6037
ny_county_fips = 36061
cook_county_fips = 17031
atl_county_fips = 13135

df_deaths <- select(df_full,FIPS,DATE,CUMULATIVE.DEATHS) %>% filter(FIPS==atl_county_fips) %>% as_tibble()
df_deaths$DATE <- as.Date(df_deaths$DATE, format = "%Y-%m-%d")
dates_ts <- as.ts(df_deaths$DATE)
ggplot(data=df_deaths, aes(x=DATE,y=CUMULATIVE.DEATHS),group=1)+geom_line(color='blue',size=2)

forecast_interval = 25
ny_ts_train <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(dates_ts), end=max(dates_ts)-forecast_interval)
ny_ts <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(dates_ts), end=max(dates_ts))

fit <- auto.arima(ny_ts_train)
forecast <- forecast(fit,h=forecast_interval)
autoplot(forecast)+autolayer(ny_ts)


