class Config:
	"""
	Classe para gerenciar configurações do projeto.
	"""

	NOMECLATURA = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"]
	PRIORIDADE = [0.1526, 0.1121, 0.0997, 0.2269, 0.0992, 0.0831, 0.0954, 0.0756, 0.0277, 0.0277]
	INDICADOR = [
			"Porcentagem das vias pavimentadas",
			"Distância entre pontos",
			"Integração municipal do sistema de transporte",
			"Pontualidade – cumprir horários",
			"Frequência de atendimento",
			"Cumprimento dos itinerários",
			"Abrangência da rede – atender a cidade",
			"Treinamento e capacitação dos motoristas",
			"Existência Sistema de informação pela internet",
			"Valor da Tarifa ",
		]

config = Config()
