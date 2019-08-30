import csv
from sys import argv
import pandas as pd
import numpy as np
from collections import Counter
feature_file = open(argv[1],'r')
dataarray = csv.reader(feature_file,delimiter=',')
x = np.zeros(736)
y = np.zeros(736)
z = np.zeros(736)
dates = []
for i,row in enumerate(dataarray):
	x[i] = float(row[1])
	y[i] = float(row[2])
	z[i] = float(row[3]) + 1
	dates.append(row[0])
x = x/max(x)
y = y/max(y)
z = z/max(abs(z))
df = pd.DataFrame({
   # 'x': x,
   # 'y': y,
	'z': z
})

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans.fit(df)
labels = kmeans.predict(df)
c = Counter(labels)
print c
# print "date,type"
# for j,i in enumerate(labels):
	# print "%s,%d"%(dates[j],i)