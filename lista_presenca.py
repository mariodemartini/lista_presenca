import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

# Função para conectar e criar a tabela no banco de dados SQLite
def criar_banco():
    conn = sqlite3.connect('presenca_alunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dia_aula TEXT NOT NULL,
            situacao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar os dados no banco de dados e na lista
def salvar_dados():
    nome_aluno = entry_nome.get()
    dia_aula = entry_dia.get()
    situacao = situacao_var.get()

    if nome_aluno and dia_aula and situacao:
        conn = sqlite3.connect('presenca_alunos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO alunos (nome, dia_aula, situacao) VALUES (?, ?, ?)', 
                       (nome_aluno, dia_aula, situacao))
        conn.commit()
        conn.close()

        # Atualiza a lista exibida
        carregar_dados()
        
        # Limpa os campos após salvar
        limpar_campos()
    else:
        print("Preencha todos os campos!")

# Função para carregar os dados salvos no banco de dados e exibi-los na lista
def carregar_dados():
    for row in lista_dados.get_children():
        lista_dados.delete(row)
    
    conn = sqlite3.connect('presenca_alunos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, dia_aula, situacao FROM alunos')
    rows = cursor.fetchall()
    for row in rows:
        lista_dados.insert('', 'end', values=row)
    conn.close()

# Função para deletar o dado selecionado
def deletar_dados():
    selecionado = lista_dados.selection()
    if selecionado:
        item = lista_dados.item(selecionado)
        id_selecionado = item['values'][0]
        
        conn = sqlite3.connect('presenca_alunos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM alunos WHERE id = ?', (id_selecionado,))
        conn.commit()
        conn.close()

        # Atualiza a lista exibida
        carregar_dados()
        limpar_campos()

# Função para selecionar um item na lista para edição
def selecionar_dado(event):
    selecionado = lista_dados.selection()
    if selecionado:
        item = lista_dados.item(selecionado)
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, item['values'][1])
        entry_dia.set_date(item['values'][2])
        situacao_var.set(item['values'][3])

# Função para atualizar o dado selecionado
def atualizar_dados():
    selecionado = lista_dados.selection()
    if selecionado:
        item = lista_dados.item(selecionado)
        id_selecionado = item['values'][0]
        
        nome_aluno = entry_nome.get()
        dia_aula = entry_dia.get()
        situacao = situacao_var.get()

        if nome_aluno and dia_aula and situacao:
            conn = sqlite3.connect('presenca_alunos.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE alunos SET nome = ?, dia_aula = ?, situacao = ? WHERE id = ?', 
                           (nome_aluno, dia_aula, situacao, id_selecionado))
            conn.commit()
            conn.close()

            # Atualiza a lista exibida
            carregar_dados()
            limpar_campos()
        else:
            print("Preencha todos os campos!")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_dia.set_date('')
    situacao_var.set('Presente')

# Criando a janela principal
janela = tk.Tk()
janela.title("Registro de Presença")

# Label e Entry para Nome do Aluno
label_nome = tk.Label(janela, text="Nome do Aluno:")
label_nome.grid(row=0, column=0, padx=10, pady=5)

entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

# Label e DateEntry para Dia da Aula (calendário)
label_dia = tk.Label(janela, text="Dia da Aula:")
label_dia.grid(row=1, column=0, padx=10, pady=5)

entry_dia = DateEntry(janela, date_pattern='yyyy-mm-dd')  # Adiciona um calendário para selecionar a data
entry_dia.grid(row=1, column=1, padx=10, pady=5)

# Label e RadioButton para Situação (Presente ou Ausente)
label_situacao = tk.Label(janela, text="Situação:")
label_situacao.grid(row=2, column=0, padx=10, pady=5)

situacao_var = tk.StringVar(value="Presente")
radio_presente = tk.Radiobutton(janela, text="Presente", variable=situacao_var, value="Presente")
radio_presente.grid(row=2, column=1, padx=10, pady=5)

radio_ausente = tk.Radiobutton(janela, text="Ausente", variable=situacao_var, value="Ausente")
radio_ausente.grid(row=2, column=2, padx=10, pady=5)

# Botão para salvar os dados
botao_salvar = tk.Button(janela, text="Salvar", command=salvar_dados)
botao_salvar.grid(row=3, column=0, padx=10, pady=10)

# Botão para atualizar os dados
botao_atualizar = tk.Button(janela, text="Atualizar", command=atualizar_dados)
botao_atualizar.grid(row=3, column=1, padx=10, pady=10)

# Botão para deletar os dados
botao_deletar = tk.Button(janela, text="Deletar", command=deletar_dados)
botao_deletar.grid(row=3, column=2, padx=10, pady=10)

# Tabela para exibir os dados salvos
colunas = ('ID', 'Nome', 'Dia da Aula', 'Situação')
lista_dados = ttk.Treeview(janela, columns=colunas, show='headings')
lista_dados.heading('ID', text='ID')
lista_dados.heading('Nome', text='Nome')
lista_dados.heading('Dia da Aula', text='Dia da Aula')
lista_dados.heading('Situação', text='Situação')

lista_dados.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Evento de clique na lista para selecionar um item
lista_dados.bind('<<TreeviewSelect>>', selecionar_dado)

# Chamar a função para criar o banco de dados
criar_banco()

# Carregar dados existentes na inicialização
carregar_dados()

# Iniciar o loop da janela
janela.mainloop()
