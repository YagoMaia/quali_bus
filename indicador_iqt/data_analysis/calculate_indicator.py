import numpy as np
import pandas as pd
import geopandas as gpd
# from shapely.geometry import LineString
from shapely.wkt import loads
from .classificator import IndicadoresClassificator
from ..utils.colors import color_iqt
from ..utils import models

class IndicadoresCalculator:
    """
    Classe para cálculo e avaliação de indicadores de qualidade do transporte público.
    
    Esta classe contém métodos para calcular o Índice de Qualidade do Transporte (IQT)
    e avaliar diferentes aspectos do serviço de transporte público, como pontualidade,
    infraestrutura e atendimento.

    Attributes
    ----------
    indicadores_prioridades : dict
        Dicionário contendo as informações dos indicadores com as seguintes chaves:
        - 'nomeclatura': Lista de códigos dos indicadores (I1, I2, etc.)
        - 'prioridade': Lista de pesos para cada indicador
        - 'indicador': Lista com descrições dos indicadores
    """
    
    def __init__(self):
        """
        Inicializa a classe com os valores predefinidos dos indicadores e suas prioridades.
        """
        self.indicadores_prioridades = {
            'nomeclatura': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10'],
            'prioridade': [0.1526, 0.1121, 0.0997, 0.2269, 0.0992, 0.0831, 0.0954, 0.0756, 0.0277, 0.0277],
            'indicador': [
                'Porcentagem das vias pavimentadas', #* OK
                'Distância entre pontos', #? Pegar média dos pontos?
                'Integração municipal do sistema de transporte', #* OK
                'Pontualidade – cumprir horários', #* OK
                'Frequência de atendimento', #* OK
                'Cumprimento dos itinerários', #* OK
                'Abrangência da rede – atender a cidade', #! Nem ideia
                'Treinamento e capacitação dos motoristas', #* OK
                'Existência Sistema de informação pela internet', #* OK
                'Valor da Tarifa ' #* OK
            ]
        }
        self.cumprimento = None
        self.pontualidade = None
        self.dados_linhas = None
        self.dados_completos = None
        self.residencias = None
        self.pontos_onibus = None
    
    def load_dados_linha(self, df_line: pd.DataFrame):
        """
        Carrega os dados de frequência de atendimento a partir de um DataFrame.
        """
        try:
            if models.validate_df_dados_linhas(df_line):
                df_copy = df_line.copy()
                
                self.dados_linhas = gpd.GeoDataFrame(df_copy)
                self.dados_linhas['geometry'] = self.dados_linhas['geometry'].apply(loads)
                self.dados_linhas.groupby(['linha'])
        except Exception as error:
            print("Erro ao carregar dados de linha: ", error)
            self.dados_linhas = None
            
    def load_cumprimento(self, df_cumprimento: pd.DataFrame):
        """
        Carrega os dados de cumprimento do itinerário a partir de um DataFrame.
        """
        try:
            if models.validate_df_pontualidade(df_cumprimento):
                self.cumprimento = self.cumprimento_itinerario(df_cumprimento)
        except Exception as error:
            print("Erro ao carregar dados de cumprimento: ", error)
            self.cumprimento = None
            
    def load_frequencia_atendimento(self, df_frequencia: pd.DataFrame):
        """
        Carrega os dados de frequência de atendimento a partir de um DataFrame.
        """
        try:
            if models.validate_df_frequencia(df_frequencia):
                self.frequencia = self.frequencia_atendimento(df_frequencia)
        except:
            self.frequencia = None         
    def load_pontualidade(self, df_pontualidade: pd.DataFrame):
        """
        Carrega os dados de pontualidade a partir de um DataFrame.
        """
        try:
            if models.validate_df_pontualidade(df_pontualidade):
                self.pontualidade = self.calcular_pontualidade(df_pontualidade)
        except:
            self.pontualidade = None
    
    def load_residencias(self, df_residencias: gpd.GeoDataFrame):
        """
        Carrega os dados de residências a partir de um GeoDataFrame.
        """
        try:
            if models.validate_residencias(df_residencias):
                self.residencias = self.tratar_residencias(df_residencias)
        except:
            self.residencias = None
        
    def load_pontos_onibus(self, df_pontos_onibus: gpd.GeoDataFrame):
        """
        Carrega os dados de pontos de ônibus a partir de um GeoDataFrame.
        """
        try:
            if models.validate_pontos_onibus(df_pontos_onibus):
                self.pontos_onibus = self.tratar_pontos_onibus(df_pontos_onibus)
        except:
            self.pontos_onibus = None
    
    def cumprimento_itinerario(self, df_cumprimento: pd.DataFrame):
        
        df_temp = df_cumprimento.copy()
        
        df_temp[['linha', 'sentido']] = df_temp['Trajeto'].str.extract(r'(\d+)\s*-\s*.*\((ida|volta)\)')
        df_temp.replace("-", pd.NA, inplace=True)
        df_temp.dropna(subset=['KM Executado'], inplace=True)
        df_temp['KM Executado'] = pd.to_numeric(df_temp['KM Executado'], errors='coerce')
        df_temp = df_temp.groupby(['linha'])['KM Executado'].mean().reset_index()

        return df_temp

    def calcular_pontualidade(self, df_pontualidade: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula a pontuação para o indicador de pontualidade.
        """
        try:
            df_temp = df_pontualidade.copy()
            
            df_temp[['linha', 'sentido']] = df_temp['Trajeto'].str.extract(r'(\d+)\s*-\s*.*\((ida|volta)\)')
            df_temp['sentido'] = df_temp['sentido'].replace({'ida': 'IDA', 'volta': 'VOLTA'})
            df_temp = df_temp.drop('Trajeto', axis=1)
            df_temp.replace("-", pd.NA, inplace=True)
            df_temp['com_horario'] = df_temp[['Chegada ao ponto', 'Partida Real', 'Chegada Real']].notna().any(axis=1)
            df_temp = df_temp.groupby('linha')['com_horario'].value_counts(normalize=False).unstack(fill_value=0)

            # # Renomeia as colunas para maior clareza
            df_temp.columns = ['sem_horario', 'com_horario']

            # # Calcula a proporção de viagens sem horário sobre o total de viagens para cada grupo
            df_temp['pontualidade'] = df_temp['com_horario'] / (df_temp['sem_horario'] + df_temp['com_horario'])
            df_temp = df_temp.drop(['sem_horario', 'com_horario'], axis=1)
            
            return df_temp
        except Exception as error:
            print("Erro ao calcular pontualidade: ", error)
            return None

    def frequencia_atendimento(self, df_frequencia: pd.DataFrame) -> pd.DataFrame:
        """Calcula o tempo médio de operação por rota (linha).

        Args:
            df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'duracao' para a duração das viagens.

        Returns:
            pd.DataFrame: DataFrame com o tempo médio de operação por rota.

        Example:
            >>> tempo_medio_operacao(df)
            linha sentido duracao
            101    IDA    45.0
            102    VOLTA  37.5
            103    IDA    50.2
        """
        df_temp = df_frequencia.copy()
        
        df_temp['hsstart'] = pd.to_datetime(df_temp['hsstart'], format="%H:%M:%S")
        df_temp['hsstop'] = pd.to_datetime(df_temp['hsstop'], format="%H:%M:%S")

        # Calcular a duração como a diferença entre hsstop e hsstart
        df_temp['frequencia_atendimento'] = df_temp['hsstop'] - df_temp['hsstart']
        df_temp['frequencia_atendimento'] = df_temp['frequencia_atendimento'].apply(lambda x: int(x.total_seconds() / 60))

        df_temp['datai'] = pd.to_datetime(df_temp['datai'], format="%d/%m/%Y")
        df_temp['dataf'] = pd.to_datetime(df_temp['dataf'], format="%d/%m/%Y")
        
        # df_temp['sentido'] = df_temp['sentido'].replace({0: 'IDA', 1: 'VOLTA'})

        df_temp = df_temp.groupby(['linha'])['frequencia_atendimento'].mean().reset_index()
        
        return df_temp
    
    def merge_dados(self):
        try:
            self.dados_linhas['distancia_km'] = self.dados_linhas['geometry'].length * 100
            self.cumprimento['cumprimento_itinerario'] = self.cumprimento['KM Executado'] / self.dados_linhas['distancia_km']

            self.dados_completos = pd.merge(self.dados_linhas, self.cumprimento, on=['linha'])
            self.dados_completos = pd.merge(self.dados_completos, self.frequencia, on=['linha'])
            self.dados_completos = pd.merge(self.dados_completos, self.pontualidade, on=['linha'])
            
            self.dados_completos = gpd.GeoDataFrame(self.dados_completos)
            
        except Exception as e:
            print(f"Erro ao mesclar os dados: {e}")
    
    def tratar_pontos_onibus(self, df_pontos_onibus: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Trata os dados de pontos de ônibus para calcular a distância entre eles.
        """
        try:
            df_temp = df_pontos_onibus.copy()
            return df_temp.to_crs(3857)
            # Converte latitude e longitude para geometria
        except Exception as error:
            print("Erro ao tratar pontos de ônibus: ", error)
            return None
        
    def tratar_residencias(self, df_residencias: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Trata os dados de residências para calcular a distância entre elas.
        """
        try:
            df_temp = df_residencias.copy()
            return df_temp.to_crs(3857)
            # Converte latitude e longitude para geometria
        except Exception as error:
            print("Erro ao tratar residências: ", error)
            return None
    
    
    
    def classificar_linha(self):
        classificador = IndicadoresClassificator()
        self.merge_dados()
        self.classificao_linhas = classificador.classificar_linhas(self.dados_completos)
    
    def calcula_iqt(self, linha: list) -> float:
        """
        Calcula o Índice de Qualidade do Transporte (IQT) para uma linha específica.

        Parameters
        ----------
        linha : list
            Lista contendo os valores dos indicadores para uma linha específica.
            O primeiro elemento é ignorado, e os demais devem corresponder aos
            indicadores na ordem definida em indicadores_prioridades.

        Returns
        -------
        float
            Valor do IQT calculado.

        Notes
        -----
        O cálculo é feito através da soma ponderada dos indicadores dividida pelo
        produto do desvio padrão das prioridades e quantidade de indicadores.
        """
        try:
            # Multiplicando indicadores pelo peso de cada um
            # valores_indicadores = linha
            prioridades = self.indicadores_prioridades['prioridade']
            soma_ponderada = np.dot(linha, prioridades)

            # Calculando o desvio padrão das prioridades
            desvio_padrao_prioridades = np.std(prioridades)
            
            # Calculando o IQT
            iqt = soma_ponderada / (desvio_padrao_prioridades * len(prioridades))
            return iqt
        
        except Exception as e:
            print(f"Erro ao calcular IQT: {e}")
            return 0.0
    
    def processar_iqt(self):
        valores_iqt, cores = [], []
        for index, row in self.classificao_linhas.iterrows():
            # Excluir as colunas 'linha' e 'sentido' e converter para lista
            valores_indicadores = row.iloc[1:].tolist()  # Pegando valores de 'I1', 'I3', 'I4', etc.
            
            # Chamar a função de cálculo do IQT passando os valores da linha
            iqt = self.calcula_iqt(valores_indicadores)
            cor = color_iqt(iqt)
            valores_iqt.append(iqt)
            cores.append(cor)
        self.dados_completos['iqt'] = valores_iqt
        self.dados_completos['cor'] = cores