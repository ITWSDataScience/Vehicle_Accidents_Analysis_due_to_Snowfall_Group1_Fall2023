import numpy as np

if __name__ == '__main__':
	data = np.genfromtxt('../data/combined_dataset.csv', delimiter = ',', skip_header = 1)
	training_data = []

	# sum up temp & rain by quarters
	for i in range(len(data)):
		# loop by child care center
		curr_row = data[i]
		row = [0] * 8

		# rain
		for y in range(1, 121, 12):
			# loop by year
			for quarter in range(4):
				# loop by quarter
				for month in range(3):
					# add each month to corresponding quarter
					row[quarter] += curr_row[y + quarter * 3 + month]
		
		# temp
		for y in range(121, 241, 12):
			# loop by year
			for quarter in range(4):
				# loop by quarter
				for month in range(3):
					# add each month to corresponding quarter
					row[quarter + 4] += curr_row[y + quarter * 3 + month]
		training_data.append([curr_row[0]] + row)
	
	# compute avg
	for i in range(len(training_data)):
		for j in range(1, 9):
			training_data[i][j] /= 30
	
	# output training data to csv
	outfile = open('../data/training_data.csv', 'a')
	outfile.write('ID,avg_rainfall_spring,avg_rainfall_summer,avg_rainfall_autumn,avg_rainfall_winter,')
	outfile.write('avg_temperature_spring,avg_temperature_summer,avg_temperature_autumn,avg_temperature_winter\n')
	for i in range(len(training_data)):
		for j in range(8):
			outfile.write(str(training_data[i][j]) + ',')
		outfile.write(str(training_data[i][8]) + '\n')
	outfile.close()
