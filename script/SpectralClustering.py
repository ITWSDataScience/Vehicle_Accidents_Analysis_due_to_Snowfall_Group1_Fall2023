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
clustering = SpectralClustering(4, assign_labels='discretize')
# Fit and get cluster labels
result = clustering.fit_predict(train_data)
d = dict()
d["0"] = []
d["1"] = []
d["2"] = []
d["3"] = []
for i in range(len(result)):
	d[str(result[i])].append(data[i])
for i in range(4):
    Spring_Rainfall = []
    Summer_Rainfall = []
    Autumn_Rainfall = []
    Winter_Rainfall = []
    Spring_Temperature = []
    Summer_Temperature = []
    Autumn_Temperature = []
    Winter_Temperature = []
    for j in range(len(d[str(i)])):
        Spring_Rainfall.append(d[str(i)][j][1])
        Summer_Rainfall.append(d[str(i)][j][2])
        Autumn_Rainfall.append(d[str(i)][j][3])
        Winter_Rainfall.append(d[str(i)][j][4])
        Spring_Temperature.append(d[str(i)][j][5])
        Summer_Temperature.append(d[str(i)][j][6])
        Autumn_Temperature.append(d[str(i)][j][7])
        Winter_Temperature.append(d[str(i)][j][8])
    print("cluster" + str(i) + ":" + str(len(d[str(i)])) + " " + str(np.mean(Spring_Rainfall)) + " " + str(np.mean(Summer_Rainfall)) + " " + str(np.mean(Autumn_Rainfall)) + " " + str(np.mean(Winter_Rainfall)) + " " + str(np.mean(Spring_Temperature)) + " " + str(np.mean(Summer_Temperature)) + " " + str(np.mean(Autumn_Temperature)) + " " + str(np.mean(Winter_Temperature)))

score = silhouette_score(train_data, result)
print("Silhouette score: ", score)

filename = '../data/spectral_result.csv'
with open(filename, 'w') as outfile:
    outfile.write('ID, Lat, Lon, Label\n')
    for i in range(len(result)):
        outfile.write(str(data[i][0]) + ',' + str(lacation[data[i][0]][0]) + ',' + str(lacation[data[i][0]][1]) + ',' + str(result[i]) + '\n')


