import customtkinter as ctk
import sqlite3
from tkinter import messagebox


# =========================
# BANCO DE DADOS
# =========================

def create_table():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    """

    cursor.execute(sql)
    conn.commit()
    conn.close()


def create_user(nome, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO usuarios (nome, senha) VALUES (?, ?)"
        cursor.execute(sql, (nome, senha))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(nome, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios WHERE nome = ? AND senha = ?"
    cursor.execute(sql, (nome, senha))

    usuario = cursor.fetchone()

    conn.close()
    return usuario


def update_user(nome, senha_antiga, senha_nova):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    sql_verifica = "SELECT * FROM usuarios WHERE nome = ? AND senha = ?"
    cursor.execute(sql_verifica, (nome, senha_antiga))

    usuario = cursor.fetchone()

    if usuario:
        sql_update = "UPDATE usuarios SET senha = ? WHERE nome = ?"
        cursor.execute(sql_update, (senha_nova, nome))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def delete_user(nome, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    sql_verifica = "SELECT * FROM usuarios WHERE nome = ? AND senha = ?"
    cursor.execute(sql_verifica, (nome, senha))

    usuario = cursor.fetchone()

    if usuario:
        sql_delete = "DELETE FROM usuarios WHERE nome = ?"
        cursor.execute(sql_delete, (nome,))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


# =========================
# FUNÇÕES DA INTERFACE
# =========================

def cadastrar():
    nome = entry_nome.get()
    senha = entry_senha.get()
    confirmar = entry_confirmar_senha.get()

    if nome == "" or senha == "" or confirmar == "":
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    if senha != confirmar:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        return

    if create_user(nome, senha):
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário já existe!")


def login():
    nome = entry_nome.get()
    senha = entry_senha.get()

    if login_user(nome, senha):
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")


def atualizar():
    nome = entry_nome.get()
    senha_antiga = entry_senha.get()
    senha_nova = entry_nova_senha.get()

    if nome == "" or senha_antiga == "" or senha_nova == "":
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    if update_user(nome, senha_antiga, senha_nova):
        messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha antiga incorretos!")


def deletar():
    nome = entry_nome.get()
    senha = entry_senha.get()

    if nome == "" or senha == "":
        messagebox.showerror("Erro", "Preencha nome e senha!")
        return

    if delete_user(nome, senha):
        messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")


# =========================
# INTERFACE
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Sistema CRUD de Usuários")
janela.geometry("400x500")


titulo = ctk.CTkLabel(
    janela,
    text="Sistema de Login",
    font=("Arial", 20)
)
titulo.pack(pady=20)


entry_nome = ctk.CTkEntry(
    janela,
    placeholder_text="Digite o nome"
)
entry_nome.pack(pady=10)


entry_senha = ctk.CTkEntry(
    janela,
    placeholder_text="Digite a senha",
    show="*"
)
entry_senha.pack(pady=10)


entry_confirmar_senha = ctk.CTkEntry(
    janela,
    placeholder_text="Confirme a senha",
    show="*"
)
entry_confirmar_senha.pack(pady=10)


entry_nova_senha = ctk.CTkEntry(
    janela,
    placeholder_text="Digite a nova senha",
    show="*"
)
entry_nova_senha.pack(pady=10)


botao_cadastrar = ctk.CTkButton(
    janela,
    text="Cadastrar Usuário",
    command=cadastrar
)
botao_cadastrar.pack(pady=10)


botao_login = ctk.CTkButton(
    janela,
    text="Login",
    command=login
)
botao_login.pack(pady=10)


botao_atualizar = ctk.CTkButton(
    janela,
    text="Redefinir Senha",
    command=atualizar
)
botao_atualizar.pack(pady=10)


botao_deletar = ctk.CTkButton(
    janela,
    text="Deletar Usuário",
    command=deletar
)
botao_deletar.pack(pady=10)


# cria tabela ao iniciar
create_table()

janela.mainloop()