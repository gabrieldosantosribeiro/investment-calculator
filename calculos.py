# Simula o crescimento do patrimônio mês a mês
def simular_crescimento(aporte_inicial, aporte_mensal, taxa_juros, tempo_meses):

    patrimonio = aporte_inicial
    historico = []
    tempo_meses = int(tempo_meses)

    for mes in range(1, tempo_meses + 1):

        patrimonio *= (1 + taxa_juros)
        patrimonio += aporte_mensal

        historico.append({
            'mes': mes,
            'patrimonio': patrimonio
        })

    return historico


# Calcula quantos meses são necessários para atingir o valor desejado
def calcular_tempo(valor_futuro, aporte_inicial, aporte_mensal, taxa_juros):

    patrimonio = aporte_inicial
    tempo_meses = 0

    while patrimonio < valor_futuro:
        patrimonio *= (1 + taxa_juros)
        patrimonio += aporte_mensal
        tempo_meses += 1

    return tempo_meses


# Calcula o aporte mensal necessário para atingir o valor desejado
def calcular_aporte(valor_futuro, aporte_inicial, taxa_juros, tempo_meses):

    aporte_mensal = (
        (valor_futuro - aporte_inicial * (1 + taxa_juros) ** tempo_meses)
        /
        (((1 + taxa_juros) ** tempo_meses - 1) / taxa_juros)
    )

    return aporte_mensal