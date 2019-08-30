import csv
from sys import argv
import pandas as pd
import numpy as np
from collections import Counter
feature_file = open(argv[1],'r')
dataarray = csv.reader(feature_file,delimiter=',')
n = [np.zeros(592) for i in range(20)]
dates = []
for i,row in enumerate(dataarray):
	for j in range(1,20):
		n[j-1][i] = float(row[j])
	dates.append(row[0])

df = pd.DataFrame({
	'n'+str(i):nn for i,nn in enumerate(n)
})

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4)
kmeans.fit(df)
labels = kmeans.predict(df)
c = Counter(labels)
print c
# print "date,type"
for j,i in enumerate(labels):
	#if( i == 0):
	print "%s,%d"%(dates[j],i)