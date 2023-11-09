import csv
file = "Child_Care_Centers.csv"
with open(file, "r") as file:
    reader = csv.reader(file)
    file2 = open("Child_Care_Centers_clean.csv", "w")
    for row in reader:
        file2.write(row[3] + "," + row[17] + "," + row[18] + "\n")
    file2.close()