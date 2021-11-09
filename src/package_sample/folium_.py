import folium

map_ = folium.Map(location=[52.8067, -2.1207], zoom_start=14)
map_.save('osm.html')
