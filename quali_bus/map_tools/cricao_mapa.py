import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from folium.plugins import Fullscreen, GroupedLayerControl, HeatMap
from matplotlib.patches import Patch

from ..data_analysis.classificar_indicadores import ClassificarIndicadores
from ..utils.associador import Associador
from ..utils.cores import gerar_cores_pasteis
from .camadas import adicionar_linha_ao_mapa, adicionar_linha_ao_mapa_sem_grupo


class MapaIQT:
	"""Classe para criar e gerenciar mapas interativos de Índice de Qualidade do Transporte (IQT).

	Esta classe fornece funcionalidades para inicializar um mapa centrado em uma cidade,
	adicionar camadas de rotas e classificá-las de acordo com o IQT (Índice de Qualidade
	do Transporte).

	Attributes:
		gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade.
		mapa (folium.Map): Objeto de mapa Folium inicializado.
		legenda (str): String contendo informações sobre a legenda do mapa.
	"""

	def __init__(self, gdf_city: gpd.GeoDataFrame):
		"""Inicializa um mapa centrado na cidade com uma camada base de bairros.

		Args:
			gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade. Deve conter uma coluna 'geometry' com os polígonos dos bairros.
		"""
		self.gdf_city = gdf_city
		self.mapa = self._inicializar_mapa(self.gdf_city)
		self.mapa_de_calor = self._inicializar_mapa(self.gdf_city)
		self.base_map = self._criar_mapa_base()
		self.linhas = gpd.GeoDataFrame()
		self.legenda = ""

	def _inicializar_mapa(self, gdf_city: gpd.GeoDataFrame) -> folium.Map:
		"""Inicializa um mapa Folium centrado na cidade com uma camada base de bairros.

		Args:
			gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade. Deve conter uma coluna 'geometry' com os polígonos dos bairros.

		Returns:
			folium.Map: Mapa Folium inicializado com:
				- Camada base CartoDB Voyager
				- Zoom inicial de 12
				- Camada de bairros estilizada
				- Centrado no centroide médio da cidade

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa = mapa_iqt._inicializar_mapa(gdf_city)
		"""
		bounds = gdf_city.total_bounds

		center_lat = (bounds[1] + bounds[3]) / 2
		center_lon = (bounds[0] + bounds[2]) / 2

		map_routes = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB Voyager")

		folium.GeoJson(
			gdf_city, style_function=lambda feature: {"fillColor": "white", "color": "black", "weight": 0.7, "fillOpacity": 0.5}, name="Bairros"
		).add_to(map_routes)

		map_routes.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

		Fullscreen().add_to(map_routes)

		return map_routes

	def classificar_rota(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
		"""Adiciona rotas ao mapa base e as classifica por cor de acordo com o IQT.

		Esta função itera sobre cada rota no GeoDataFrame e adiciona cada uma
		individualmente ao mapa, utilizando cores diferentes com base no seu IQT.

		Args:
			gdf_routes (gpd.GeoDataFrame): GeoDataFrame contendo as rotas a serem adicionadas.
				Deve conter as seguintes colunas:
				- geometria_linha: geometria do tipo LineString
				- id_linha: nome da rota para o tooltip
				- iqt: índice de qualidade para determinação da cor

		Returns:
			folium.Map: Mapa Folium com as rotas adicionadas e classificadas por cor
				de acordo com o IQT.

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> gdf_routes = gpd.read_file("caminho/para/rotas.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa_final = mapa_iqt.classificar_rota(gdf_routes)
			>>> mapa_final.save("mapa_rotas.html")
		"""
		for _, line in gdf_routes.iterrows():
			adicionar_linha_ao_mapa_sem_grupo(line, self.mapa)
		return self.mapa

	def classificar_rota_grupo(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map | None:
		"""Adiciona rotas ao mapa base, classificadas por cor e organizadas em grupos de camadas.

		Esta função agrupa as rotas com base em sua classificação IQT, cria grupos de
		camadas no mapa e adiciona controles para ativar/desativar grupos de camadas.

		Args:
			gdf_routes (gpd.GeoDataFrame): GeoDataFrame contendo as rotas a serem adicionadas.
				Deve conter as seguintes colunas:
				- geometria_linha: geometria do tipo LineString
				- id_linha: nome da rota para o tooltip
				- iqt: índice de qualidade para determinação da cor

		Returns:
			folium.Map: Mapa Folium com as rotas adicionadas, classificadas por cor
				e organizadas em grupos de camadas de acordo com o IQT.
			None: Se ocorrer algum erro no processo.

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> gdf_routes = gpd.read_file("caminho/para/rotas.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa_final = mapa_iqt.classificar_rota_grupo(gdf_routes)
			>>> mapa_final.save("mapa_rotas_grupos.html")
		"""
		grupos = {}
		self.linhas = gdf_routes.copy()
		classificador = ClassificarIndicadores()
		listas_grupo = []

		for _, line in gdf_routes.iterrows():
			classificao_iqt = classificador.classificacao_iqt_pontuacao(line.iqt)

			grupo = grupos.get(classificao_iqt, None)
			if grupo is None:
				grupo = folium.FeatureGroup(name=classificao_iqt)
				listas_grupo.append(grupo)
				self.mapa.add_child(grupo)
				grupos[classificao_iqt] = grupo
			adicionar_linha_ao_mapa(line, grupo)

		GroupedLayerControl(groups={"classificacao": listas_grupo}, collapsed=False).add_to(self.mapa)

		return self.mapa

	def gerar_mapa_de_calor(self, associador: Associador):
		"""Função para gerar o mapa de calor."""
		dados = associador.get_geodataframe_com_distancia()
		pontos = [[row["latitude"], row["longitude"], row["distancia"]] for _, row in dados.iterrows()]

		# Adicionar o HeatMap ao mapa
		# gradient = {.1: "green", .2: "blue", .4: "yellow", .6: "orange", 1: "red"}
		HeatMap(pontos, radius=25, blur=15, max_zoom=1).add_to(self.mapa_de_calor)

		return self.mapa_de_calor

	def _criar_mapa_base(self):
		bairros = self.gdf_city.copy()
		bounds = bairros.total_bounds

		center_lat = (bounds[1] + bounds[3]) / 2
		center_lon = (bounds[0] + bounds[2]) / 2

		base_map = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB Voyager")
		quantidade_bairros = bairros.shape[0]
		cores = gerar_cores_pasteis(quantidade_bairros)
		# bairros["cor"] = [cor_pastel() for _ in range(len(bairros))]

		for index, bairro in bairros.iterrows():
			folium.GeoJson(
				bairro.geometry,
				style_function=lambda x, cor=cores[index]: {"fillColor": cor, "color": "black", "weight": 0.5, "fillOpacity": 0.6},
				tooltip=bairro.get("nome", None),
			).add_to(base_map)

		base_map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

		self.grupo_dinamico = folium.FeatureGroup(name="Linha e Buffer")
		base_map.add_child(self.grupo_dinamico)

		return base_map

	def mostrar_abrangencia_linha(self, id_linha: str):
		"""
		Mostra a abrangência de uma linha de ônibus específica no mapa.
		"""
		# Filtrar o GeoDataFrame para obter apenas a linha específica

		# mapa = self.base_map

		# self.grupo_dinamico._children.clear()

		linha = self.linhas[self.linhas["id_linha"] == id_linha]
		if linha.empty:
			print(f"Não foi encontrada nenhuma linha com o ID {id_linha}.")
			return
		# Extrair a geometria da linha
		linha_utm = linha.to_crs(epsg=31983)
		# geometria_linha = linha.geometry.iloc[0]
		buffer_500m = linha_utm.buffer(500)

		gdf_buffer = gpd.GeoDataFrame(geometry=buffer_500m, crs="EPSG:31983").to_crs(epsg=4326)

		# folium.GeoJson(linha.geometry.iloc[0], style_function=lambda x: {"color": "red", "weight": 3}, name="Linha Selecionada").add_to(
		# 	self.grupo_dinamico
		# )
		# folium.GeoJson(
		# 	buffer_500m.geometry.iloc[0], style_function=lambda x: {"color": "blue", "weight": 1, "fillColor": "blue", "fillOpacity": 0.2}
		# ).add_to(self.grupo_dinamico)

		# return self.base_map
		fig, ax = plt.subplots(figsize=(10, 10))
		self.gdf_city.plot(ax=ax, color="lightgray", edgecolor="black")
		gdf_buffer.plot(ax=ax, color="blue", alpha=0.3, label="Buffer")
		linha.plot(ax=ax, color="red", linewidth=2, label="Linha")

		legend_elements = [
			Patch(facecolor="lightgray", edgecolor="black", label="Bairros"),
			Patch(facecolor="blue", edgecolor="blue", alpha=0.3, label="Buffer"),
			Patch(facecolor="red", edgecolor="red", label="Linha"),
		]

		plt.legend(handles=legend_elements)

		plt.title("Linha com Buffer sobre Bairros")
		plt.axis("off")
		plt.savefig("mapa_com_buffer.png", dpi=300)
		plt.show()
