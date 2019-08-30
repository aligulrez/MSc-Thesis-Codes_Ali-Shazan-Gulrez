# code for finding normalised gn, to remove sasonality and stationarity 
from datetime import datetime
import numpy as np
import pandas as pd
import pvlib
import math
import matplotlib.pyplot as plt
import csv
from sys import argv
#MM-DD-YYYY format date
# The code here truncates the number of points in the morning and evening hours to remove obvious variance so that PCA runs well
date_rng = pd.date_range(start=argv[1][4:6]+"/"+argv[1][6:8]+"/"+argv[1][0:4]+' 05:00:00', end=argv[1][4:6]+"/"+argv[1][6:8]+"/"+argv[1][0:4]+' 20:00:00', tz='US/Hawaii',freq='t')
timestamp_date_rng = pd.to_datetime(date_rng, infer_datetime_format=True)
# the code calculates the zenith and apparent elevation to be used as inputs to Bird and modified Solis model 
solar_position = pvlib.solarposition.get_solarposition(timestamp_date_rng, latitude=21.31, longitude=-158.08, altitude=None, pressure=None, method="nrel_numpy", temperature=25)
zeniths = solar_position['zenith']
apparent_elevation = solar_position['apparent_elevation']
ghi_bird = []
ghi_solis = []
#calculating the AM based on Kasten relation 
for zen in zeniths:
	if(zen < 89):
		am= abs((1/math.cos(math.radians(zen)))+0.15/(93.885-zen)**1.25)
	else:
		am = 0
	ghi_bird.append(pvlib.clearsky.bird(zenith=zen, airmass_relative=am, aod380=0.15, aod500=0.1, precipitable_water=1.5, ozone=0.3, pressure=101325.0, dni_extra=1367.0, asymmetry=0.85, albedo=0.2)['ghi'])

sensor_data_file=open(argv[1],'r')
dataarray=csv.reader(sensor_data_file,delimiter=',')
sensor1=[float(row[6]) for row in dataarray]
skipped_sensor_data = []
normalized_gn = []
for i in range(0,len(sensor1),60):
	skipped_sensor_data.append(sensor1[i])
# dividing the irradiance data with the clear sky model to get a normalised gn     
for i in range(0,len(ghi_bird)):
        if(ghi_bird[i] != 0):
                normalized_gn.append(skipped_sensor_data[i]/ghi_bird[i])
        else:
                normalized_gn.append(0.00001)
print normalized_gn
# plt.plot(normalized_gn)
# plt.show()
