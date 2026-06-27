import streamlit as st

# ==========================
# CONFIGURAÇÃO
# ==========================

st.set_page_config(page_title="Sistema de Estoque", layout="wide")
st.title("📦 Sistema de Estoque")

# Inicializa estoque na sessão
if "estoque" not in st.session_state:
    st.session_state.estoque = []


# ==========================
# FUNÇÕES
# ==========================

def adicionar_produto(nome, quantidade, preco):

    if nome.strip() == "":
        return "Erro: nome vazio"

    if quantidade == "" or preco == "":
        return "Erro: quantidade ou preço vazio"

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        return "Erro: quantidade ou preço inválido"

    produto = {
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    }

    st.session_state.estoque.append(produto)

    return "Produto adicionado com sucesso"


def listar_produtos():

    return st.session_state.estoque


def buscar_produto(nome):

    for produto in st.session_state.estoque:
        if produto["nome"].lower() == nome.lower():
            return produto

    return None


def remover_produto(nome):

    for produto in st.session_state.estoque:
        if produto["nome"].lower() == nome.lower():
            st.session_state.estoque.remove(produto)
            return True

    return False


# ==========================
# MENU
# ==========================

menu = st.sidebar.selectbox(
    "Menu",
    ["Adicionar", "Listar", "Buscar", "Remover", "Sair"]
)

# ==========================
# ADICIONAR
# ==========================

if menu == "Adicionar":

    st.subheader("➕ Adicionar Produto")

    nome = st.text_input("Nome do produto")
    quantidade = st.text_input("Quantidade")
    preco = st.text_input("Preço")

    if st.button("Salvar"):

        resultado = adicionar_produto(nome, quantidade, preco)
        st.write(resultado)

# ==========================
# LISTAR
# ==========================

elif menu == "Listar":

    st.subheader("📋 Lista de Produtos")

    produtos = listar_produtos()

    if len(produtos) == 0:
        st.info("Nenhum produto cadastrado")
    else:
        for i, p in enumerate(produtos, start=1):
            st.write(f"{i}. {p['nome']} | Qtd: {p['quantidade']} | Preço: R$ {p['preco']}")


# ==========================
# BUSCAR
# ==========================

elif menu == "Buscar":

    st.subheader("🔎 Buscar Produto")

    nome = st.text_input("Digite o nome")

    if st.button("Buscar"):

        resultado = buscar_produto(nome)

        if resultado:
            st.success("Produto encontrado")
            st.write(resultado)
        else:
            st.error("Produto não encontrado")


# ==========================
# REMOVER
# ==========================

elif menu == "Remover":

    st.subheader("❌ Remover Produto")

    nome = st.text_input("Digite o nome do produto")

    if st.button("Remover"):

        resultado = remover_produto(nome)

        if resultado:
            st.success("Produto removido com sucesso")
        else:
            st.error("Produto não encontrado")


# ==========================
# SAIR
# ==========================

elif menu == "Sair":
    st.warning("Feche a aba do navegador para sair")
