import folium

def add_map_layers(m, gdf_moc, gdf, gdf_ibge):
    # Adiciona camada de bairros
    folium.GeoJson(
        gdf_moc,
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 0.7,
            'fillOpacity': 0.5,
        },
        name='Bairros'
    ).add_to(m)

def add_line_to_map(linha, geometry, group, color):
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in zip(geometry.xy[0], geometry.xy[1])],
        color=color,
        weight=2.5,
        opacity=1,
        tooltip=linha
    ).add_to(group)

def add_line_to_map_sem_grupo(linha, geometry, m, color):
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in zip(geometry.xy[0], geometry.xy[1])],
        color=color,
        weight=3,
        opacity=1,
        tooltip=linha
    ).add_to(m)
