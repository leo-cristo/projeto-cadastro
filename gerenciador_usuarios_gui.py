import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import csv
from tkinter import filedialog

# Função para criar a tabela se não existir
def criar_tabela():
    with sqlite3.connect("meu_banco_de_dados.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT,
                telefone TEXT,
                endereco TEXT,
                idade INTEGER,
                cpf TEXT,
                data_nascimento TEXT
            )
        ''')
        conn.commit()

# Função para exportar dados para CSV
def exportar_para_csv():
    try:
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        
        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            dados = cursor.fetchall()
            
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([desc[0] for desc in cursor.description])  # Cabeçalhos
                writer.writerows(dados)  # Dados
        
        messagebox.showinfo("Exportar CSV", "Dados exportados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível exportar os dados. Erro: {e}")

# Função para inserir dados na tabela
def inserir_usuario():
    try:
        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, email, telefone, endereco, idade, cpf, data_nascimento)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry_nome.get(),
                entry_email.get(),
                entry_telefone.get(),
                entry_endereco.get(),
                int(entry_idade.get()),
                entry_cpf.get(),
                entry_data_nascimento.get()
            ))
            conn.commit()
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        listar_usuarios()  # Atualizar a lista após adição
        limpar_campos()  # Limpar campos após adição
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível adicionar o usuário. Erro: {e}")

# Função para atualizar dados na tabela
def atualizar_usuario():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Nenhum usuário selecionado para atualizar.")
            return
        
        usuario_id = tree.item(selected_item)['values'][0]

        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios
                SET nome = ?, email = ?, telefone = ?, endereco = ?, idade = ?, cpf = ?, data_nascimento = ?
                WHERE id = ?
            ''', (
                entry_nome.get(),
                entry_email.get(),
                entry_telefone.get(),
                entry_endereco.get(),
                int(entry_idade.get()),
                entry_cpf.get(),
                entry_data_nascimento.get(),
                usuario_id
            ))
            conn.commit()
        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
        listar_usuarios()  # Atualizar a lista após atualização
        limpar_campos()  # Limpar campos após atualização
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível atualizar o usuário. Erro: {e}")

# Função para excluir dados da tabela
def excluir_usuario():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Nenhum usuário selecionado para excluir.")
            return
        
        usuario_id = tree.item(selected_item)['values'][0]

        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
            conn.commit()
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        listar_usuarios()  # Atualizar a lista após exclusão
        limpar_campos()  # Limpar campos após exclusão
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível excluir o usuário. Erro: {e}")

# Função para listar os usuários na tabela
def listar_usuarios():
    try:
        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            
            for row in tree.get_children():
                tree.delete(row)
            
            for row in rows:
                tree.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível listar os usuários. Erro: {e}")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)

# Função para redefinir o contador de IDs
def redefinir_contador_ids():
    try:
        with sqlite3.connect("meu_banco_de_dados.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")
            conn.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível redefinir o contador de IDs. Erro: {e}")

# Redefinir o contador de IDs
redefinir_contador_ids()

# Criar a tabela no banco de dados
criar_tabela()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerenciador de Usuários")

# Campos de entrada
tk.Label(root, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Label(root, text="Telefone").grid(row=2, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1)

tk.Label(root, text="Endereço").grid(row=3, column=0)
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=3, column=1)

tk.Label(root, text="Idade").grid(row=4, column=0)
entry_idade = tk.Entry(root)
entry_idade.grid(row=4, column=1)

tk.Label(root, text="CPF").grid(row=5, column=0)
entry_cpf = tk.Entry(root)
entry_cpf.grid(row=5, column=1)

tk.Label(root, text="Data de Nascimento").grid(row=6, column=0)
entry_data_nascimento = tk.Entry(root)
entry_data_nascimento.grid(row=6, column=1)

# Botões
tk.Button(root, text="Adicionar", command=inserir_usuario).grid(row=7, column=0)
tk.Button(root, text="Atualizar", command=atualizar_usuario).grid(row=7, column=1)
tk.Button(root, text="Excluir", command=excluir_usuario).grid(row=7, column=2)
tk.Button(root, text="Listar", command=listar_usuarios).grid(row=7, column=3)
tk.Button(root, text="Exportar para CSV", command=exportar_para_csv).grid(row=7, column=4)

# Tabela para exibir dados
cols = ("ID", "Nome", "Email", "Telefone", "Endereço", "Idade", "CPF", "Data de Nascimento")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=8, column=0, columnspan=5)

# Inicializar a interface gráfica
root.mainloop()
