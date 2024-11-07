import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_boxplot_passageiros_por_rota(df: pd.DataFrame):
    """Plota um boxplot da distribuição de passageiros por rota.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para as rotas e 'qtpsg' para a quantidade de passageiros.

    Returns:
        None: A função exibe o gráfico, mas não retorna nenhum valor.

    Example:
        >>> plot_boxplot_passageiros_por_rota(df)
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='qtpsg', y='linha', data=df, hue='linha')
    plt.title('Distribuição de Passageiros por Rota')
    plt.xlabel('Número de Passageiros')
    plt.ylabel('Rotas')
    plt.xticks(rotation=45)
    plt.show()


def plot_boxplot_valores_arrecadados_por_rota(df: pd.DataFrame):
    """Plota um boxplot da distribuição dos valores arrecadados por rota.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar as rotas e 'valor_jornada' para os valores arrecadados.

    Returns:
        None: A função exibe o gráfico, mas não retorna nenhum valor.

    Example:
        >>> plot_boxplot_valores_arrecadados_por_rota(df)
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='valor_jornada', y='linha', data=df, hue='linha')
    plt.title('Distribuição dos Valores Arrecadados por Rota')
    plt.ylabel('Rota')
    plt.xlabel('Valor Arrecadado')
    plt.xticks(rotation=45)
    plt.show()


def plot_duracao_medio_por_mes(df: pd.DataFrame):
    """Plota um boxplot da distribuição do tempo de viagem por rota.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar as rotas e 'duracao_minutos' para a duração das viagens em minutos.

    Returns:
        None: A função exibe o gráfico, mas não retorna nenhum valor.

    Example:
        >>> plot_duracao_medio_por_mes(df)
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='duracao_minutos', y='linha', data=df, hue='linha')
    plt.title('Distribuição de Tempo de Viagem')
    plt.xlabel('Tempo de Duração')
    plt.ylabel('Rotas')
    plt.show()
