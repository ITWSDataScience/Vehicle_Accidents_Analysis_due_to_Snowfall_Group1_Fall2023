import folium
def read_data(file_name):
    """
    Reads the data from the file and returns a list of lists.
    """
    data = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line.split(","))
    return data
def get_coordinates(data):
    """
    Returns a list of coordinates from the data.
    """
    coordinates = []
    for row in range(1, len(data)):
        coordinates.append([float(data[row][0]), float(data[row][1])])
    return coordinates

def show_on_map(coordinates):
    """
    Shows the coordinates on a map.
    """
    map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)
    map.save("map.html")
if __name__ == "__main__":
    file = "Child_Care_Centers.csv"
    data = read_data(file)
    coordinates = get_coordinates(data)
    show_on_map(coordinates)