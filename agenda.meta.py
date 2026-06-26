import streamlit as st
import json
import os

ARQUIVO = "contatos_meta.json"

def carregar():
    return json.load(open(ARQUIVO, "r", encoding="utf-8")) if os.path.exists(ARQUIVO) else []

def salvar(dados):
    json.dump(dados, open(ARQUIVO, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

st.title("📒 Agenda Meta AI")

contatos = carregar()
aba1, aba2, aba3 = st.tabs(["Adicionar", "Listar/Buscar", "Remover"])

with aba1:
    with st.form("add", clear_on_submit=True):
        nome = st.text_input("Nome")
        tel = st.text_input("Telefone")
        foto = st.text_input("URL da Foto")
        if st.form_submit_button("Salvar"):
            if nome:
                contatos.append({"nome": nome, "telefone": tel, "foto": foto})
                salvar(contatos)
                st.success("Contato adicionado!")
                st.rerun()
            else: st.error("Nome não pode ser vazio")

with aba2:
    termo = st.text_input("Buscar por nome")
    lista = [c for c in contatos if termo.lower() in c["nome"].lower()] if termo else contatos
    st.dataframe(lista, use_container_width=True)

with aba3:
    nome_rem = st.text_input("Nome exato para remover")
    if st.button("Remover"):
        contatos = [c for c in contatos if c["nome"]!= nome_rem]
        salvar(contatos)
        st.success("Removido!")
        st.rerun()