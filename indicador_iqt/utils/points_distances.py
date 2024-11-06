import numpy as np
import geopandas as gpd

def euclidean_distance(coordinates_array_pontos_onibus, coord):
    return np.sqrt(np.sum(np.square(np.array(coordinates_array_pontos_onibus) - np.array(coord)), axis=1))

def calculate_distance(residencias : gpd.GeoDataFrame, pontos_onibus : gpd.GeoDataFrame):
    coordinates_array_residencias = np.array(residencias[['Longitude', 'Latitude']]) 
    coordinates_array_pontos_onibus = np.array(pontos_onibus[['Longitude', 'Latitude']])
    
    distancias_dados = {'pontos': [], 'distancias': []}
    
    for coord in coordinates_array_residencias:
        distancias = euclidean_distance(coordinates_array_pontos_onibus, coord)
        distancias_dados['pontos'].append(np.argmin(distancias))
        distancias_dados['distancias'].append(np.min(distancias))
        
    return distancias_dados