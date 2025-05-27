def main():
import pandas as pd
import random


def dataframe(ticker, trimestre):

    return pd.DataFrame({
        'Receita': [random.randint(1000, 5000)],
        'Lucro': [random.randint(-500, 1000)],
        'PL': [random.randint(1000, 4000)],
        'Capital Investido': [random.randint(2000, 5000)],
        'WACC': [0.1]
    })

def indices_basicos(df):
    return df.iloc[0].to_dict()

def indices_liquidez(basicos): return {'Liquidez Corrente': random.uniform(1, 2)}
def indices_giro_tesouraria(basicos): return {'Giro': random.uniform(1, 4)}
def indices_endividamento(basicos): return {'Endividamento': random.uniform(0.3, 0.8)}
def indices_emprestimos(basicos): return {'Dívida Bruta': random.randint(100, 500)}
def indices_juros(basicos): return {'Custo da Dívida': random.uniform(0.05, 0.15)}
def indice_nao_realizavel(basicos): return {'Não Realizável': random.randint(100, 300)}
def indices_rentabilidade(basicos): return {'ROE': random.uniform(0, 15), 'EVA': random.randint(-200, 400)}
def indices_ciclos(b1, b2): return {'Ciclo Operacional': random.randint(30, 90)}

def print_dict(title, ticker, trimestre, dicionario):
    print(f"{title} — {ticker} — {trimestre}")
    for k, v in dicionario.items():
        print(f"  {k}: {v}")
    print()


def gravar_indicadores(data_dict):
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df.index.name = "Empresa"
    return df

def escolher_melhor_empresa(df, criterio="ROE"):
    if criterio not in df.columns:
        raise ValueError(f"Critério '{criterio}' não encontrado no DataFrame.")
    melhor = df[criterio].idxmax()
    return melhor, df.loc[melhor]

def main():
    list_ticker = ["BRFS3", "MRFG3", "BEEF3", "BAUH4", "MNPR3"]
    list_tri = ["20234T", "20244T"]

    indicadores = {}

    for ticker in list_ticker:
        list_basicos = []
        for trimestre in list_tri:
            df = dataframe(ticker, trimestre)
            basicos = indices_basicos(df)
            liquidas = indices_liquidez(basicos)
            giro = indices_giro_tesouraria(basicos)
            endividamento = indices_endividamento(basicos)
            emprestimo = indices_emprestimos(basicos)
            juros = indices_juros(basicos)
            nao_realizavel = indice_nao_realizavel(basicos)
            rentabilidade = indices_rentabilidade(basicos)

            list_basicos.append(basicos)

            print_dict("Índices Básicos",        ticker, trimestre, basicos)
            print_dict("Índices de Liquidez",     ticker, trimestre, liquidas)
            print_dict("Giro de Tesouraria",      ticker, trimestre, giro)
            print_dict("Índice de Endividamento", ticker, trimestre, endividamento)
            print_dict("Empréstimos",             ticker, trimestre, emprestimo)
            print_dict("Índice de Juros",         ticker, trimestre, juros)
            print_dict("Não Realizável",          ticker, trimestre, nao_realizavel)
            print_dict("Rentabilidade",           ticker, trimestre, rentabilidade)

        ciclos = indices_ciclos(list_basicos[0], list_basicos[1])
        print(f"Ciclos — {ticker} — {list_tri[0]} & {list_tri[1]}")
        for key, value in ciclos.items():
            print(f"  {key}: {value}")
        print()

       
        indicadores[ticker] = {
            "ROE": rentabilidade["ROE"],
            "EVA": rentabilidade["EVA"]
        }

    df_indicadores = gravar_indicadores(indicadores)
    print("\nIndicadores Consolidados:")
    print(df_indicadores)

    for criterio in ["ROE", "EVA"]:
        melhor_empresa, dados = escolher_melhor_empresa(df_indicadores, criterio)
        print(f"\nMelhor empresa com base em {criterio}: {melhor_empresa}")
        print(dados)

if __name__ == "__main__":
    main()
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


tickers = ["BRFS3.SA", "MRFG3.SA", "BEEF3.SA", "BAUH4.SA", "MNPR3.SA"]


anos = [1, 5, 10]

def calcular_retorno_acumulado(ticker, anos):
    hoje = datetime.today()
    resultados = {}

    for ano in anos:
        data_inicio = hoje - timedelta(days=ano * 365)
        dados = yf.download(ticker, start=data_inicio, end=hoje)

        if dados.empty:
            resultados[f"{ano}y"] = None
            continue

        preco_inicio = dados['Adj Close'].iloc[0]
        preco_fim = dados['Adj Close'].iloc[-1]
        retorno = (preco_fim / preco_inicio - 1) * 100
        resultados[f"{ano}y"] = round(retorno, 2)

    return resultados


resultados = {}
for ticker in tickers:
    resultados[ticker] = calcular_retorno_acumulado(ticker, anos)

df_backtest = pd.DataFrame(resultados).T
df_backtest.columns = [f"Retorno {col}" for col in df_backtest.columns]
df_backtest.index.name = "Empresa"

print("\nRetornos Acumulados (%):")
print(df_backtest)

import matplotlib.pyplot as plt

def plotar_backtest(df):
    for col in df.columns:
        plt.figure()
        df[col].plot(kind='bar')
        plt.title(f"Retorno Acumulado - {col}")
        plt.ylabel("Retorno (%)")
        plt.xlabel("Empresa")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

plotar_backtest(df_backtest)
