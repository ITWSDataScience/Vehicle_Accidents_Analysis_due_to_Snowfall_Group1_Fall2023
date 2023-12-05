import pandas as pd
import numpy as np

df = pd.read_csv('../data/dbscan_result.csv')
# col = [ID,avg_rain_q1,avg_rain_q2,avg_rain_q3,avg_rain_q4,avg_temp_q1,avg_temp_q2,avg_temp_q3,avg_temp_q4,cluster,LATITUDE,LONGITUDE]

# calculate each cluster's average rain and temperature in each quarter
result_li = []
for i in range(-1, 4):
    cluster = df[df['cluster'] == i]
    avg_rain_q1 = round(cluster['avg_rain_q1'].mean(), 2)
    avg_rain_q2 = round(cluster['avg_rain_q2'].mean(), 2)
    avg_rain_q3 = round(cluster['avg_rain_q3'].mean(), 2)
    avg_rain_q4 = round(cluster['avg_rain_q4'].mean(), 2)
    avg_temp_q1 = round(cluster['avg_temp_q1'].mean(), 2)
    avg_temp_q2 = round(cluster['avg_temp_q2'].mean(), 2)
    avg_temp_q3 = round(cluster['avg_temp_q3'].mean(), 2)
    avg_temp_q4 = round(cluster['avg_temp_q4'].mean(), 2)
    
    result_li.append([i, len(cluster), avg_rain_q1, avg_rain_q2, avg_rain_q3, avg_rain_q4, avg_temp_q1, avg_temp_q2, avg_temp_q3, avg_temp_q4])
# write to csv
result = pd.DataFrame(result_li, columns=['cluster', 'count', 'avg_rain_q1', 'avg_rain_q2', 'avg_rain_q3', 'avg_rain_q4', 'avg_temp_q1', 'avg_temp_q2', 'avg_temp_q3', 'avg_temp_q4'])
print(result)
result.to_csv('../data/dbscan_statistics.csv', index=False)