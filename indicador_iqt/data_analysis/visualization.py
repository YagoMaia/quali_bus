# src/my_transport_analysis/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_boxplot_passageiros_por_rota(df :pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='qtpsg', y='linha', data=df, hue='linha')
    plt.title('Distribuição de Passageiros por Rota')
    plt.xlabel('Número de Passageiros')
    plt.ylabel('Rotas')
    plt.xticks(rotation=45)
    plt.show()

def plot_boxplot_valores_arrecadados_por_rota(df :pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='valor_jornada', y='linha', data=df, hue='linha')
    plt.title('Distribuição dos Valores Arrecadados por Rota')
    plt.ylabel('Rota')
    plt.xlabel('Valor Arrecadado')
    plt.xticks(rotation=45)
    plt.show()

def plot_duracao_medio_por_mes(df :pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='duracao_minutos', y='linha', data=df, hue='linha')
    plt.title('Distribuição de Tempo de Viagem')
    plt.xlabel('Tempo de Duração')
    plt.ylabel('Rotas')
    plt.show()