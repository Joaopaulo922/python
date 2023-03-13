""" CADASTRO DE CLIENTES E PRODUTOS e projeto de tela de vendas """
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
#from relatorios import Relatorios

import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
root = tk.Tk()

class Validadores():
    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100000
    def validate_entry4(self, text):
        if text == "": return True
        try:
            value = float(text)
        except ValueError:
            return False
        return len(text) < 10
class Gradiente(Canvas):
    def __init__(self, parent, color1="white", color2="black", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event = None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (r_ratio * i))
            nb = int(b1 + (r_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags= ("gradient"), fill=color)
        self.lower("gradient")
class Relatorios():
    def printClient(self):
        webbrowser.open("cliente.pdf")
    def geraRelaCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()
        self.enderecoRel = self.endereco_entry.get()
        self.debitoRel = self.debito_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo:' + self.codigoRel)
        self.c.drawString(50, 660, 'Nome:' + self.nomeRel)
        self.c.drawString(50, 620, 'Telefone:' + self.telefoneRel)
        self.c.drawString(50, 580, 'Endereco:' + self.enderecoRel)
        self.c.drawString(50, 540, 'Cidade:' + self.cidadeRel)
        self.c.drawString(50, 500, 'Debito:' + self.debitoRel)

        self.c.rect(20, 720, 550, 250, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printClient()
    def print_produto(self):
        webbrowser.open("relatorio_dos_produtos.pdf")
    def gera_relatorio_produtos(self):
        self.c = canvas.Canvas("relatorio_dos_produtos.pdf")

        self.codigopRel = self.codigoP_entry.get()
        self.produtoRel = self.nome_produto_entry.get()
        self.tamanhoRel = self.tamanho_entry.get()
        self.marcaRel = self.marca_entry.get()
        self.quantidadeRel = self.quantidade_entry.get()
        self.precoRel = self.preco_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Produto')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo:' + self.codigopRel)
        self.c.drawString(50, 660, 'Nome:' + self.produtoRel)
        self.c.drawString(50, 620, 'Tamanho:' + self.tamanhoRel)
        self.c.drawString(50, 580, 'Marca:' + self.marcaRel)
        self.c.drawString(50, 540, 'Quantidade em estoque:' + self.quantidadeRel)
        self.c.drawString(50, 500, 'Valor:' + self.precoRel)

        self.c.rect(20, 720, 550, 250, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.print_produto()
# aplicação
class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.debito_entry.delete(0, END)
    def limpa_telaProdutos(self):
        self.nome_produto_entry.delete(0, END)
        self.codigoP_entry.delete(0, END)
        self.tamanho_entry.delete(0, END)
        self.marca_entry.delete(0, END)
        self.quantidade_entry.delete(0, END)
        self.preco_entry.delete(0, END)
    def conecta_bd(self):
        self.com = sqlite3.connect("clientes.bd")
        self.cursor = self.com.cursor()
    def conecta_bd_P(self):
        self.conn = sqlite3.connect("estoque.bd")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.com.close()
    def monta_tabelas(self):
        self.conecta_bd();print("Conectando ao banco de dados")
        # criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40),
                endereco INTEGER(20) NOT NULL,
                debito
               
           );
        """)
        self.com.commit();print("Banco de dados criado.")
        self.desconecta_bd(); print("Banco de dados desconectado.")
    def monta_estoque(self):
        self.conecta_bd_P();
        print("Conectando ao banco de dados")
        # criar estoque
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                cod INTEGER PRIMARY KEY,
                nome_produto CHAR(40) NOT NULL,
                tamanho INTEGER(20),
                marca CHAR(40),
                quantidade INTEGER(20) NOT NULL,
                valor INTERGER (20)

            );
        """)
        self.conn.commit();
        print("Banco de dados criado.")
        self.desconecta_bd(); print("estoque criado")
        print("Banco de dados desconectado.")
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.endereco = self.endereco_entry.get()
        self.debito = self.debito_entry.get()
    def variaveisProdutos(self):
        self.codigoP = self.codigoP_entry.get()
        self.nomeP = self.nome_produto_entry.get()
        self.tamanho = self.tamanho_entry.get()
        self.marca = self.marca_entry.get()
        self.quantidade = self.quantidade_entry.get()
        self.preco = self.preco_entry.get()
    def add_cliente(self):
        self.variaveis()
        if self.nome_entry.get() == "":
           msg = "Para cadastrar um novo cliente é necessario \n"
           msg += "que seja digitado pelo menos um nome"
           messagebox.showinfo("Cadastro de clientes - Aviso!!!", msg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade, endereco, debito)
            VALUES (?, ?, ?, ?, ?)""", (self.nome, self.telefone, self.cidade, self.endereco, self.debito))
            self.com.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()
    def adicionar_produto(self):
        self.variaveisProdutos()
        if self.nome_produto_entry.get() == "":
           msg = "Para cadastrar um novo produto é necessario \n"
           msg += "que seja digitado pelo menos um nome"
           messagebox.showinfo("Cadastro de produtos - Aviso!!!", msg)
        else:
            self.conecta_bd_P()

            self.cursor.execute(""" INSERT INTO estoque (nome_produto, tamanho, marca, quantidade, valor)
            VALUES (?, ?, ?, ?, ?)""", (self.nomeP, self.tamanho, self.marca, self.quantidade, self.preco))
            self.conn.commit()
            self.desconecta_bd()
            self.select_listaProdutos()
            self.limpa_telaProdutos()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, 
        cidade, endereco, debito FROM clientes ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def select_listaProdutos(self):
        self.listaCli1.delete(*self.listaCli1.get_children())
        self.conecta_bd_P()
        lista1 = self.cursor.execute(""" SELECT cod, nome_produto, tamanho, 
        marca, quantidade, valor FROM estoque ORDER BY nome_produto ASC; """)
        for i in lista1:
            self.listaCli1.insert("", END, values=i)
        self.desconecta_bd()
    def onDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
            self.endereco_entry.insert(END, col5)
            self.debito_entry.insert(END, col6)
    def ondoubleclick_produtos(self, event):
        self.limpa_telaProdutos()
        self.listaCli1.selection()

        for n in self.listaCli1.selection():
            col1, col2, col3, col4, col5, col6 = self.listaCli1.item(n, 'values')
            self.codigoP_entry.insert(END, col1)
            self.nome_produto_entry.insert(END, col2)
            self.tamanho_entry.insert(END, col3)
            self.marca_entry.insert(END, col4)
            self.quantidade_entry.insert(END,col5)
            self.preco_entry.insert(END, col6)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ?""", (self.codigo))
        self.com.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def deletar_produto(self):
        self.variaveisProdutos()
        self.conecta_bd_P()
        self.cursor.execute(""" DELETE FROM estoque WHERE cod = ?""", (self.codigoP))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_telaProdutos()
        self.select_listaProdutos()
    def alterar_cliente(self):

        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?, endereco = ? , debito = ? WHERE cod = ? """,
                            (self.nome, self.telefone, self.cidade, self.endereco, self.debito, self.codigo))
        self.com.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def alterar_produtos(self):
        self.variaveisProdutos()
        self.conecta_bd_P()
        self.cursor.execute(
            """ UPDATE estoque SET nome_produto = ?, tamanho = ?, marca = ?,quantidade = ?, valor = ? WHERE cod = ? """,
            (self.nomeP, self.tamanho, self.marca,self.quantidade, self.preco, self.codigoP))
        self.conn.commit()
        self.desconecta_bd()
        self.select_listaProdutos()
        self.limpa_telaProdutos()
    def buscar_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade, endereco, debito FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)

        self.limpa_tela()
        self.desconecta_bd()
    def buscar_produto(self):
        self.conecta_bd_P()
        self.listaCli1.delete(*self.listaCli1.get_children())

        self.nome_produto_entry.insert(END, '%')
        nome = self.nome_produto_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_produto, tamanho, marca, valor FROM estoque
            WHERE nome_produto LIKE '%s' ORDER BY nome_produto ASC""" % nome)
        buscanomePro = self.cursor.fetchall()
        for i in buscanomePro:
            self.listaCli1.insert("", END, values=i)

        self.limpa_telaProdutos()
        self.desconecta_bd()
