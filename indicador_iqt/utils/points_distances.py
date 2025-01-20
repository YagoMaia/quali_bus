import numpy as np
import geopandas as gpd
# import numpy as np
# from copy import deepcopy
from shapely.geometry import LineString, Point

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
    residencias = residencias.to_crs(epsg=3857)
    pontos_onibus = pontos_onibus.to_crs(epsg=3857)
    
    coordinates_array_residencias = np.array(residencias[['Longitude', 'Latitude']])
    coordinates_array_pontos_onibus = np.array(pontos_onibus[['Longitude', 'Latitude']])
    
    distancias_dados = {'pontos': [], 'distancias': []}
    
    for coord in coordinates_array_residencias:
        distancias = euclidean_distance(coordinates_array_pontos_onibus, coord)
        distancias_dados['pontos'].append(np.argmin(distancias))
        distancias_dados['distancias'].append(np.min(distancias))
    
    return distancias_dados

#TODO: Decompor as coordenadas da linha (LineString)
#TODO: Distanca euclidiana desses pontos para todos os pontos de onibus
#TODO: Pegar o ponto mais proximo de cada ponto da linha

class Vinculador_Pontos:
    def __init__(self, coord_geral: np.array, coord_linha: np.array, coord_residencia : np.array, linha_ponto, nomes):
        """
        Classe para vincular pontos de ônibus a pontos mais próximos em uma linha.

        Args:
            coord_geral (np.array): Coordenadas gerais dos pontos de ônibus.
            coord_linha (np.array): Coordenadas das linhas (LineString).
            linha_ponto (dict): Dicionário para armazenar os pontos vinculados a cada linha.
            nomes (list): Lista de nomes das linhas.
        """
        self.pontos_onibus = coord_geral
        self.coordenadas_linhas = coord_linha
        self.coordenadas_residencias = coord_residencia
        self.lp = linha_ponto
        self.nomes = nomes

    def euclidean_distance(self, ponto):
        """
        Calcula a distância euclidiana entre um ponto e todos os pontos de ônibus.

        Args:
            ponto_linha (np.array): Coordenadas do ponto para ser calculado a distância.

        Returns:
            np.array: Distâncias euclidianas para todos os pontos de ônibus.
        """
        return np.sqrt(
            np.sum(
                np.square(ponto - self.pontos_onibus), axis=1
            )
        )

    def decompose_linestring(self, linestring):
        """
        Decompõe um LineString em coordenadas individuais.

        Args:
            linestring (LineString): Objeto LineString.

        Returns:
            np.array: Coordenadas dos pontos da linha.
        """
        return np.array(linestring.coords)

    def link_coords(self):
        """
        Vincula os pontos de ônibus aos pontos mais próximos em cada linha.

        Returns:
            dict: Dicionário contendo os pontos vinculados e suas linhas.
        """
        dados = {
            'linha': [],
            'ponto': []
        }
        for pontos_linha, nome in zip(self.coordenadas_linhas, self.nomes):
            # Decompor LineString em coordenadas
            if isinstance(pontos_linha, LineString):
                pontos_linha = self.decompose_linestring(pontos_linha)

            for ponto_linha in pontos_linha:
                # Calcular distância euclidiana
                distances = self.euclidean_distance(ponto_linha)
                # Encontrar o ponto mais próximo
                idx_min = np.argmin(distances)
                x, y = self.pontos_onibus[idx_min]

                # Vincular ponto à linha se a distância for aceitável
                if np.min(distances) <= 0.002:
                    self.lp[nome].add(idx_min)
                dados['ponto'].append((x, y))
                dados['linha'].append(nome)
        return dados