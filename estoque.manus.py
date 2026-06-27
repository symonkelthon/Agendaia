"""
Sistema de Controle de Estoque - Streamlit
Requisitos: pip install streamlit
"""

import streamlit as st
import json
import os

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Controle de Estoque",
    page_icon="📦",
    layout="centered"
)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ARQUIVO_ESTOQUE = "estoque.json"
LIMITE_ESTOQUE_BAIXO = 5  # Alerta quando quantidade for <= 5

# ─────────────────────────────────────────────
# FUNÇÕES DE PERSISTÊNCIA
# ─────────────────────────────────────────────

def carregar_estoque() -> dict:
    """Carrega os produtos do arquivo JSON."""
    if not os.path.exists(ARQUIVO_ESTOQUE):
        return {}
    with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_estoque(estoque: dict) -> None:
    """Salva o dicionário de estoque no arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
        json.dump(estoque, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────────
# FUNÇÕES DE NEGÓCIO
# ─────────────────────────────────────────────

def adicionar_produto(estoque: dict, nome: str, qtd: int, preco: float) -> tuple[bool, str]:
    """Adiciona um novo produto ao estoque."""
    nome = nome.strip()
    if not nome:
        return False, "O nome do produto não pode estar vazio."
    if nome.lower() in [p.lower() for p in estoque]:
        return False, f"O produto '{nome}' já existe no estoque."
    
    estoque[nome] = {
        "quantidade": qtd,
        "preco": preco
    }
    salvar_estoque(estoque)
    return True, f"Produto '{nome}' cadastrado com sucesso!"


def atualizar_estoque(estoque: dict, nome: str, valor: int, tipo: str) -> tuple[bool, str]:
    """Realiza entrada (+) ou saída (-) de estoque."""
    if nome not in estoque:
        return False, "Produto não encontrado."
    
    if tipo == "Entrada":
        estoque[nome]["quantidade"] += valor
    else:  # Saída
        if estoque[nome]["quantidade"] < valor:
            return False, f"Estoque insuficiente! Saldo atual: {estoque[nome]['quantidade']}"
        estoque[nome]["quantidade"] -= valor
        
    salvar_estoque(estoque)
    return True, f"{tipo} de {valor} unidades realizada para '{nome}'."


def remover_produto(estoque: dict, nome: str) -> tuple[bool, str]:
    """Remove permanentemente um produto do estoque."""
    if nome in estoque:
        del estoque[nome]
        salvar_estoque(estoque)
        return True, f"Produto '{nome}' removido com sucesso!"
    return False, "Produto não encontrado."


# ─────────────────────────────────────────────
# INICIALIZAÇÃO DO ESTADO
# ─────────────────────────────────────────────

if "estoque" not in st.session_state:
    st.session_state.estoque = carregar_estoque()

# ─────────────────────────────────────────────
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────────

st.title("📦 Sistema de Estoque")

# Sidebar para Alertas de Estoque Baixo
with st.sidebar:
    st.header("⚠️ Alertas")
    estoque_baixo = [n for n, d in st.session_state.estoque.items() if d["quantidade"] <= LIMITE_ESTOQUE_BAIXO]
    if estoque_baixo:
        for item in estoque_baixo:
            st.warning(f"**{item}** está com estoque baixo ({st.session_state.estoque[item]['quantidade']} unid.)")
    else:
        st.success("Tudo em dia! Nenhum item baixo.")

# Abas do Sistema
tab_listar, tab_add, tab_movimentar, tab_buscar, tab_remover = st.tabs([
    "📋 Listar", "➕ Novo Produto", "🔄 Entrada/Saída", "🔍 Buscar", "🗑️ Remover"
])

# ══════════════════════════════════════════════
# ABA 1 — LISTAR PRODUTOS
# ══════════════════════════════════════════════
with tab_listar:
    st.subheader("Produtos em Estoque")
    if not st.session_state.estoque:
        st.info("O estoque está vazio.")
    else:
        # Criar uma tabela simples
        dados_tabela = []
        for nome, info in st.session_state.estoque.items():
            status = "🔴 Baixo" if info["quantidade"] <= LIMITE_ESTOQUE_BAIXO else "🟢 OK"
            dados_tabela.append({
                "Produto": nome,
                "Qtd": info["quantidade"],
                "Preço (R$)": f"{info['preco']:.2f}",
                "Status": status
            })
        st.table(dados_tabela)

# ══════════════════════════════════════════════
# ABA 2 — ADICIONAR PRODUTO
# ══════════════════════════════════════════════
with tab_add:
    st.subheader("Cadastrar Novo Produto")
    with st.form("form_add", clear_on_submit=True):
        nome_in = st.text_input("Nome do Produto")
        col1, col2 = st.columns(2)
        with col1:
            qtd_in = st.number_input("Quantidade Inicial", min_value=0, step=1, value=0)
        with col2:
            preco_in = st.number_input("Preço Unitário (R$)", min_value=0.0, step=0.01, format="%.2f")
        
        btn_add = st.form_submit_button("Cadastrar")
    
    if btn_add:
        # Blindagem: Streamlit number_input já garante que não seja vazio, mas validamos o nome
        ok, msg = adicionar_produto(st.session_state.estoque, nome_in, qtd_in, preco_in)
        if ok: st.success(msg)
        else: st.error(msg)

# ══════════════════════════════════════════════
# ABA 3 — MOVIMENTAÇÃO (ENTRADA/SAÍDA)
# ══════════════════════════════════════════════
with tab_movimentar:
    st.subheader("Entrada e Saída de Itens")
    if not st.session_state.estoque:
        st.info("Cadastre produtos primeiro.")
    else:
        with st.form("form_mov"):
            prod_sel = st.selectbox("Selecione o Produto", options=list(st.session_state.estoque.keys()))
            tipo_mov = st.radio("Tipo de Operação", ["Entrada", "Saída"], horizontal=True)
            qtd_mov = st.number_input("Quantidade", min_value=1, step=1)
            btn_mov = st.form_submit_button("Confirmar Movimentação")
            
        if btn_mov:
            ok, msg = atualizar_estoque(st.session_state.estoque, prod_sel, qtd_mov, tipo_mov)
            if ok: 
                st.success(msg)
                st.rerun()
            else: 
                st.error(msg)

# ══════════════════════════════════════════════
# ABA 4 — BUSCAR PRODUTO
# ══════════════════════════════════════════════
with tab_buscar:
    st.subheader("Pesquisar Produto")
    termo = st.text_input("Digite o nome do produto para buscar").strip()
    if termo:
        # Busca insensível a maiúsculas/minúsculas no nome do produto
        encontrados = {n: d for n, d in st.session_state.estoque.items() if termo.lower() in n.lower()}
        if encontrados:
            for n, d in encontrados.items():
                with st.expander(f"📦 {n}", expanded=True):
                    st.write(f"**Quantidade:** {d['quantidade']}")
                    st.write(f"**Preço:** R$ {d['preco']:.2f}")
                    if d['quantidade'] <= LIMITE_ESTOQUE_BAIXO:
                        st.warning("⚠️ Atenção: Estoque Baixo!")
        else:
            st.error("Produto não encontrado.")

# ══════════════════════════════════════════════
# ABA 5 — REMOVER PRODUTO
# ══════════════════════════════════════════════
with tab_remover:
    st.subheader("Remover do Sistema")
    if not st.session_state.estoque:
        st.info("Nada para remover.")
    else:
        prod_rem = st.selectbox("Escolha o produto para apagar", options=list(st.session_state.estoque.keys()), key="rem")
        st.warning(f"Cuidado: Isso apagará '{prod_rem}' permanentemente.")
        if st.button("🗑️ Confirmar Remoção"):
            ok, msg = remover_produto(st.session_state.estoque, prod_rem)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

# Rodapé informando como sair (Streamlit encerra parando o terminal)
st.divider()
st.caption("Para 'Sair do Programa', basta fechar a aba do navegador e parar o processo no terminal (Ctrl+C).")
