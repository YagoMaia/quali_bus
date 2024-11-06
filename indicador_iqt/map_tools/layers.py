import folium
from ..utils.colors import color_iqt

# def add_map_layers(m, gdf_moc, gdf, gdf_ibge):
#     # Adiciona camada de bairros
#     folium.GeoJson(
#         gdf_moc,
#         style_function=lambda feature: {
#             'fillColor': 'white',
#             'color': 'black',
#             'weight': 0.7,
#             'fillOpacity': 0.5,
#         },
#         name='Bairros'
#     ).add_to(m)

def add_line_to_map(line, map_routes, group):
    geometry = line['geometry']
    tooltip_line = line['Name']
    color = color_iqt(line['iqt'])
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in zip(geometry.xy[0], geometry.xy[1])],
        color=color,
        weight=2.5,
        opacity=1,
        tooltip=tooltip_line
    ).add_to(group).add_to(map_routes)

def add_line_to_map_sem_grupo(line, map_routes):
    geometry = line['geometry']
    tooltip_line = line['Name']
    color = color_iqt(line['iqt'])
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in zip(geometry.xy[0], geometry.xy[1])],
        color=color,
        weight=3,
        opacity=1,
        tooltip=tooltip_line
    ).add_to(map_routes)