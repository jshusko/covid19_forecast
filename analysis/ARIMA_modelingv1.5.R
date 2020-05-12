library(dplyr)
library(ggplot2)
library(forecast)
library(anytime)
library(tibble)
library(ggpubr)

### PREPROCESS ### 
df_full <- read.csv("./preprocess/master_5-8-20.csv") %>% as_tibble() 
df_full

### Individual County Simple Model ###

counties = list(list('Los Angeles County',6037),list('New York County',36061),list('Cook County',17031),list('Gwinnett County',13135),
             list('Harris County',48201),list('King County',53033),list('Suffolk County',25025),list('Hennepin County',27053),list('Hillsborough County',12057))

forecast_interval = 21
plist <- list()
j <- 1 
for (i in counties) {
  df_deaths <- select(df_full,FIPS,DATE,CUMULATIVE.DEATHS) %>% filter(FIPS==i[2]) %>% as_tibble()
  df_deaths$DATE <- as.Date(df_deaths$DATE, format = "%Y-%m-%d")
  ts_train <- ts(df_full$CUMULATIVE.DEATHS, start=c(2020,22),end=c(2020,128-forecast_interval),frequency=365)
  ts_actual <- ts(df_full$CUMULATIVE.DEATHS, start=c(2020,22),end=c(2020,128),frequency=365)
  #ts_train <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(df_deaths$DATE), end=max(df_deaths$DATE)-forecast_interval)
  #ts_actual <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=min(dates_ts), end=max(dates_ts))
  fit <- auto.arima(ts_train,stepwise=FALSE, approximation=FALSE)
  forecast <- forecast(fit,h=forecast_interval)
  plot <- autoplot(forecast,xlab='Months',ylab='Deaths',main=i[1]) + autolayer(ts_actual) 
  name <- paste("plot",j,sep="_")
  tmp <- list(plot)
  plist[name] <- tmp
  j <- j + 1
}

ggarrange(plist[1]$plot_1,plist[2]$plot_2,plist[3]$plot_3,plist[4]$plot_4,plist[5]$plot_5,plist[6]$plot_6,plist[7]$plot_7,plist[8]$plot_8,plist[9]$plot_9)

