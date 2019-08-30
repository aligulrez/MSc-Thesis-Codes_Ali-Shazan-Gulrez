# code for importing and plotting Oahu data, both clear sky models and for calculating the skill index
from datetime import datetime
import numpy as np
import pandas as pd
import pvlib
import math
import matplotlib.pyplot as plt
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
import csv
from sys import argv
#z = open('new7.csv','a')
date_rng = pd.date_range(start=argv[1]+' 05:00:00', end=argv[1]+' 20:00:00', tz='US/Hawaii',freq='t')
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
	# if(abs(val) < 1400):
		# ghi.append(val)
	# else:
		# ghi.append(0)
for app_elv in apparent_elevation:
	ghi_solis.append(pvlib.clearsky.simplified_solis(apparent_elevation = app_elv, aod700=0.1, precipitable_water=1.5, pressure=101600.0, dni_extra=1367.0)['ghi'])

shazgyan=open(argv[2],'r')
dataarray=csv.reader(shazgyan,delimiter=',')
sensor1=[float(row[6]) for row in dataarray]
skipped_sensor_data = []
skipped_sensor_data_pers = []
mae_bird = 0
nmbe_bird =0
mae_pers=0
rmse_pers=0
mbe_pers=0
nmbe_pers=0
rmse_bird = 0
mae_solis = 0
rmse_solis = 0
mbe_bird = 0
mbe_solis = 0
persistence_factor = 15
for i in range(0,len(sensor1),60):
	skipped_sensor_data.append(sensor1[i])
for i in range(0,len(sensor1),60*persistence_factor):
	for j in range(persistence_factor):
		skipped_sensor_data_pers.append(sensor1[i])
for i in range(0,len(ghi_bird)):
	mae_bird += abs(skipped_sensor_data[i] - ghi_bird[i])
	rmse_bird += (skipped_sensor_data[i] - ghi_bird[i])**2
	
	
	mbe_bird += skipped_sensor_data[i] - ghi_bird[i]

for i in range(0,len(ghi_solis)):
	mae_solis += abs(skipped_sensor_data[i] - ghi_solis[i])
	mbe_solis += skipped_sensor_data[i] - ghi_solis[i]
	rmse_solis += (skipped_sensor_data[i] - ghi_solis[i])**2
for i in range(0,len(ghi_bird)):
	mae_pers += abs(skipped_sensor_data[i] - skipped_sensor_data_pers[i])
	rmse_pers += (skipped_sensor_data[i] - skipped_sensor_data_pers[i])**2
	mbe_pers += skipped_sensor_data[i] - skipped_sensor_data_pers[i]

mae_bird = mae_bird/len(ghi_bird)
nmae_bird= mae_bird/max(skipped_sensor_data)
mbe_bird = mbe_bird/len(ghi_bird)
rmse_bird = math.sqrt(rmse_bird/len(ghi_bird))
nrmse_bird=rmse_bird/max(skipped_sensor_data)
mae_solis = mae_solis/len(ghi_solis)
mbe_solis = mbe_solis/len(ghi_solis)
rmse_solis = math.sqrt(rmse_solis/len(ghi_solis))
mae_pers = mae_pers/len(skipped_sensor_data)
mbe_pers = mbe_pers/len(skipped_sensor_data)
nmae_pers =mae_pers/max(skipped_sensor_data)
nmbe_bird=mbe_bird/max(skipped_sensor_data)
rmse_pers = math.sqrt(rmse_pers/len(skipped_sensor_data))
nmae_solis=mae_solis/max(skipped_sensor_data)
nrmse_solis=rmse_solis/max(skipped_sensor_data)
nrmse_pers = rmse_pers/max(skipped_sensor_data)


#print "Bird Mean absolute error = %f\nRoot Mean Square error = %f"%(mae_bird,rmse_bird)
#print "Solis Mean absolute error = %f\nRoot Mean Square error = %f"%(mae_solis,rmse_solis)
#print argv[1]+",%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"%(mae_bird,mbe_bird,rmse_bird,mae_solis,mbe_solis,rmse_solis,mae_pers,mbe_pers,nmae_pers,nmbe_bird,rmse_pers,nmae_solis,nrmse_solis,nrmse_pers)
#.write(argv[1]+",%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"%(mae_bird,mbe_bird,rmse_bird,nmae_bird,mae_solis,mbe_solis,rmse_solis,mae_pers,mbe_pers,nmae_pers,nmbe_bird,rmse_pers,nmae_solis,nrmse_solis,nrmse_pers,nrmse_bird))
#z.close()
x= [i for i in range(len(ghi_solis))]
plt.plot(x,ghi_bird,x,ghi_solis,x,skipped_sensor_data,x,skipped_sensor_data_pers[0:len(x)])
plt.xlabel("Time (Minutes)", fontsize=20)
plt.ylabel(r'$Solar$ $Irradiance$ $GHI$ $(W/m^2)$', fontsize= 20)
plt.legend(["GHI_Bird","GHI_Solis","Actual data","Persistence data"],fontsize= 20)
plt.show()
