import os
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega e processa um arquivo CSV contendo dados de horários e datas, realizando as conversões
    necessárias para os tipos datetime.

    Parameters
    ----------
    file_path : str
        Caminho completo para o arquivo CSV a ser carregado.

    Returns
    -------
    pd.DataFrame
        DataFrame processado contendo as seguintes colunas:
        - hsstart: datetime - Horário de início
        - hsstop: datetime - Horário de término
        - duracao: timedelta - Duração calculada (hsstop - hsstart)
        - datai: datetime - Data inicial
        - dataf: datetime - Data final
        - duracao_minutos: int - Duração em minutos

    Notes
    -----
    O arquivo CSV deve conter as colunas: 'hsstart', 'hsstop', 'datai', 'dataf'
    com os seguintes formatos:
    - hsstart, hsstop: "%H:%M:%S"
    - datai, dataf: "%d/%m/%Y"
    """
    df = pd.read_csv(file_path, delimiter=',')
   
    # Conversões de datetime
    df['hsstart'] = pd.to_datetime(df['hsstart'], format="%H:%M:%S")
    df['hsstop'] = pd.to_datetime(df['hsstop'], format="%H:%M:%S")
    df['duracao'] = df['hsstop'] - df['hsstart']
    df['datai'] = pd.to_datetime(df['datai'], format="%d/%m/%Y")
    df['dataf'] = pd.to_datetime(df['dataf'], format="%d/%m/%Y")
    df['duracao_minutos'] = df['duracao'].dt.total_seconds() // 60
    df['duracao_minutos'] = df['duracao_minutos'].astype(int)
   
    return df

def load_integrations(file_path: str) -> pd.Series:
    """
    Carrega um arquivo CSV de integrações e retorna uma série contendo as linhas de origem únicas.

    Parameters
    ----------
    file_path : str
        Caminho completo para o arquivo CSV de integrações.

    Returns
    -------
    pd.Series
        Série contendo valores únicos da coluna 'LINHA ORIGEM'.

    Notes
    -----
    O arquivo CSV deve conter uma coluna chamada 'LINHA ORIGEM'.
    A função remove duplicatas antes de retornar os valores.
    """
    df_integrations = pd.read_csv(file_path, delimiter=',')
    df_integrations = df_integrations.drop_duplicates(subset=['LINHA ORIGEM'])
    df_integrations = df_integrations['LINHA ORIGEM']
    return df_integrations