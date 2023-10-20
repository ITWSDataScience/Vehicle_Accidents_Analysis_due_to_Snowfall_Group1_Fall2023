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

def generate_dat_mat(data, sequence_len, ol):
	ret = []
	for i in range(len(data)-sequence_len+1):
		exist_outlier = 0
		for ind in ol:
			if ind >= i and ind < i+sequence_len:
				exist_outlier = 1
		if exist_outlier == 0:
			ret.append(data[i:sequence_len+i].tolist())
	return np.array(ret)





if __name__ == '__main__':

	# =====================================================================================
	# adjust parameters here
	sequence_len = 11
	lstm_layer_num = 50
	lstm_epoch_num = 50
	# =====================================================================================

	# read processed data
	accidents_data_file_name = 'NY_car_accidents_data.csv'
	accidents_data = pd.read_csv(accidents_data_file_name)
	accidents_data = accidents_data.values
	

	# detect outliers
	print('\n\nDetecting outliers for car accidents data using IQR method, r set to 1.5')
	acc_num = accidents_data[:, 1]
	acc_num = acc_num.tolist()
	q75, q25 = np.percentile(acc_num, [75 ,25])
	print('  25, 50, 75 quartile:', q25, np.median(acc_num), q75)
	iqr = q75 - q25
	upper = q75 + 1.5*iqr
	lower = q25 - 1.5*iqr
	print('  upper and lower fence:', upper, lower)
	ol = []
	for i in range(len(acc_num)):
		if acc_num[i] > upper or acc_num[i] < lower:
			ol.append(i)
	print(' ', len(ol), 'outliers found in car accidents data')
	for ind in ol:
		print('    dates:', accidents_data[ind, 0], 'accidents number:', accidents_data[ind, 1])


	# generate data matrix without outlier
	print('\nGenerating car accidents sequence data without outliers')
	data = generate_dat_mat(accidents_data[:, 1], sequence_len, ol)
	print(data)
	print('data matrix dimension:', np.shape(data))

	

	# Naive Prediction based on car accidents data only
	print('\nRunning naive prediction')
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
	print('test data standard deviation:', np.std(y_test))
	print('average percentage difference from actual value:', perc_diff_avg*100, '%')