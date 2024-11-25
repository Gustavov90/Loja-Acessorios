import sqlite3
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from tkinter.ttk import Combobox, Treeview, Entry, Button, Label, Style
import pandas as pd
from datetime import datetime
from PIL import Image, ImageTk


class LojaAcessorios:
    def __init__(self):
        self.janela = Tk()
        self.janela.title("Loja de Acessórios Automotivos")
        self.janela.geometry("600x600")

        # Estilo ttk
        style = Style()
        style.configure('TButton', font=('Arial', 12), padding=2)
        style.configure('TLabel', font=('Arial', 12))


        self.painel_esquerdo = Frame(self.janela, width=200, bg="lightgray")
        self.painel_esquerdo.pack(side=LEFT, fill=Y)

        self.painel_direita = Frame(self.janela, bg="white")
        self.painel_direita.pack(side=RIGHT, fill=BOTH, expand=True)

        self.adicionar_logo()
        self.criar_botoes()
        self.janela.mainloop()

    def adicionar_logo(self):
        """Adiciona um logo no painel esquerdo."""
        try:
            logo = Image.open("logo.png")
            logo = logo.resize((200, 200))
            logo_tk = ImageTk.PhotoImage(logo)

            logo_label = Label(self.painel_esquerdo, image=logo_tk)
            logo_label.image = logo_tk
            logo_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o logo: {e}")

    def criar_botoes(self):
        """Cria os botões no painel esquerdo."""
        Button(self.painel_esquerdo, text="Venda", command=self.registrar_venda).pack(fill=X, pady=5)
        Button(self.painel_esquerdo, text="Adicionar Produto", command=self.adicionar_produto).pack(fill=X, pady=5)
        Button(self.painel_esquerdo, text="Excluir Produto", command=self.excluir_produto).pack(fill=X, pady=5)
        Button(self.painel_esquerdo, text="Importar Produtos", command=self.importar_excel).pack(fill=X, pady=5)
        Button(self.painel_esquerdo, text="Relatório de Vendas", command=self.gerar_relatorio_vendas).pack(fill=X,
                                                                                                                 pady=5)
        Button(self.painel_esquerdo, text="Consulta Estoque", command=self.listar_produtos).pack(fill=X, pady=5)

    def adicionar_produto(self):
        """Adiciona um produto ao banco de dados."""
        self.limpar_painel_direita()
        Label(self.painel_direita, text="Adicionar Produto").pack(pady=10)

        Label(self.painel_direita, text="Nome:").pack(pady=5)
        entrada_nome = Entry(self.painel_direita)
        entrada_nome.pack(pady=5)

        Label(self.painel_direita, text="Categoria:").pack(pady=5)
        entrada_categoria = Entry(self.painel_direita)
        entrada_categoria.pack(pady=5)

        Label(self.painel_direita, text="Preço:").pack(pady=5)
        entrada_preco = Entry(self.painel_direita)
        entrada_preco.pack(pady=5)

        Label(self.painel_direita, text="Estoque:").pack(pady=5)
        entrada_estoque = Entry(self.painel_direita)
        entrada_estoque.pack(pady=5)

        Button(self.painel_direita, text="Adicionar",
               command=lambda: self.adicionar_produto_db(entrada_nome, entrada_categoria, entrada_preco,
                                                         entrada_estoque)).pack(pady=10)

    def adicionar_produto_db(self, entrada_nome, entrada_categoria, entrada_preco, entrada_estoque):
        """Adiciona um produto ao banco de dados."""
        nome = entrada_nome.get()
        categoria = entrada_categoria.get()
        try:
            preco = float(entrada_preco.get())
            estoque = int(entrada_estoque.get())
            if preco < 0 or estoque < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos e não negativos.")
            return

        if nome and categoria:
            with sqlite3.connect("loja_acessorios.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "Produto já existe.")
                else:
                    cursor.execute("INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?)",
                                   (nome, categoria, preco, estoque))
                    messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                    entrada_nome.delete(0, END)
                    entrada_categoria.delete(0, END)
                    entrada_preco.delete(0, END)
                    entrada_estoque.delete(0, END())
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")

    def excluir_produto(self):
        """Exclui um produto do banco de dados."""
        nome_produto = simpledialog.askstring("Excluir Produto", "Digite o nome do produto a ser excluído:")
        if nome_produto:
            with sqlite3.connect("loja_acessorios.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome_produto,))
                if cursor.rowcount > 0:
                    messagebox.showinfo("Sucesso", f"Produto {nome_produto} excluído com sucesso!")
                else:
                    messagebox.showerror("Erro", "Produto não encontrado.")
        else:
            messagebox.showerror("Erro", "Nome do produto não fornecido.")

    def importar_excel(self):
        """Importa produtos de um arquivo Excel."""
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                with sqlite3.connect("loja_acessorios.db") as conn:
                    cursor = conn.cursor()
                    for _, row in df.iterrows():
                        cursor.execute("INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?)",
                                       (row['Nome'], row['Categoria'], row['Preço'], row['Estoque']))
                messagebox.showinfo("Sucesso", "Produtos importados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar produtos: {e}")

    def registrar_venda(self):
        """Registra a venda de um produto."""
        self.limpar_painel_direita()
        Label(self.painel_direita, text="Registrar Venda").pack(pady=10)

        # Combobox para selecionar o nome do produto
        Label(self.painel_direita, text="Produto:").pack(pady=5)
        nome_produto_var = StringVar()
        produtos_combo = Combobox(self.painel_direita, textvariable=nome_produto_var)
        produtos_combo.pack(pady=5)

        # Carregar produtos para a combobox
        with sqlite3.connect("loja_acessorios.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM produtos")
            produtos = cursor.fetchall()
            produtos_combo['values'] = [produto[0] for produto in produtos]

        # Campo para selecionar a quantidade
        Label(self.painel_direita, text="Quantidade:").pack(pady=5)
        quantidade_var = IntVar()
        entry_quantidade = Entry(self.painel_direita, textvariable=quantidade_var)
        entry_quantidade.pack(pady=5)

        # Exibir o estoque atual do produto
        Label(self.painel_direita, text="Estoque Atual:").pack(pady=5)
        estoque_atual_label = Label(self.painel_direita, text="0")
        estoque_atual_label.pack(pady=5)

        # Listbox para mostrar itens selecionados
        self.listbox_vendas = Listbox(self.painel_direita)
        self.listbox_vendas.pack(pady=10, fill=BOTH, expand=True)

        # Atualizar o estoque ao selecionar o produto
        def atualizar_estoque(event):
            nome_produto = nome_produto_var.get()
            with sqlite3.connect("loja_acessorios.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT estoque FROM produtos WHERE nome = ?", (nome_produto,))
                estoque_atual = cursor.fetchone()
                if estoque_atual:
                    estoque_atual_label.config(text=f"{estoque_atual[0]}")

        produtos_combo.bind("<<ComboboxSelected>>", atualizar_estoque)

        # Função para adicionar item à lista de vendas
        def adicionar_item():
            nome_produto = nome_produto_var.get()
            quantidade_vendida = quantidade_var.get()
            if nome_produto and quantidade_vendida > 0:
                self.listbox_vendas.insert(END, f"{nome_produto} - {quantidade_vendida}")
                quantidade_var.set(0)  # Limpa o campo de quantidade
            else:
                messagebox.showerror("Erro", "Por favor, selecione um produto e insira uma quantidade válida.")

        # Botão para adicionar item à lista de vendas
        Button(self.painel_direita, text="Adicionar Item", command=adicionar_item).pack(pady=10)

        # Função para efetuar a venda
        def efetuar_venda():
            if self.listbox_vendas.size() > 0:
                with sqlite3.connect("loja_acessorios.db") as conn:
                    cursor = conn.cursor()
                    for i in range(self.listbox_vendas.size()):
                        item = self.listbox_vendas.get(i)
                        nome_produto, quantidade_vendida = item.split(" - ")
                        quantidade_vendida = int(quantidade_vendida)

                        cursor.execute("SELECT estoque FROM produtos WHERE nome = ?", (nome_produto,))
                        estoque_atual = cursor.fetchone()
                        if estoque_atual and estoque_atual[0] >= quantidade_vendida:
                            novo_estoque = estoque_atual[0] - quantidade_vendida
                            cursor.execute("UPDATE produtos SET estoque = ? WHERE nome = ?",
                                           (novo_estoque, nome_produto))

                            # Registrar a venda
                            data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            cursor.execute("INSERT INTO vendas (produto, quantidade, data_venda) VALUES (?, ?, ?)",
                                           (nome_produto, quantidade_vendida, data_venda))
                        else:
                            messagebox.showerror("Erro", f"Estoque insuficiente para o produto: {nome_produto}.")
                            return

                messagebox.showinfo("Sucesso", "Vendas registradas com sucesso!")
                self.listbox_vendas.delete(0, END)  # Limpa a lista após registrar as vendas
            else:
                messagebox.showerror("Erro", "Nenhum item selecionado para venda.")

        # Botão para efetuar a venda
        Button(self.painel_direita, text="Efetuar Venda", command=efetuar_venda).pack(pady=10)

    def gerar_relatorio_vendas(self):
        """Gera um relatório de vendas."""
        with sqlite3.connect("loja_acessorios.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT produto, quantidade, data_venda FROM vendas")
            vendas = cursor.fetchall()

        if vendas:
            df = pd.DataFrame(vendas, columns=["Produto", "Quantidade", "Data de Venda"])
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Sucesso", "Relatório de vendas gerado com sucesso!")
        else:
            messagebox.showinfo("Sem Vendas", "Não há vendas registradas.")

    def listar_produtos(self):
        """Lista produtos por categoria usando Treeview."""
        self.limpar_painel_direita()
        Label(self.painel_direita, text="Listar Produtos").pack(pady=10)

        # Campo de pesquisa
        Label(self.painel_direita, text="Pesquisar Produto:").pack(pady=5)
        entrada_pesquisa = Entry(self.painel_direita)
        entrada_pesquisa.pack(pady=5)

        # Treeview para listar produtos
        tree = Treeview(self.painel_direita, columns=("Nome", "Categoria", "Preço", "Estoque"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("Categoria", text="Categoria")
        tree.heading("Preço", text="Preço")
        tree.heading("Estoque", text="Estoque")
        tree.pack(fill=BOTH, expand=True)

        # Atualizar a lista de produtos
        def atualizar_lista():
            query = entrada_pesquisa.get()
            with sqlite3.connect("loja_acessorios.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome, categoria, preco, estoque FROM produtos WHERE nome LIKE ?",
                               ('%' + query + '%',))
                produtos = cursor.fetchall()
                for item in tree.get_children():
                    tree.delete(item)
                for produto in produtos:
                    tree.insert("", "end", values=produto)

        entrada_pesquisa.bind("<KeyRelease>", lambda event: atualizar_lista())

    def limpar_painel_direita(self):
        """Limpa o painel direito."""
        for widget in self.painel_direita.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    LojaAcessorios()