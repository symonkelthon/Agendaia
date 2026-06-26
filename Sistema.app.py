

import streamlit as st
import io

try:
    from PIL import Image
except ImportError:
    st.error("Dependencia 'pillow' ausente. Crie requirements.txt com: streamlit\npillow")
    st.stop()

st.set_page_config(page_title="Sistema Master v3.0", layout="wide")

# ==============================
# CAMADA DE ESTADO
# ==============================
def init_state():
    """Inicializa todos os bancos de dados."""
    if "agenda_db" not in st.session_state:
        st.session_state.agenda_db = {} # {nome: {"tel": str, "foto": bytes}}
    if "estoque_db" not in st.session_state:
        st.session_state.estoque_db = {} # {nome: {"qtd": int, "preco": float}}
    if "minilang" not in st.session_state:
        st.session_state.minilang = {"vars": {}, "prog": []} # RAM + Programa

init_state()

# ==============================
# CAMADA BACK-END: REGRAS DE NEGOCIO
# ==============================

# --- 1. Modulo Agenda ---
def agenda_add(nome: str, tel: str, foto_bytes: bytes | None) -> str:
    """Adiciona/atualiza contato. Valida nome."""
    if not nome.strip():
        return "Erro: Nome nao pode ser vazio."
    if not tel.strip():
        return "Erro: Telefone nao pode ser vazio."
    st.session_state.agenda_db[nome] = {"tel": tel, "foto": foto_bytes}
    return f"Contato '{nome}' salvo com sucesso."

def agenda_remove(nome: str) -> str:
    """Remove contato por nome exato."""
    if nome in st.session_state.agenda_db:
        del st.session_state.agenda_db[nome]
        return f"Contato '{nome}' removido."
    return "Erro: Contato nao encontrado."

def agenda_busca(termo: str) -> dict:
    """Busca contatos por nome parcial, case-insensitive."""
    termo = termo.lower()
    return {n: d for n, d in st.session_state.agenda_db.items() if termo in n.lower()}

def agenda_list() -> dict:
    return st.session_state.agenda_db

# --- 2. Modulo Estoque ---
def estoque_add(nome: str, qtd: int, preco: float) -> str:
    """Cadastra ou atualiza produto. Valida campos."""
    if not nome.strip():
        return "Erro: Nome do produto nao pode ser vazio."
    st.session_state.estoque_db[nome] = {"qtd": qtd, "preco": preco}
    return f"Produto '{nome}' salvo. Qtd: {qtd} | R$ {preco:.2f}"

def estoque_entrada(nome: str, qtd: int) -> str:
    if nome not in st.session_state.estoque_db: return "Erro: Produto nao existe."
    st.session_state.estoque_db[nome]["qtd"] += qtd
    return f"Entrada OK. '{nome}': {st.session_state.estoque_db[nome]['qtd']} un"

def estoque_saida(nome: str, qtd: int) -> str:
    if nome not in st.session_state.estoque_db: return "Erro: Produto nao existe."
    if st.session_state.estoque_db[nome]["qtd"] < qtd: return "Erro: Saldo insuficiente."
    st.session_state.estoque_db[nome]["qtd"] -= qtd
    return f"Saida OK. '{nome}': {st.session_state.estoque_db[nome]['qtd']} un"

def estoque_remove(nome: str) -> str:
    if nome in st.session_state.estoque_db:
        del st.session_state.estoque_db[nome]
        return f"Produto '{nome}' removido."
    return "Erro: Produto nao encontrado."

def estoque_busca(nome: str) -> dict | None:
    return st.session_state.estoque_db.get(nome)

def estoque_list() -> dict:
    return st.session_state.estoque_db

# --- 3. Modulo MINILANG ---
def minilang_exec(linha: str) -> str:
    """Executa 1 linha da MINILANG. Equivale ao executar_comando."""
    m = st.session_state.minilang
    partes = linha.strip().split()
    if not partes: return ""

    cmd = partes[0].upper()
    out = []

    if cmd == "RODA":
        out.append("--- EXECUTANDO PROGRAMA ---")
        for cmd_salvo in m["prog"]:
            out.append(minilang_exec(cmd_salvo))
        out.append("---------------------------")
        m["prog"].clear()
        return "\n".join(out)

    if cmd in ["GUARDA", "SOMA"]:
        if len(partes) < 3: return "ERRO: Argumentos insuficientes."
        nome, val_str = partes[1], partes[2]
        try: val = int(val_str)
        except ValueError: return "ERRO: O valor precisa ser inteiro."

        m["prog"].append(linha) # Salva no historico

        if cmd == "GUARDA":
            m["vars"][nome] = val
            return f"{nome} = {val}"
        if cmd == "SOMA":
            if nome not in m["vars"]: return "ERRO: nome nao existe. Use GUARDA."
            m["vars"][nome] += val
            return f"{nome} agora = {m['vars'][nome]}"

    if cmd == "MOSTRA":
        if len(partes) < 2: return "ERRO: Informe o nome da variavel."
        nome = partes[1]
        m["prog"].append(linha)
        if nome not in m["vars"]: return "ERRO: nome nao existe. Use GUARDA."
        return str(m["vars"][nome])

    return f"ERRO: Comando '{cmd}' invalido."

