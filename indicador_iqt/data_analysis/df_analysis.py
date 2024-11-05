# src/my_transport_analysis/analysis.py
import pandas as pd

def viagens_por_rota(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['empresa'].count()

def media_passageiros_por_rota(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['qtpsg'].mean()

def valor_arrecadado_por_rota(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['valor_jornada'].sum()

def tempo_medio_operacao(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['duracao'].mean()

def demanda_comparativa(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['qtpsg'].sum().sort_values(ascending=False)

def comparacao_valores(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby('linha')['valor_jornada'].sum().sort_values(ascending=False)

def agrupar_por_dia(df : pd.DataFrame) -> pd.DataFrame: 
    return df.groupby(['datai', 'linha'])[['qtpsg', 'valor_jornada']].sum().reset_index()

def agrupar_duracao_por_mes(df : pd.DataFrame) -> pd.DataFrame: 
    df['mes'] = df['datai'].dt.month
    return df.groupby(['mes', 'linha'])['duracao_minutos'].mean().reset_index()
