"""
Sistema Master v2.1
Adicionado: Upload de foto no modulo Agenda.

Alteracao de schema: agenda_db: {nome: {"tel": str, "foto": bytes | None}}
"""

import streamlit as st
from PIL import Image
import io

# Configuracao
st.set_page_config(page_title="Sistema Master", layout="wide")

# ==============================
# CAMADA DE ESTADO
# ==============================
def init_state():
    """Inicializa o estado da aplicacao."""
    defaults = {
        "agenda_db": {}, # {str: {"tel": str, "foto": bytes}}
        "estoque_db": {},
        "minilang_vars": {},
        "minilang_prog": []
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
    """Adiciona ou atualiza um contato com foto opcional."""
    if not nome or not tel:
        return "Erro: Nome e Telefone sao obrigatorios."
    st.session_state.agenda_db[nome] = {"tel": tel, "foto": foto_bytes}
    return f"Contato '{nome}' salvo."

def agenda_remove(nome: str) -> str:
    """Remove um contato."""
    if nome in st.session_state.agenda_db:
        del st.session_state.agenda_db[nome]
        return f"Contato '{nome}' removido."
    return f"Erro: Contato '{nome}' nao encontrado."

def agenda_list() -> dict:
    """Retorna o dicionario de contatos."""
    return st.session_state.agenda_db

# --- Modulo Estoque ---
def estoque_cadastra(prod: str, qtd: int) -> str:
    if not prod: return "Erro: Nome do produto e obrigatorio."
    st.session_state.estoque_db = qtd
    return f"Produto '{prod}' cadastrado."

def estoque_entrada(prod: str, qtd: int) -> str:
    if prod not in st.session_state.estoque_db: return f"Erro: '{prod}' nao existe."
    st.session_state.estoque_db += qtd
    return f"Entrada OK. '{prod}': {st.session_state.estoque_db} un"

def estoque_saida(prod: str, qtd: int) -> str:
    if prod not in st.session_state.estoque_db: return f"Erro: '{prod}' nao existe."
    if st.session_state.estoque_db < qtd: return f"Erro: Saldo insuficiente."
    st.session_state.estoque_db -= qtd
    return f"Saida OK. '{prod}': {st.session_state.estoque_db} un"

def estoque_relatorio() -> dict:
    return st.session_state.estoque_db

# --- Modulo MINILANG ---
def minilang_add(linha: str) -> None:
    if linha.strip(): st.session_state.minilang_prog.append(linha.strip())

def minilang_run() -> str:
    output = []
    for linha in st.session_state.minilang_prog:
        partes = linha.split()
        if not partes: continue
        cmd = partes[0].upper()
        try:
            if cmd == "GUARDA" and len(partes) == 3:
                st.session_state.minilang_vars[partes[1]] = int(partes[2])
                output.append(f"{partes[1]} = {partes[2]}")
            elif cmd == "SOMA" and len(partes) == 3:
                var = partes[1]
                if var in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[var] += int(partes[2])
                    output.append(f"{var} = {st.session_state.minilang_vars[var]}")
            elif cmd == "TIRA" and len(partes) == 3:
                var = partes[1]
                if var in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[var] -= int(partes[2])
                    output.append(f"{var} = {st.session_state.minilang_vars[var]}")
            elif cmd == "VE" and len(partes) == 2:
                val = st.session_state.minilang_vars.get(partes[1], "VAR_INEXISTENTE")
                output.append(f"{partes[1]} = {val}")
            elif cmd == "APAGA" and len(partes) == 2:
                st.session_state.minilang_vars.pop(partes[1], None)
                output.append(f"Variavel '{partes[1]}' removida.")
        except (ValueError, IndexError):
            output.append(f"Erro de sintaxe em: '{linha}'")
    st.session_state.minilang_prog.clear()
    return "\n".join(output