from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

data = np.genfromtxt('../data/clean_iqr.csv', delimiter = ',', skip_header = 1)
temp = np.genfromtxt('../data/Child_Care_Centers_clean.csv', delimiter = ',', skip_header = 1)
lacation = dict()
for i in range(len(temp)):
    lacation[temp[i][0]] = temp[i][1:]
train_data = data[:, 1:]
train_data = scaler.fit_transform(train_data)

# Initialize SpectralClustering
clustering = SpectralClustering(n_clusters=6, assign_labels='discretize')
# Fit and get cluster labels
clustering.fit(train_data)
labels = clustering.labels_

# Calculate silhouette score
score = silhouette_score(train_data, labels)
print("Silhouette score: ", score)

filename = '../data/spectral_result.csv'
with open(filename, 'w') as outfile:
    outfile.write('ID, Lat, Lon, Label\n')
    for i in range(len(labels)):
        outfile.write(str(data[i][0]) + ',' + str(lacation[data[i][0]][0]) + ',' + str(lacation[data[i][0]][1]) + ',' + str(labels[i]) + '\n')


