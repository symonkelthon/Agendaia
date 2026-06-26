import streamlit as st
import json
import os

ARQUIVO = "estoque_meta.json"

def carregar():
    return json.load(open(ARQUIVO, "r", encoding="utf-8")) if os.path.exists(ARQUIVO) else []

def salvar(dados):
    json.dump(dados, open(ARQUIVO, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

st.title("📦 Estoque Meta AI")

produtos = carregar()
aba1, aba2, aba3 = st.tabs(["Adicionar", "Listar/Buscar", "Remover"])

with aba1:
    with st.form("add_prod", clear_on_submit=True):
        nome = st.text_input("Nome do produto")
        qtd = st.number_input("Quantidade", 0, step=1)
        preco = st.number_input("Preço R$", 0.0, step=0.01, format="%.2f")
        if st.form_submit_button("Cadastrar"):
            if nome:
                produtos.append({"nome": nome, "quantidade": qtd, "preco": preco})
                salvar(produtos)
                st.success("Produto cadastrado!")
                st.rerun()

with aba2:
    termo = st.text_input("Buscar produto exato")
    lista = [p for p in produtos if p["nome"].lower()== termo.lower()] if termo else produtos
    st.dataframe(lista, use_container_width=True)

with aba3:
    nome_rem = st.text_input("Nome exato para remover")
    if st.button("Remover"):
        produtos = [p for p in produtos if p["nome"]!= nome_rem]
        salvar(produtos)
        st.success("Removido!")
        st.rerun()