import streamlit as st
import json
import os
from PIL import Image

ARQUIVO = "agenda.json"
PASTA_FOTOS = "fotos"

os.makedirs(PASTA_FOTOS, exist_ok=True)

st.set_page_config(page_title="Agenda de Contatos", layout="centered")

# 1. Funções de Persistência
def carregar_contatos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_contatos(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# 2. Estado inicial
if "contatos" not in st.session_state:
    st.session_state.contatos = carregar_contatos()

st.title("Agenda de Contatos SK")

tab1, tab2, tab3, tab4 = st.tabs(["Adicionar", "Listar", "Buscar", "Remover"])

# TAB 1: Adicionar contato - SEM EMAIL
with tab1:
    st.subheader("Adicionar Novo Contato")
    nome = st.text_input("Nome", key="add_nome")
    telefone = st.text_input("Telefone", key="add_tel")
    foto = st.file_uploader("Foto do Contato", type=["png", "jpg", "jpeg"])

    if st.button("Salvar Contato"):
        if not nome or not telefone:
            st.error("Erro: Nome e telefone são obrigatórios.")
        elif nome in st.session_state.contatos:
            st.error("Erro: Contato já existe.")
        else:
            caminho_foto = ""
            if foto:
                caminho_foto = os.path.join(PASTA_FOTOS, f"{nome}.png")
                Image.open(foto).save(caminho_foto)

            st.session_state.contatos[nome] = {"telefone": telefone, "foto": caminho_foto}
            salvar_contatos(st.session_state.contatos)
            st.success(f"Contato {nome} adicionado!")
            st.rerun()

# TAB 2: Listar contatos
with tab2:
    st.subheader("Lista de Contatos")
    if st.session_state.contatos:
        for nome, dados in st.session_state.contatos.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                if dados["foto"] and os.path.exists(dados["foto"]):
                    st.image(dados["foto"], width=80)
            with col2:
                st.write(f"**{nome}**")
                st.write(f"Tel: {dados['telefone']}")
            st.divider()
    else:
        st.info("Agenda vazia.")

# TAB 3: Buscar contato
with tab3:
    st.subheader("Buscar Contato")
    busca = st.text_input("Digite o nome", key="busca")
    if busca:
        if busca in st.session_state.contatos:
            d = st.session_state.contatos[busca]
            st.success(f"**{busca}**")
            st.write(f"Telefone: {d['telefone']}")
            if d["foto"] and os.path.exists(d["foto"]):
                st.image(d["foto"], width=150)
        else:
            st.warning("Contato não encontrado")

# TAB 4: Remover contato
with tab4:
    st.subheader("Remover Contato")
    if st.session_state.contatos:
        remover = st.selectbox("Selecione o contato", options=list(st.session_state.contatos.keys()))
        if st.button("Remover"):
            if remover in st.session_state.contatos:
                # Apaga a foto do disco se existir
                foto_path = st.session_state.contatos[remover]["foto"]
                if foto_path and os.path.exists(foto_path):
                    os.remove(foto_path)
                del st.session_state.contatos[remover]
                salvar_contatos(st.session_state.contatos)
                st.success(f"Contato {remover} removido.")
                st.rerun()
            else:
                st.warning("Contato não encontrado")
    else:
        st.info("Agenda vazia.")