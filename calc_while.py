"""
Teste de calculadora de IMC com LOOP while.
"""


Ideal = 'IMC acima de 18.5 até 24.9 é considerado ideal. \n'
magro = 'Abaixo de 18 de IMC é considerado magreza, e pode ser um risco para a saúde.\n'
exesso = 'IMC entre 25 a 30, você está com exesso de peso e deve procurar melhorar sua saúde. \n'
gordo = 'Você deve começar a se preocupar mais com sua saúde, vá fazer exercicios! \n'


resposta = ''
while resposta != 0:
    print('Seja Bem-vindo ao teste de calculadora de IMC.\n')
    entrada_nome = input('Como é o seu nome?')
    nome = entrada_nome.title()
    print(f'Olá {nome}, vamos dar inicio ao calculo.\n')

    entrada_peso = float(input('Informe seu peso (Kg):'))
    entrada_altura = float(input('Informe sua altura (Mt) (separe com um ".") :'))
    imc = entrada_peso / (entrada_altura ** 2)
    print(f'{nome}, você pesa {entrada_peso} Kg, e mede {entrada_altura} Mts.')

    numeroIMC = imc
    numeroIMC_formatado = "{:.2f}".format(numeroIMC)
    imc = imc
    print('Seu IMC é:', numeroIMC_formatado)

    if imc < 18.5:
        print(f' {nome} você esta abaixo do peso ideal!\n')
        print(f'{magro}')
    elif 18.5 <= imc < 25:
        print(f'{nome}, você esta com o peso ideal.\n')
        print(f' {Ideal}')
    elif 25 <= imc < 30:
        print(f'{nome}, Você esta com sobrepeso.\n')
        print(f'{gordo}')
    elif 30 <= imc < 35:
        print(f'{nome}, Você esta com obesidade grau 1.\n')
        print(f'{gordo}')
    elif 35 <= imc < 100:
        print(f'{nome}, Você esta com obesidade.\n')
        print(f'{gordo}')

    print(f' Obrigado {nome}, por testar a aplicação.')
    print('O teste foi reiniciado!\n')
