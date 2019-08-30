#pred_pers_plot.py class1_data\pred_22_1.txt dates_all.txt class_1 22
# code for importing and plotting Oahu data, both clear sky models and for calculating the skill index
from datetime import datetime
import numpy as np
import pandas as pd
import pvlib
import math
import matplotlib.pyplot as plt
plt.rc('xtick', labelsize=25)
plt.rc('ytick', labelsize=25)
import csv
from sys import argv
import os
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
z = open(argv[1],'r')
predict_data = np.array([float(ch) for ch in z.readline()[0:-1].strip().split(',')])
z.close()
dates_file = open(argv[2],'r')
dates = [line.strip() for line in dates_file]
dates_file.close()
class_file = open(argv[3],'r')
class_indexes = [int(line.strip())-2 for line in class_file]
class_file.close()
selected_date = dates[class_indexes[int(argv[4])]]
date_rng = pd.date_range(start=selected_date[4:6]+"/"+selected_date[6:8]+"/"+selected_date[0:4]+' 05:00:00', end=selected_date[4:6]+"/"+selected_date[6:8]+"/"+selected_date[0:4]+' 20:00:00', tz='US/Hawaii',freq='t')
timestamp_date_rng = pd.to_datetime(date_rng, infer_datetime_format=True)
solar_position = pvlib.solarposition.get_solarposition(timestamp_date_rng, latitude=21.31, longitude=-158.08, altitude=None, pressure=None, method="nrel_numpy", temperature=25)
zeniths = solar_position['zenith']
apparent_elevation = solar_position['apparent_elevation']
ghi_bird = []
ghi_solis = []
for zen in zeniths:
	if(zen < 89):
		am= abs((1/math.cos(math.radians(zen)))+0.15/(93.885-zen)**1.25)
	else:
		am = 0
	ghi_bird.append(pvlib.clearsky.bird(zenith=zen, airmass_relative=am, aod380=0.15, aod500=0.1, precipitable_water=1.5, ozone=0.3, pressure=101325.0, dni_extra=1367.0, asymmetry=0.85, albedo=0.2)['ghi'])

ghi_bird_trunc = np.array(ghi_bird[167:-168])
mult_data = ghi_bird_trunc * predict_data
shazgyan=open(os.path.join("data",selected_date+".txt"),'r')
dataarray=csv.reader(shazgyan,delimiter=',')
sensor1=[float(row[6]) for row in dataarray]
skipped_sensor_data = []
skipped_sensor_data_pers = []
persistence_factor = 15
for i in range(0,len(sensor1),60):
	skipped_sensor_data.append(sensor1[i])
	
for i in range(0,len(sensor1),60*persistence_factor):
	for j in range(persistence_factor):
		skipped_sensor_data_pers.append(sensor1[i])
skipped_sensor_data_trunc = skipped_sensor_data[167:-168]
skipped_sensor_data_pers_trunc = skipped_sensor_data_pers[167:-168]
x = [i for i in range(len(mult_data))]
x_p = [i for i in range(len(skipped_sensor_data_pers_trunc))]
plt.xlabel("Time (Minutes)", fontsize=25)
plt.ylabel(r'$Solar$ $Irradiance$ $GHI$ $(W/m^2)$', fontsize= 25)

#plt.plot(x,mult_data,x,skipped_sensor_data_trunc,x_p,skipped_sensor_data_pers_trunc)
plt.plot(x,mult_data,x,skipped_sensor_data_trunc,x_p,skipped_sensor_data_pers_trunc)
plt.legend(["Predicted data","Actual data","Persistence data"],fontsize= 20)
plt.show()
error_pred_mse = math.sqrt(mean_squared_error(skipped_sensor_data_trunc, mult_data))
error_pred_mae = mean_absolute_error(skipped_sensor_data_trunc, mult_data)
error_pers_mse = math.sqrt(mean_squared_error(skipped_sensor_data_trunc, skipped_sensor_data_pers_trunc[0:len(x)]))
error_pers_mae = mean_absolute_error(skipped_sensor_data_trunc, skipped_sensor_data_pers_trunc[0:len(x)])
#rmse = math.sqrt(rmse_bird/len(ghi_bird))
print "date:%s"%(selected_date)
print('Pred MAE: %.3f,MSE: %.3f' %(error_pred_mae,error_pred_mse))
print('Pers MAE: %.3f,MSE: %.3f' %(error_pers_mae,error_pers_mse))
z = open("save.csv",'w')
for i in range(0,len(mult_data),15):
	z.write(str(mult_data[i]))
	z.write(",")
z.close()