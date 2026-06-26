"""
Sistema Master v2.3
Sistema multi-modulo: Agenda com Foto, Estoque e MINILANG.

Correcoes v2.3:
1. Import seguro de Pillow com st.stop() se ausente.
2. Renderizacao de imagem via io.BytesIO para compatibilidade Cloud.
3. Titulo dinamico por modulo.
"""

import streamlit as st
import io

# Import seguro: evita tela preta se Pillow nao estiver instalado
try:
    from PIL import Image
except ImportError:
    st.error("Dependencia 'pillow' nao instalada. Crie o arquivo requirements.txt com: streamlit\npillow")
    st.stop()

st.set_page_config(page_title="Sistema Master v2.3", layout="wide")

# ==============================
# CAMADA DE ESTADO
# ==============================
def init_state():
    """Inicializa todos os bancos de dados em memoria."""
    defaults = {
        "agenda_db": {}, # {str: {"tel": str, "foto": bytes | None}}
        "estoque_db": {}, # {str: int}
        "minilang_vars": {}, # {str: int}
        "minilang_prog": [] # [str]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ==============================
# CAMADA BACK-END: REGRAS DE NEGOCIO
# ==============================

# --- Modulo Agenda ---
def agenda_add(nome: str, tel: str, foto_bytes: bytes | None) -> str:
    """Adiciona ou atualiza contato. Foto e opcional."""
    if not nome or not tel:
        return "Erro: Nome e Telefone sao obrigatorios."
    st.session_state.agenda_db[nome] = {"tel": tel, "foto": foto_bytes}
    return f"Contato '{nome}' salvo."

def agenda_remove(nome: str) -> str:
    """Remove contato pelo nome."""
    if nome in st.session_state.agenda_db:
        del st.session_state.agenda_db[nome]
        return f"Contato '{nome}' removido."
    return f"Erro: Contato '{nome}' nao encontrado."

def agenda_list() -> dict:
    """Retorna dicionario completo da agenda."""
    return st.session_state.agenda_db

# --- Modulo Estoque ---
def estoque_cadastra(prod: str, qtd: int) -> str:
    """Cadastra produto com quantidade inicial."""
    if not prod:
        return "Erro: Nome do produto e obrigatorio."
    st.session_state.estoque_db = qtd
    return f"Produto '{prod}' cadastrado com {qtd} un."

def estoque_entrada(prod: str, qtd: int) -> str:
    """Adiciona quantidade ao estoque existente."""
    if prod not in st.session_state.estoque_db:
        return f"Erro: Produto '{prod}' nao existe."
    st.session_state.estoque_db += qtd
    return f"Entrada OK. '{prod}': {st.session_state.estoque_db} un"

def estoque_saida(prod: str, qtd: int) -> str:
    """Remove quantidade se houver saldo."""
    if prod not in st.session_state.estoque_db:
        return f"Erro: Produto '{prod}' nao existe."
    if st.session_state.estoque_db < qtd:
        return f"Erro: Saldo insuficiente. Disponivel: {st.session_state.estoque_db}"
    st.session_state.estoque_db -= qtd
    return f"Saida OK. '{prod}': {st.session_state.estoque_db} un"

def estoque_relatorio() -> dict:
    """Retorna dicionario completo do estoque."""
    return st.session_state.estoque_db

# --- Modulo MINILANG ---
def minilang_add(linha: str) -> None:
    """Adiciona linha ao programa se nao for vazia."""
    if linha.strip():
        st.session_state.minilang_prog.append(linha.strip())

def minilang_run() -> str:
    """Executa o programa acumulado e retorna log."""
    output = []
    for linha in st.session_state.minilang_prog:
        partes = linha.split()
        if not partes:
            continue
        cmd = partes[0].upper()
        try:
            if cmd == "GUARDA" and len(partes) == 3:
                st.session_state.minilang_vars[partes[1]] = int(partes[2])
                output.append(f"{partes[1]} = {partes[2]}")
            elif cmd == "SOMA" and len(partes) == 3:
                var = partes[1]
                if var in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[var] += int(partes[2])
                    output.append(f"{var} = {st.session_state.minilang_vars[var]}")
            elif cmd == "TIRA" and len(partes) == 3:
                var = partes[1]
                if var in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[var] -= int(partes[2])
                    output.append(f"{var} = {st.session_state.minilang_vars[var]}")
            elif cmd == "VE" and len(partes) == 2:
                val = st.session_state.minilang_vars.get(partes[1], "VAR_INEXISTENTE")
                output.append(f"{partes[1]} = {val}")
            elif cmd == "APAGA" and len(partes) == 2:
                st.session_state.minilang_vars.pop(partes[1], None)
                output.append(f"Variavel '{partes[1]}' removida.")
            else:
                output.append(f"Comando invalido: '{linha}'")
        except (ValueError, IndexError):
            output.append(f"Erro de sintaxe em: '{linha}'")

    st.session_state.minilang_prog.clear()
    return "\n".join(output) if output else "Programa vazio."

def minilang_reset() -> None:
    """Limpa programa e variaveis."""
    st.session_state.minilang_prog.clear()
    st.session_state.minilang_vars.clear()

# ==============================
# CAMADA FRONT-END: INTERFACE
# ==============================

# Navegacao com titulo dinamico
modulo = st.radio(
    "Modulo",
    ["Agenda", "Estoque", "MINILANG"],
    horizontal=True,
    label_visibility="collapsed"
)
st.title(f"Sistema Master v2.3 - {modulo}")

# --- UI Agenda ---
if modulo == "Agenda":
    st.header("Agenda de Contatos")

    with st.form("form_agenda_add", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            nome = st.text_input("Nome")
            tel = st.text_input("Telefone")
        with col2:
            foto_file = st.file_uploader("Foto", type=["png", "jpg", "jpeg"])
        if st.form_submit_button("Adicionar", type="primary"):
            foto_bytes = foto_file.read() if foto_file else None
            st.info(agenda_add(nome, tel, foto_bytes))
            st.rerun()

    col_del1, col_del2 = st.columns([2, 1])
    with col_del1:
        nome_del = st.text_input("Remover por Nome", key="del_nome")
    with col_del2:
        st.write("")
        if st.button("Remover"):
            st.warning(agenda_remove(nome_del))
            st.rerun()

    st.subheader("Contatos Cadastrados")
    db = agenda_list()
    if not db:
        st.info("Nenhum contato cadastrado.")
    else:
        for nome, dados in db.items():
            with st.container(border=True):
                col_img, col_txt = st.columns([1, 4])
                with col_img:
                    if dados["foto"]:
                        st.image(io.BytesIO(dados["foto"]), width=80, caption="")
                with col_txt:
                    st.markdown(f"**{nome}**")
                    st.text(f"Telefone: {dados['tel']}")

# --- UI Estoque ---
elif modulo == "Estoque":
    st.header("Controle de Estoque")
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.form("form_estoque_cad", clear_on_submit=True):
            prod = st.text_input("Produto")
            qtd = st.number_input("Qtd Inicial", min_value=0, step=1)
            if st.form_submit_button("Cadastrar"):
                st.info(estoque_cadastra(prod, qtd))
                st.rerun()

    with c2:
        prod_in = st.selectbox("Produto Entrada", [""] + list(estoque_relatorio().keys()))
        qtd_in = st.number_input("Qtd Entrada", min_value=1, step=1, key="qtd_in")
        if st.button("Dar Entrada", use_container_width=True):
            st.info(estoque_entrada(prod_in, qtd_in))
            st.rerun()

    with c3:
        prod_out = st.selectbox("Produto Saida", [""] + list(estoque_relatorio().keys()), key="prod_out")
        qtd_out = st.number_input("Qtd Saida", min_value=1, step=1, key="qtd_out")
        if st.button("Dar Saida", use_container_width=True):
            st.info(estoque_saida(prod_out, qtd_out))
            st.rerun()

    st.subheader("Relatorio Atual")
    st.dataframe(estoque_relatorio(), use_container_width=True)

# --- UI MINILANG ---
elif modulo == "MINILANG":
    st.header("MINILANG v1.0")
    st.caption("Comandos: GUARDA x 10 | SOMA x 5 | TIRA x 2 | VE x | APAGA x")

    cmd = st.text_input("Comando")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Adicionar Linha", use_container_width=True):
            minilang_add(cmd)
            st.rerun()
    with c2:
        if st.button("Limpar Tudo", use_container_width=True):
            minilang_reset()
            st.rerun()

    st.text_area("Programa", value="\n".join(st.session_state.minilang_prog), height=150, disabled=True)

    if st.button("Executar Programa", type="primary", use_container_width=True):
        st.success(minilang_run())

    st.subheader("Estado das Variaveis")
    st.json(st.session_state.minilang_vars)

st.divider()
st.caption("Versao v2.3 | Dados em memoria. Encerramento do app = perda de dados.")