import os
import fiona
import geopandas as gpd
import pandas as pd

def load_routes(file_path):
    fiona.drvsupport.supported_drivers['libkml'] = 'rw'
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
    gdf_list = []
    for layer in fiona.listlayers(file_path):
        gdf = gpd.read_file(file_path, driver='LIBKML', layer=layer)
        gdf_list.append(gdf)
    gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    gdf = gdf.query("Description != ''")
    gdf[['linha', 'sentido']] = gdf['Name'].str.split(' - ', expand=True)
    del gdf['Name']
    return gdf

def load_neighborhoods(file_path):
    gdf_city = gpd.read_file(file_path)
    gdf_city = gdf_city.to_crs(epsg=3857)
    return gdf_city