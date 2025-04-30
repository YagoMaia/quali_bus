import random

import contextily as ctx
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class VisualizacaoBairros:
	"""
	Classe para visualizar dados de bairros e linhas de transporte público.
	"""

	def _gerar_cores(self, n: int) -> list[str]:
		"""
		Gera uma lista de cores pastéis em formato hexadecimal.

		Parâmetros:
		- n (int): número de cores desejadas

		Retorna:
		- List[str]: lista com 'n' cores em formato hexadecimal
		"""
		cores = []
		for _ in range(n):
			r = random.randint(150, 255)
			g = random.randint(150, 255)
			b = random.randint(150, 255)
			cor_hex = f"#{r:02X}{g:02X}{b:02X}"
			cores.append(cor_hex)
		return cores

	def distribuicao_linhas_por_bairro(self, bairros: gpd.GeoDataFrame, linestrings: gpd.GeoDataFrame) -> None:
		"""
		Distribui linhas de transporte público por bairros e gera um mapa.
		"""
		if bairros.crs != linestrings.crs:
			linestrings = linestrings.to_crs(bairros.crs)

		bairros["num_linestrings"] = 0

		for idx, bairro in bairros.iterrows():
			linestrings_intersect = linestrings[linestrings.intersects(bairro.geometry)]
			bairros.at[idx, "num_linestrings"] = len(linestrings_intersect)

		bairros_web = bairros.to_crs(epsg=3857)

		fig, ax = plt.subplots(1, 1, figsize=(15, 15))

		agrupamento = bairros[["num_linestrings"]].groupby("num_linestrings").count()
		num_classes = len(agrupamento)
		colors = self._gerar_cores(num_classes)
		cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

		bairros_web.plot(
			column="num_linestrings",
			ax=ax,
			cmap=cmap,
			scheme="quantiles",
			k=num_classes,
			legend=False,
			edgecolor="black",  # <-- Adiciona borda preta
			linewidth=0.5,
		)

		ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

		patches = []
		for index, i in enumerate(agrupamento.iterrows()):
			label = f"{i[0]} linestrings"
			patches.append(mpatches.Patch(color=colors[index], label=label))

		ax.legend(handles=patches, loc="lower right", title="Linestrings por Bairro", frameon=True, framealpha=0.9)

		plt.title("Distribuição de Linestrings por Bairro", fontsize=16)
		plt.tight_layout()

		total_linestrings = len(linestrings)
		max_linestrings = bairros["num_linestrings"].max()
		min_linestrings = bairros["num_linestrings"].min()
		mean_linestrings = bairros["num_linestrings"].mean()

		stats_text = (
			f"Total de linestrings: {total_linestrings}\n"
			f"Máximo por bairro: {max_linestrings}\n"
			f"Mínimo por bairro: {min_linestrings}\n"
			f"Média por bairro: {mean_linestrings:.2f}"
		)

		plt.figtext(0.15, 0.05, stats_text, fontsize=12, bbox={"facecolor": "white", "alpha": 0.8})

		plt.show()
