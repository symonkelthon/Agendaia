import streamlit as st

st.set_page_config(page_title="Sistema Master v2.0", layout="wide")
st.title("🚀 SISTEMA MASTER v2.0")
st.caption("Agenda + Estoque + MINILANG | Desenvolvido com Meta AI")

# ========== ESTADO = DADOS FICAM NA MEMÓRIA DO APP ==========
if 'agenda_db' not in st.session_state:
    st.session_state.agenda_db = {} # {nome: telefone}
if 'estoque_db' not in st.session_state:
    st.session_state.estoque_db = {} # {produto: qtd}
if 'minilang_vars' not in st.session_state:
    st.session_state.minilang_vars = {} # {var: valor}
if 'minilang_prog' not in st.session_state:
    st.session_state.minilang_prog = [] # [linha1, linha2]

# ========== BACK-END = REGRA DE NEGÓCIO PURA ==========
# --- BACK-END AGENDA ---
def backend_agenda_add(nome, tel):
    if not nome or not tel: return "Erro: Preencha nome e telefone."
    st.session_state.agenda_db[nome] = tel
    return f"Contato '{nome}' salvo."

def backend_agenda_remove(nome):
    if nome in st.session_state.agenda_db:
        del st.session_state.agenda_db[nome]
        return f"'{nome}' removido."
    return f"Erro: '{nome}' não encontrado."

# --- BACK-END ESTOQUE ---
def backend_estoque_cadastra(prod, qtd):
    if not prod: return "Erro: Digite um produto."
    st.session_state.estoque_db[prod] = int(qtd)
    return f"Produto '{prod}' cadastrado com {qtd} un."

def backend_estoque_entrada(prod, qtd):
    if prod not in st.session_state.estoque_db: return f"Erro: '{prod}' não existe."
    st.session_state.estoque_db[prod] += int(qtd)
    return f"Entrada OK. {prod}: {st.session_state.estoque_db[prod]} un"

def backend_estoque_saida(prod, qtd):
    if prod not in st.session_state.estoque_db: return f"Erro: '{prod}' não existe."
    qtd = int(qtd)
    if st.session_state.estoque_db[prod] < qtd: return f"Erro: Estoque insuficiente. Tem {st.session_state.estoque_db[prod]}"
    st.session_state.estoque_db[prod] -= qtd
    return f"Saída OK. {prod}: {st.session_state.estoque_db[prod]} un"

# --- BACK-END MINILANG ---
def backend_minilang_add_linha(linha):
    if linha.strip(): st.session_state.minilang_prog.append(linha.strip())

def backend_minilang_executa():
    saida = []
    for linha in st.session_state.minilang_prog:
        partes = linha.split()
        if not partes: continue
        cmd = partes[0].upper()

        try:
            if cmd == "GUARDA" and len(partes) == 3:
                st.session_state.minilang_vars[partes[1]] = int(partes[2])
                saida.append(f"✓ {partes[1]} = {partes[2]}")
            elif cmd == "SOMA" and len(partes) == 3:
                if partes[1] in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[partes[1]] += int(partes[2])
                    saida.append(f"✓ {partes[1]} agora = {st.session_state.minilang_vars[partes[1]]}")
            elif cmd == "TIRA" and len(partes) == 3:
                if partes[1] in st.session_state.minilang_vars:
                    st.session_state.minilang_vars[partes[1]] -= int(partes[2])
                    saida.append(f"✓ {partes[1]} agora = {st.session_state.minilang_vars[partes[1]]}")
            elif cmd == "VE" and len(partes) == 2:
                val = st.session_state.minilang_vars.get(partes[1], "VAR NÃO EXISTE")
                saida.append(f"{partes[1]} = {val}")
            elif cmd == "APAGA" and len(partes) == 2:
                if partes[1] in st.session_state.minilang_vars:
                    del st.session_state.minilang_vars[partes[1]]
                    saida.append(f"✓ {partes[1]} apagada")
        except ValueError:
            saida.append(f"Erro: '{linha}' - Valor precisa ser número inteiro.")

    st.session_state.minilang_prog = [] # Limpa programa depois de rodar
    return "\n".join(saida) if saida else "Programa vazio."

def backend_minilang_limpa():
    st.session_state.minilang_prog = []
    st.session_state.minilang_vars = {}

# ========== FRONT-END = INTERFACE STREAMLIT ==========
tab1, tab2, tab3 = st.tabs(["📒 AGENDA", "📦 ESTOQUE", "💻 MINILANG"])

# --- FRONT AGENDA ---
with tab1:
    st.header("Agenda de Contatos")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("form_add_contato"):
            nome = st.text_input("Nome")
            tel = st.text_input("Telefone")
            if st.form_submit_button("Adicionar Contato"):
                st.success(backend_agenda_add(nome, tel))
                st.rerun()
    with col2:
        nome_remover = st.text_input("Nome para Remover")
        if st.button("Remover Contato"):
            st.warning(backend_agenda_remove(nome_remover))
            st.rerun()

    st.subheader("Contatos Salvos")
    st.dataframe(st.session_state.agenda_db, use_container_width=True)

# --- FRONT ESTOQUE ---
with tab2:
    st.header("Controle de Estoque")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.form("form_cadastra"):
            prod = st.text_input("Produto Novo")
            qtd = st.number_input("Qtd Inicial", 0, 10000, 0)
            if st.form_submit_button("Cadastrar"):
                st.success(backend_estoque_cadastra(prod, qtd))
                st.rerun()
    with col2:
        prod_in = st.selectbox("Produto Entrada", options=[""] + list(st.session_state.estoque_db.keys()))
        qtd_in = st.number_input("Qtd Entrada", 1, 10000, 1)
        if st.button("Dar Entrada"):
            st.success(backend_estoque_entrada(prod_in, qtd_in))
            st.rerun()
    with col3:
        prod_out = st.selectbox("Produto Saída", options=[""] + list(st.session_state.estoque_db.keys()), key="out")
        qtd_out = st.number_input("Qtd Saída", 1, 10000, 1)
        if st.button("Dar Saída"):
            st.success(backend_estoque_saida(prod_out, qtd_out))
            st.rerun()

    st.subheader("Relatório de Estoque")
    st.dataframe(st.session_state.estoque_db, use_container_width=True)

# --- FRONT MINILANG ---
with tab3:
    st.header("MINILANG v1.0 - Sua Primeira Linguagem")
    st.info("Comandos: GUARDA x 10 | SOMA x 5 | TIRA x 2 | VE x | APAGA x")

    col1, col2 = st.columns([3,1])
    with col1:
        cmd = st.text_input("Digite o comando:", placeholder="EX: GUARDA vida 100")
    with col2:
        st.write("") # espaçamento
        if st.button("Adicionar Linha"):
            backend_minilang_add_linha(cmd)
            st.rerun()

    st.code("\n".join(st.session_state.minilang_prog) if st.session_state.minilang_prog else "# Programa vazio", language="python")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ RODAR PROGRAMA", type="primary"):
            st.success(backend_minilang_executa())
    with col2:
        if st.button("🗑️ LIMPAR TUDO"):
            backend_minilang_limpa()
            st.rerun()

    st.subheader("Variáveis na Memória")
    st.json(st.session_state.minilang_vars)

st.divider()
st.caption("Obs: Os dados são perdidos ao reiniciar o app. V3.0 terá salvamento em.json")
