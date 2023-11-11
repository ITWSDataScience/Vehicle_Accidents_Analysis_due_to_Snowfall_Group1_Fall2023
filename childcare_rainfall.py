import csv

if __name__ == '__main__':
    li = ['id/date']
    month = 3
    for i in range(2013, 2024):
        while month < 13:
            if i == 2023 and month == 3:
                break
            if month < 10:
                month_str = '0' + str(month)
            else:
                month_str = str(month)
            li.append(str(i) + '-' + month_str + '-01')
            month += 1
        month = 1

    temp = open('D:\RPI\DSdata\Child_Care_Centers_clean.csv', 'r')
    child_care = csv.reader(temp)
    row_col_li, row_col_num = [], 0
    print("---start to read row and col number---")
    for idx, i in enumerate(child_care):  # loop through all child care centers
        if idx == 0:
            continue
        id, lat, lon = i[0], round(float(i[1]), 1), round(float(i[2]), 1)
        row_num = int((90.0 - lat) * 10 + 1)
        col_num = int((180.0 + lon) * 10 + 1)
        print('id:', id, 'row_num:', row_num, 'col_num:', col_num)
        row_col_li.append([id, row_num, col_num])
        row_col_num += 1
    temp.close()
    print("---finish reading row and col number---")

    print("---start to write---")
    result = [li]
    for idx, row_col in enumerate(row_col_li):
        result.append([row_col[0]])
    """
    result = [
        ['id/date', '2013-03-01', '2013-04-01', ...],
        ['id1', 'data1', 'data2', ...],
        ...
    ]
    row_col_li = [
        [id1, row_num1, col_num1],
        ...
    ]
    """
    # read data from nasa's temperature data
    for date_idx, date in enumerate(li[1:]):
        print('---------', date, date_idx, '---------')
        f = open('D:/RPI/DSdata/rainfalldata/GPM_3IMERGM_' + date + '_rgb_3600x1800.SS.CSV', 'r')
        reader = csv.reader(f)
        data_li = []
        for idx, data in enumerate(reader):
            data_li.append(data)
        for x, y in enumerate(row_col_li):
            print(x, y[0])
            result[x + 1].append(data_li[y[1]][y[2]])
        f.close()
    print("numer of id:", row_col_num)
    print("shape: ", len(result), len(result[0]), len(result[1]))
    f_final = open('D:\RPI\DSdata\child_care_rainfall_final.csv', 'w')
    writer = csv.writer(f_final)
    writer.writerows(result)
    f_final.close()
    print("---program finished---")
