import netCDF4
import numpy as np
import pandas as pd
import random
from datetime import datetime
from scipy import stats

# lat lon coords in NY
coords_in_NY = [[41.5, -74.5, -74.5], [42.5, -78.5, -73.5], [43.5, -75.5, -73.5], [44.5, -75.5, -73.5]]

def read_snowfall():
	print('\n\nGenerating snowfall data file')
	path = 'data/snowfall/'
	y = 2012
	m = 1
	filename = 'GLDAS_NOAH10_M.A201401.021.nc4'
	f = netCDF4.Dataset(path + filename)
	lat = f.variables['lat'][:].tolist()
	lon = f.variables['lon'][:].tolist()
	inds = []
	for i in range(len(lat)):
		for j in range(len(lon)):
			latind = int(lat[i] - 41.5)
			if latind >= 0 and latind <= 3:
				lonrange = coords_in_NY[latind]
				if lon[j] >= lonrange[1] and lon[j] <= lonrange[2]:
					inds.append([i, j])
	
	dat = []
	while y < 2023:
		datestr = str(y)
		if m < 10:
			datestr += '0' + str(m)
		else:
			datestr += str(m)
		fname = 'GLDAS_NOAH10_M.A' + datestr + '.021.nc4'
		f = netCDF4.Dataset(path + fname)
		snowfall = f.variables['SnowDepth_inst']
		sf = snowfall[:,:][0]
		sfsum = 0
		for ind in inds:
			sfsum += sf[ind[0], ind[1]]
		sfavg = sfsum / len(inds)
		dat.append([y, m, sfavg])


		if m == 12:
			print('  finished generating', y, 'monthly average snowfall in meters')
			m = 1
			y += 1
		else:
			m += 1
	

	open("snowfall.csv", "w").close()
	outf = open('snowfall.csv', 'a')
	outf.write('year,month,snowfall_avg\n')
	for t in dat:
		outf.write(str(t[0]) + ',' + str(t[1]) + ',' + str(t[2]) + '\n')
	outf.close()


def read_car_accidents():
	print('\n\nGenerating car accidents data file')
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
		if int(t[:4]) > 2022:
			break
	
	
	open("NY_car_accidents_data.csv", "w").close()
	f = open('NY_car_accidents_data.csv', 'a')
	f.write('date,accident_count\n')
	for i in range(len(dat)):
		f.write(str(date[i]) + ',' + str(dat[i]) + '\n')
	f.close()




if __name__ == '__main__':
	

	read_snowfall()
	read_car_accidents()
	

	