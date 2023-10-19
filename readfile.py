import netCDF4
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import random
from datetime import datetime
from scipy import stats

def read_snowfall():
	path = 'data/snowfall/'
	fname = 'GLDAS_NOAH10_M.A200001.021.nc4'
	f = netCDF4.Dataset(path + fname)
	print(f.variables.keys())
	print('\n\n')
	snowfall = f.variables['SnowDepth_inst']
	lat = f.variables['lat']
	lon = f.variables['lon']
	print(lat[:])
	print(lon[:])
	print(snowfall)
	sf = snowfall[:,:][0]

	open("snowfall.csv", "w").close()
	outf = open('snowfall.csv', 'a')
	for i in range(len(sf)):
		l = ''
		for j in range(len(sf[0])):
			l += ',' + str(sf[i, j])
		l = l[1:] + '\n'
		outf.write(l)
	outf.close()


def read_car_accidents():
	car_acc_f = pd.read_csv("data/Motor_Vehicle_Collisions_-_Crashes_20231013.csv")
	car_acc_f = car_acc_f.values
	dates = car_acc_f[:,0]
	for i in range(len(dates)):
		curr = dates[i].split('/')
		dates[i] = '/'.join([curr[2], curr[0], curr[1]])
	dates = np.sort(dates)
	dat = []
	count = 0
	curr = dates[0]
	for t in dates:
		if curr == t:
			count += 1
		else:
			dat.append(count)
			count = 1
			curr = t
	dat.pop()
	dat = np.array(dat)
	return dat

def generate_dat_mat(data, sequence_len):
	ret = data[:sequence_len]
	for i in range(1, len(data)-sequence_len):
		ret = np.vstack([ret, data[i:sequence_len+i]])
	return ret

if __name__ == '__main__':
	

	# read_snowfall()
	car_accident_data = read_car_accidents()
	

	# Naive Prediction Test Run based on car accidents data only

	# =====================================================================================
	# adjust parameters here
	sequence_len = 11
	lstm_layer_num = 50
	lstm_epoch_num = 50
	# =====================================================================================

	data = generate_dat_mat(car_accident_data, sequence_len)
	y = data[:, 10]
	X = np.delete(data, 10, 1)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

	model = tf.keras.Sequential()
	model.add(layers.LSTM(lstm_layer_num, activation='relu', input_shape=(sequence_len-1, 1)))
	model.add(layers.Dense(1))

	model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])
	model.fit(X_train, y_train, epochs=lstm_epoch_num, verbose=1)

	# for i in range(50):
	# 	temp = X_test[i, :].reshape((1, sequence_len-1, 1))
	# 	pred = model.predict(temp, verbose=1)
	# 	print(pred[0][0], y_test[i])

	temp = X_test.reshape((len(X_test), sequence_len-1, 1))
	pred = model.predict(temp, verbose=1)
	pred_ = []
	for t in pred:
		pred_.append(t[0])
	pred_ = np.array(pred_)
	ttestres = stats.ttest_ind(pred_, y_test)
	print(ttestres)
	psum = 0
	perc_diff_sum = 0
	for i in range(len(pred)):
		pred[i][0] = int(pred[i][0])
		psum += abs(pred[i][0] - y_test[i])
		perc_diff_sum += abs(pred[i][0] - y_test[i]) / y_test[i]
	mae = psum / len(X_test)
	perc_diff_avg = perc_diff_sum / len(y_test)
	print('train data size:', len(X_train), 'test data size:', len(X_test))
	print('MAE:', mae)
	print('test data mean:', np.mean(y_test))
	print('average percentage difference from actual value:', perc_diff_avg*100, '%')