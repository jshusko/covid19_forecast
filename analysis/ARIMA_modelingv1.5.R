library(dplyr)
library(ggplot2)
library(forecast)
library(anytime)
library(ggpubr)

### PREPROCESS ### 
df_full <- read.csv("./preprocess/master_5-8-20.csv") %>% as_tibble() 
df_full

### Individual County Simple Model ###
la = 6037
ny = 36061
cook = 17031
gwinnett = 13135
harris = 48201
tompkins = 36109
suffolk = 25025
hennepin = 27053 
hillsborough = 12057
counties = c(la,ny,cook,gwinnett,harris,tompkins,suffolk,hennepin,hillsborough)

forecast_interval = 21
forecast_interval = 21
plist <- list()
j <- 1 
for (i in counties) {
  df_deaths <- select(df_full,FIPS,DATE,CUMULATIVE.DEATHS) %>% filter(FIPS==i) %>% as_tibble()
  df_deaths$DATE <- as.Date(df_deaths$DATE, format = "%Y-%m-%d")
  dates_ts <- as.ts(df_deaths$DATE)
  ts_train <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(dates_ts), end=max(dates_ts)-forecast_interval)
  ts_actual <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(dates_ts), end=max(dates_ts))
  fit <- auto.arima(ts_train,stepwise = FALSE, approximation = FALSE)
  forecast <- forecast(fit,h=forecast_interval)
  plot <- autoplot(forecast) + autolayer(ts_actual)
  name <- paste("plot",j,sep="_")
  tmp <- list(plot)
  plist[name] <- tmp
  j <- j + 1
}

ggarrange(plist[1]$plot_1,plist[2]$plot_2,plist[3]$plot_3,plist[4]$plot_4,plist[5]$plot_5,plist[6]$plot_6,plist[7]$plot_7,plist[8]$plot_8,plist[9]$plot_9)

