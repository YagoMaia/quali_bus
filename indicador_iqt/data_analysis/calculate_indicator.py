import numpy as np

class Indicadores:
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
            'nomeclatura': ['I4', 'I1', 'I2', 'I3', 'I5', 'I7', 'I6', 'I8', 'I9', 'I10'],
            'prioridade': [0.2269, 0.1526, 0.1121, 0.0997, 0.0992, 0.0954, 0.0831, 0.0756, 0.0277, 0.0277],
            'indicador': ['Pontualidade – cumprir horários', 'Porcentagem das vias pavimentadas', 
                         'Distância entre pontos', 'Integração municipal do sistema de transporte', 
                         'Frequência de atendimento', 'Abrangência da rede – atender a cidade', 
                         'Cumprimento dos itinerários', 'Treinamento e capacitação dos motoristas', 
                         'Existência Sistema de informação pela internet', 'Valor da Tarifa '],
        }

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
        valores_indicadores = linha[1:]
        soma_ponderada = sum(p * w for p, w in zip(valores_indicadores, self.indicadores_prioridades['prioridade']))
        desvio_padrao_pessoas = np.std(self.indicadores_prioridades['prioridade'])
        iqt = soma_ponderada / (desvio_padrao_pessoas * np.len(self.indicadores_prioridades['prioridade']))
        return iqt

    def pontualidade_pontuacao(self, pontualidade: float) -> int:
        """
        Calcula a pontuação para o indicador de pontualidade.

        Parameters
        ----------
        pontualidade : float
            Valor entre 0 e 1 representando a taxa de pontualidade.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: pontualidade >= 0.95
            - 2: 0.90 <= pontualidade < 0.95
            - 1: 0.80 <= pontualidade < 0.90
            - 0: pontualidade < 0.80
        """
        if 0.95 <= pontualidade:
            return 3
        elif 0.90 <= pontualidade < 0.95:
            return 2
        elif 0.80 <= pontualidade < 0.90:
            return 1
        else:
            return 0

    def porcentagem_vias_pavimentadas(self, porcentagem: float) -> int:
        """
        Calcula a pontuação para o indicador de vias pavimentadas.

        Parameters
        ----------
        porcentagem : float
            Valor entre 0 e 1 representando a porcentagem de vias pavimentadas.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: porcentagem >= 1
            - 2: 0.95 <= porcentagem < 0.99
            - 1: 0.85 <= porcentagem < 0.95
            - 0: porcentagem < 0.85
        """
        if 1 <= porcentagem:
            return 3
        elif 0.95 <= porcentagem < 0.99:
            return 2
        elif 0.85 <= porcentagem < 0.95:
            return 1
        else:
            return 0

    def distancia_pontos(self, distancia: float) -> int:
        """
        Calcula a pontuação para o indicador de distância entre pontos.

        Parameters
        ----------
        distancia : float
            Distância em metros entre os pontos de parada.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: distancia >= 250
            - 2: 250 <= distancia < 400
            - 1: 400 <= distancia < 500
            - 0: distancia >= 500 ou distancia < 250
        """
        if 250 <= distancia:
            return 3
        elif 250 <= distancia < 400:
            return 2
        elif 400 <= distancia < 500:
            return 1
        else:
            return 0

    def integracao_municipal(self, integracao: float) -> int:
        """
        Calcula a pontuação para o indicador de integração municipal.

        Parameters
        ----------
        integracao : float
            Valor entre 0 e 1 representando o nível de integração municipal.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: integracao >= 1
            - 2: 0.95 <= integracao < 1
            - 1: 0.85 <= integracao < 0.95
            - 0: integracao < 0.85
        """
        if 1 <= integracao:
            return 3
        elif 0.95 <= integracao < 1:
            return 2
        elif 0.85 <= integracao < 0.95:
            return 1
        else:
            return 0

    def frequencia_atendimento(self, frequencia: float) -> int:
        """
        Calcula a pontuação para o indicador de frequência de atendimento.

        Parameters
        ----------
        frequencia : float
            Tempo em minutos entre atendimentos.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: frequencia <= 10
            - 2: 10 < frequencia <= 15
            - 1: 15 < frequencia <= 30
            - 0: frequencia > 30
        """
        if frequencia <= 10:
            return 3
        elif frequencia <= 15:
            return 2
        elif 15 < frequencia <= 30:
            return 1
        else:
            return 0

    def cumprimento_etinerarios(self, etinerario: float) -> int:
        """
        Calcula a pontuação para o indicador de cumprimento de itinerários.

        Parameters
        ----------
        etinerario : float
            Valor entre 0 e 1 representando a taxa de cumprimento dos itinerários.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: etinerario >= 1
            - 2: 0.8 <= etinerario <= 0.9
            - 1: 0.5 <= etinerario <= 0.7
            - 0: etinerario < 0.5
        """
        if 1 <= etinerario:
            return 3
        elif 0.9 <= etinerario <= 0.8:
            return 2
        elif 0.7 <= etinerario <= 0.5:
            return 1
        else:
            return 0

    def treinamento_capacitacao(self, treinamento: float) -> int:
        """
        Calcula a pontuação para o indicador de treinamento e capacitação.

        Parameters
        ----------
        treinamento : float
            Valor entre 0 e 1 representando o nível de treinamento dos motoristas.

        Returns
        -------
        int
            Pontuação atribuída:
            - 3: treinamento >= 1
            - 2: 0.95 <= treinamento <= 0.98
            - 1: 0.90 <= treinamento <= 0.95
            - 0: treinamento < 0.90
        """
        if 1 <= treinamento:
            return 3
        elif 0.98 <= treinamento <= 0.95:
            return 2
        elif 0.90 <= treinamento <= 0.95:
            return 1
        else:
            return 0

    def classificacao_iqt(self, iqt: float) -> str:
        """
        Classifica o IQT em categorias qualitativas.

        Parameters
        ----------
        iqt : float
            Valor do Índice de Qualidade do Transporte (IQT).

        Returns
        -------
        str
            Classificação do IQT:
            - 'Excelente': iqt >= 3.0
            - 'Bom': 2.0 <= iqt < 3.0
            - 'Suficiente': 1.0 <= iqt < 2.0
            - 'Insuficiente': iqt < 1.0
        """
        if iqt >= 3.0:
            return 'Excelente'
        elif 2 <= iqt < 3.0:
            return 'Bom'
        elif 1.0 <= iqt < 2:
            return 'Suficiente'
        else:
            return 'Insuficiente'