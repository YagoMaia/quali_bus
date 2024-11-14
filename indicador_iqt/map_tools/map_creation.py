import geopandas as gpd
import folium
from folium.plugins import GroupedLayerControl
from .layers import add_line_to_map_no_group, group_sentido, add_line_to_map
from ..data_analysis.classificator import IndicadoresClassificator

def create_map() -> None:
    """
    Função placeholder para criação de mapa.
    
    Esta função atualmente não implementa nenhuma funcionalidade (pass).
    Pode ser expandida no futuro para incluir configurações iniciais
    ou parâmetros específicos para a criação do mapa.
    """
    pass

def initialize_map(gdf_city: gpd.GeoDataFrame) -> folium.Map:
    """
    Inicializa um mapa Folium centrado na cidade com uma camada base de bairros.
    
    Parameters
    ----------
    gdf_city : gpd.GeoDataFrame
        GeoDataFrame contendo as geometrias dos bairros da cidade.
        Deve conter uma coluna 'geometry' com os polígonos dos bairros.
        
    Returns
    -------
    folium.Map
        Mapa Folium inicializado com:
        - Camada base CartoDB Voyager
        - Zoom inicial de 12
        - Camada de bairros estilizada
        - Centrado no centroide médio da cidade
        
    Notes
    -----
    O estilo dos bairros é definido com:
    - Preenchimento branco (fillColor: white)
    - Borda preta fina (color: black, weight: 0.7)
    - Transparência de 50% (fillOpacity: 0.5)
    
    Example
    -------
    >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
    >>> mapa = initialize_map(gdf_city)
    >>> mapa.save('mapa_cidade.html')
    """
    # Define centro do mapa
    map_center = [gdf_city.geometry.centroid.y.mean(), gdf_city.geometry.centroid.x.mean()]
    map_routes = folium.Map(location=map_center, zoom_start=12, tiles='CartoDB Voyager')
   
    folium.GeoJson(
        gdf_city,
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',    
            'weight': 0.7,
            'fillOpacity': 0.5,
        },
        name='Bairros'
    ).add_to(map_routes)
   
    return map_routes

def classification_routes(map_routes: folium.Map, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
    """
    Adiciona rotas classificadas ao mapa base.
    
    Parameters
    ----------
    map_routes : folium.Map
        Mapa Folium base onde as rotas serão adicionadas.
        Geralmente é o mapa retornado por initialize_map().
    
    gdf_routes : gpd.GeoDataFrame
        GeoDataFrame contendo as rotas a serem adicionadas.
        Deve conter as seguintes colunas:
        - geometry: geometria do tipo LineString
        - linha: nome da rota para o tooltip
        - iqt: índice de qualidade para determinação da cor
        
    Returns
    -------
    folium.Map
        Mapa Folium com as rotas adicionadas e classificadas por cor
        de acordo com o IQT.
        
    Notes
    -----
    - Cada rota é adicionada individualmente ao mapa usando add_line_to_map_no_group
    - A classificação por cores é determinada pelo valor do IQT de cada rota
    - As cores são definidas pela função color_iqt (importada indiretamente
      através de add_line_to_map_no_group)
    
    Example
    -------
    >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
    >>> gdf_routes = gpd.read_file('caminho/para/rotas.geojson')
    >>> mapa = initialize_map(gdf_city)
    >>> mapa_final = classification_routes(mapa, gdf_routes)
    >>> mapa_final.save('mapa_rotas.html')
    """
    for index, line in gdf_routes.iterrows():
        # line_dict = line.to_dict()  # Converte a linha para um dicionário
        add_line_to_map_no_group(line, map_routes)
    return map_routes

def classification_routes_group(map_routes: folium.Map, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
    """
    Adiciona rotas classificadas ao mapa base.
    
    Parameters
    ----------
    map_routes : folium.Map
        Mapa Folium base onde as rotas serão adicionadas.
        Geralmente é o mapa retornado por initialize_map().
    
    gdf_routes : gpd.GeoDataFrame
        GeoDataFrame contendo as rotas a serem adicionadas.
        Deve conter as seguintes colunas:
        - geometry: geometria do tipo LineString
        - linha: nome da rota para o tooltip
        - iqt: índice de qualidade para determinação da cor
        
    Returns
    -------
    folium.Map
        Mapa Folium com as rotas adicionadas e classificadas por cor
        de acordo com o IQT.
        
    Notes
    -----
    - Cada rota é adicionada individualmente ao mapa usando add_line_to_map_no_group
    - A classificação por cores é determinada pelo valor do IQT de cada rota
    - As cores são definidas pela função color_iqt (importada indiretamente
      através de add_line_to_map_no_group)
    
    Example
    -------
    >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
    >>> gdf_routes = gpd.read_file('caminho/para/rotas.geojson')
    >>> mapa = initialize_map(gdf_city)
    >>> mapa_final = classification_routes(mapa, gdf_routes)
    >>> mapa_final.save('mapa_rotas.html')
    """
    sentido_groups = {'IDA': {}, 'VOLTA': {} }
    classificador = IndicadoresClassificator()
    listas_grupo = []
    for index, line in gdf_routes.iterrows():
        # line_dict = line.to_dict()  # Converte a linha para um dicionário
        classificao_iqt = classificador.classificacao_iqt(line.iqt)
        grupo = sentido_groups.get(line.sentido, None).get(classificao_iqt, None)
        if grupo is None:
            grupo = folium.FeatureGroup(name=f'{line.sentido} - {classificao_iqt}')
            listas_grupo.append(grupo)
            map_routes.add_child(grupo)
            sentido_groups[line.sentido][classificao_iqt] = grupo
        add_line_to_map(line, map_routes, grupo)
        
    GroupedLayerControl(
        groups={'classificacao': listas_grupo},
        collapsed=False,
    ).add_to(map_routes)
    
    return map_routes