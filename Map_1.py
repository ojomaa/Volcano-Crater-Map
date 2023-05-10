from turtle import color
from xml.etree.ElementPath import get_parent_map
import folium
import pandas

#Pull Map from Folium
Map1 = folium.Map(location=[36.1, -115.2], zoom_start=5, tiles="Stamen Terrain")
data = pandas.read_csv("Volcanoes.csv")

#collect data from csv
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

omarv = folium.FeatureGroup(name="Volcanoes")
omarp = folium.FeatureGroup(name = "Population")

# separate the elevation points into 3 categories
def colelev(elevation):
    if int(elevation) < 1000:
        return "green"
    elif int(elevation) >=1000 and int(elevation) <2000:
        return "blue"
    else:
        return "red"

#create the circle marker for each location
for lt, ln, elevate, nm in zip(lat, lon, elev, name):
    omarv.add_child(folium.CircleMarker(
        location = [lt, ln],
        popup =  "Volcano Name: " + str(nm) + ", Elevation: " + str(elevate) + " m",
        radius = "10",
        color = colelev(elevate),
        fill_color = colelev(elevate),
        fill_opacity = "0.5",
        name = "Markers",
    ))

#add the population layer on top of the map
omarp.add_child(folium.GeoJson(
     data = open("world.json",encoding = "utf-8-sig").read(),
     style_function= lambda x: {"color": "red" if x['properties']['POP2005'] < 10000000 else "green" if 10000000< x['properties']['POP2005'] <=100000000 else "blue"},
     name = "population overlay",
     ))

#add all info to Map1
Map1.add_child(omarv)
Map1.add_child(omarp)

folium.LayerControl(
    position= 'bottomright'
).add_to(Map1)

#save Map1
Map1.save("Map1.html")