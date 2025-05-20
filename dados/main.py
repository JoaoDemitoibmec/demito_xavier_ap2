def main():

    list_ticker = []
    list_ticker.append("BRFS3")
    list_ticker.append("MRFG3")
    list_ticker.append("BEEF3")
    list_ticker.append("BAUH4")
    list_ticker.append("MNPR3")
    

    list_tri = []
    list_tri.append("20234T")
    list_tri.append("20244T")
    
    list_df = []
    list_liquidez = []
    list_giro_tesouraria = []
    list_endividamento = []
    list_emprestimos = []
    list_juros = []
    list_nao_realizavel = []
    list_ciclos = []
    list_rentabilidade = []

    for ticker in list_ticker:
        list_basicos = []
        for trimestre in list_tri:
            df = dataframe(ticker, trimestre)
            list_df.append(df)

            basicos = indices_basicos(df)
            liquidas = indices_liquidez(basicos)
            giro = indices_giro_tesouraria(basicos)
            endividamento = indices_endividamento(basicos)
            emprestimo = indices_emprestimos(basicos)
            juros = indices_juros(basicos)
            nao_realizavel = indice_nao_realizavel(basicos)
            rentabilidade = indices_rentabilidade(basicos)

            list_basicos.append(basicos)

            list_liquidez.append(liquidas)
            list_giro_tesouraria.append(giro)
            list_endividamento.append(endividamento)
            list_emprestimos.append(emprestimo)
            list_juros.append(juros)
            list_nao_realizavel.append(nao_realizavel)
            list_rentabilidade.append(rentabilidade)

            print_dict("Índices Básicos",        ticker, trimestre, basicos)
            print_dict("Índices de Liquidez",     ticker, trimestre, liquidas)
            print_dict("Giro de Tesouraria",      ticker, trimestre, giro)
            print_dict("Índice de Endividamento", ticker, trimestre, endividamento)
            print_dict("Empréstimos",             ticker, trimestre, emprestimo)
            print_dict("Índice de Juros",         ticker, trimestre, juros)
            print_dict("Não Realizável",          ticker, trimestre, nao_realizavel)
            print_dict("Rentabilidade",          ticker, trimestre, rentabilidade)

        
        ciclos = indices_ciclos(list_basicos[0], list_basicos[1])
        list_basicos.clear()

        list_ciclos.append(ciclos)

        header = f"Ciclos — {ticker} — {list_tri[0]} & {list_tri[1]}"
        print(header)
        for key, value in ciclos.items():
            print(f"  {key}: {value}")
        print()

        import pandas as pd


empresas = ["BRFS3", "MRFG3", "BEEF3", "BAUH4", "MNPR3"]


def gravar_indicadores(data_dict):
    """
    Recebe um dicionário com os indicadores por empresa e retorna um DataFrame consolidado.
    
    Exemplo de data_dict:
    {
        "BRFS3": {"ROE": 5.2, "EVA": -120},
        "MRFG3": {"ROE": 12.4, "EVA": 300},
        ...
    }
    """
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df.index.name = "Empresa"
    return df


def escolher_melhor_empresa(df, criterio="ROE"):
    """
    Compara as empresas com base no critério fornecido e retorna a melhor.
    Pode ser usado com 'ROE', 'EVA' ou outro indicador existente no DataFrame.
    """
    if criterio not in df.columns:
        raise ValueError(f"Critério '{criterio}' não encontrado no DataFrame.")
    
    if criterio == "EVA":
        melhor = df[criterio].idxmax()
    else:
        melhor = df[criterio].idxmax()
        
    return melhor, df.loc[melhor]


if __name__ == "__main__":
    indicadores = {
        "BRFS3": {"ROE": 4.3, "EVA": -150},
        "MRFG3": {"ROE": 9.1, "EVA": 220},
        "BEEF3": {"ROE": 11.0, "EVA": 180},
        "BAUH4": {"ROE": 7.5, "EVA": 90},
        "MNPR3": {"ROE": 6.8, "EVA": 75}
    }

    df_indicadores = gravar_indicadores(indicadores)
    print("Indicadores Consolidados:")
    print(df_indicadores)

    melhor_empresa, dados = escolher_melhor_empresa(df_indicadores, criterio="ROE")
    print(f"\nMelhor empresa com base no ROE: {melhor_empresa}\n{dados}")
