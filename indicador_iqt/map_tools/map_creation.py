import geopandas as gpd
import folium
from folium.plugins import GroupedLayerControl, Fullscreen, MeasureControl
from .layers import add_line_to_map_no_group, add_line_to_map
from ..data_analysis.classificator import IndicadoresClassificator

class MapaIQT:
    def __init__(self, gdf_city: gpd.GeoDataFrame):
        """
        Inicializa um mapa centrado na cidade com uma camada base de bairros.
        """
        self.gdf_city = gdf_city
        self.map = self._initialize_map(self.gdf_city)
        self.legenda = ""

    def _initialize_map(self, gdf_city: gpd.GeoDataFrame) -> folium.Map:
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
        
        bounds = gdf_city.total_bounds  # [minx, miny, maxx, maxy]
    
    # Calcula o centro do mapa
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        
        # map_center = [gdf_city.geometry.centroid.y.mean(), gdf_city.geometry.centroid.x.mean()]
        map_routes = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB Voyager')
    
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
        
        
        map_routes.fit_bounds([
            [bounds[1], bounds[0]],  # [lat_min, lon_min]
            [bounds[3], bounds[2]]   # [lat_max, lon_max]
        ])
    
        # Adiciona controle de zoom
        Fullscreen().add_to(map_routes)
        
        # Adiciona uma barra de escala
        map_routes.add_child(MeasureControl(
            position='bottomleft',
            primary_length_unit='meters',
            secondary_length_unit='kilometers'
        ))

        return map_routes

    def classification_routes(self, map_routes: folium.Map, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
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

    def classification_routes_group(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map | None:
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
        grupos = {}
        classificador = IndicadoresClassificator()
        listas_grupo = []
        for index, line in gdf_routes.iterrows():
            classificao_iqt = classificador.classificacao_iqt(line.iqt)
            
            grupo = grupos.get(classificao_iqt, None)
            if grupo is None:
                grupo = folium.FeatureGroup(name=classificao_iqt)
                listas_grupo.append(grupo)
                self.map.add_child(grupo)
                grupos[classificao_iqt] = grupo
            add_line_to_map(line, grupo)
            
        GroupedLayerControl(
            groups={'classificacao': listas_grupo},
            collapsed=False,
        ).add_to(self.map)
        
        self._add_legend()

    def _get_style(self, iqt: float, is_highlighted: bool = False) -> dict:
        """
        Retorna o estilo da linha baseado no IQT e se está destacada.
        """
        # Cores base por classificação
        colors = {
            'Excelente': '#2ca02c',  # Verde
            'Bom': '#1f77b4',        # Azul
            'Regular': '#ff7f0e',     # Laranja
            'Ruim': '#d62728'        # Vermelho
        }
        
        # Definir cor base baseado no IQT
        if iqt >= 0.8:
            base_color = colors['Excelente']
        elif iqt >= 0.6:
            base_color = colors['Bom']
        elif iqt >= 0.4:
            base_color = colors['Regular']
        else:
            base_color = colors['Ruim']
        
        # Estilo padrão
        style = {
            'color': base_color,
            'weight': 2,
            'opacity': 0.8
        }
        
        # Se destacada, ajusta o estilo
        if is_highlighted:
            style.update({
                'weight': 4,
                'opacity': 1.0
            })
        
        return style

    def _add_legend(self):
        """
        Adiciona uma legenda ao mapa mostrando as cores por classificação.
        """
        legend_html = '''
        <div style="position: fixed; 
                bottom: 50px; 
                left: 50px; 
                z-index: 1000; 
                background-color: white;
                padding: 10px; 
                border-radius: 5px; 
                border: 2px solid grey; 
                font-size: 14px;">
        <h4 style="margin-top: 0;">Classificação IQT</h4>
        <div style="margin: 5px 0;"><i style="background: #2ca02c; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Excelente (≥0.8)</div>
        <div style="margin: 5px 0;"><i style="background: #1f77b4; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Bom (0.6-0.79)</div>
        <div style="margin: 5px 0;"><i style="background: #ff7f0e; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Regular (0.4-0.59)</div>
        <div style="margin: 5px 0;"><i style="background: #d62728; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Ruim (<0.4)</div>
        </div>
        '''
        self.map.get_root().html.add_child(folium.Element(legend_html))