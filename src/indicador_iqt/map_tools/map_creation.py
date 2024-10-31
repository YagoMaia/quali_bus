import os
import fiona
import geopandas as gpd
import pandas as pd
import folium
from .layers import add_map_layers, add_line_to_map_sem_grupo
from .styles import get_legend_html

def initialize_map(path):
    # Ativa drivers para libkml
    fiona.drvsupport.supported_drivers['libkml'] = 'rw'
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

    # Define paths
    kmz_file_path = os.path.join(path, "linhas_observatório.kmz")
    kml_file_path = os.path.join(path, "linhas_tratadas.kml")
    shapefile_moc = os.path.join(path, "bairros_sirgas.shp")
    shapefile_ibge = os.path.join(path, "IBGE", "MG_Municipios_2022.shp")

    # Carrega geodataframes
    gdf_list = []
    for layer in fiona.listlayers(kml_file_path):
        if layer != 'Linhas prontas':
            gdf = gpd.read_file(kml_file_path, driver='LIBKML', layer=layer)
            gdf_list.append(gdf)
    
    gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    gdf_filtered = gdf.query("Name != '' and Name != '1' and Name != 'inativo'")
    
    gdf_moc = gpd.read_file(shapefile_moc)
    gdf_ibge = gpd.read_file(shapefile_ibge)
    
    # Define centro do mapa
    map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=12, tiles='CartoDB Voyager')
    
    # Adiciona camadas e geometria
    add_map_layers(m, gdf_moc, gdf, gdf_ibge)
    
    # Adiciona legenda
    legenda_html = get_legend_html(gdf)
    m.get_root().html.add_child(folium.Element(legenda_html))
    
    return m
