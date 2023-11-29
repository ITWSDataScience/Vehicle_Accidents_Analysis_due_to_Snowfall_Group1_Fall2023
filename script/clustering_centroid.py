import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_samples, silhouette_score

def output_result(data, result, fname):
	# output kmeans result to csv
	coords_f = np.genfromtxt('../data/Child_Care_Centers_clean.csv', delimiter = ',', skip_header = 1)

	open(fname, 'w').close()
	outfile = open(fname, 'a')
	outfile.write('ID,lat,lon,cluster,avg_rainfall_spring,avg_rainfall_summer,avg_rainfall_autumn,avg_rainfall_winter,')
	outfile.write('avg_temperature_spring,avg_temperature_summer,avg_temperature_autumn,avg_temperature_winter\n')

	ind = 0
	for i in range(len(coords_f)):
		if coords_f[i][0] == data[ind][0]:
			for j in range(3):
				outfile.write(str(coords_f[i][j]) + ',')
			outfile.write(str(result[ind]) + ',')
			for j in range(1, 8):
				outfile.write(str(data[ind][j]) + ',')
			outfile.write(str(data[ind][8]) + '\n')
			ind += 1
	outfile.close()


def cluster_stats(data, result, cluster_num):
	titles = ['Spring Rainfall', 'Summer Rainfall', 'Autumn Rainfall', 'Winter Rainfall'
	, 'Spring Temperature', 'Summer Temperature', 'Autumn Temperature', 'Winter Temperature']
	clusters = []
	for i in range(cluster_num):
		clusters.append([])
	for i in range(len(result)):
		clusters[result[i]].append(data[i])
	for i in range(cluster_num):
		clusters[i] = np.array(clusters[i])
		print('  cluster', i, 'stats:')
		for j in range(8):
			arr = clusters[i][:, j]
			print('   ', titles[j] + ': avg:', np.mean(arr), 'std:', np.std(arr), 'min:', np.min(arr), 'max:', np.max(arr))


if __name__ == '__main__':
	data = np.genfromtxt('../data/training_data.csv', delimiter = ',', skip_header = 1)
	train_data = data[:, 1:]
	
	# predefined number of clusters
	cluster_num = 4

	print('\nKmeans result:')
	print('Number of clusters:', cluster_num)
	kmeans_model = KMeans(n_clusters = cluster_num)
	result = kmeans_model.fit_predict(train_data)
	unique, counts = np.unique(result, return_counts = True)
	for i in range(len(unique)):
		print('  cluster', unique[i], 'size:', counts[i])
	print('total counts:', np.sum(counts))
	silhouette_avg = silhouette_score(train_data, result)
	print('silhouette score:', silhouette_avg)
	# sample_silhouette_values = silhouette_samples(train_data, result)
	# print(sample_silhouette_values)
	cluster_stats(train_data, result, cluster_num)

	output_result(data, result, '../data/kmeans_result.csv')


	print('\n\nGaussian Mixture result:')
	print('Number of clusters:', cluster_num)
	gaussian_model = GaussianMixture(n_components = cluster_num)
	gaussian_model.fit(train_data)
	gaussian_result = gaussian_model.predict(train_data)
	unique, counts = np.unique(gaussian_result, return_counts = True)
	for i in range(len(unique)):
		print('  cluster', unique[i], 'size:', counts[i])
	print('total counts:', np.sum(counts))
	silhouette_avg = silhouette_score(train_data, gaussian_result)
	print('silhouette score:', silhouette_avg)
	cluster_stats(train_data, gaussian_result, cluster_num)

	output_result(data, gaussian_result, '../data/gaussian_result.csv')