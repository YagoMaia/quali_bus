import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
from indicador_iqt.data_analysis.calculate_indicator import IndicadoresCalculator

@pytest.fixture
def calculator():
    """
    Fixture para criar uma instância da classe IndicadoresCalculator.
    """
    return IndicadoresCalculator()


@pytest.fixture
def lines():
    """
    Fixture para criar um GeoDataFrame de linhas fictícias.
    """
    data = {
        'linha': ["1501"],
        'rota': ["LINESTRING Z (-43.88156644059743 -16.70073765826833 0, -43.88142926517379 -16.69999706663925 0, -43.8820968983508 -16.69988680484133 0, -43.8819873470774 -16.69911084930691 0, -43.88190489230887 -16.69899957081534 0, -43.88129594299133 -16.69831881961529 0, -43.88098272312113 -16.69838557938928 0)"],
        'via_pavimentada': [1],
        'integracao': ["Integração tarifária temporal ocorre em determinados pontos, apenas com transferências intramodais"],
        'treinamento_motorista': [1],
        'informacao_internet': ["Integração tarifária temporal ocorre em determinados pontos, apenas com transferências intramodais"],
        'valor_tarifa' : ["Aumento equivalente ao índice"],
    }
    # return gpd.GeoDataFrame(data, geometry='rota', crs="EPSG:4326")
    return data

@pytest.fixture
def sample_lines(lines):
    """
    Fixture para carregar um DataFrame de linhas.
    """
    return pd.DataFrame(lines)

@pytest.fixture
def sample_frequencia_atendimento():
    """
    
    """
    data = {'empresa': [1,2,3],
    'uds_id': [6220486, 6220487, 6220489],
    'hsstart': ["06:07:57", "06:07:59", "06:10:59"],
    'hsstop': ["06:10:57", "06:15:59", "06:19:59"],
    'datai': ["01/01/2024", "01/01/2024", "01/01/2024"],
    'dataf': ["01/01/2024", "01/01/2024", "01/01/2024"],
    'sentido': [1,0,0],
    'linha': ["4601", "4601", "4601"],
    'carro': ["20103", "20103", "20103"],
    'qtpsg': [1, 10, 41],
    'valor_jornada': [12, 19, 23],
    'nao_sei': [1, 0, 0]}
    
    return pd.DataFrame(data)

@pytest.fixture
def sample_pontualidade():
    """
    Fixture para criar um DataFrame fictício para teste de pontualidade.
    """
    data = {
        'Data': ["01/01/2024", "01/01/2024"],
        'Trajeto': ["1702 - Sentido Mangues (ida)", "1702 - Sentido Mangues (volta)"],
        'Chegada ao ponto': ["05:34:26", "-"],
        'Partida Planejada': ["05:45:00", "05:55:00"],
        'Partida Real': ["00:42:00", "-"],
        'Diff Partida': ["-00:03:00", "00:03:00"],
        'Chegada Planejada': ["05:55:00", "06:05:00"],
        'Chegada Real': ["05:52:00", "-"],
        'Diff Chegada': ["-00:03:00", "00:03:00"],
        'Tempo Viagem': ["00:15:00", "-"],
        'KM Executado': [19, 0]
    }

    return pd.DataFrame(data)

def test_load_dados_linha(calculator, sample_lines):
    """
    Testa o método `load_dados_linha` para carregar linhas.
    """
    calculator.load_dados_linha(sample_lines)
    
    assert calculator.dados_linhas is not None
    
def test_load_frequencia_atendimento(calculator, sample_frequencia_atendimento):
    """
    Testa o método `load_frequencia_atendimento` para carregar frequência de atendimento.
    """
    # calculator.load_dados_linha(sample_lines)
    calculator.load_frequencia_atendimento(sample_frequencia_atendimento)

    assert calculator.frequencia_atendimento is not None

def test_load_pontualidade(calculator, sample_pontualidade):
    """
    Testa o método `load_pontualidade` para carregar pontualidade.
    """
    calculator.load_pontualidade(sample_pontualidade)
    assert calculator.pontualidade is not None
    
def test_load_cumprimento(calculator, sample_pontualidade):
    """
    Testa o método `load_cumprimento` para carregar cumprimento.
    """
    calculator.load_cumprimento(sample_pontualidade)
    assert calculator.cumprimento is not None