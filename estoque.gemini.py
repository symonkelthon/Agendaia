import streamlit as st
import json
import os

ARQUIVO = "estoque.json"

# ========= FUNÇÕES =========
def carregar_estoque():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_estoque(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Controle de Estoque", layout="centered")
st.title("📦 CONTROLE DE ESTOQUE")

estoque = carregar_estoque()

tab1, tab2, tab3, tab4 = st.tabs(["1. Adicionar", "2. Listar", "3. Buscar", "4. Remover"])

# 1. Adicionar Produto
with tab1:
    st.subheader("Adicionar Produto")
    with st.form("form_add", clear_on_submit=True):
        nome = st.text_input("Nome do produto: ").strip()
        qtd_input = st.text_input("Quantidade: ").strip()
        preco_input = st.text_input("Preço R$ use ponto: ").strip()

        if st.form_submit_button("Cadastrar"):
            if not nome:
                st.error("Erro: O nome do produto não pode ser vazio!")
            elif not qtd_input or not preco_input:
                st.error("Erro: Quantidade e Preço não podem ser vazios!")
            else:
                try:
                    quantidade = int(qtd_input)
                    preco = float(preco_input)
                    estoque[nome] = {"quantidade": quantidade, "preco": preco}
                    salvar_estoque(estoque)
                    st.success(f"Produto '{nome}' adicionado com sucesso!")
                    st.rerun()
                except ValueError:
                    st.error("Erro: Quantidade precisa ser inteiro e Preço número!")

# 2. Listar Produtos
with tab2:
    st.subheader("Lista de Produtos no Estoque")
    if not estoque:
        st.info("O estoque está completamente vazio.")
    else:
        for nome, dados in estoque.items():
            with st.container(border=True):
                st.write(f"**Produto:** {nome}")
                st.write(f"**Quantidade:** {dados['quantidade']}")
                st.write(f"**Preço:** R$ {dados['preco']:.2f}")

# 3. Buscar Produto
with tab3:
    st.subheader("Buscar Produto")
    nome_busca = st.text_input("Digite o nome do produto: ").strip()
    if st.button("Buscar"):
        if nome_busca in estoque:
            dados = estoque[nome_busca]
            st.success("Produto Encontrado:")
            st.write(f"**Nome:** {nome_busca}")
            st.write(f"**Quantidade:** {dados['quantidade']}")
            st.write(f"**Preço:** R$ {dados['preco']:.2f}")
        else:
            st.warning("Produto não encontrado.")

# 4. Remover Produto
with tab4:
    st.subheader("Remover Produto")
    nome_remover = st.text_input("Digite o nome do produto para remover: ").strip()
    if st.button("Remover"):
        if nome_remover in estoque:
            del estoque[nome_remover]
            salvar_estoque(estoque)
            st.success(f"Produto '{nome_remover}' removido com sucesso!")
            st.rerun()
        else:
            st.warning("Produto não encontrado.")