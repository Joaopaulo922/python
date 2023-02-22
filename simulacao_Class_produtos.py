"""
  item.mostra_item() "CÓDIGO PARA  MOSTAR OS PRODUTOS"
OBS# colar abaixo de cada item caso deseje que o mesmo seja printado.


"""

class Produtos:

    def __init__(self, nome, marca, descricao, tamanho, valor):
        self.__nome = nome
        self.__marca = marca
        self.__descricao = descricao
        self.__tamanho = tamanho
        self.__valor = valor
    def mostra_item(self):
        print(f"Produto: {nome}\nMarca: {marca}\nDescrição:{descricao}\nTamanho: {tamanho}\nValor: {valor}\n")

nome = 'Vestido'
marca = 'Prada'
descricao = 'Vestuario'
tamanho = 'M'
valor = 52.15
item = Produtos(nome, marca, descricao ,tamanho, valor)
item.mostra_item()

nome = 'Carro'
marca = 'Ford'
descricao = 'Automovel'
tamanho = 'Hatc'
valor = 30000
item2 = Produtos(nome, marca, descricao, tamanho, valor)


nome = 'iPhone 14 pro max'
marca = 'Apple'
descricao = 'Telefone'
tamanho = '1TB'
valor = 15000
item = Produtos(nome, marca, descricao, tamanho, valor)


nome = 'Pc Gamer'
marca = 'Longtech'
descricao = 'Processador i9x, placa de video 16gb'
tamanho = '1TB'
valor = 25000
item = Produtos(nome, marca, descricao, tamanho, valor)


nome = 'Calculadora mb-tech'
marca = ' MB-tech'
descricao = 'Informatica'
tamanho = 'P'
valor = 25
item = Produtos(nome, marca, descricao, tamanho, valor)


