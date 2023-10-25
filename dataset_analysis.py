import numpy as np
import pandas as pd

def accidents_data_analysis():
	print('Implementing car accidents data analysis:')
	accidents_data_file_name = 'NY_car_accidents_data.csv'
	accidents_data = pd.read_csv(accidents_data_file_name)
	accidents_data = accidents_data.values
	print('dataset:')
	print(accidents_data)

	print('\navg accidents count for each day of a week:')
	dw = 6
	dw_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	stat_dw = [0]*7
	dw_count = [0]*7
	for i in range(len(accidents_data)):
		stat_dw[dw] += int(accidents_data[i, 1])
		dw_count[dw] += 1
		if dw == 6:
			dw = 0
		else:
			dw += 1
	for i in range(7):
		print(dw_name[i]+':', stat_dw[i] / dw_count[i])

	print('\n\ndaily avg accidents for each month of a year:')
	stat_my = [0]*12
	my_count = [0]*12
	for i in range(len(accidents_data)):
		currdate = accidents_data[i, 0].split('/')
		currm = int(currdate[1])
		stat_my[currm-1] += int(accidents_data[i, 1])
		my_count[currm-1] += 1
	for i in range(12):
		stat_my[i] /= my_count[i]
		print('month', i+1, ':', stat_my[i])
	start = 2
	end = 10
	print('daily avg from Mar to Oct (no snowfall season):', np.sum(stat_my[start:end]) / 8)
	print('daily avg from Nov to Feb (snowfall season):', (np.sum(stat_my[:start]) + np.sum(stat_my[end:])) / 4)

	print('\n\ndaily avg accidents for each year:')
	y = 2012
	y_sum = 0
	y_count = 0
	for i in range(len(accidents_data)):
		currdate = accidents_data[i, 0].split('/')
		curry = int(currdate[0])
		if curry != y:
			print(y, 'daily avg:', y_sum / y_count)
			y_sum = 0
			y_count = 0
			y = curry
		y_sum += int(accidents_data[i, 1])
		y_count += 1
	print(y, 'daily avg:', y_sum / y_count)

if __name__ == '__main__':
	accidents_data_analysis()