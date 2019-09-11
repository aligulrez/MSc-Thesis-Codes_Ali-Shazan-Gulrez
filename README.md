data_points.py
This file plots and calcultaes the skill factor of Clear sky model data and persistence data with respect to Oahu irradiance data 
arguments
argument 1: date in mm/dd/yyyy
argumnet 2: data file
example: C:\Users\ashaz\Python Trial>data_points.py "12/23/2010" Data\20101223.txt

kt_distribution.py
This file plots and calculates the cler sky index kt distribution 
arguments
argument 1: date in mm/dd/yyyy
argumnet 2: data file
example: C:\Users\ashaz\Python Trial>kt_distribution.py "12/23/2010" Data\20101223.txt

kmeans_solar.py
This file clusters the days with respect to kt distribution histogram
arguments
argument 1: kt distribution file
example: C:\Users\ashaz\Python Trial>kmeans_solar.py features_kt_all.csv

pca.py
This file generates princial components of truncated normalized gn for all days and plots scree graph 
arguments
argument 1: file containing normalized ghi values for all days
argument 2: boolean value for making scree plot (1 = plot, 0 = no plot)
example: C:\Users\ashaz\Python Trial>pca.py Data\gn_vals_trunc.csv 1

kmeans_cluster.py
This file clusters the days with respect to pca of normalised ghi and k means clustering. It also plots the distribution with respect to 
pca1 and pca2 and calculates the silhouette index
arguments
argument 1: file containing pca of normalised ghi values for all days.
example: C:\Users\ashaz\Python Trial>kmeans_cluster.py Data\gn_pca_trunc.csv

arima.py
This file trains the arima model and plots the forecasted normalized irradiance value with respect actual normalized Oahu data 
arguments
argument 1: file containing normalised ghi values for all days.
argument 2: file containing dates of specified class
argument 3: specific day of the class of which forecast is required
argument 4: output file to save the forecasted data 
example: C:\Users\ashaz\Python Trial>arima.py Data\gn_vals_trunc.csv class_0 22 outtest220.txt

pred_pers_plot.py
This file denormalises the arima forecast and compares it with persistence forecast to get rmse and mae skill metrics with 
respect to actual data 
arguments
argument 1: file containing normalised ghi values for forecasted day.
argument 2: list of all days
argument 3: file containing dates of specified class
argument 4: specific day of the class of which forecast is required 
example: C:\Users\ashaz\Python Trial>pred_pers_plot.py class1_data\pred_22_1.txt dates_all.txt class_1 22

predictive_control_1pass.py
This file calculates Ebres with respect to predictive data 
argument 1: file containing predictive data for particular day 
argument 2: file containing predictive demand data for that day
argument 3: binary value (use 0 to initialize Ebres)
example: C:\Users\ashaz\Python Trial\battery_bhasam>predictive_control_1pass.py 08082019_pred.csv 08082019_oahu_demand.txt 0

predictive_control_1pass.py
This file runs the predictive control algorithm based on predictive solar power derived from predictive solar forecast. therefore it takes ebres as exogeneous input 
which was calculated earlier 
argument 1: file containing predictive data for particular day in 15 minute resolution
argument 2: file containing predictive demand data for that day
argument 3: binary value (can use both 0 or 1)
argument 4: ebres data as calculated and saved from previous file
example: C:\Users\ashaz\Python Trial\battery_bhasam>predictive_control_1pass.py 20100809_15mins.txt 08082019_oahu_demand.txt 1 ebres_08082019.txt

predictive_control_1pass.py
This file runs the business as usual case with ebres = 0 so as to compare the performance indicators (SCR and CLR)
argument 1: file containing predictive data for particular day in 15 minute resolution
argument 2: file containing predictive demand data for that day
argument 3: binary value (use 1 for ebres=0)
example: C:\Users\ashaz\Python Trial\battery_bhasam>predictive_control_1pass.py 20100809_15mins.txt 08082019_oahu_demand.txt 1





