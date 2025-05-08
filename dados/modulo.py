import pandas as pd
import requests


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
HEADERS = {"Authorization": f"JWT {TOKEN}"}
https://laboratoriodefinancas.com/api/v1/balanco

def dataframe(ticker, trimestre):
    params = {'ticker': ticker, 'ano_tri': trimestre}
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=HEADERS)
    dados = response.json()['dados'][0]['balanco']
    return pd.DataFrame(dados)

def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[0]

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[1]

def indices_basicos(df):
    return {
        'ativo_circulante': valor_contabil(df, '^1.0', 'ativo cir'),
        'passivo_circulante': valor_contabil(df, '^2.0', 'passivo cir'),
        'estoques': valor_contabil(df, '^1.0', 'estoque'),
        'caixa_equivalentes': valor_contabil(df, '^1.0', 'caixa'),
        'aplicacoes': valor_contabil(df, '^1.0', 'aplica'),
        'patrimonio_liquido': valor_contabil(df, '^2.*', 'patrim'),
        'ativo_total': valor_contabil(df, '^1.*', 'ativo total'),
        'passivo_nao_circulante': valor_contabil(df, '^2.0', 'passivo n.o cir')
    }

def indices_liquidez(b):
    return {
        'Liquidez Corrente': round(b['ativo_circulante'] / b['passivo_circulante'], 2),
        'Liquidez Seca': round((b['ativo_circulante'] - b['estoques']) / b['passivo_circulante'], 2),
        'Liquidez Imediata': round((b['caixa_equivalentes'] + b['aplicacoes']) / b['passivo_circulante'], 2),
        'Liquidez Geral': round((b['ativo_circulante'] + b['ativo_total'] - b['ativo_circulante']) / (b['passivo_circulante'] + b['passivo_nao_circulante']), 2)
    }

def indices_giro_tesouraria(b):
    return {
        'Giro de Caixa': round(b['caixa_equivalentes'] / b['ativo_circulante'], 2)
    }

def indices_endividamento(b):
    total_passivo = b['passivo_circulante'] + b['passivo_nao_circulante']
    return {
        'Endividamento Geral': round(total_passivo / (total_passivo + b['patrimonio_liquido']), 2),
        'Solvência': round(b['ativo_total'] / total_passivo, 2),
        'Composição do Endividamento': round(b['passivo_circulante'] / total_passivo, 2)
    }

def indices_emprestimos(df):
    cp = valor_contabil(df, '^2.01', 'empr') + valor_contabil(df, '^2.01', 'deb')
    lp = valor_contabil(df, '^2.02', 'empr') + valor_contabil(df, '^2.02', 'deb')
    return {'Emprestimos CP': cp, 'Emprestimos LP': lp}

def indices_juros(df):
    juros = valor_contabil(df, '^3.', 'juros') * -1
    return {'Despesas com Juros': juros}

def indice_nao_realizavel(df):
    intang = valor_contabil(df, '^1.*', 'intang')
    return {'Ativos Não Realizáveis': intang}

def indices_rentabilidade(df, b):
    lucro_liquido = valor_contabil(df, '^3.0', 'lucro líquido')
    roe = lucro_liquido / b['patrimonio_liquido']
    roa = lucro_liquido / b['ativo_total']
    return {'ROE': round(roe, 2), 'ROA': round(roa, 2)}

def print_dict(name, ticker, trimestre, data):
    print(f"Empresa: {name} ({ticker}) - Trimestre: {trimestre}")
    for chave, valor in data.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    for nome, ticker in EMPRESAS.items():
        try:
            df = dataframe(ticker, ANO_TRI)
            b = indices_basicos(df)
            liquidez = indices_liquidez(b)
            giro = indices_giro_tesouraria(b)
            endiv = indices_endividamento(b)
            rentab = indices_rentabilidade(df, b)

            resultado = {**liquidez, **giro, **endiv, **rentab}
            print_dict(nome, ticker, ANO_TRI, resultado)
            print("-" * 40)

        except Exception as e:
            print(f"Erro ao processar {nome}: {str(e)}")
