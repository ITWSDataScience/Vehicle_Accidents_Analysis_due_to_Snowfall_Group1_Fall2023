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
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression

def generate_dat_mat(indata, sf, sequence_len, ol):
	data = indata[:, 1]
	ret = []
	for i in range(len(data)-sequence_len+1):
		exist_outlier = 0
		for ind in ol:
			if ind >= i and ind < i+sequence_len:
				exist_outlier = 1
		if exist_outlier == 0:
			row = data[i:sequence_len+i].tolist()
			currdate = indata[sequence_len+i-1, 0].split('/')
			if not (int(currdate[0]), int(currdate[1])) in sf:
				print('date', indata[sequence_len+i-1, 0], 'not found')
				break
			row.insert(sequence_len-1, sf[(int(currdate[0]), int(currdate[1]))])
			ret.append(row)
	return np.array(ret)

def generate_dat_mat_v2(indata, sf, xlen, ylen, ol):
	data = indata[:, 1]
	ret = []
	for i in range(len(data)-xlen-ylen+1):
		exist_outlier = 0
		for ind in ol:
			if ind >= i and ind < i+xlen+ylen:
				exist_outlier = 1
		if exist_outlier == 0:
			row = data[i:xlen+i].tolist()
			currsf = 0
			for ind in range(i+xlen, i+xlen+ylen):
				currdate = indata[ind, 0].split('/')
				if not (int(currdate[0]), int(currdate[1])) in sf:
					print('ERROR: date', indata[ind, 0], 'not found')
					break
				currsf += sf[(int(currdate[0]), int(currdate[1]))]
			currsf /= ylen
			row.append(currsf)
			row.append(np.sum(data[xlen+i:xlen+ylen+i]))
			ret.append(row)
	return np.array(ret)

def prediction_result_analysis(pred, y_test):
	# ttestres = stats.ttest_ind(pred, y_test)
	# print(ttestres)
	psum = 0
	perc_diff_sum = 0
	for i in range(len(pred)):
		psum += abs(pred[i] - y_test[i])
		perc_diff_sum += abs(pred[i] - y_test[i]) / y_test[i]
	mae = psum / len(pred)
	perc_diff_avg = perc_diff_sum / len(y_test)
	print('MAE:', mae)
	print('test data mean:', np.mean(y_test))
	print('test data standard deviation:', np.std(y_test))
	print('average percentage difference from actual value:', perc_diff_avg*100, '%')


