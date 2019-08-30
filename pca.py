# code for PCA analysis, scree plot for 100 pca components and plotting the scree plot 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sys import argv
from sys import stdout
# load dataset into Pandas DataFrame
df = pd.read_csv(argv[1],header = None)

# Separating out the features
x = df.values
# Standardizing the features
x = StandardScaler().fit_transform(x)
# pca = PCA()
pca = PCA(n_components=100)
principalComponents = pca.fit_transform(x)

# Draw a scree plot and a PCA plot

#The following code constructs the Scree plot
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
x=range(1,len(per_var)+1)
plt.bar(x, height=per_var, tick_label=labels)
plt.xticks(x, labels, rotation='vertical',fontsize=8)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')
if(argv[2] == "1"):
    plt.show()
for val in principalComponents:
    for i in val:
        stdout.write(str(i))
        stdout.write(",")
    stdout.write("\n")
