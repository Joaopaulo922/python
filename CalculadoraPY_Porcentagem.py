
# programa para reallização de calculo de produtos em porcentagem, realiza um calculo por vez.

var = input('Digite valor do produto, separado por um ponto "." .')
z = float(var)
soma = z * 0.32
total = soma + z
print(f'total com 32%, {total}')





# Programa com while, nunca vai ser interrompido. pois o valor não chegará a zero.

resposta = ''
while resposta != 0:
    resposta = input('Informe o valor do produto para realizar o calculo.?')
    resposta1 = float(resposta)
    soma = resposta1 * 0.45
    total = soma + resposta1
    print(f'Valor do produto é: {total}')
print(f'Obrigado por utilizar a aplicação!')
