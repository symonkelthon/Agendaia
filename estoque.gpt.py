import streamlit as st

# ==========================
# CONFIGURAÇÃO
# ==========================

st.set_page_config(page_title="Estoque Pro", layout="wide")
st.title("📦 Sistema de Estoque Completo")

# ==========================
# ESTOQUE EM MEMÓRIA
# ==========================

if "estoque" not in st.session_state:
    st.session_state.estoque = []


# ==========================
# CONFIG
# ==========================

ESTOQUE_MINIMO_ALERTA = 5


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
        return "Erro: valores inválidos"

    produto = {
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    }

    st.session_state.estoque.append(produto)

    return "Produto adicionado com sucesso"


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


def entrada_estoque(nome, quantidade):

    produto = buscar_produto(nome)

    if not produto:
        return "Produto não encontrado"

    try:
        quantidade = int(quantidade)
    except ValueError:
        return "Quantidade inválida"

    if quantidade <= 0:
        return "Quantidade deve ser maior que zero"

    produto["quantidade"] += quantidade

    return "Entrada de estoque realizada"


def saida_estoque(nome, quantidade):

    produto = buscar_produto(nome)

    if not produto:
        return "Produto não encontrado"

    try:
        quantidade = int(quantidade)
    except ValueError:
        return "Quantidade inválida"

    if quantidade <= 0:
        return "Quantidade deve ser maior que zero"

    if produto["quantidade"] < quantidade:
        return "Erro: estoque insuficiente"

    produto["quantidade"] -= quantidade

    return "Saída de estoque realizada"


def alerta_estoque_baixo(produto):

    return produto["quantidade"] <= ESTOQUE_MINIMO_ALERTA


# ==========================
# MENU
# ==========================

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Adicionar",
        "Listar",
        "Buscar",
        "Entrada",
        "Saída",
        "Remover"
    ]
)


# ==========================
# ADICIONAR
# ==========================

if menu == "Adicionar":

    st.subheader("➕ Adicionar Produto")

    nome = st.text_input("Nome")
    quantidade = st.text_input("Quantidade inicial")
    preco = st.text_input("Preço")

    if st.button("Salvar"):

        resultado = adicionar_produto(nome, quantidade, preco)
        st.write(resultado)


# ==========================
# LISTAR
# ==========================

elif menu == "Listar":

    st.subheader("📋 Produtos em Estoque")

    if len(st.session_state.estoque) == 0:
        st.info("Nenhum produto cadastrado")
    else:

        for p in st.session_state.estoque:

            alerta = alerta_estoque_baixo(p)

            if alerta:
                st.error(f"⚠ ESTOQUE BAIXO: {p['nome']}")

            st.write(
                f"**{p['nome']}** | "
                f"Qtd: {p['quantidade']} | "
                f"Preço: R$ {p['preco']}"
            )


# ==========================
# BUSCAR
# ==========================

elif menu == "Buscar":

    st.subheader("🔎 Buscar Produto")

    nome = st.text_input("Nome")

    if st.button("Buscar"):

        produto = buscar_produto(nome)

        if produto:
            st.success("Produto encontrado")
            st.write(produto)

            if alerta_estoque_baixo(produto):
                st.warning("⚠ Estoque baixo")
        else:
            st.error("Produto não encontrado")


# ==========================
# ENTRADA
# ==========================

elif menu == "Entrada":

    st.subheader("📥 Entrada de Estoque")

    nome = st.text_input("Produto")
    quantidade = st.text_input("Quantidade para entrada")

    if st.button("Adicionar estoque"):

        resultado = entrada_estoque(nome, quantidade)
        st.write(resultado)


# ==========================
# SAÍDA
# ==========================

elif menu == "Saída":

    st.subheader("📤 Saída de Estoque")

    nome = st.text_input("Produto")
    quantidade = st.text_input("Quantidade para saída")

    if st.button("Remover estoque"):

        resultado = saida_estoque(nome, quantidade)
        st.write(resultado)


# ==========================
# REMOVER
# ==========================

elif menu == "Remover":

    st.subheader("❌ Remover Produto")

    nome = st.text_input("Nome")

    if st.button("Remover"):

        if remover_produto(nome):
            st.success("Produto removido")
        else:
            st.error("Produto não encontrado")
