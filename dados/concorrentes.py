import pandas as pd
import requests


TOKEN = "import pandas as pd
import requests


TOKEN = "access: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5MTI0MTEwLCJpYXQiOjE3NDY1MzIxMTAsImp0aSI6IjQyYWE2YjY1MTgxNDRiYWI5ZTEwMjdhNmNkMGY4OGE1IiwidXNlcl9pZCI6NzF9.ufeTn4PE1QgHudPISZTsHiZCC4xh2fxvLWXjFCOM0jc" 
HEADERS = {"Authorization": f"JWT {TOKEN}"}
ANO_TRI = "20234T"


EMPRESAS = {
    'BRF': 'BRFS3',
    'Marfrig': 'MRFG3',
    'Minerva': 'BEEF3',
    'Excelsior': 'BAUH4',
    'Minupar': 'MNPR3'
}


def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[0]

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[1]


def calcular_indicadores(ticker):
    params = {'ticker': ticker, 'ano_tri': ANO_TRI}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=HEADERS)
    dados = r.json()['dados'][0]['balanco']
    df = pd.DataFrame(dados)

    resultados = {}

    ac = valor_contabil(df, '^1.0', 'ativo cir')
    pc = valor_contabil(df, '^2.0', 'passivo cir')
    estoque = valor_contabil(df, '^1.0', 'estoque')
    desp_antec = valor_contabil(df, '^1.0', 'despesa')
    caixa = valor_contabil(df, '^1.0', 'caixa')
    aplic_fin = valor_contabil(df, '^1.0', 'aplica')
    arnc = valor_contabil(df, '^1.0', 'realiz')
    pnc = valor_contabil(df, '^2.0', 'passivo n.o cir')

    resultados['Liquidez Corrente'] = round(ac / pc, 2)
    resultados['Liquidez Seca'] = round((ac - estoque - desp_antec) / pc, 2)
    resultados['Liquidez Imediata'] = round((caixa + aplic_fin) / pc, 2)
    resultados['Liquidez Geral'] = round((ac + arnc) / (pc + pnc), 2)

    pl = valor_contabil(df, '^2.*', 'patrim')
    total_passivo = pc + pnc
    total_ativo = valor_contabil(df, '^1.*', 'ativo total')

    resultados['CT/CP'] = round(total_passivo / pl, 2)
    resultados['Endividamento Geral'] = round(total_passivo / (total_passivo + pl), 2)
    resultados['Solvencia'] = round(total_ativo / total_passivo, 2)
    resultados['Compos. Endividamento'] = round(pc / total_passivo, 2)


    pon = sum([
        valor_contabil(df, '^2.01', 'empr'),
        valor_contabil(df, '^2.02', 'empr'),
        valor_contabil(df, '^2.01', 'deb'),
        valor_contabil(df, '^2.02', 'deb')
    ])
    disponivel = caixa + aplic_fin
    divida_liquida = pon - disponivel
    investimento = pon + pl
    capital_oneroso = divida_liquida + pl

    resultados['Div. Líquida / PL'] = round(divida_liquida / pl, 2)
    resultados['Div. Líquida / Cap. Oneroso'] = round(divida_liquida / capital_oneroso, 2)

 
    wi = pon / investimento
    we = pl / investimento
    ir = valor_contabil(df, '^3.0', 'imposto de renda') * -1
    lair = valor_contabil_2(df, '^3.0', 'antes')
    aliquota = ir / lair
    desp_fin = valor_contabil(df, '^3.', 'despesas financeiras') * -1
    beneficio_trib = desp_fin * aliquota
    desp_fin_liquida = desp_fin - beneficio_trib
    ki = desp_fin_liquida / pon
    ke = 0.12
    resultados['CMPC'] = round((wi * ki) + (we * ke), 4)


    investimentos = valor_contabil(df, '^1.*', 'invest')
    intang = valor_contabil(df, '^1.*', 'intang')
    imobil = valor_contabil(df, '^1.*', 'imobil')
    resultados['Índice de PL'] = round((investimentos + intang + imobil) / pl, 2)

    return resultados


resultado_final = {}
for nome, ticker in EMPRESAS.items():
    try:
        resultado_final[nome] = calcular_indicadores(ticker)
    except Exception as e:
        resultado_final[nome] = {'Erro': str(e)}


