import geopandas as gpd
import pandas as pd


def validar_gdf_city(df: pd.DataFrame) -> bool:
	"""Valida um DataFrame contendo informações sobre áreas urbanas.

	Args:
		df (pd.DataFrame): DataFrame contendo os dados a serem validados.

	Returns:
		bool: True se o DataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no DataFrame.
	"""
	required_columns = [
		"OBJECTID",
		"Shape_Leng",
		"Shape_Area",
		"Nome_Polo",
		"FID_1",
		"Shape_Ar_1",
		"Nome_Pol_1",
		"RendaDomc_",
		"Domicilios",
		"Moradores",
		"RendaPerca",
		"geometry",
	]
	missing_columns = [col for col in required_columns if col not in df.columns]
	if missing_columns:
		raise ValueError(f"gdf_city está faltando colunas: {missing_columns}")
	return True


def validar_df_dados_linhas(df: pd.DataFrame) -> bool:
	"""Valida um DataFrame contendo informações sobre linhas de transporte.

	Args:
		df (pd.DataFrame): DataFrame contendo os dados das linhas.

	Returns:
		bool: True se o DataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no DataFrame.
	"""
	required_columns = ["linha", "geometry", "via_pavimentada", "integracao", "treinamento_motorista", "informacao_internet", "valor_tarifa"]
	missing_columns = [col for col in required_columns if col not in df.columns]
	if missing_columns:
		raise ValueError(f"df_dados_linhas está faltando colunas: {missing_columns}")
	return True


def validar_df_frequencia(df: pd.DataFrame) -> bool:
	"""Valida um DataFrame contendo informações sobre frequência de viagens.

	Args:
		df (pd.DataFrame): DataFrame contendo os dados de frequência.

	Returns:
		bool: True se o DataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no DataFrame.
	"""
	required_columns = ["hsstart", "hsstop", "data", "sentido", "linha", "qtpsg", "valor_jornada"]
	missing_columns = [col for col in required_columns if col not in df.columns]
	if missing_columns:
		raise ValueError(f"df_frequencia está faltando colunas: {missing_columns}")
	return True


def validar_df_pontualidade(df: pd.DataFrame) -> bool:
	"""Valida um DataFrame contendo informações sobre pontualidade de transporte.

	Args:
		df (pd.DataFrame): DataFrame contendo os dados de pontualidade.

	Returns:
		bool: True se o DataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no DataFrame.
	"""
	required_columns = ["Data", "Trajeto", "Chegada ao ponto", "Partida Real", "Chegada Real"]
	missing_columns = [col for col in required_columns if col not in df.columns]
	if missing_columns:
		raise ValueError(f"df_pontualidade está faltando colunas: {missing_columns}")
	return True


def validar_df_cumprimento(df: pd.DataFrame) -> bool:
	"""Valida um DataFrame contendo informações sobre cumprimento de rotas.

	Args:
		df (pd.DataFrame): DataFrame contendo os dados de cumprimento de rotas.

	Returns:
		bool: True se o DataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no DataFrame.
	"""
	required_columns = ["Data", "Trajeto", "KM Executado"]
	missing_columns = [col for col in required_columns if col not in df.columns]
	if missing_columns:
		raise ValueError(f"df_cumprimento está faltando colunas: {missing_columns}")
	return True


def validar_residencias(gdf: gpd.GeoDataFrame) -> bool:
	"""Valida um GeoDataFrame contendo informações sobre residências.

	Args:
		gdf (gpd.GeoDataFrame): GeoDataFrame contendo os dados das residências.

	Returns:
		bool: True se o GeoDataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no GeoDataFrame.
	"""
	required_columns = ["ID", "Longitude", "Latitude"]
	missing_columns = [col for col in required_columns if col not in gdf.columns]
	if missing_columns:
		raise ValueError(f"gdf_residências está faltando colunas: {missing_columns}")
	return True


def validar_pontos_onibus(gdf: gpd.GeoDataFrame) -> bool:
	"""Valida um GeoDataFrame contendo informações sobre pontos de ônibus.

	Args:
		gdf (gpd.GeoDataFrame): GeoDataFrame contendo os dados dos pontos de ônibus.

	Returns:
		bool: True se o GeoDataFrame contiver todas as colunas esperadas.

	Raises:
		ValueError: Se alguma coluna estiver faltando no GeoDataFrame.
	"""
	required_columns = ["ID", "Longitude", "Latitude"]
	missing_columns = [col for col in required_columns if col not in gdf.columns]
	if missing_columns:
		raise ValueError(f"gdf_pontos_onibus está faltando colunas: {missing_columns}")
	return True
