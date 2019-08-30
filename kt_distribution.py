#Plots the Kt distribution
#kt_distribution.py "10/07/2011" data\20111007.txt
from datetime import datetime
import numpy as np
import pandas as pd
import pvlib
import math
import matplotlib.pyplot as plt
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
import csv
from sys import argv
# z = open('features_kt_all.csv','a')
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

sensor_data_file=open(argv[2],'r')
dataarray = csv.reader(sensor_data_file,delimiter=',')
sensor_data =[float(row[6]) for row in dataarray]
kt = []

for x,i in enumerate(range(0,len(sensor_data),60)):
	if(ghi_bird[x] != 0):
		if(sensor_data[i]/ghi_bird[x] > 1.0):
			kt.append(1.0)
		else:
			kt.append(sensor_data[i]/ghi_bird[x])
weights = np.ones_like(kt)/len(kt)
n,bins,patches = plt.hist(kt,bins=[0.05*i for i in range(1,21)],rwidth=0.9,weights=weights)
plt.xlabel("Clear sky Index ($k_t$)", fontsize=14)
plt.ylabel("Probability", fontsize=14)
# z.write(argv[1]+",")
# for i in n:
	# z.write(str(i)+",")
# z.write('\n')
# z.close()
plt.yticks(np.arange(0,0.6,0.1))
plt.show()
