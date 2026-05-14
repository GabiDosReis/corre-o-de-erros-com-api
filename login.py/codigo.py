import customtkinter as ctk
from tkinter import messagebox
import sqlite3

# =====================================================
# CONFIGURAÇÕES INICIAIS
# =====================================================

ctk.set_appearance_mode("dark")  # modo escuro
ctk.set_default_color_theme("blue")  # tema azul


# =====================================================
# BANCO DE DADOS
# =====================================================

def conectar():
    """
    Faz a conexão com o banco de dados SQLite
    """
    return sqlite3.connect("usuarios.db")


def criar_tabela():
    """
    Cria a tabela usuarios caso ela não exista
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def limpar_campos():
    """
    Limpa todos os campos da tela
    """
    entry_email.delete(0, "end")
    entry_senha.delete(0, "end")
    entry_confirmar.delete(0, "end")


def validar_formulario(email, senha, confirmar):
    """
    Faz a validação dos campos
    """

    if not email or not senha or not confirmar:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return False

    if "@" not in email:
        messagebox.showerror("Erro", "Digite um e-mail válido.")
        return False

    if len(senha) < 6:
        messagebox.showerror(
            "Erro",
            "A senha deve ter no mínimo 6 caracteres."
        )
        return False

    if senha != confirmar:
        messagebox.showerror(
            "Erro",
            "As senhas não coincidem."
        )
        return False

    return True


# =====================================================
# CREATE - CADASTRAR
# =====================================================

def cadastrar_usuario():
    email = entry_email.get()
    senha = entry_senha.get()
    confirmar = entry_confirmar.get()

    if not validar_formulario(email, senha, confirmar):
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (email, senha)
            VALUES (?, ?)
        """, (email, senha))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Usuário cadastrado com sucesso!"
        )

        limpar_campos()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Erro",
            "Este e-mail já está cadastrado."
        )


# =====================================================
# READ - BUSCAR
# =====================================================

def buscar_usuario():
    email = entry_email.get()

    if not email:
        messagebox.showerror(
            "Erro",
            "Digite o e-mail para buscar."
        )
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE email = ?
    """, (email,))

    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        entry_senha.delete(0, "end")
        entry_senha.insert(0, usuario[2])

        messagebox.showinfo(
            "Sucesso",
            "Usuário encontrado!"
        )
    else:
        messagebox.showerror(
            "Erro",
            "Usuário não encontrado."
        )


# =====================================================
# UPDATE - ATUALIZAR
# =====================================================

def atualizar_usuario():
    email = entry_email.get()
    nova_senha = entry_senha.get()

    if not email or not nova_senha:
        messagebox.showerror(
            "Erro",
            "Digite e-mail e nova senha."
        )
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE email = ?
    """, (nova_senha, email))

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo(
            "Sucesso",
            "Senha atualizada com sucesso!"
        )
    else:
        messagebox.showerror(
            "Erro",
            "Usuário não encontrado."
        )

    conn.close()


# =====================================================
# DELETE - EXCLUIR
# =====================================================

def excluir_usuario():
    email = entry_email.get()

    if not email:
        messagebox.showerror(
            "Erro",
            "Digite o e-mail para excluir."
        )
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE email = ?
    """, (email,))

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo(
            "Sucesso",
            "Usuário excluído com sucesso!"
        )
        limpar_campos()
    else:
        messagebox.showerror(
            "Erro",
            "Usuário não encontrado."
        )

    conn.close()


# =====================================================
# INTERFACE
# =====================================================

janela = ctk.CTk()
janela.title("Sistema CRUD de Usuários")
janela.geometry("500x550")
janela.resizable(False, False)

criar_tabela()

# Título

titulo = ctk.CTkLabel(
    janela,
    text="Cadastro de Usuários",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=20)

# Campo Email

entry_email = ctk.CTkEntry(
    janela,
    placeholder_text="Digite seu e-mail",
    width=350,
    height=40
)
entry_email.pack(pady=10)

# Campo Senha

entry_senha = ctk.CTkEntry(
    janela,
    placeholder_text="Digite sua senha",
    show="*",
    width=350,
    height=40
)
entry_senha.pack(pady=10)

# Confirmar senha

entry_confirmar = ctk.CTkEntry(
    janela,
    placeholder_text="Confirme sua senha",
    show="*",
    width=350,
    height=40
)
entry_confirmar.pack(pady=10)

# Botões

ctk.CTkButton(
    janela,
    text="Cadastrar",
    command=cadastrar_usuario,
    width=250,
    height=40
).pack(pady=8)

ctk.CTkButton(
    janela,
    text="Buscar",
    command=buscar_usuario,
    width=250,
    height=40
).pack(pady=8)

ctk.CTkButton(
    janela,
    text="Atualizar",
    command=atualizar_usuario,
    width=250,
    height=40
).pack(pady=8)

ctk.CTkButton(
    janela,
    text="Excluir",
    command=excluir_usuario,
    width=250,
    height=40
).pack(pady=8)

ctk.CTkButton(
    janela,
    text="Limpar Campos",
    command=limpar_campos,
    width=250,
    height=40
).pack(pady=8)

# Executar sistema

janela.mainloop()