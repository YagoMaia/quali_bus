# src/my_transport_analysis/data_loader.py
import os
import pandas as pd

def load_data(file_path):
    """Carrega o arquivo CSV e converte colunas para datetime conforme necessário."""
    # filepath = os.path.join(path, filename)
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
