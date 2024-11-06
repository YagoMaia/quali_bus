import numpy as np

class Indicadores:
    def __init__(self):
        self.indicadores_prioridades = {
        'nomeclatura': ['I4', 'I1', 'I2', 'I3', 'I5', 'I7', 'I6', 'I8', 'I9', 'I10'],
        'prioridade': [0.2269, 0.1526, 0.1121, 0.0997, 0.0992, 0.0954, 0.0831, 0.0756, 0.0277, 0.0277],
        'indicador': ['Pontualidade – cumprir horários', 'Porcentagem das vias pavimentadas', 'Distância entre pontos', 'Integração municipal do sistema de transporte', 'Frequência de atendimento', 'Abrangência da rede – atender a cidade', 'Cumprimento dos itinerários', 'Treinamento e capacitação dos motoristas', 'Existência Sistema de informação pela internet', 'Valor da Tarifa '],
        }
        
    def calcula_iqt(self, linha):
        valores_indicadores = linha[1:]
        soma_ponderada = sum(p * w for p, w in zip(valores_indicadores, self.indicadores_prioridades['prioridade']))
        desvio_padrao_pessoas = np.std(self.indicadores_prioridades['prioridade'])
        iqt = soma_ponderada / (desvio_padrao_pessoas * np.len(self.indicadores_prioridades['prioridade']))
        return iqt
    
    def pontualidade_pontuacao(self, pontualidade):
        if 0.95 <= pontualidade:
            return 3
        elif 0.90 <= pontualidade < 0.95:
            return 2
        elif 0.80 <= pontualidade < 0.90:
            return 1
        else:
            return 0
    
    def porcentagem_vias_pavimentadas(self, porcentagem):
        if 1 <= porcentagem:
            return 3
        elif 0.95 <= porcentagem < 0.99:
            return 2
        elif 0.85 <= porcentagem < 0.95:
            return 1
        else:
            return 0
        
    def distancia_pontos(self, distancia):
        if 250 <= distancia:
            return 3
        elif 250 <= distancia < 400:
            return 2
        elif 400 <= distancia < 500:
            return 1
        else:
            return 0
    
    def integracao_municipal(self, integracao):
        if 1 <= integracao:
            return 3
        elif 0.95 <= integracao < 1:
            return 2
        elif 0.85 <= integracao < 0.95:
            return 1
        else:
            return 0
    def frequencia_atendimento(self, frequencia):
        if frequencia <= 10:
            return 3
        elif frequencia <= 15:
            return 2
        elif 15 < frequencia <= 30:
            return 1
        else:
            return 0
    
    def cumprimento_etinerarios(self, etinerario):
        if 1 <= etinerario:
            return 3
        elif 0.9 <= etinerario <= 0.8:
            return 2
        elif 0.7 <= etinerario <= 0.5:
            return 1
        else:
            return 0
        
    def treinamento_capacitacao(self, treinamento):
        if 1 <= treinamento:
            return 3
        elif 0.98 <= treinamento <= 0.95:
            return 2
        elif 0.90 <= treinamento <= 0.95:
            return 1
        else:
            return 0
        
    
    def classificacao_iqt(self, iqt):
        if iqt >= 3.0:
            return 'Excelente'
        elif 2 <= iqt < 3.0:
            return 'Bom'
        elif 1.0 <= iqt < 2:
            return 'Suficiente'
        else:
            return 'Insuficiente'