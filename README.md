# Indicador IQT

Biblioteca Python para análise e classificação de indicadores de qualidade do transporte urbano, com foco em transporte coletivo. O `indicador_iqt` fornece ferramentas para processar e validar dados de transporte, aplicando classificações específicas de acordo com métricas de qualidade. A biblioteca permite trabalhar com dados de rotas, frequência, pontualidade e outros dados relevantes ao transporte público.

<!-- ## Índice

- [Instalação](#instalação)
- [Funcionalidades](#funcionalidades)
  - [Carregar Arquivos Geoespaciais](#carregar-arquivos-geoespaciais)
  - [Filtrar e Manipular Dados Geoespaciais](#filtrar-e-manipular-dados-geoespaciais)
  - [Gerar Mapas Interativos](#gerar-mapas-interativos)
  - [Adicionar Linhas com Cores Personalizadas](#adicionar-linhas-com-cores-personalizadas)
- [Exemplo de Uso](#exemplo-de-uso)
- [Referências](#referências)

--- -->

## Instalação

Para instalar a biblioteca `indicador_iqt`, basta clonar o repositório e instalar as dependências:

```bash
git clone https://github.com/YagoMaia/indicador_iqt
cd indicador_iqt
pip install -r requirements.txt
```

Certifique-se de que as bibliotecas necessárias como `folium`, `geopandas`, `geopandas`, `pandas`, e `fiona` estejam corretamente instaladas.

## Funcionalidades

A biblioteca `indicador_iqt` foi projetada para auxiliar na análise e visualização de dados de transporte urbano. As principais funcionalidades incluem:

### Classificação de Indicadores de Qualidade do Transporte (IQT):

- Classificação de rotas e dados de transporte com base em métricas de qualidade predefinidas.
- Uso da classe `IndicadoresClassificator` para categorizar rotas e dados de transporte.

### Validação de DataFrames:

- Funções de validação para verificar se os DataFrames possuem as colunas necessárias antes do processamento.
- Funções específicas para validar `gdf_city`, `df_dados_linhas`, `df_frequencia`, e `df_pontualidade`, levantando erros se houver colunas ausentes.

### Mapeamento de Rotas com Folium:

- Criação de mapas interativos utilizando a biblioteca Folium.
- Funções para adicionar rotas, grupos e outros dados geoespaciais ao mapa.

### Manipulação de Dados GTFS:

- Manipulação e análise de dados GTFS (General Transit Feed Specification) utilizando o modulo `gtfs_functions`.

## Pré-requisitos

Para utilizar esta biblioteca, é necessário ter os seguintes pacotes instalados:

- `Pandas` para manipulação de dados
- `Folium` para criação de mapas interativos
- `Geopandas` para manipulação de dados geoespaciais

## Contribuição

Sinta-se à vontade para contribuir para a biblioteca indicador_iqt. Para contribuir, faça um fork do repositório, crie uma branch para suas alterações e envie um pull request. Agradecemos suas sugestões e melhorias.

- Faça o fork do projeto
- Crie uma branch com suas funcionalidades (`git checkout -b feature/NovaFuncionalidade`)
- Commit suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
- Envie para o branch (`git push origin feature/NovaFuncionalidade`)
- Crie um novo Pull Request