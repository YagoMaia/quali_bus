import numpy as np
import geopandas as gpd

def euclidean_distance(coordinates_array_pontos_onibus: np.ndarray, coord: np.ndarray) -> np.ndarray:
    """
    Calcula a distância euclidiana entre um ponto de referência e um array de coordenadas.

    Esta função implementa o cálculo da distância euclidiana entre um ponto específico
    e múltiplos pontos de ônibus. O cálculo é vetorizado usando numpy para maior eficiência.

    Args:
        coordinates_array_pontos_onibus (np.ndarray): Array NumPy contendo as coordenadas
            dos pontos de ônibus. Cada linha deve conter [longitude, latitude].
        coord (np.ndarray): Array NumPy contendo as coordenadas do ponto de referência
            no formato [longitude, latitude].

    Returns:
        np.ndarray: Array contendo as distâncias euclidianas entre o ponto de referência
            e cada ponto de ônibus.

    Notes:
        A distância é calculada usando a fórmula euclidiana:
        sqrt((x2-x1)² + (y2-y1)²)
        
        Note que esta é uma distância linear e não considera a curvatura da Terra,
        sendo mais apropriada para análises em áreas geográficas pequenas.
    """
    return np.sqrt(np.sum(np.square(np.array(coordinates_array_pontos_onibus) - np.array(coord)), axis=1))

def calculate_distance(residencias: gpd.GeoDataFrame, pontos_onibus: gpd.GeoDataFrame) -> dict:
    """
    Calcula as menores distâncias entre residências e pontos de ônibus.

    Para cada residência, esta função encontra o ponto de ônibus mais próximo e calcula
    a distância até ele. Os resultados são armazenados em um dicionário contendo os
    índices dos pontos mais próximos e suas respectivas distâncias.

    Args:
        residencias (gpd.GeoDataFrame): GeoDataFrame contendo as localizações das residências.
            Deve conter as colunas 'Longitude' e 'Latitude'.
        pontos_onibus (gpd.GeoDataFrame): GeoDataFrame contendo as localizações dos pontos
            de ônibus. Deve conter as colunas 'Longitude' e 'Latitude'.

    Returns:
        dict: Dicionário contendo duas chaves:
            - 'pontos': Lista com os índices dos pontos de ônibus mais próximos para
                       cada residência.
            - 'distancias': Lista com as menores distâncias entre cada residência e
                           seu ponto de ônibus mais próximo.

    Example:
        >>> residencias_gdf = gpd.GeoDataFrame({
        ...     'Latitude': [-23.550520, -23.551000],
        ...     'Longitude': [-46.633308, -46.634000]
        ... })
        >>> pontos_onibus_gdf = gpd.GeoDataFrame({
        ...     'Latitude': [-23.550000, -23.551500],
        ...     'Longitude': [-46.633000, -46.634500]
        ... })
        >>> resultado = calculate_distance(residencias_gdf, pontos_onibus_gdf)
        >>> print(resultado)
        {'pontos': [0, 1], 'distancias': [0.000584, 0.000678]}
    """
    coordinates_array_residencias = np.array(residencias[['Longitude', 'Latitude']])
    coordinates_array_pontos_onibus = np.array(pontos_onibus[['Longitude', 'Latitude']])
    
    distancias_dados = {'pontos': [], 'distancias': []}
    
    for coord in coordinates_array_residencias:
        distancias = euclidean_distance(coordinates_array_pontos_onibus, coord)
        distancias_dados['pontos'].append(np.argmin(distancias))
        distancias_dados['distancias'].append(np.min(distancias))
    
    return distancias_dados