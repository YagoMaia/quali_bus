import os
import pandas as pd

# Caminho do diretório onde os arquivos estão localizados
path = os.path.abspath(os.path.dirname(__name__))
path_arquivos = os.path.join(path, 'moc_bus')

# Lista para armazenar os dataframes
dataframes = []

colunas = ['empresa', 'uds_id', 'hsstart', 'hsstop', 'datai', 'dataf', 'sentido', 'linha', 'carro', 'qtpsg', 'valor_jornada', 'nao_sei']
tipos_dados = {
    'EMPRESA': 'int32',          # INT
    'UDS_ID': 'int64',           # BIGINT
    'HSSTART': 'object',         # TIME (usado 'object' pois pandas não tem tipo TIME nativo)
    'HSSTOP': 'object',          # TIME (usado 'object' pois pandas não tem tipo TIME nativo)
    'DATAI': 'datetime64[ns]',   # DATE
    'DATAF': 'datetime64[ns]',   # DATE
    'SENTIDO': 'int16',          # SMALLINT
    'LINHA': 'int32',            # INT
    'CARRO': 'int64',            # BIGINT
    'QTPGS': 'int32',            # INT
    'VALOR_JORNADA': 'float64',  # DECIMAL(10, 2)
    'NAO_SEI': 'float64'         # DECIMAL(10, 2)
}

# Navega por todas as pastas e subpastas
for pasta, subpastas, arquivos in os.walk(path_arquivos):
    for arquivo in arquivos:
        # Verifica se o arquivo é um CSV
        if arquivo.endswith(".csv"):
            # Caminho completo do arquivo CSV
            caminho_arquivo = os.path.join(pasta, arquivo)
            # print(caminho_arquivo)
            # Lê o arquivo CSV e adiciona na lista de dataframes
            df = pd.read_csv(caminho_arquivo, names=colunas, dtype=tipos_dados, delimiter=',', skiprows=1, on_bad_lines='skip')
            df.fillna(0, inplace=True)

            dataframes.append(df)

# Concatena todos os dataframes
print("Exportando csv")
df_combinado = pd.concat(dataframes, ignore_index=True)
df_combinado['uds_id'] = df_combinado['uds_id'].astype(int)
df_combinado['sentido'] = df_combinado['sentido'].astype(int)
df_combinado['carro'] = df_combinado['carro'].astype(int)
df_combinado['qtpsg'] = df_combinado['qtpsg'].astype(int)
df_combinado['linha'] = df_combinado['linha'].astype(str)
# df_combinado['motorista_treinado'] = 1


# Exporta para um novo arquivo CSV
df_combinado.to_csv(os.path.join(path, 'arquivo_combinado2.csv'), index=False)