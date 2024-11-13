import numpy as np
import pandas as pd
import geopandas as gpd
from .classificator import IndicadoresClassificator
from ..utils.colors import color_iqt

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
    
    def __init__(self, df_linha : pd.DataFrame):
        """
        Inicializa a classe com os valores predefinidos dos indicadores e suas prioridades.
        """
        self.dados_linhas = self.load_line_data(df_linha)
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

    def cumprimento_itinerario(self):
        colunas_desnecessarias = ["'Veiculo Planejado'", 'Veiculo Real', 'Motorista', 'Vel. Media Km', 'Temp.Ponto', 'Passageiro', 'Status da Viagem', 'Desc. Status da Viagem','Unnamed: 26', 'Unnamed: 25', 'Unnamed: 24', 'Empresa', 'Tabela', 'Viagem Editada']

        df = df.drop(colunas_desnecessarias, axis=1)
        df[['linha', 'sentido']] = df['Trajeto'].str.extract(r'(\d+)\s*-\s*.*\((ida|volta)\)')
        df = df.drop('Trajeto', axis=1)
        df.replace("-", pd.NA, inplace=True)
        # df['com_horario'] = df[['Chegada ao ponto', 'Partida Real', 'Chegada Real']].notna().any(axis=1)
        self.cumprimento = df.groupby(['linha', 'sentido'])['KM Executado'].mean().reset_index()

        # # Renomeia as colunas para maior clareza
        # self.cumprimento.columns = ['sem_horario', 'com_horario']
        self.dados_linhas['distancia_km'] = self.dados_linhas['geometry'].length / 1000
        # # Calcula a proporção de viagens sem horário sobre o total de viagens para cada grupo
        self.cumprimento['cumprimento_itinerario'] = self.cumprimento['KM Executado'] / self.cumprimento['distancia_km']
        # self.cumprimento.drop(['sem_horario', 'com_horario'])
        self.dados_linhas = pd.merge(self.dados_linhas, self.cumprimento, on=['linha', 'sentido'])
        
    
    def load_line_data(self, df_line: pd.DataFrame) -> gpd.GeoDataFrame:
        """
        Carrega os dados de frequência de atendimento a partir de um DataFrame.
        """
        try:
            return gpd.GeoDataFrame(df_line) # Linha, Sentido, Geometria, (Km), Via Pavimentada, Integração, Treinamento, Existência informação internet, Valor Tarifa
        except:
            return None

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

    def pontualidade(self, df: pd.DataFrame) -> int:
        """
        Calcula a pontuação para o indicador de pontualidade.
        """
        colunas_desnecessarias = ["'Veiculo Planejado'", 'Veiculo Real', 'Motorista', 'Vel. Media Km', 'Temp.Ponto', 'Passageiro', 'Status da Viagem', 'Desc. Status da Viagem','Unnamed: 26', 'Unnamed: 25', 'Unnamed: 24', 'Empresa', 'Tabela', 'Viagem Editada']

        self.pontualidade = df

        self.pontualidade = self.pontualidade.drop(colunas_desnecessarias, axis=1)
        self.pontualidade[['linha', 'sentido']] = self.pontualidade['Trajeto'].str.extract(r'(\d+)\s*-\s*.*\((ida|volta)\)')
        self.pontualidade['sentido'] = self.pontualidade['sentido'].replace({'ida': 'IDA', 'volta': 'VOLTA'})
        self.pontualidade = self.pontualidade.drop('Trajeto', axis=1)
        self.pontualidade.replace("-", pd.NA, inplace=True)
        self.pontualidade['com_horario'] = self.pontualidade[['Chegada ao ponto', 'Partida Real', 'Chegada Real']].notna().any(axis=1)
        self.pontualidade = self.pontualidade.groupby(['linha', 'sentido'])['com_horario'].value_counts(normalize=False).unstack(fill_value=0)

        # # Renomeia as colunas para maior clareza
        self.pontualidade.columns = ['sem_horario', 'com_horario']

        # # Calcula a proporção de viagens sem horário sobre o total de viagens para cada grupo
        self.pontualidade['pontualidade'] = self.pontualidade['com_horario'] / (self.pontualidade['sem_horario'] + self.pontualidade['com_horario'])
        self.pontualidade = self.pontualidade.drop(['sem_horario', 'com_horario'], axis=1)
        self.dados_linhas = pd.merge(self.dados_linhas, self.pontualidade, on=['linha', 'sentido'])
        self.dados_linhas = gpd.GeoDataFrame(self.dados_linhas)

    def frequencia_atendimento(self, df: pd.DataFrame) -> pd.DataFrame:
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
        df['hsstart'] = pd.to_datetime(df['hsstart'], format="%H:%M:%S")
        df['hsstop'] = pd.to_datetime(df['hsstop'], format="%H:%M:%S")

        # Calcular a duração como a diferença entre hsstop e hsstart
        df['frequencia_atendimento'] = df['hsstop'] - df['hsstart']
        df['frequencia_atendimento'] = df['frequencia_atendimento'].apply(lambda x: int(x.total_seconds() / 60))

        df['datai'] = pd.to_datetime(df['datai'], format="%d/%m/%Y")
        df['dataf'] = pd.to_datetime(df['dataf'], format="%d/%m/%Y")
        
        df['sentido'] = df['sentido'].replace({0: 'IDA', 1: 'VOLTA'})

        self.frequencia_atendimento = df.groupby(['linha', 'sentido'])['frequencia_atendimento'].mean().reset_index()
        
        self.dados_linhas = pd.merge(self.dados_linhas, self.frequencia_atendimento, on=['linha', 'sentido'])
        self.dados_linhas = gpd.GeoDataFrame(self.dados_linhas)
        
    def classificar_linha(self):
        classificador = IndicadoresClassificator()
        self.classificao_linhas = classificador.classificar_linhas(self.dados_linhas)
    
    
    def processar_iqt(self):
        valores_iqt, cores = [], []
        for index, row in self.classificao_linhas.iterrows():
            # Excluir as colunas 'linha' e 'sentido' e converter para lista
            valores_indicadores = row.iloc[2:].tolist()  # Pegando valores de 'I1', 'I3', 'I4', etc.
            
            # Chamar a função de cálculo do IQT passando os valores da linha
            iqt = self.calcula_iqt(valores_indicadores)
            cor = color_iqt(iqt)
            valores_iqt.append(iqt)
            cores.append(cor)
        self.dados_linhas['iqt'] = valores_iqt
        self.dados_linhas['cor'] = cores