# Covid-19 forecasting and Non-Pharmaceutical Interventions on county level data
This is the repository for scripts and data used to write a paper studying using ARIMA models to forecast Covid-19 cumulative deaths on the county level, and tree-based methods to evaluate the relationship between county demographics and Non-Pharmaceutical Interventions (NPIs).
This was a final project for ORIE 4740 at Cornell University, but feel free to use the datasets and models for further research.

Datasets used:
 - [Time-Series of cumulative deaths for U.S. counties using NPI days in effect and demographics as additional features](preprocess/master_5-8-20.csv)
 - [Demographic, health-related, and political features for each U.S. county](preprocess/master_yu) provided by the [Yu Group](https://github.com/Yu-Group/covid19-severity-prediction)
 
Models:
 - [R script to run ARIMA models on Time-series data set](analysis/ARIMA_modelingv1.5.R)
 - [Python notebook to run Random Forest on the extensive demographics data set](analysis/RF classifier vF.ipynb)
 
 Contact us:
 - Catherine Appleby (ORIE '21) at jws383@cornell.edu
 - John Miller (ORIE '20) at jmm754@cornell.edu
 - Jacob Shusko (ORIE/CS '21) at jws383@cornell.edu 

