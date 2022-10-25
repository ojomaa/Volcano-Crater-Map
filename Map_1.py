from turtle import color
from xml.etree.ElementPath import get_parent_map
import folium
import pandas

#Map1 pulled a Map from folium then location pinned it down to a specific lat and long. 
#the tiles is just the map design that you want to use from folium
Map1 = folium.Map(location=[36.1, -115.2], zoom_start=5, tiles="Stamen Terrain")
data = pandas.read_csv("Volcanoes.csv")

#these were created to single out the data from a specific column in the csv to be used in folium. 
#So lat pulled all the latitudes in the csv and stored it. Same with the rest of them
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

omarv = folium.FeatureGroup(name="Volcanoes")
omarp = folium.FeatureGroup(name = "Population")

# a function was created to have a dynamic marker that takes in the elevation and based off the number, it returned a specific color
# the function was stored to later be used in the CircleMarker
def colelev(elevation):
    if int(elevation) < 1000:
        return "green"
    elif int(elevation) >=1000 and int(elevation) <2000:
        return "blue"
    else:
        return "red"

#when using multiple groups or whatever theyre called, use the zip(). If you dont you can only use one group
#created a folium Circle marker then added parameters to pinpoint each location, give it a popup with a name and elevation
#then i colored the marker based on its elevation. in color = and fill_color = i called the function i created earlier.
#see how that works huh lol
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

#tried to define it as a function then call it in folium.GeoJson but couldnt figure it out so i just kept this script in case i do manage to figure it out.
#for now i just used lamba x to create the function inside folium.GeoJson and it worked so far
def colpop(population):
    if int(population) < 10000000:
        return "green"
    elif int(population) >=10000000 and int(population) <100000000:
        return "blue"
    else:
        return "red"

#this was for adding the population layer on top of the map
omarp.add_child(folium.GeoJson(
     data = open("world.json",encoding = "utf-8-sig").read(),
     style_function= lambda x: {"color": "red" if x['properties']['POP2005'] < 10000000 else "green" if 10000000< x['properties']['POP2005'] <=100000000 else "blue"},
     name = "population overlay",
     ))

#add this at the end so it can be added to the map
Map1.add_child(omarv)
Map1.add_child(omarp)

folium.LayerControl(
    position= 'bottomright'
).add_to(Map1)

#save the map to the html link so you can open it and see the results
Map1.save("Map1.html")

#one thing i didnt understand is that before adding the featuregroup to the volcano code and the population code i was only able to toggle the
#population code in the layer control but not the volcano code. I then added the featuregroup and it fixed hte problem but i dont understand why