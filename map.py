import folium
import pandas

df = pandas.read_csv("Volcanoes.txt")

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""



def color_produce(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


for i in range(len(df)):
    lat = df.loc[i, 'LAT']
    lon = df.loc[i, 'LON']
    elev = df.loc[i, 'ELEV']
    name = df.loc[i, 'NAME']
    iframe = folium.IFrame(html=html % (name, name, elev), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lat, lon], radius=6,
                                     popup=folium.Popup(iframe),
                                     fill_color=color_produce(elev),
                                     color='grey',
                                     fill=True,
                                     fill_opacity=0.7))

# for i in range(len(df)):
#     lat = df.loc[i, 'LAT']
#     lon = df.loc[i, 'LON']
#     elev = df.loc[i, 'ELEV']
#     fg.add_child(folium.Marker(location=[lat, lon],
#                                popup=folium.Popup(str(elev)+'m',parse_html=True),
#                                icon=folium.Icon(color='green')))

fgp = folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
                            style_function=lambda x:{'fillColor':'green'
                            if x['properties']['POP2005']<10000000 else 'yellow'
                            if 10000000<=x['properties']['POP2005']<20000000 else 'red'}))



map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