df_resultados = pd.DataFrame(resultado_final).T
print(df_resultados)



HEADERS = {"access: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5MTI0MTEwLCJpYXQiOjE3NDY1MzIxMTAsImp0aSI6IjQyYWE2YjY1MTgxNDRiYWI5ZTEwMjdhNmNkMGY4OGE1IiwidXNlcl9pZCI6NzF9.ufeTn4PE1QgHudPISZTsHiZCC4xh2fxvLWXjFCOM0jc": f"JWT {TOKEN}"}
ANO_TRI = "20234T"


EMPRESAS = {
    'BRF': 'BRFS3',
    'Marfrig': 'MRFG3',
    'Minerva': 'BEEF3',
    'Excelsior': 'BAUH4',
    'Minupar': 'MNPR3'
}

def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[0]

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_desc = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_desc]['valor'].values[1]


def calcular_indicadores(ticker):
    params = {'ticker': ticker, 'ano_tri': ANO_TRI}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=HEADERS)
    dados = r.json()['dados'][0]['balanco']
    df = pd.DataFrame(dados)

    resultados = {}

    ac = valor_contabil(df, '^1.0', 'ativo cir')
    pc = valor_contabil(df, '^2.0', 'passivo cir')
    estoque = valor_contabil(df, '^1.0', 'estoque')
    desp_antec = valor_contabil(df, '^1.0', 'despesa')
    caixa = valor_contabil(df, '^1.0', 'caixa')
    aplic_fin = valor_contabil(df, '^1.0', 'aplica')
    arnc = valor_contabil(df, '^1.0', 'realiz')
    pnc = valor_contabil(df, '^2.0', 'passivo n.o cir')

    resultados['Liquidez Corrente'] = round(ac / pc, 2)
    resultados['Liquidez Seca'] = round((ac - estoque - desp_antec) / pc, 2)
    resultados['Liquidez Imediata'] = round((caixa + aplic_fin) / pc, 2)
    resultados['Liquidez Geral'] = round((ac + arnc) / (pc + pnc), 2)

    pl = valor_contabil(df, '^2.*', 'patrim')
    total_passivo = pc + pnc
    total_ativo = valor_contabil(df, '^1.*', 'ativo total')

    resultados['CT/CP'] = round(total_passivo / pl, 2)
    resultados['Endividamento Geral'] = round(total_passivo / (total_passivo + pl), 2)
    resultados['Solvencia'] = round(total_ativo / total_passivo, 2)
    resultados['Compos. Endividamento'] = round(pc / total_passivo, 2)

    pon = sum([
        valor_contabil(df, '^2.01', 'empr'),
        valor_contabil(df, '^2.02', 'empr'),
        valor_contabil(df, '^2.01', 'deb'),
        valor_contabil(df, '^2.02', 'deb')
    ])
    disponivel = caixa + aplic_fin
    divida_liquida = pon - disponivel
    investimento = pon + pl
    capital_oneroso = divida_liquida + pl

    resultados['Div. Líquida / PL'] = round(divida_liquida / pl, 2)
    resultados['Div. Líquida / Cap. Oneroso'] = round(divida_liquida / capital_oneroso, 2)

   
    wi = pon / investimento
    we = pl / investimento
    ir = valor_contabil(df, '^3.0', 'imposto de renda') * -1
    lair = valor_contabil_2(df, '^3.0', 'antes')
    aliquota = ir / lair
    desp_fin = valor_contabil(df, '^3.', 'despesas financeiras') * -1
    beneficio_trib = desp_fin * aliquota
    desp_fin_liquida = desp_fin - beneficio_trib
    ki = desp_fin_liquida / pon
    ke = 0.12
    resultados['CMPC'] = round((wi * ki) + (we * ke), 4)

 
    investimentos = valor_contabil(df, '^1.*', 'invest')
    intang = valor_contabil(df, '^1.*', 'intang')
    imobil = valor_contabil(df, '^1.*', 'imobil')
    resultados['Índice de PL'] = round((investimentos + intang + imobil) / pl, 2)

    return resultados


resultado_final = {}
for nome, ticker in EMPRESAS.items():
    try:
        resultado_final[nome] = calcular_indicadores(ticker)
    except Exception as e:
        resultado_final[nome] = {'Erro': str(e)}


df_resultados = pd.DataFrame(resultado_final).T
print(df_resultados)


