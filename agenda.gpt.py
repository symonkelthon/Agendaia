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

st.title("📒 Agenda de Contatos")

contatos = carregar_contatos()

aba1, aba2, aba3, aba4 = st.tabs(["Adicionar", "Listar", "Buscar", "Remover"])

with aba1:
    st.subheader("Adicionar Contato")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")
    foto = st.text_input("Caminho da foto")
    if st.button("Salvar Contato"):
        if nome == "":
            st.error("Nome não pode ser Vazio")
        else:
            contatos.append({"nome": nome, "telefone": telefone, "foto": foto})
            salvar_contatos(contatos)
            st.success("Contato adicionado com sucesso!")

with aba2:
    st.subheader("Lista de Contatos")
    if not contatos:
        st.info("Nenhum contato cadastrado.")
    for i, c in enumerate(contatos, start=1):
        st.write(f"**Contato {i}**")
        st.write(f"Nome: {c['nome']}")
        st.write(f"Telefone: {c['telefone']}")
        st.write(f"Foto: {c['foto']}")

with aba3:
    st.subheader("Buscar Contato")
    termo = st.text_input("Digite o nome para buscar")
    if st.button("Buscar"):
        encontrados = [c for c in contatos if termo.lower() in c["nome"].lower()]
        if not encontrados:
            st.warning("Nenhum contato encontrado.")
        for c in encontrados:
            st.write(f"Nome: {c['nome']} | Tel: {c['telefone']}")

with aba4:
    st.subheader("Remover Contato")
    nome_remover = st.text_input("Digite o nome do contato para remover")
    if st.button("Remover"):
        contatos = [c for c in contatos if c["nome"].lower() != nome_remover.lower()]
        salvar_contatos(contatos)
        st.success("Contato removido se existia.")