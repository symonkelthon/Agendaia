import streamlit as st
import json
import os

ARQUIVO = "contatos.json"

def carregar_contatos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []

def salvar_contatos(contatos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(contatos, arquivo, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Agenda de Contatos", layout="centered")
st.title("📒 AGENDA DE CONTATOS")

contatos = carregar_contatos()

tab1, tab2, tab3, tab4 = st.tabs(["1. Adicionar", "2. Remover", "3. Listar", "4. Buscar"])

# 1 - Adicionar contato
with tab1:
    st.subheader("Adicionar Contato")
    with st.form("form_add", clear_on_submit=True):
        nome = st.text_input("Nome: ")
        telefone = st.text_input("Telefone: ")
        foto = st.text_input("Caminho da foto: ")

        if st.form_submit_button("Salvar Contato"):
            if nome.strip() == "":
                st.error("Erro: Nome não pode ser Vazio!")
            else:
                contato = {"nome": nome.strip(), "telefone": telefone.strip(), "foto": foto.strip()}
                contatos.append(contato)
                salvar_contatos(contatos)
                st.success("Contato adicionado com sucesso!")

# 2 - Remover contato
with tab2:
    st.subheader("Remover Contato")
    nome_remover = st.text_input("Digite o nome do contato para remover: ").strip().lower()
    if st.button("Remover"):
        antes = len(contatos)
        contatos = [c for c in contatos if c["nome"].lower() != nome_remover]
        if len(contatos) < antes:
            salvar_contatos(contatos)
            st.success("Contato removido com sucesso!")
            st.rerun()
        else:
            st.warning("Contato não encontrado.")

# 3 - Listar contatos
with tab3:
    st.subheader("Lista de Contatos")
    if not contatos:
        st.info("Nenhum contato cadastrado.")
    else:
        for indice, contato in enumerate(contatos, start=1):
            with st.container(border=True):
                st.write(f"**Contato {indice}**")
                st.write(f"**Nome:** {contato['nome']}")
                st.write(f"**Telefone:** {contato['telefone']}")
                st.write(f"**Foto:** {contato['foto']}")

# 4 - Buscar contato
with tab4:
    st.subheader("Buscar Contato")
    termo = st.text_input("Digite o nome para buscar: ").strip().lower()
    if st.button("Buscar"):
        encontrados = [c for c in contatos if termo in c["nome"].lower()]
        if not encontrados:
            st.warning("Nenhum contato encontrado.")
        else:
            st.success(f"{len(encontrados)} resultado(s) encontrado(s)")
            for contato in encontrados:
                st.write(f"**Nome:** {contato['nome']} | **Telefone:** {contato['telefone']} | **Foto:** {contato['foto']}")