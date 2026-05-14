import customtkinter as ctk
import requests

# ==========================================
# CONFIGURAÇÃO DA API
# ==========================================

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

# ==========================================
# CONFIGURAÇÕES DA JANELA
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Python Error AI Helper")
app.geometry("850x700")

# ==========================================
# TÍTULO
# ==========================================

titulo = ctk.CTkLabel(
    app,
    text="🐍 Explicador Inteligente de Erros Python",
    font=("Arial", 30, "bold")
)
titulo.pack(pady=20)

# ==========================================
# TEXTO INFORMATIVO
# ==========================================

info = ctk.CTkLabel(
    app,
    text="Cole abaixo o erro do Python ou o traceback completo:",
    font=("Arial", 16)
)
info.pack(pady=5)

# ==========================================
# CAMPO DE ENTRADA
# ==========================================

entrada_erro = ctk.CTkTextbox(
    app,
    width=720,
    height=180,
    font=("Consolas", 14)
)
entrada_erro.pack(pady=10)

# ==========================================
# ÁREA DE RESULTADO
# ==========================================

resultado = ctk.CTkTextbox(
    app,
    width=720,
    height=320,
    font=("Arial", 14)
)
resultado.pack(pady=15)

# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================

def explicar_erro():

    erro = entrada_erro.get("1.0", "end").strip()

    # ===== VERIFICA SE ESTÁ VAZIO =====

    if erro == "":

        resultado.delete("1.0", "end")

        resultado.insert(
            "1.0",
            "⚠️ Digite algum erro primeiro."
        )

        return

    # ===== MENSAGEM DE CARREGAMENTO =====

    resultado.delete("1.0", "end")

    resultado.insert(
        "1.0",
        "⏳ Analisando erro com IA..."
    )

    # ==========================================
    # CABEÇALHOS DA API
    # ==========================================

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # ==========================================
    # PROMPT PARA IA
    # ==========================================

    prompt = f"""
Você é um professor especialista em Python.

Explique o erro abaixo de forma simples e didática para iniciantes.

ERRO:
{erro}

Sua resposta deve conter:

1. Nome do erro
2. O que significa
3. Possíveis causas
4. Como corrigir
5. Exemplo correto
6. Dicas para evitar esse erro

Explique de forma amigável e fácil de entender.
"""

    # ==========================================
    # DADOS ENVIADOS PARA API
    # ==========================================

    data = {
    "model": "llama-3.1-8b-instant",

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.3,

        "max_tokens": 1200
    }

    # ==========================================
    # REQUISIÇÃO DA API
    # ==========================================

    try:

        resposta = requests.post(
            URL,
            headers=headers,
            json=data
        )

        resposta_json = resposta.json()

        # ==========================================
        # PEGA TEXTO DA RESPOSTA
        # ==========================================

        texto = resposta_json["choices"][0]["message"]["content"]

        # ==========================================
        # MOSTRA RESULTADO
        # ==========================================

        resultado.delete("1.0", "end")

        resultado.insert(
            "1.0",
            texto
        )

    # ==========================================
    # TRATAMENTO DE ERRO
    # ==========================================

    except Exception as erro_api:

        resultado.delete("1.0", "end")

        resultado.insert(
            "1.0",
            f"""
❌ Erro ao conectar com a API.

Possíveis causas:
• API KEY inválida
• Sem internet
• API fora do ar
• Biblioteca requests não instalada

Erro técnico:
{erro_api}
"""
        )

# ==========================================
# BOTÃO
# ==========================================

botao = ctk.CTkButton(
    app,
    text="🚀 Explicar Erro com IA",
    command=explicar_erro,
    width=260,
    height=50,
    font=("Arial", 16, "bold")
)

botao.pack(pady=10)

# ==========================================
# BOTÃO LIMPAR
# ==========================================

def limpar():

    entrada_erro.delete("1.0", "end")

    resultado.delete("1.0", "end")

botao_limpar = ctk.CTkButton(
    app,
    text="🗑 Limpar",
    command=limpar,
    width=180,
    height=40,
    fg_color="gray"
)

botao_limpar.pack(pady=5)

# ==========================================
# RODAR APP
# ==========================================

app.mainloop()