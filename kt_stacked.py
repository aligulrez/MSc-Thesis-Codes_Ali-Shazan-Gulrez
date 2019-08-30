#The code, plots the cluster spectrum of different classes
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import csv
from matplotlib.lines import Line2D


gn_data_file = open(argv[1],'r')
class_list_file = open(argv[2],'r')
#Get all the points in this class
points = []
dataarray = [[float(num) for num in row] for row in csv.reader(gn_data_file,delimiter=',')]

for line in class_list_file:
    points.append(int(line.strip())-2)
# setting bar width and number of points, averaging in 10 minutes period
bar_width = 10
num_bars = int(520/bar_width)
ind = np.arange(num_bars)

width = 1       # the width of the bars: can also be len(x) sequence
bins = [0.09*i for i in range(11)]
bins.append(10)
counts = []
colors = ['#003fe5','#0396d9','#07ceba','#0ac364','#0db71a','#7ca111','#958113','#8a4714','#7f1715','#Af1720','#ff1729']
for i in range(num_bars):
    data = []
    for j in points:
        for val in dataarray[j][bar_width*i:(bar_width*(i+1))+1]:
            data.append(val)
        # print data
    vals = np.array(np.histogram(data,bins)[0])
    vals = vals/float(sum(vals))
    counts.append(vals)

vals = []
prev = np.array([0 for i in range(num_bars)])
custom_lines = [Line2D([0], [0], color=col, lw=4) for col in colors]

for j in range(len(bins)-1):                 
    vals = np.array([counts[i][j] for i in range(num_bars)])
    plt.bar(ind, vals,bottom=prev,width= width,edgecolor='k',color=colors[j])
    prev = prev + vals
plt.xticks([i for i in range(num_bars)],[str(10*i) for i in range(num_bars)],rotation='vertical')
plt.xlabel("Minutes")
plt.ylabel("Probability")
plt.legend(custom_lines, ['0.00 - 0.09', '0.09 -0.18','0.18-0.27','0.27-0.36','0.36-0.45','0.45-0.54','0.54-0.63','0,63-0.72','0.72-0.81','0.81-0.90','0.90-1'],loc=1)
plt.show()
#plt.savefig(argv[2]+".png",dpi=600)


