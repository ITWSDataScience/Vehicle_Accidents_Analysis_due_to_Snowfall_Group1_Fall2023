import pandas as pd

if __name__ == "__main__":
  df1 = pd.read_csv('../data/spectral_result.csv')
  # col = ID, Lat, Lon, Label
  df2 = pd.read_csv('../data/clean_iqr.csv')
  # col = "ID","avg_rain_q1","avg_rain_q2","avg_rain_q3","avg_rain_q4","avg_temp_q1","avg_temp_q2","avg_temp_q3","avg_temp_q4"

  # merge df1 and df2
  df1 = df1.merge(df2, on='ID')
  
  # print df1 with the first 4 columns
  print(df1[df1.columns[3:4]])
  print(df1[['cluster']])