import folium
import pandas

# Website for converting .shp files because folium does not recognize .shp files : https://ogre.adc4gis.com/

df = pandas.read_csv('Volcanoes-USA.txt')
#average variable of latitude and longitude values from file in order to center us within the area of our future marker
average_lat = df['LAT'].mean()
average_lon = df['LON'].mean()
map = folium.Map(location=[average_lat,average_lon], zoom_start=4, tiles='Stamen Terrain')

#function for different coloring of particular categories
def color(elev):
    min_elev = int(min(df['ELEV']))
    max_elev = int(max(df['ELEV']))
    step_eval = int((max_elev - min_elev) / 4)
    if elev in range(min_elev, (min_elev + step_eval)):
        color = 'green'
    elif elev in range(min_elev+step_eval,(min_elev+step_eval*2)):
        color = 'blue'
    else:
        color = 'red'
    return color
#Create feature group object
fg = folium.FeatureGroup(name='Volcano Locations')
# Extracts information from the df (which is a dataframe read from a file) and adds it to the FeaturegGroup(fg)
for lat,long,name,elev in zip(df['LAT'],df['LON'],df['NAME'],df['ELEV']):
    # Add another child into map object - marker
    fg.add_child(folium.Marker(location=[lat, long],
                                popup=name,
                                icon=folium.Icon(color(elev),icon_color='#fff')))
#Add fg to the map
map.add_child(fg)

#Add another child into map object - polygons !!DO NOT INCLUDE IN LOOP !!
map.add_child(folium.GeoJson(data=open('Shapefile/World_population.json', encoding="utf-8"),name='World Population',
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<=10000000 else 'orange'\
if 10000000<x['properties']['POP2005']<20000000\
                         else 'red'}))

#Add another child into map object
map.add_child(folium.LayerControl())
#Create HTML file
map.save('Test.html')