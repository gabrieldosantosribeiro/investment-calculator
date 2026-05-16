# Converte para o padrão monetário brasileiro
def formatar_moeda(valor):

    valor_formatado = f'R$ {valor:,.2f}'

    valor_formatado = valor_formatado.replace(',', 'X')
    valor_formatado = valor_formatado.replace('.', ',')
    valor_formatado = valor_formatado.replace('X', '.')

    return valor_formatado