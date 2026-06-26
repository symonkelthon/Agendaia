"""
Sistema Master v2.2
Correcoes: SyntaxError MINILANG + Titulo dinamico por modulo.
Dependencias: streamlit, pillow
"""

import streamlit as st
from PIL import Image

# Configuracao
st.set_page_config(page_title="Sistema Master v2.2", layout="wide")

# ==============================
# CAMADA DE ESTADO
# ==============================
def init_state():
    """Inicializa o estado da aplicacao."""
    defaults = {
        "agenda_db": {}, # {str: {"tel": str, "foto": bytes}}
        "estoque_db": {}, # {str: int}
        "minilang_vars": {}, # {str: int}
        "minilang_prog": [] # [str]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ==============================
# CAMADA BACK-END
# ==============================
# --- Modulo Agenda ---
def agenda_add(nome: str, tel: str, foto_bytes: bytes | None) -> str:
    if not nome or not tel:
        return "Erro: Nome e Telefone sao obrigatorios."
    st.session_state.agenda_db[nome] = {"tel": tel, "foto": foto_bytes}
    return f"Contato '{nome}' salvo."

def agenda_remove(nome: str) -> str:
    if nome in st.session_state.agenda_db:
        del st.session_state.agenda_db[nome]
        return f"Contato '{nome}' removido."
    return f"Erro: Contato '{nome}' nao encontrado."

def agenda_list() -> dict:
    return st.session_state.agenda_db

# --- Modulo Estoque ---
def estoque_cadastra(prod: str, qtd: int) -> str:
    if not prod:
        return "Erro: Nome do produto e obrigatorio."
    st.session_state.estoque_db = qtd
    return f"Produto '{prod}' cadastrado."

def estoque_entrada(prod: str, qtd: int) -> str:
    if prod not in st.session_state.estoque_db:
        return f"Erro: '{prod}' nao existe."
    st.session_state.estoque_db += qtd
    return