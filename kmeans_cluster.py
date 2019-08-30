# plotting the pca1 and pca2 and finding silhoutte index
import csv
from sys import argv
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# This code clusters the data into four classes using k means clustering 
df = pd.read_csv(argv[1],header = None)
k = df.values
n_clusters=4
kmeans = KMeans(n_clusters)
kmeans.fit(df)
labels = kmeans.predict(df)
c = Counter(labels)
print c
#getting PCA index from the dates_file
# dates_file = open(argv[2],'r')

# for j,i in enumerate(labels):
# 	#if( i == 0):
# 	print "%s,%d"%(dates_file.readline().strip(),i)

# dates_file.close()
plot = 1
# the plotting of the cluster data based on PCA1 and PCA2 as they contain the maximum variance 
if(plot):
	colors = ['b','g','r','y']
	fig, ax = plt.subplots()
	for i,l in enumerate(labels):
		plt.scatter(k[i][0],k[i][1],color=colors[l])
	plt.xlabel("PCA1")
	plt.ylabel("PCA2")
	legend_elements = [Line2D([0], [0], marker='o', color='w', label='Class 0', markerfacecolor='b', markersize=15),
							Line2D([0], [0], marker='o', color='w', label='Class 1', markerfacecolor='g', markersize=15),
						   Line2D([0], [0], marker='o', color='w', label='Class 2', markerfacecolor='r', markersize=15),
						   Line2D([0], [0], marker='o', color='w', label='Class 3', markerfacecolor='y', markersize=15),
						]	
	ax.legend(handles=legend_elements, loc='right')                   
	plt.show()
				
# the code calculates the Silhoutte index to see the compactness of the cluster
sils = silhouette_samples(k, labels, metric='euclidean')

sil_index = [0 for i in range(n_clusters)]

for i in range(n_clusters):
        length = 0
        for j,val in enumerate(sils):
                if(labels[j] == i):
                        length += 1
                        sil_index[i] += val
        sil_index[i] = sil_index[i]/length

print sil_index
