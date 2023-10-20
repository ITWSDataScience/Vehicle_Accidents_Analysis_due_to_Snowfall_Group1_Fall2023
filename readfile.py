import netCDF4
import numpy as np
import pandas as pd
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
	date = [curr]
	for t in dates:
		if curr == t:
			count += 1
		else:
			dat.append(count)
			count = 1
			curr = t
			date.append(curr)
	dat.pop()
	date.pop()
	
	f = open('NY_car_accidents_data.csv', 'a')
	f.write('date,accident_count\n')
	for i in range(len(dat)):
		f.write(str(date[i]) + ',' + str(dat[i]) + '\n')
	f.close()




if __name__ == '__main__':
	

	# read_snowfall()
	read_car_accidents()
	

	