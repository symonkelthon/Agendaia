"""
Agenda de Contatos - Streamlit
Requisitos: pip install streamlit pillow
"""

import streamlit as st
import json
import os
from PIL import Image
import io
import base64

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agenda de Contatos",
    page_icon="📒",
    layout="centered"
)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ARQUIVO_AGENDA = "contatos.json"

# ─────────────────────────────────────────────
# FUNÇÕES DE PERSISTÊNCIA (salvar/carregar JSON)
# ─────────────────────────────────────────────

def carregar_contatos() -> dict:
    """Lê o arquivo JSON e retorna o dicionário de contatos.
    Se o arquivo não existir, retorna dicionário vazio."""
    if not os.path.exists(ARQUIVO_AGENDA):
        return {}
    with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_contatos(contatos: dict) -> None:
    """Grava o dicionário de contatos no arquivo JSON."""
    with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as f:
        json.dump(contatos, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────────
# FUNÇÕES DE NEGÓCIO
# ─────────────────────────────────────────────

def adicionar_contato(contatos: dict, nome: str, telefone: str,
                      email: str, foto_base64: str) -> tuple[bool, str]:
    """Adiciona um novo contato. Retorna (sucesso, mensagem)."""
    nome = nome.strip()
    if not nome:
        return False, "O nome não pode estar vazio."
    if nome.lower() in [k.lower() for k in contatos]:
        return False, f"Já existe um contato com o nome '{nome}'."
    contatos[nome] = {
        "telefone": telefone.strip(),
        "foto": foto_base64
    }
    salvar_contatos(contatos)
    return True, f"Contato '{nome}' adicionado com sucesso!"


def remover_contato(contatos: dict, nome: str) -> tuple[bool, str]:
    """Remove um contato pelo nome. Retorna (sucesso, mensagem)."""
    for chave in list(contatos.keys()):
        if chave.lower() == nome.lower():
            del contatos[chave]
            salvar_contatos(contatos)
            return True, f"Contato '{chave}' removido com sucesso!"
    return False, f"Contato '{nome}' não encontrado."


def buscar_contatos(contatos: dict, termo: str) -> dict:
    """Busca contatos cujo nome contenha o termo (sem distinção de maiúsculas).
    Retorna um dicionário com os resultados."""
    termo = termo.strip().lower()
    if not termo:
        return {}
    return {
        nome: dados
        for nome, dados in contatos.items()
        if termo in nome.lower()
        or termo in dados.get("telefone", "").lower()
   
    }


def imagem_para_base64(arquivo_upload) -> str:
    """Converte o arquivo de imagem enviado pelo Streamlit em string base64."""
    imagem = Image.open(arquivo_upload)
    imagem = imagem.convert("RGB")
    imagem.thumbnail((200, 200))          # redimensiona para economizar espaço
    buffer = io.BytesIO()
    imagem.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def exibir_foto(foto_base64: str, largura: int = 80) -> None:
    """Renderiza a foto do contato a partir de uma string base64."""
    if foto_base64:
        html = (
            f'<img src="data:image/jpeg;base64,{foto_base64}" '
            f'width="{largura}" style="border-radius:50%; '
            f'border:2px solid #ccc;" />'
        )
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown("🧑 *(sem foto)*")


def exibir_cartao(nome: str, dados: dict) -> None:
    """Exibe um cartão visual para um único contato."""
    with st.container(border=True):
        col_foto, col_info = st.columns([1, 3])
        with col_foto:
            exibir_foto(dados.get("foto", ""))
        with col_info:
            st.markdown(f"### {nome}")
            st.markdown(f"📞 **Telefone:** {dados.get('telefone') or '—'}")
           


# ─────────────────────────────────────────────
# INICIALIZAÇÃO DO SESSION STATE
# ─────────────────────────────────────────────

if "contatos" not in st.session_state:
    st.session_state.contatos = carregar_contatos()

# ─────────────────────────────────────────────
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────────

st.title("📒 Agenda de Contatos")
st.caption("Adicione, busque, liste e remova contatos com foto.")

aba_adicionar, aba_listar, aba_buscar, aba_remover = st.tabs([
    "➕ Adicionar", "📋 Listar", "🔍 Buscar", "🗑️ Remover"
])

# ══════════════════════════════════════════════
# ABA 1 — ADICIONAR CONTATO
# ══════════════════════════════════════════════
with aba_adicionar:
    st.subheader("Adicionar novo contato")

    with st.form("form_adicionar", clear_on_submit=True):
        nome_input    = st.text_input("Nome *", placeholder="Ex: João Silva")
        telefone_input = st.text_input("Telefone", placeholder="Ex: (11) 91234-5678")
        foto_input    = st.file_uploader(
            "Foto (opcional)", type=["jpg", "jpeg", "png", "webp"]
        )
        enviado = st.form_submit_button("Salvar contato")

    if enviado:
        foto_b64 = imagem_para_base64(foto_input) if foto_input else ""
        ok, msg = adicionar_contato(
            st.session_state.contatos, nome_input, telefone_input,  foto_b64
        )
        if ok:
            st.success(msg)
        else:
            st.error(msg)

# ══════════════════════════════════════════════
# ABA 2 — LISTAR CONTATOS
# ══════════════════════════════════════════════
with aba_listar:
    st.subheader("Todos os contatos")

    contatos = st.session_state.contatos

    if not contatos:
        st.info("Nenhum contato cadastrado ainda.")
    else:
        st.caption(f"Total: **{len(contatos)}** contato(s)")
        for nome, dados in sorted(contatos.items()):
            exibir_cartao(nome, dados)

# ══════════════════════════════════════════════
# ABA 3 — BUSCAR CONTATO
# ══════════════════════════════════════════════
with aba_buscar:
    st.subheader("Buscar contato")

    termo = st.text_input("Digite nome, telefone ", placeholder="Ex: João")

    if termo:
        resultados = buscar_contatos(st.session_state.contatos, termo)
        if resultados:
            st.caption(f"**{len(resultados)}** resultado(s) encontrado(s):")
            for nome, dados in resultados.items():
                exibir_cartao(nome, dados)
        else:
            st.warning("Nenhum contato encontrado para esse termo.")

# ══════════════════════════════════════════════
# ABA 4 — REMOVER CONTATO
# ══════════════════════════════════════════════
with aba_remover:
    st.subheader("Remover contato")

    contatos = st.session_state.contatos

    if not contatos:
        st.info("Nenhum contato cadastrado para remover.")
    else:
        nomes_disponiveis = sorted(contatos.keys())
        nome_remover = st.selectbox(
            "Selecione o contato a remover", options=nomes_disponiveis
        )

        if nome_remover:
            exibir_cartao(nome_remover, contatos[nome_remover])

        confirmar = st.button("🗑️ Confirmar remoção", type="primary")

        if confirmar and nome_remover:
            ok, msg = remover_contato(st.session_state.contatos, nome_remover)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
