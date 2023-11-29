from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler
import pandas as pd
import csv

file = ("data/training_data.csv")
data = []
with open(file, newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)
file = ("data\Child_Care_Centers_clean.csv")
locations = []
with open(file, newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        locations.append(row)
train_data = data[1:][1:]
# Convert the list of lists to float values for clustering
data_float = [[float(val) for val in row] for row in train_data]

# Preprocess the data (scaling)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_float)

# Perform OPTICS clustering
clustering = OPTICS(min_samples=50, xi=0.05, min_cluster_size=0.05)
clustering.fit(data_scaled)

# Retrieve cluster labels
labels = clustering.labels_

# Print the cluster labels
a = set(labels)
print(a)
file_path = 'optics_cluster.csv'
# Writing data to CSV file
with open(file_path, 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    
    csvwriter.writerow(['ID', 'Label'])
    # writing the data rows
    for i in range(0, len(labels)):
        csvwriter.writerow([data[i+1][0], labels[i]])
