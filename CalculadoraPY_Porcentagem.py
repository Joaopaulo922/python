"""
 programa para reallização de calculo de produtos em porcentagem, realiza um calculo por vez.
 Programa com while, nunca vai ser interrompido. pois o valor não chegará a zero.
"""


valor = ''
while valor != 0:
    entrada_valor = float(input('Informe o valor do produto para realizar o calculo.?'))
    entrada_porcentagem = float(input('Quantos porcentos deseja aplicar?'))
    porcentagem = entrada_porcentagem / 100
    total = entrada_valor + (porcentagem * entrada_valor)

    print(f'Valor do produto é: {total:.2f}\n')
print(f'Obrigado por utilizar a aplicação!')
