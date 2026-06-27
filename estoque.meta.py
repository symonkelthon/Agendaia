import streamlit as st
import json
import os

ARQUIVO = "estoque.json"
LIMITE_BAIXO = 5 # Alerta se quantidade < 5

st.set_page_config(page_title="Sistema de Estoque", layout="centered")

# 1. Funções de Persistência
def carregar_estoque():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_estoque(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# 2. Estado inicial
if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_estoque()

st.title("Sistema de Estoque SK")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Adicionar", "Listar", "Buscar", "Entrada/Saída", "Remover", "Alertas"])

# TAB 1: Adicionar produto
with tab1:
    st.subheader("Adicionar Novo Produto")
    nome = st.text_input("Nome do Produto", key="add_nome")
    qtd = st.text_input("Quantidade", key="add_qtd")
    preco = st.text_input("Preço R$", key="add_preco")

    if st.button("Salvar Produto"):
        if not nome or qtd == "" or preco == "":
            st.error("Erro: Nome, quantidade e preço são obrigatórios.")
        else:
            try:
                qtd_int = int(qtd)
                preco_float = float(preco)
                if nome in st.session_state.estoque:
                    st.error("Produto já existe. Use Entrada/Saída para atualizar.")
                else:
                    st.session_state.estoque[nome] = {"qtd": qtd_int, "preco": preco_float}
                    salvar_estoque(st.session_state.estoque)
                    st.success(f"Produto {nome} adicionado!")
                    st.rerun()
            except ValueError:
                st.error("Erro: Quantidade deve ser inteiro e Preço deve ser número.")

# TAB 2: Listar produtos
with tab2:
    st.subheader("Lista de Produtos")
    if st.session_state.estoque:
        for nome, dados in st.session_state.estoque.items():
            st.write(f"**{nome}** | Qtd: {dados['qtd']} | Preço: R$ {dados['preco']:.2f}")
    else:
        st.info("Estoque vazio.")

# TAB 3: Buscar produto
with tab3:
    st.subheader("Buscar Produto")
    busca = st.text_input("Digite o nome do produto", key="busca")
    if busca:
        if busca in st.session_state.estoque:
            d = st.session_state.estoque[busca]
            st.success(f"**{busca}** | Qtd: {d['qtd']} | Preço: R$ {d['preco']:.2f}")
        else:
            st.warning("Produto não encontrado")

# TAB 4: Entrada e Saída de estoque = Atualização de quantidade [CORRIGIDO]
with tab4:
    st.subheader("Entrada / Saída de Estoque")
    if st.session_state.estoque:
        produto = st.selectbox("Selecione o produto", options=list(st.session_state.estoque.keys()))
        tipo = st.radio("Tipo de Movimentação", ["Entrada", "Saída"], horizontal=True)
        valor = st.text_input("Quantidade para mover", key="mov_qtd")

        if st.button("Aplicar Movimentação"):
            if valor == "":
                st.error("Erro: Quantidade é obrigatória.")
            else:
                try:
                    qtd_mov = int(valor)
                    if qtd_mov <= 0:
                        st.error("Erro: Use um valor maior que zero.")
                    else:
                        if tipo == "Entrada":
                            st.session_state.estoque[produto]["qtd"] += qtd_mov
                        else: # Saída
                            if st.session_state.estoque[produto]["qtd"] < qtd_mov:
                                st.error("Erro: Estoque insuficiente para saída.")
                            else:
                                st.session_state.estoque[produto]["qtd"] -= qtd_mov
                        salvar_estoque(st.session_state.estoque)
                        st.success("Movimentação aplicada!")
                        st.rerun()
                except ValueError:
                    st.error("Erro: Digite apenas números inteiros.")
    else:
        st.info("Cadastre um produto primeiro.")

# TAB 5: Remover produto
with tab5:
    st.subheader("Remover Produto")
    if st.session_state.estoque:
        remover = st.selectbox("Selecione o produto para remover", options=list(st.session_state.estoque.keys()))
        if st.button("Remover"):
            if remover in st.session_state.estoque:
                del st.session_state.estoque[remover]
                salvar_estoque(st.session_state.estoque)
                st.success(f"Produto {remover} removido.")
                st.rerun()
            else:
                st.warning("Produto não encontrado")
    else:
        st.info("Estoque vazio.")

# TAB 6: Alerta de Estoque Baixo
with tab6:
    st.subheader(f"Alertas: Estoque < {LIMITE_BAIXO}")
    baixos = {n:d for n,d in st.session_state.estoque.items() if d['qtd'] < LIMITE_BAIXO}
    if baixos:
        for nome, dados in baixos.items():
            st.error(f"ATENÇÃO: {nome} com apenas {dados['qtd']} unidades")
    else:
        st.success("Nenhum produto com estoque baixo.")