def minilang_reset() -> None:
    st.session_state.minilang = {"vars": {}, "prog": []}

# ==============================
# CAMADA FRONT-END: UI
# ==============================
modulo = st.radio("Modulo", ["Agenda", "Estoque", "MINILANG"], horizontal=True, label_visibility="collapsed")
st.title(f"Sistema Master v3.0 - {modulo}")

# --- UI Agenda ---
if modulo == "Agenda":
    st.header("Agenda de Contatos")
    with st.form("f_agenda", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1: nome = st.text_input("Nome"); tel = st.text_input("Telefone")
        with c2: foto = st.file_uploader("Foto", type=["png", "jpg", "jpeg"])
        if st.form_submit_button("Adicionar"): st.info(agenda_add(nome, tel, foto.read() if foto else None)); st.rerun()

    c1, c2 = st.columns(2)
    with c1: nome_del = st.text_input("Remover Nome Exato")
    if c2.button("Remover"): st.warning(agenda_remove(nome_del)); st.rerun()

    termo_busca = st.text_input("Buscar por Nome")
    db = agenda_busca(termo_busca) if termo_busca else agenda_list()

    st.subheader(f"Contatos: {len(db)}")
    if not db: st.info("Nenhum contato.")
    for n, d in db.items():
        with st.container(border=True):
            c1, c2 = st.columns([1, 4])
            with c1:
                if d["foto"]: st.image(io.BytesIO(d["foto"]), width=80)
            with c2: st.markdown(f"**{n}**"); st.text(f"Tel: {d['tel']}")

# --- UI Estoque ---
elif modulo == "Estoque":
    st.header("Controle de Estoque")
    with st.form("f_estoque_add", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1: prod = st.text_input("Produto")
        with c2: qtd = st.number_input("Qtd", 0, 10000, 0)
        with c3: preco = st.number_input("Preco R$", 0.0, 10000.0, 0.0, step=0.01)
        if st.form_submit_button("Adicionar/Atualizar"): st.info(estoque_add(prod, qtd, preco)); st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        prod_in = st.selectbox("Entrada", [""] + list(estoque_list().keys()))
        qtd_in = st.number_input("Qtd", 1, 1000, 1, key="qi")
        if st.button("Dar Entrada"): st.info(estoque_entrada(prod_in, qtd_in)); st.rerun()
    with c2:
        prod_out = st.selectbox("Saida", [""] + list(estoque_list().keys()), key="po")
        qtd_out = st.number_input("Qtd", 1, 1000, 1, key="qo")
        if st.button("Dar Saida"): st.info(estoque_saida(prod_out, qtd_out)); st.rerun()
    with c3:
        prod_del = st.selectbox("Remover", [""] + list(estoque_list().keys()), key="pd")
        if st.button("Remover"): st.warning(estoque_remove(prod_del)); st.rerun()

    nome_busca = st.text_input("Buscar Produto Exato")
    if nome_busca:
        res = estoque_busca(nome_busca)
        st.json(res) if res else st.warning("Produto nao encontrado.")

    st.subheader("Relatorio")
    st.dataframe(estoque_list(), use_container_width=True)

# --- UI MINILANG ---
elif modulo == "MINILANG":
    st.header("MINILANG v1.0")
    st.code("Comandos: GUARDA x 10 | SOMA x 5 | MOSTRA x | RODA | SAIR")

    cmd = st.text_input("Comando", key="cmd_input")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Executar Linha", type="primary"):
            st.success(minilang_exec(cmd)); st.rerun()
    with c2:
        if st.button("Limpar Tudo"): minilang_reset(); st.rerun()

    st.text_area("Programa em Lote", value="\n".join(st.session_state.minilang["prog"]),height150, disabled=True)
    st.subheader("Memoria RAM")
    st.json(st.session_state.minilang["vars"])

st.divider()
st.caption("v3.0 | Dados em memoria de sessao.")