def approach_30_to_10total(accidents_data, sf, xlen, ylen, ol, lstm_layer_num, lstm_epoch_num):
	# generate data matrix without outlier
	print('\nGenerating car accidents sequence data without outliers')
	data = generate_dat_mat_v2(accidents_data, sf, xlen, ylen, ol)
	print(data)
	print('data matrix dimension:', np.shape(data))



	# Prediction based on car accidents data only
	print('\n\nImplementing First Step Prediction')
	y = data[:, xlen+1]
	X = np.delete(data, xlen+1, 1)
	Xtrain, Xtest, y_train, y_test = train_test_split(X, y, test_size = 0.3)
	X_train = np.delete(Xtrain, xlen, 1)
	X_test = np.delete(Xtest, xlen, 1)

	# Naive Approach
	print('\nNaive Approach')
	pred = []
	for i in range(len(X_test)):
		pred.append(int(np.sum(X_test[i]) / xlen * ylen))
	pred = np.array(pred)
	prediction_result_analysis(pred, y_test)
	
	# LSTM Approach
	print('\nLSTM Approach')
	lstm_model = tf.keras.Sequential()
	lstm_model.add(layers.LSTM(lstm_layer_num, activation='relu', input_shape=(xlen, 1)))
	lstm_model.add(layers.Dense(1))

	lstm_model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])
	lstm_model.fit(X_train, y_train, epochs=lstm_epoch_num, verbose=1)


	temp = X_test.reshape((len(X_test), xlen, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	print('train data size:', len(X_train), 'test data size:', len(X_test))
	prediction_result_analysis(pred, y_test)



	# Second step prediction with naive pred results and snowfall
	print('\n\nImplementing Second Step Prediction')
	# combine first step prediction and snowfall
	temp = X_train.reshape((len(X_train), xlen, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	new_X = np.column_stack((pred, Xtrain[:, xlen]))

	# Model Train
	# Multilayer Perceptron (Feed Forard Neural Netork)
	mlp = MLPRegressor(random_state=1, max_iter=500).fit(new_X, y_train)
	# Linear Regression
	lr = LinearRegression().fit(new_X, y_train)

	
	# Predict test data
	# First step
	temp = X_test.reshape((len(X_test), xlen, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	
	# Second step
	new_X = np.column_stack((pred, Xtest[:, xlen]))
	print(new_X)
	# Multilayer Perceptron (Feed Forard Neural Netork)
	print('\nMultilayer Perceptron')
	pred = mlp.predict(new_X)
	prediction_result_analysis(pred, y_test)
	print(mlp.score(new_X, y_test))

	# Linear Regression
	print('\nLinear Regression')
	pred = lr.predict(new_X)
	prediction_result_analysis(pred, y_test)
	print('linear regression coef:', lr.coef_)
	print('intercept:', lr.intercept_)


def approach_10_to_1(accidents_data, sf, sequence_len, ol, lstm_layer_num, lstm_epoch_num):
	# generate data matrix without outlier
	print('\nGenerating car accidents sequence data without outliers')
	data = generate_dat_mat(accidents_data, sf, sequence_len, ol)
	print(data)
	print('data matrix dimension:', np.shape(data))



	# Prediction based on car accidents data only
	print('\n\nImplementing First Step Prediction')
	y = data[:, sequence_len]
	X = np.delete(data, sequence_len, 1)
	Xtrain, Xtest, y_train, y_test = train_test_split(X, y, test_size = 0.3)
	X_train = np.delete(Xtrain, sequence_len-1, 1)
	X_test = np.delete(Xtest, sequence_len-1, 1)

	# Naive Approach
	print('\nNaive Approach')
	pred = []
	for i in range(len(X_test)):
		pred.append(np.sum(X_test[i]) / (sequence_len-1))
	pred = np.array(pred)
	prediction_result_analysis(pred, y_test)
	
	# LSTM Approach
	print('\nLSTM Approach')
	lstm_model = tf.keras.Sequential()
	lstm_model.add(layers.LSTM(lstm_layer_num, activation='relu', input_shape=(sequence_len-1, 1)))
	lstm_model.add(layers.Dense(1))

	lstm_model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])
	lstm_model.fit(X_train, y_train, epochs=lstm_epoch_num, verbose=1)


	temp = X_test.reshape((len(X_test), sequence_len-1, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	print('train data size:', len(X_train), 'test data size:', len(X_test))
	prediction_result_analysis(pred, y_test)



	# Second step prediction with first step pred results and snowfall
	print('\n\nImplementing Second Step Prediction')
	# combine first step prediction and snowfall
	temp = X_train.reshape((len(X_train), sequence_len-1, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	new_X = np.column_stack((pred, Xtrain[:, sequence_len-1]))

	# Model Train
	# Multilayer Perceptron (Feed Forard Neural Netork)
	mlp = MLPRegressor(random_state=1, max_iter=500).fit(new_X, y_train)
	# Linear Regression
	lr = LinearRegression().fit(new_X, y_train)

	
	# Predict test data
	# First step
	temp = X_test.reshape((len(X_test), sequence_len-1, 1))
	pred = lstm_model.predict(temp, verbose=0).tolist()
	for i in range(len(pred)):
		pred[i] = int(pred[i][0])
	pred = np.array(pred)
	
	# Second step
	new_X = np.column_stack((pred, Xtest[:, sequence_len-1]))
	print(new_X)
	# Multilayer Perceptron (Feed Forard Neural Netork)
	print('\nMultilayer Perceptron')
	pred = mlp.predict(new_X)
	prediction_result_analysis(pred, y_test)
	print(mlp.score(new_X, y_test))

	# Linear Regression
	print('\nLinear Regression')
	pred = lr.predict(new_X)
	prediction_result_analysis(pred, y_test)
	print('linear regression coef:', lr.coef_)
	print('intercept:', lr.intercept_)

if __name__ == '__main__':

	# =====================================================================================
	# adjust parameters here
	sequence_len = 11
	xlen = 30
	ylen = 10
	lstm_layer_num = 50
	lstm_epoch_num = 50
	# =====================================================================================

	# read processed data
	# car accident data
	accidents_data_file_name = 'NY_car_accidents_data.csv'
	accidents_data = pd.read_csv(accidents_data_file_name)
	accidents_data = accidents_data.values
	
	# snowfall data
	snowfall_data_file_name = 'snowfall.csv'
	snowfall_data = pd.read_csv(snowfall_data_file_name)
	snowfall_data = snowfall_data.values
	sf = dict()
	for i in range(len(snowfall_data)):
		if int(snowfall_data[i][1]) > 3 and int(snowfall_data[i][1]) < 10:
			sf[(int(snowfall_data[i][0]), int(snowfall_data[i][1]))] = 0
		
		else:
			sf[(int(snowfall_data[i][0]), int(snowfall_data[i][1]))] = snowfall_data[i][2]

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

	# approach_30_to_10total(accidents_data, sf, xlen, ylen, ol, lstm_layer_num, lstm_epoch_num)
	approach_10_to_1(accidents_data, sf, sequence_len, ol, lstm_layer_num, lstm_epoch_num)