class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.root = root
        self.validar_Entradas()
        self.cores()
        self.tela()
        self.frames_tela()
        self.widgets_frame_1()
        self.lista_frame2()
        self.lista1_frame2()
        self.monta_tabelas()
        self.monta_estoque()
        self.select_lista()
        self.select_listaProdutos()
        self.Menus()
        root.mainloop()
    # configuração da tela
    def cores(self):
        self.cinza = "#e6e1e1"
        self.verde = "#6af77d"
        self.azul = "#3784b8"
        self.vermelho = "#f21d32"
        self.laranja = "#fc9e05"
        self.amarelo = "#e1ed02"
        self.corTela = "#e3e6e8"
        self.vermelho2 = "#8a0806"
        self.azul2 = "#1d89db"
        self.verde2 = "#41e056"
        self.cor_nova = "#d6d2c5"
        self.cor1 = "#1e1f1e"  # preta
        self.cor2 = "#f0eeeb"  # braco
        self.cor3 = "#05ceed"  # azul
        self.cor4 = "#8b8c8c"  # cinza
        self.cor5 = "#f79c0a"  # laraja
    def tela(self):
        self.root.title('APLICAÇÃO WEB')
        self.root.configure(bg="#ada5a5")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        #self.root.maxsize(width=800, height=900)
        self.root.minsize(width=600, height=600)
    # criando tela/frames
    def frames_tela(self):

        self.frame_1 = Frame(self.root, bd=4, bg=self.cinza, highlightbackground=self.cinza, highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)



        self.frame_2 = Frame(self.root, bd=4, highlightbackground=self.cinza, highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    # criando botoes
    def widgets_frame_1(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba3 = Frame(self.abas)

        self.aba1.configure(background =self.cor_nova)
        self.aba2.configure(background=self.cor_nova)
        self.aba3.configure(background=self.cor_nova)

        self.abas.add(self.aba1, text="Clientes")
        self.abas.add(self.aba2, text="Produtos")
        self.abas.add(self.aba3, text="Adicionais")
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        # variaveis balão
        text_blLimpar = "Limpar conteúdo das caixas de entrada."
        text_blApagar = "Apagar dados do cliente."
        text_blAlterar = "Editar dados do cliente."
        textoBalao_buscar = "Digite no campo o cliente que deseja pesquisar."
        text_blNovo = "Adicionar novo cliente."

        self.canvas_bt = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground= 'gray',
                                highlightthickness=4)
        self.canvas_bt.place(relx=0.19, rely=0.08, relwidth=0.22, relheight=0.19)

        self.canvas_bt = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground='gray',
                                highlightthickness=4)
        self.canvas_bt.place(relx=0.59, rely=0.08, relwidth=0.32, relheight=0.19)
        # botao limpar
        self.bt_limpar = Button(self.aba1, text="Limpar", bg=self.vermelho, bd=3, fg="white",
                                activebackground=self.vermelho2, activeforeground='white'
                                , font=("verdana", 8, "bold"),
                                command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth= 0.1, relheight=0.15)
        ToolTip(self.bt_limpar, msg=text_blLimpar)
        # botao buscar
        self.bt_buscar = Button(self.aba1, text="Buscar", bg=self.verde, bd=3, fg="white",activebackground=self.verde2,
                                activeforeground='white', font=("verdana", 8, "bold")
                                , command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.30, rely=0.1, relwidth=0.1, relheight=0.15)

        ToolTip(self.bt_buscar, msg=textoBalao_buscar)
        # botao novo
        self.bt_novo = Button(self.aba1, text="Novo", bg=self.azul, bd=3, fg="white", activebackground=self.azul2,
                              activeforeground='white', font=("verdana", 8, "bold"),
                              command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        ToolTip(self.bt_novo, msg=text_blNovo)
        # botao alterar
        self.bt_alterar = Button(self.aba1, text="Alterar", bg=self.azul, bd=3, fg="white",
                                 activebackground=self.azul2, activeforeground='white'
                                 ,font=("verdana", 8, "bold"), command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        ToolTip(self.bt_alterar, msg=text_blAlterar)
        # botao apagar
        self.bt_apagar = Button(self.aba1, text="Apagar", bd=3, fg="white",
                                activebackground=self.vermelho2, activeforeground='white',
                                font=("verdana", 8, "bold"), bg=self.vermelho,
                                command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        ToolTip(self.bt_apagar, msg=text_blApagar)

        # criando label e entrada de codigo
        self.lb_codigo = Label(self.aba1, text="Código", fg="black", bg=self.cor_nova)
        self.lb_codigo.place(relx=0.05, rely=0.05)
        self.codigo_entry = Entry(self.aba1, bg=self.corTela, validate="key", validatecommand=self.vcmd2)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.08)

        # criando label nome cliente
        self.lb_nome = Label(self.aba1, text="Nome", fg="black", bg=self.cor_nova)
        self.lb_nome.place(relx=0.05, rely=0.35)
        self.nome_entry = Entry(self.aba1, bg=self.corTela)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.5)

        # criando entrada_telefone
        self.lb_telefone = Label(self.aba1, text="Telefone", fg="black", bg=self.cor_nova)
        self.lb_telefone.place(relx=0.05, rely=0.6)
        self.telefone_entry = Entry(self.aba1, bg=self.corTela, validate="key", validatecommand=self.vcmd4)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        # criando entrada endereco
        self.lb_endereco = Label(self.aba1, text="Endereço", fg="black", bg=self.cor_nova)
        self.lb_endereco.place(relx=0.05, rely=0.8)
        self.endereco_entry = Entry(self.aba1, bg=self.corTela)
        self.endereco_entry.place(relx=0.05, rely=0.9, relwidth=0.8)

        #criando entrada_cidade
        self.lb_cidade = Label(self.aba1, text="Cidade", fg="black", bg=self.cor_nova)
        self.lb_cidade.place(relx=0.5, rely=0.6)
        self.cidade_entry = Entry(self.aba1, bg=self.corTela)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

        #CRIANDO ENTRADA VALOR DEBITO
        self.lb_debito = Label(self.aba1, text="Debito", fg="black", bg=self.cor_nova)
        self.lb_debito.place(relx=0.79, rely=0.4)
        self.debito_entry = Entry(self.aba1, bg=self.corTela,  validate="key", validatecommand=self.vcmd4)
        self.debito_entry.place(relx=0.79, rely=0.5, relwidth=0.1)

        # drop down button
        self.Tipvar = StringVar()
        self.Tipv = ("Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viuvo(a)")
        self.Tipvar.set("Solteiro(a)")
        self.popupMenu = OptionMenu(self.aba3, self.Tipvar, *self.Tipv)
        self.popupMenu.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.2)
        self.estado_civil = self.Tipvar.get()

        ## criando calendario
        self.bt_calendario = Button(self.aba3, text="Data", command=self.Calendario)
        self.bt_calendario.place(relx=0.5, rely=0.02)
        self.entry_data = Entry(self.aba3, width=10)
        self.entry_data.place(relx=0.5, rely=0.2)

        # botao Vender
        self.bt_vender = Button(self.aba1, text="Vender", bd=3, fg="white",
                                activebackground=self.verde2, activeforeground='white',
                                font=("verdana", 8, "bold"), bg=self.verde2, command = self.janela3)
        self.bt_vender.place(relx=0.9, rely=0.85, relwidth=0.1, relheight=0.15)

        # ABA 2 OBJETOS:

        # BOTOES ABA2 PRODUTOS
        # botao limpar
        self.bt_limparP = Button(self.aba2, text="Limpar", bg=self.vermelho, bd=3, fg="white",
                                activebackground=self.vermelho2, activeforeground='white'
                                , font=("verdana", 8, "bold"), command=self.limpa_telaProdutos)
        self.bt_limparP.place(relx=0.75, rely=0.8, relwidth=0.25, relheight=0.15)
        ToolTip(self.bt_limparP, msg="Limpar a tela")

        # botao buscar
        self.bt_buscarP = Button(self.aba2, text="Buscar", bg=self.verde, bd=3, fg="white",activebackground=self.verde2,
                                activeforeground='white', font=("verdana", 8, "bold"), command=self.buscar_produto
                             )
        self.bt_buscarP.place(relx=0.75, rely=0.2, relwidth=0.25, relheight=0.15)

        ToolTip(self.bt_buscarP, msg="Digite um produto para realizar a busca")

        # botao novo
        self.bt_novoP = Button(self.aba2, text="Adicionar Produto", bg=self.azul, bd=3, fg="white", activebackground=self.azul2,
                              activeforeground='white', font=("verdana", 8, "bold"), command=self.adicionar_produto)
        self.bt_novoP.place(relx=0.75, rely=0.01, relwidth=0.25, relheight=0.15)
        ToolTip(self.bt_novoP, msg="Adicionar novo produto")

        # botao alterar
        self.bt_alterarP = Button(self.aba2, text="Alterar Produto", bg=self.azul, bd=3, fg="white",
                                 activebackground=self.azul2, activeforeground='white'
                                 ,font=("verdana", 8, "bold"), command=self.alterar_produtos)
        self.bt_alterarP.place(relx=0.75, rely=0.4, relwidth=0.25, relheight=0.15)
        ToolTip(self.bt_alterarP, msg="Altera produto selecionado")

        # Botao apagar
        self.bt_apagarP = Button(self.aba2, text="Apagar", bd=3, fg="white",
                                activebackground=self.vermelho2, activeforeground='white',
                                font=("verdana", 8, "bold"), bg=self.vermelho, command=self.deletar_produto)
        self.bt_apagarP.place(relx=0.75, rely=0.60, relwidth=0.25, relheight=0.15)
        ToolTip(self.bt_apagarP, msg="Apaga produto selacionado")

        # criando entrada produtos
        self.lb_nome_produto = Label(self.aba2, text="Produto", fg="black", bg=self.cor_nova)
        self.lb_nome_produto.place(relx=0.4, rely=0.1)
        self.nome_produto_entry = Entry(self.aba2, bg=self.corTela)
        self.nome_produto_entry.place(relx=0.4, rely=0.2, relwidth=0.27)

        # criando entrada objeto aba2 codigo
        self.lb_codigoP = Label(self.aba2, text="Codigo", fg="black", bg=self.cor_nova)
        self.lb_codigoP.place(relx=0.05, rely=0.1)
        self.codigoP_entry = Entry(self.aba2, bg=self.corTela, validate="key", validatecommand=self.vcmd2)
        self.codigoP_entry.place(relx=0.05, rely=0.2, relwidth=0.2)

        # criando entrada objeto aba2 marca
        self.lb_marca = Label(self.aba2, text="Marca", fg="black", bg=self.cor_nova)
        self.lb_marca.place(relx=0.05, rely=0.4)
        self.marca_entry = Entry(self.aba2, bg=self.corTela)
        self.marca_entry.place(relx=0.05, rely=0.5, relwidth=0.2)

        # criando entrada objeto aba2 tamanho
        self.lb_tamanho = Label(self.aba2, text="Tamanho", fg="black", bg=self.cor_nova)
        self.lb_tamanho.place(relx=0.4, rely=0.4)
        self.tamanho_entry = Entry(self.aba2, bg=self.corTela)
        self.tamanho_entry.place(relx=0.4, rely=0.5, relwidth=0.1)

        # criando entrada objeto aba2 Quantidade
        self.lb_quantidade = Label(self.aba2, text="Quantidade", fg="black", bg=self.cor_nova)
        self.lb_quantidade.place(relx=0.05, rely=0.65)
        self.quantidade_entry = Entry(self.aba2, bg=self.corTela,  validate="key", validatecommand=self.vcmd4)
        self.quantidade_entry.place(relx=0.05, rely=0.75, relwidth=0.1)

        # criando entrada objeto aba2 PREÇO
        self.lb_preco = Label(self.aba2, text="Valor", fg="black", bg=self.cor_nova)
        self.lb_preco.place(relx=0.4, rely=0.65)
        self.preco_entry = Entry(self.aba2, bg=self.corTela, validate="key", validatecommand=self.vcmd4)
        self.preco_entry.place(relx=0.4, rely=0.75, relwidth=0.1)

        # botao Vender
        self.bt_vender2 = Button(self.aba2, text="Vender", bd=3, fg="white",
                                activebackground=self.verde2, activeforeground='white',
                                font=("verdana", 8, "bold"), bg=self.verde2, command=self.janela3)
        self.bt_vender2.place(relx=0.63, rely=0.8, relwidth=0.1, relheight=0.15)
    # LISTAS FRAME 2
    def lista_frame2(self):
        self.abas = ttk.Notebook(self.frame_2)
        self.aba4 = Gradiente(self.abas)
        self.aba5 = Gradiente(self.abas)
        self.aba4.configure(background=self.cinza)
        self.aba5.configure(background=self.cinza)
        self.abas.add(self.aba4, text="Clientes")
        self.abas.add(self.aba5, text="Estoque")
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        self.listaCli = ttk.Treeview(self.aba4, height=3,
                                     column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
        self.listaCli.heading("#5", text="Endereco")
        self.listaCli.heading("#6", text="Débito")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=150)
        self.listaCli.column("#3", width=115)
        self.listaCli.column("#4", width=100)
        self.listaCli.column("#5", width=110)
        self.listaCli.column("#6", width=120)
        self.listaCli.place(relx=0.03, rely=0.1, relwidth=0.95, relheight=0.85)
        self.scroolLista = Scrollbar(self.aba4, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.onDoubleClick)
    def lista1_frame2(self):
        self.listaCli1 = ttk.Treeview(self.aba5, height=3,
                                      column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaCli1.heading("#0", text="")
        self.listaCli1.heading("#1", text="Codigo")
        self.listaCli1.heading("#2", text="Produto")
        self.listaCli1.heading("#3", text="Tamanho")
        self.listaCli1.heading("#4", text="Marca")
        self.listaCli1.heading("#5", text="Quantidade")
        self.listaCli1.heading("#6", text="Valor")
        self.listaCli1.column("#0", width=1)
        self.listaCli1.column("#1", width=50)
        self.listaCli1.column("#2", width=150)
        self.listaCli1.column("#3", width=70)
        self.listaCli1.column("#4", width=50)
        self.listaCli1.column("#5", width=70)
        self.listaCli1.column("#6", width=90)
        self.listaCli1.place(relx=0.03, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.aba5, orient='vertical')
        self.listaCli1.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli1.bind("<Double-1>", self.ondoubleclick_produtos)
    # MENUS
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu3 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorios Clientes", menu=filemenu2)
        menubar.add_cascade(label="Relatorios dos produtos", menu=filemenu3)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelaCliente)
        filemenu3.add_command(label="Ficha produtos", command=self.gera_relatorio_produtos)
    # JANELA
    def janela2(self):
        root2 = tk.Toplevel()
        root2.title('Clientes')
        root2.configure(bg='lightblue')
        root2.geometry("500x500")
        root2.resizable(False, False)
        #root2.transient(self.root)
        root2.focus_force()
        root2.grab_set()

        # frame da tela de procurar clientes
        self.frame_4 = Frame(root2, bd=4, highlightbackground=self.cinza, highlightthickness=3)
        self.frame_4.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        # botões e labels tela de procurar clientes
        self.lb_pCliente = Label(self.frame_4, text="Procurar", fg="black", bg=self.cor_nova)
        self.lb_pCliente.place(relx=0.01, rely=0.01)
        self.pCliente_entry = Entry(self.frame_4, bg=self.corTela)
        self.pCliente_entry.place(relx=0.01, rely=0.05, relwidth=0.5)
        # Botão sair
        self.bt_sair_tela_pClientes = tk.Button(self.frame_4, text="SAIR", bd=3, fg="white",
                                            activebackground=self.vermelho2, activeforeground='white',
                                            font=("verdana", 8, "bold"), bg=self.vermelho, command=root2.destroy)
        self.bt_sair_tela_pClientes.place(relx=0.80, rely=0.02, relwidth=0.15, relheight=0.06)
        # treeview para listar os clientes
        self.verClientes = ttk.Treeview(self.frame_4, height=3,
                                        column=("col1", "col2", "col3", "col4", "col5"))
        self.verClientes.heading("#0", text="")
        self.verClientes.heading("#1", text="Codigo")
        self.verClientes.heading("#2", text="Nome")
        self.verClientes.heading("#3", text="Telefone")
        self.verClientes.heading("#4", text="Cidade")
        self.verClientes.heading("#5", text="Endereço")

        self.verClientes.column("#0", width=1)
        self.verClientes.column("#1", width=60)
        self.verClientes.column("#2", width=250)
        self.verClientes.column("#3", width=50)
        self.verClientes.column("#4", width=50)
        self.verClientes.column("#5", width=50)
        self.verClientes.place(relx=0.01, rely=0.30, relwidth=0.96, relheight=0.96)
    def janela3(self):
        tela_venda = tk.Toplevel()
        tela_venda.title("Realizar venda")
        tela_venda.configure(bg=self.cor_nova)
        tela_venda.geometry("700x500")
        tela_venda.resizable(True, True)
        tela_venda.transient(self.root)
        tela_venda.focus_force()
        tela_venda.grab_set()

        self.frame_3 = Frame(tela_venda, bd=4, highlightbackground=self.cinza, highlightthickness=3)
        self.frame_3.place(relx=0.01, rely=0.01, relwidth=1, relheight=1)
        # botao vender
        self.bt_realizar_Venda = tk.Button(self.frame_3, text="Vender", bd=3, fg="white",
                               activebackground=self.verde2, activeforeground='white',
                               font=("verdana", 8, "bold"), bg=self.verde2, command=self.janela_FinalizarVenda)
        self.bt_realizar_Venda.place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.05)
        # botao cancelar compra
        self.bt_cancelar_Venda = tk.Button(self.frame_3, text="Cancelar", bd=3, fg="white",
                                   activebackground=self.vermelho2, activeforeground='white',
                                   font=("verdana", 8, "bold"), bg=self.vermelho)
        self.bt_cancelar_Venda.place(relx=0.1, rely=0.02, relwidth=0.1, relheight=0.05)
        # Botão procurar produtos
        self.bt_produrar_Produto = tk.Button(self.frame_3, text="Produrar produto", bd=3, fg="white",
                                   activebackground=self.vermelho2, activeforeground='white',
                                   font=("verdana", 8, "bold"), bg=self.azul)
        self.bt_produrar_Produto.place(relx=0.5, rely=0.02, relwidth=0.2, relheight=0.05)
        # Botão procurar clientes
        self.bt_produrar_clientestv = tk.Button(self.frame_3, text="Produrar clientes", bd=3, fg="white",
                                             activebackground=self.vermelho2, activeforeground='white',
                                             font=("verdana", 8, "bold"), bg=self.azul, command=self.janela2)
        self.bt_produrar_clientestv.place(relx=0.25, rely=0.02, relwidth=0.2, relheight=0.05)
        # Botão sair
        self.bt_sair_tela_venda = tk.Button(self.frame_3, text="SAIR", bd=3, fg="white",
                                             activebackground=self.vermelho2, activeforeground='white',
                                             font=("verdana", 8, "bold"), bg=self.vermelho, command= tela_venda.destroy)
        self.bt_sair_tela_venda.place(relx=0.75, rely=0.02, relwidth=0.2, relheight=0.05)



        # criando entrada nome
        self.lb_produtovenda = Label(self.frame_3, text="Produto", fg="black", bg=self.cor_nova)
        self.lb_produtovenda.place(relx=0.01, rely=0.2)
        self.nome_produtoVenda_entry = Entry(self.frame_3, bg=self.corTela)
        self.nome_produtoVenda_entry.place(relx=0.01, rely=0.25, relwidth=0.5)

        self.lb_quantidadeovenda = Label(self.frame_3, text="Quantidade", fg="black", bg=self.cor_nova)
        self.lb_quantidadeovenda.place(relx=0.55, rely=0.2)
        self.quantidadevenda_entry = Entry(self.frame_3, bg=self.corTela)
        self.quantidadevenda_entry.place(relx=0.55, rely=0.25, relwidth=0.2)

        self.lb_totalvenda = Label(self.frame_3, text="Total", fg="black", bg=self.cor_nova)
        self.lb_totalvenda.place(relx=0.85, rely=0.2)
        self.totalvenda_entry = Entry(self.frame_3, bg=self.corTela)
        self.totalvenda_entry.place(relx=0.85, rely=0.25, relwidth=0.1)

        self.listaprod = ttk.Treeview(self.frame_3, height=3,
                                      column=("col1", "col2", "col3", "col4", "col5"))
        self.listaprod.heading("#0", text="")
        self.listaprod.heading("#1", text="Codigo")
        self.listaprod.heading("#2", text="Produto")
        self.listaprod.heading("#3", text="Quantidade")
        self.listaprod.heading("#4", text="Valor und")
        self.listaprod.heading("#5", text="Total")

        self.listaprod.column("#0", width=15)
        self.listaprod.column("#1", width=35)
        self.listaprod.column("#2", width=250)
        self.listaprod.column("#3", width=50)
        self.listaprod.column("#4", width=50)
        self.listaprod.column("#5", width=50)

        self.listaprod.place(relx=0.01, rely=0.40, relwidth=0.70, relheight=0.96)


        # criando botoes
    def janela_FinalizarVenda(self):
        fvenda = tk.Toplevel()
        fvenda.title('Finalizar venda')
        fvenda.geometry("400x500")
        fvenda.resizable(False, False)
        fvenda.focus_force()
        fvenda.grab_set()
        # frame finalizar vendas
        self.frame_5 = Frame(fvenda, bd=4, highlightbackground=self.cinza, highlightthickness=3)
        self.frame_5.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)


        # entrys e labels
        self.lb_total = Label(self.frame_5, text="Valor", fg="black", bg=self.cor_nova)
        self.lb_total.place(relx=0.01, rely=0.2, relwidth=0.2, relheight=0.05)
        self.frame_6 = Frame(fvenda, bd=4,highlightbackground=self.azul, highlightthickness=3 )
        self.frame_6.place(relx=0.03, rely=0.25, relwidth=0.2, relheight=0.09)

        self.lb_totaldesconto = Label(self.frame_5, text="Desconto", fg="black", bg=self.cor_nova)
        self.lb_totaldesconto.place(relx=0.01, rely=0.4, relwidth=0.2, relheight=0.05)
        self.frame_7 = Frame(fvenda, bd=4, highlightbackground=self.azul, highlightthickness=3)
        self.frame_7.place(relx=0.03, rely=0.45, relwidth=0.2, relheight=0.09)

        self.lb_totalPagar = Label(self.frame_5, text="Total com desconto", fg="black", bg=self.cor_nova)
        self.lb_totalPagar.place(relx=0.01, rely=0.7, relwidth=0.28, relheight=0.05)
        self.frame_6 = Frame(fvenda, bd=4, highlightbackground=self.azul, highlightthickness=3)
        self.frame_6.place(relx=0.03, rely=0.75, relwidth=0.2, relheight=0.09)

        # botao
        self.bt_sairFV = tk.Button(self.frame_5, text="SAIR", bd=3, fg="white",
                                            activebackground=self.vermelho2, activeforeground='white',
                                            font=("verdana", 8, "bold"), bg=self.vermelho, command=fvenda.destroy)
        self.bt_sairFV.place(relx=0.75, rely=0.8, relwidth=0.2, relheight=0.05)

        self.bt_confirmarVenda = tk.Button(self.frame_5, text="Confirmar", bd=3, fg="white",
                                   activebackground=self.azul, activeforeground='white',
                                   font=("verdana", 8, "bold"), bg=self.azul2)
        self.bt_confirmarVenda.place(relx=0.75, rely=0.6, relwidth=0.2, relheight=0.05)

        # BOTÃO CALCULADORA
        self.bt_calculadora = tk.Button(self.frame_5, text="Calculadora", bd=3, fg="white",
                                           activebackground=self.azul, activeforeground='white',
                                           font=("verdana", 8, "bold"), bg=self.azul2, command=self.calculadora)
        self.bt_calculadora.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.05)

        # ENTRY ENTRY DO DESCONTO
        self.Valordesconto = Label(self.frame_5, text="Desconto", fg="black", bg=self.cor_nova)
        self.Valordesconto.place(relx=0.60, rely=0.2)
        self.Valordesconto_entry = Entry(self.frame_5, bg=self.corTela)
        self.Valordesconto_entry.place(relx=0.60, rely=0.25, relwidth=0.2)
    def calculadora(self):
        telacalculadora = tk.Toplevel()
        telacalculadora.title("Calculadora")
        telacalculadora.geometry("235x310")
        telacalculadora.resizable(False, False)
        telacalculadora.grab_set()
        telacalculadora.config(bg=self.cor1)

        # criando frame
        self.frame_tela = Frame(telacalculadora, width=235, height=50, bg=self.cor3)
        self.frame_tela.place(relx=0.01, rely=0.01, relwidth=0.99, relheight=0.19 )

        self.frame_corpo = Frame(telacalculadora, width=235, height=268)
        self.frame_corpo.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.99 )
        # variavel todos valores
        todos_valores = ""
        valor_texto = StringVar()

        def entrada_valor(event):
            global todos_valores
            todos_valores = todos_valores + str(event)

            # passar valor para a tela
            valor_texto.set(todos_valores)

        def calcular():
            global todos_valores
            resultado = eval(todos_valores)
            valor_texto.set(str(resultado))

        def limpar_tela():
            global todos_valores
            todos_valores = ""
            valor_texto.set("")

        # criando label


        self.app_label = Label(self.frame_tela, textvariable=valor_texto, width=16, height=2, padx=7, relief=FLAT,
                          anchor='e',
                          justify=RIGHT, font=('Ivy 18'), bg=self.azul, fg=self.cor2)
        self.app_label.place(x=0, y=0)

        # criando botoes
        self.b_1 = tk.Button(self.frame_corpo,  command=lambda: limpar_tela(),text="C", width=11, height=2,
                             bg=self.cor4,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_1.place(x=0, y=0)
        self.b_2 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('%'), text="%", width=5, height=2,
                             bg=self.cor4,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_2.place(x=118, y=0)
        self.b_3 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('/'), text="/", width=5, height=2,
                             bg=self.cor5, fg=self.cor1,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_3.place(x=177, y=0)

        self.b_4 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('7'), text="7", width=5, height=2,
                             bg=self.cor4,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_4.place(x=0, y=52)
        self.b_5 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('8'), text="8", width=5, height=2,
                             bg=self.cor4, fg=self.cor1,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_5.place(x=59, y=52)
        self.b_6 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('9'), text="9", width=5, height=2,
                             bg=self.cor4, fg=self.cor1,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_6.place(x=118, y=52)
        self.b_7 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('*'), text="*", width=5, height=2,
                             bg=self.cor5, fg=self.cor1,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_7.place(x=177, y=52)

        self.b_8 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('4'), text="4", width=5, height=2,
                             bg=self.cor4,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_8.place(x=0, y=102)
        self.b_9 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('5'), text="5", width=5, height=2,
                             bg=self.cor4, fg=self.cor1,
                             font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_9.place(x=59, y=102)
        self.b_10 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('6'), text="6", width=5, height=2,
                              bg=self.cor4, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_10.place(x=118, y=102)
        self.b_11 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('-'), text="-", width=5, height=2,
                              bg=self.cor5, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_11.place(x=177, y=102)

        self.b_12 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('1'), text="1", width=5, height=2,
                              bg=self.cor4,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_12.place(x=0, y=153)
        self.b_13 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('2'), text="2", width=5, height=2,
                              bg=self.cor4, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_13.place(x=59, y=153)
        self.b_14 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('3'), text="3", width=5, height=2,
                              bg=self.cor4, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_14.place(x=118, y=153)
        self.b_15 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('+'), text="+", width=5, height=2,
                              bg=self.cor5, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_15.place(x=177, y=153)

        self.b_16 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('0'), text="0", width=11, height=2,
                              bg=self.cor4,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_16.place(x=0, y=206)
        self.b_17 = tk.Button(self.frame_corpo, command=lambda: entrada_valor('.'), text=".", width=5, height=2,
                              bg=self.cor4, fg=self.cor1,
                              font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
        self.b_17.place(x=118, y=206)

        self.b_18 = tk.Button(self.frame_corpo, command=lambda: calcular(), text='=', width=5, height=2, bg=self.cor5,
                              fg=self.cor1,
                              font=('Ivy 13 bold'),
                              relief=RAISED, overrelief=RIDGE)
        self.b_18.place(x=177, y=206)
    def validar_Entradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry2), "%P")
        self.vcmd4 = (self.root.register(self.validate_entry4), "%P")
    def Calendario(self):
        self.calendario1= Calendar(self.aba3, fg="gray75", bg="blue",
                                   font=("Times", "9", "bold"),locale="pt_br" )
        self.calendario1.place(relx=0.5, rely=0.1)
        self.calData = Button(self.aba3, text="Inserir Data",
         command=self.print_cal)
        self.calData.place(relx=0.55, rely=0.85, height=25, width=100)
    def print_cal(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_data.delete(0, END)
        self.entry_data.insert(END, dataIni)
        self.calData.destroy()
Application()
