
class Indicadores:
    
    def calcular_pontualidade(self, linha):
        query_atendidas = 20 #Fazer query no banco de dados retornando a quantidade de viagens que atendem os horários estabecidos
        query_totais = 400
        return (query_atendidas/query_totais) * 100
    
    def calcular_rua_pavimentada(self, linha):
        query = 50 #Fazer query no banco de dados retornando a porcentagem da via que é pavimentada
        return query
    
    def calcular_distancia_entre_pontos(self, linha):
        query = {'12':3, '23':1, '34':2} #Fazer query no banco de dados retornando a classificação entre os pontos
        soma = 0
        for classificacao in query.values():
            soma += classificacao
        return soma/len(query)
    
    def calcular_frequencia_atendimento(self, linha):
        query = {'12':3, '23':1, '34':2} #Fazer query no banco de dados retornando a classificação entre os pontos
        soma = 0
        for classificacao in query.values():
            soma += classificacao
        return soma/len(query)
    
    def calcular_capacitacao_motorista(self, linha):
        query_capacitados = 5 #Fazer query no banco de dados a quantidade de motoristas capacitados
        query_totais = 50
        return query_capacitados/query_totais