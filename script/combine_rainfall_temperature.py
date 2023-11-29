
import csv

def format_header(filename, header):
    new_header = []
    for name in header:
        if filename == "child_care_rainfall_final.csv":
            new_name = 'rain'
        elif filename == "child_care_temperature_final.csv":
            new_name = 'temp'
        else:
            print("ERROR")
            break
        
        m = name.split("-")
        for val in m:
            new_name += "_" + val
        
        new_header.append(new_name.strip())
    return new_header

def read_data_file(filename, int_field_indices=[], float_field_indices=[]):
    lineno = 0
    data = dict()
    filereader = csv.reader(open(filename, encoding="utf-8"), delimiter=",", quotechar='"')
    for line in filereader:
        lineno += 1
        if lineno == 1:
            data['ids'] = format_header(filename, line[1:121])
            continue
        
        outlier = False
        for i in range(len(line)):
            if i == 0:
                # id number
                line[i] = int(line[i])
            else:
                line[i] = float(line[i])
                if line[i] == 99999.0:
                    outlier = True
        
        if len(line) != 0 and outlier == False:
            data[line[0]] = line[1:121]
    return data

def merge(rainfall, temperature):
    # tempareture dataset has less datapoints, merging based on temperature
    combined = dict()
    new_rainfall = dict()
    for id in temperature.keys():
        if id in rainfall.keys():
            new_rainfall[id] = rainfall[id]
            combined[id] = rainfall[id] + temperature[id]
    return new_rainfall, combined


if __name__ == '__main__':
    # data from 2013-03-01 to 2023-02-01
    filename1 = "child_care_rainfall_final.csv"
    # data from 2013-03-01 to 2023-03-01
    filename2 = "child_care_temperature_final.csv"

    # a dictionary where key is the id of the childcare centers
    # the value is the rainfall data from 2013-03-01 to 2023-02-01
    # rainfall has 6335 lines including header
    rainfall = read_data_file(filename1)

    # after removing invalid datapoints temperature has 4308 datapoints (including header)
    temperature = read_data_file(filename2)

    # rainfall with 4308 datapoints, common with temperature
    # followed by temperature data from 2013-03-01 to 2023-02-01
    rainfall, combined = merge(rainfall, temperature)

    # Extract 'ids' for the header
    header = ['ID'] + combined['ids']

    # Remove 'ids' from data to be exported
    data = {key: value for key, value in combined.items() if key != 'ids'}

    # CSV file name
    csv_file = 'combined_dataset.csv'

    # Create and write to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for id, value in data.items():
            writer.writerow([id] + value)
