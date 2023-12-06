import pandas as pd
import numpy as np

if __name__ == "__main__":
  df1 = pd.read_csv('../data/spectral_result.csv')
  df2 = pd.read_csv('../data/spectral_statistics.csv')
  # df1col = [ID,avg_rain_q1,avg_rain_q2,avg_rain_q3,avg_rain_q4,avg_temp_q1,avg_temp_q2,avg_temp_q3,avg_temp_q4,cluster,LATITUDE,LONGITUDE]
  # df2col = cluster,count,avg_rain_q1,avg_rain_q2,avg_rain_q3,avg_rain_q4,avg_temp_q1,avg_temp_q2,avg_temp_q3,avg_temp_q4
  rain_data = df2[['avg_rain_q1', 'avg_rain_q2', 'avg_rain_q3', 'avg_rain_q4']]
  # get each cluster's highest rain
  rain_max = rain_data.max(axis=1)
  df2['highest_rain'] = rain_max
  
  # sort df2 by highest_rain and season 2's temperature
  df2 = df2.sort_values(by=['highest_rain', 'avg_temp_q2'], ascending=True)
  # reset index
  df2 = df2.reset_index(drop=True)
  after_neg1 = False
  for idx, row in df2.iterrows():
    if row['cluster'] == -1:
      after_neg1 = True
      df1.loc[df1['cluster'] == row['cluster'], 'rank'] = int(-1)
      continue
    if after_neg1:
      idx -= 1
    print('cluster: ', row['cluster'], 'idx: ', idx)
    # if df1['cluster'] == df2['cluster'], change df1's cluster to idx
    df1.loc[df1['cluster'] == row['cluster'], 'rank'] = int(idx)
  df1['rank'] = df1['rank'].astype(int)

  print(df1[['ID', 'cluster', 'rank']])

  df1.to_csv('../data/spectral_result.csv', index=False)