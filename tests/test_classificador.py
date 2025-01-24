import pytest
import pandas as pd
from indicador_iqt.data_analysis.classificator import IndicadoresClassificator

@pytest.fixture
def classificator():
    """Fixture para criar uma instância da classe IndicadoresClassificator."""
    return IndicadoresClassificator()

def test_pontualidade_pontuacao(classificator):
    """Testa o método de pontuação de pontualidade."""
    assert classificator.pontualidade_pontuacao(0.96) == 3
    assert classificator.pontualidade_pontuacao(0.92) == 2
    assert classificator.pontualidade_pontuacao(0.85) == 1
    assert classificator.pontualidade_pontuacao(0.70) == 0

def test_porcentagem_vias_pavimentadas(classificator):
    """Testa o método de pontuação de vias pavimentadas."""
    assert classificator.porcentagem_vias_pavimentadas(1.0) == 3
    assert classificator.porcentagem_vias_pavimentadas(0.97) == 2
    assert classificator.porcentagem_vias_pavimentadas(0.90) == 1
    assert classificator.porcentagem_vias_pavimentadas(0.80) == 0

def test_distancia_pontos(classificator):
    """Testa o método de pontuação de distância entre pontos."""
    assert classificator.distancia_pontos(50) == 3
    assert classificator.distancia_pontos(150) == 2
    assert classificator.distancia_pontos(300) == 1
    assert classificator.distancia_pontos(500) == 0

def test_integracao_municipal(classificator):
    """Testa o método de pontuação de integração municipal."""
    assert classificator.integracao_municipal('Sistema de transporte público totalmente integrado com terminais com o uso de bilhete eletrônico para integração intra e intermodal') == 3
    assert classificator.integracao_municipal('Sistema de transporte público totalmente integrado com terminais com o uso de bilhete eletrônico para integração intramodal somente') == 2
    assert classificator.integracao_municipal('Integração tarifária temporal ocorre em determinados pontos, apenas com transferências intramodais') == 1
    assert classificator.integracao_municipal('Sem integração') == 0

def test_frequencia_atendimento(classificator):
    """Testa o método de pontuação de frequência de atendimento."""
    assert classificator.frequencia_atendimento(5) == 3
    assert classificator.frequencia_atendimento(12) == 2
    assert classificator.frequencia_atendimento(25) == 1
    assert classificator.frequencia_atendimento(35) == 0

def test_cumprimento_itinerarios(classificator):
    """Testa o método de pontuação de cumprimento de itinerários."""
    assert classificator.cumprimento_itinerarios(1.0) == 3
    assert classificator.cumprimento_itinerarios(0.85) == 2
    assert classificator.cumprimento_itinerarios(0.6) == 1
    assert classificator.cumprimento_itinerarios(0.4) == 0

def test_treinamento_capacitacao(classificator):
    """Testa o método de pontuação de treinamento e capacitação."""
    assert classificator.treinamento_capacitacao(1.0) == 3
    assert classificator.treinamento_capacitacao(0.96) == 2
    assert classificator.treinamento_capacitacao(0.92) == 1
    assert classificator.treinamento_capacitacao(0.80) == 0

def test_informacao_internet(classificator):
    """Testa o método de pontuação de informação na internet."""
    assert classificator.informacao_internet('Possuir informações em site e aplicativo atualizados') == 3
    assert classificator.informacao_internet('Possuir informações em site parcialmente atualizado') == 2
    assert classificator.informacao_internet('Possuir informação em site desatualizado') == 1
    assert classificator.informacao_internet('Sem informações') == 0

def test_valor_tarifa(classificator):
    """Testa o método de pontuação de valor de tarifa."""
    assert classificator.valor_tarifa('Não houve aumento da tarifa ') == 3
    assert classificator.valor_tarifa('Aumento inferior ao índice') == 2
    assert classificator.valor_tarifa('Aumento equivalente ao índice') == 1
    assert classificator.valor_tarifa('Aumento superior ao índice') == 0

def test_classificacao_iqt(classificator):
    """Testa o método de classificação do IQT."""
    assert classificator.classificacao_iqt(3.5) == 'Excelente'
    assert classificator.classificacao_iqt(2.5) == 'Bom'
    assert classificator.classificacao_iqt(1.5) == 'Suficiente'
    assert classificator.classificacao_iqt(0.5) == 'Insuficiente'

def test_classificar_linhas(classificator):
    """Testa o método de classificação de linhas."""
    # Criando um DataFrame de exemplo
    dados_exemplo = pd.DataFrame({
        'linha': ['L1'],
        'via_pavimentada': [1.0],
        'distancia': [150],
        'integracao': ['Sistema de transporte público totalmente integrado com terminais com o uso de bilhete eletrônico para integração intra e intermodal'],
        'pontualidade': [0.96],
        'frequencia_atendimento': [5],
        'cumprimento_itinerario': [1.0],
        'proporcao': [1.0],
        'treinamento_motorista': [1.0],
        'informacao_internet': ['Possuir informações em site e aplicativo atualizados'],
        'valor_tarifa': ['Não houve aumento da tarifa ']
    })
    
    classificacao = classificator.classificar_linhas(dados_exemplo)
    
    assert len(classificacao) == 1
    assert all(classificacao.iloc[0, 1:] == [3, 2, 3, 3, 3, 3, 3, 3, 3, 3])
    assert classificacao.columns.tolist() == ['linha', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10']