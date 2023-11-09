import folium
import csv
def read_data(file_name):
    """
    Reads the data from the file and returns a list of lists.
    """
    coordinates = []
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        K = 0
        for row in reader:
            if(K == 0):
                K = K + 1
                continue
            else:
                Lat = float(row[17])
                Lon = float(row[18])
                if(Lat > 24.3 and Lat < 31.0 and Lon > -87.6 and Lon < -80.0):
                    coordinates.append((Lat, Lon))
    return coordinates

def show_on_map(coordinates):
    """
    Shows the coordinates on a map.
    """
    florida_bounding_box = [[24.396308, -87.634896], [31.000888, -79.974306]]
    florida_center = [(florida_bounding_box[0][0] + florida_bounding_box[1][0]) / 2, 
                  (florida_bounding_box[0][1] + florida_bounding_box[1][1]) / 2]
    map = folium.Map(location=florida_center, zoom_start=7)
    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)
    map.save("map.html")
if __name__ == "__main__":
    file = "Child_Care_Centers.csv"
    coordinates = read_data(file)
    show_on_map(coordinates)