library(dplyr)
library(ggplot2)
library(forecast)
library(anytime)
library(tibble)
library(ggpubr)

### PREPROCESS ### 
df_full <- read.csv("./preprocess/master_5-8-20.csv") %>% as_tibble() 
df_full

### County Subset ARIMA ###
# training is optimal 
counties = list(list('Los Angeles County',6037),list('New York County',36061),list('Cook County',17031),list('Gwinnett County',13135),
             list('Harris County',48201),list('King County',53033),list('Suffolk County',25025),list('Hennepin County',27053),list('Hillsborough County',12057))
forecast_interval = 21
plist <- list() # plots
flist <- list() # fits
elist <- list() # mse on forecast interval
j <- 1 
for (i in counties) {
  df_deaths <- select(df_full,FIPS,DATE,CUMULATIVE.DEATHS) %>% filter(FIPS==i[2]) %>% as_tibble()
  df_deaths$DATE <- as.Date(df_deaths$DATE, format = "%Y-%m-%d")
  ts_train <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=c(2020,22), end=c(2020,128-forecast_interval),frequency=365)
  ts_actual <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=c(2020,22), end=c(2020,128),frequency=365)
  fit <- auto.arima(ts_train,stepwise=FALSE, approximation=FALSE)
  forecast <- forecast(fit,h=forecast_interval)
  plot <- autoplot(forecast,main=i,ylab="Deaths") + autolayer(ts_actual,show.legend=FALSE)
  res <- tail(forecast$residuals,forecast_interval) %>% as.numeric()
  mse <- sum(res^2)
  name <- paste("plot",j,sep="_")
  plist[name] <- list(plot)
  flist[name] <- list(fit)
  elist[name] <- mse
  j <- j + 1
}

average_mse_subopt <- Reduce('+',elist)/length(elist) # average MSE over all counties in data set
max_mse_subopt <- Reduce('max',elist) # max MSE over all counties in data set
ggarrange(plist[1]$plot_1,plist[2]$plot_2,plist[3]$plot_3,plist[4]$plot_4,plist[5]$plot_5,plist[6]$plot_6,plist[7]$plot_7,plist[8]$plot_8,plist[9]$plot_9,label.x="test")

par(mfrow=c(3,3))
acf1 = acf(flist[1]$plot_1$residuals,main=counties[1])
acf2 = acf(flist[2]$plot_2$residuals,main=counties[2])
acf3 = acf(flist[3]$plot_3$residuals,main=counties[3])
acf4 = acf(flist[4]$plot_4$residuals,main=counties[4])
acf5 = acf(flist[5]$plot_5$residuals,main=counties[5])
acf6 = acf(flist[6]$plot_6$residuals,main=counties[6])
acf7 = acf(flist[7]$plot_7$residuals,main=counties[7])
acf8 = acf(flist[8]$plot_8$residuals,main=counties[8])
acf9 = acf(flist[9]$plot_9$residuals,main=counties[9])


### All Counties ARIMA (w/o plotting) ###
# training is optimal
df_subset <- select(df_full,FIPS,DATE,CUMULATIVE.DEATHS)
df_subset$DATE <- as.Date(df_subset$DATE, format = "%Y-%m-%d")
all_counties =  unique(df_full$FIPS)
forecast_interval = 7
flist_opt <- list() # fits
elist_opt <- list() # mse on forecast interval
for (i in all_counties) {
  df_deaths <- df_subset %>% filter(FIPS==i) %>% as_tibble()
  df_deaths$DATE <- as.Date(df_deaths$DATE, format = "%Y-%m-%d")
  ts_train <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=c(2020,22), end=c(2020,128-forecast_interval),frequency=365)
  ts_actual <- ts(data=df_deaths$CUMULATIVE.DEATHS, start=c(2020,22), end=c(2020,128),frequency=365)
  fit <- auto.arima(ts_train,stepwise=FALSE, approximation=FALSE)
  forecast <- forecast(fit,h=forecast_interval)
  res <- tail(forecast$residuals,forecast_interval) %>% as.numeric()
  mse <- sum(res^2)
  flist_opt[toString(i)] <- list(fit)
  elist_opt[toString(i)] <- mse
}
average_mse_opt <- Reduce('+',elist_opt)/length(elist) # average MSE over all counties in data set
max_mse_opt <- Reduce('max',elist_opt) # max MSE over all counties in data set
average_mse_opt; max_mse_opt
