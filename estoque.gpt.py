import streamlit as st

if 'produtos' not in st.session_state:
    st.session_state.produtos = []

st.title("📦 Sistema de Estoque")

aba1, aba2, aba3, aba4 = st.tabs(["Adicionar", "Listar", "Buscar", "Remover"])

with aba1:
    st.subheader("Adicionar Produto")
    nome = st.text_input("Nome do produto", key="nome_prod")
    quantidade = st.number_input("Quantidade", min_value=0, step=1, key="qtd_prod")
    preco = st.number_input("Preço R$", min_value=0.0, step=0.01, format="%.2f", key="preco_prod")

    if st.button("Cadastrar Produto"):
        if nome == "":
            st.error("Erro: nome não pode ser vazio.")
        else:
            st.session_state.produtos.append({"nome": nome, "quantidade": quantidade, "preco": preco})
            st.success("Produto cadastrado com sucesso!")

with aba2:
    st.subheader("Lista de Produtos")
    if not st.session_state.produtos:
        st.info("Nenhum produto cadastrado.")
    else:
        for p in st.session_state.produtos:
            st.write("--------------------")
            st.write(f"**Nome:** {p['nome']}")
            st.write(f"**Quantidade:** {p['quantidade']}")
            st.write(f"**Preço:** R$ {p['preco']:.2f}")

with aba3:
    st.subheader("Buscar Produto")
    nome_busca = st.text_input("Digite o nome do produto", key="busca_prod")
    if st.button("Buscar"):
        encontrado = [p for p in st.session_state.produtos if p["nome"].lower() == nome_busca.lower()]
        if encontrado:
            p = encontrado[0]
            st.success("Produto encontrado")
            st.write(f"**Nome:** {p['nome']}")
            st.write(f"**Quantidade:** {p['quantidade']}")
            st.write(f"**Preço:** R$ {p['preco']:.2f}")
        else:
            st.warning("Produto não encontrado")

with aba4:
    st.subheader("Remover Produto")
    nome_remover = st.text_input("Digite o nome do produto", key="remove_prod")
    if st.button("Remover"):
        antes = len(st.session_state.produtos)
        st.session_state.produtos = [p for p in st.session_state.produtos if p["nome"].lower()!= nome_remover.lower()]
        if len(st.session_state.produtos) < antes:
            st.success("Produto removido com sucesso!")
        else:
            st.warning("Produto não encontrado")