import streamlit as st

if "prog" not in st.session_state: st.session_state.prog = []
if "vars" not in st.session_state: st.session_state.vars = {}

def executar():
    out = []
    for linha in st.session_state.prog:
        p = linha.strip().split()
        if not p: continue
        cmd = p[0].upper()
        try:
            if cmd=="GUARDA": st.session_state.vars[p[1]] = int(p[2])
            elif cmd=="SOMA": st.session_state.vars[p[1]] += int(p[2])
            elif cmd=="TIRA": st.session_state.vars[p[1]] -= int(p[2])
            elif cmd=="VE": out.append(f"{p[1]} = {st.session_state.vars[p[1]]}")
            elif cmd=="APAGA": del st.session_state.vars[p[1]]
            else: out.append(f"Comando desconhecido: {cmd}")
        except KeyError: out.append(f"Erro: Variável '{p[1]}' não existe")
        except: out.append("Erro: valor inválido")
    return "\n".join(out)

st.title("💻 Minilinguagem Meta AI v1.0")
col1, col2 = st.columns(2)

with col1:
    cod = st.text_area("Digite seu programa aqui", value="\n".join(st.session_state.prog), height=220)
    c1, c2, c3 = st.columns(3)
    if c1.button("RODAR ▶️"):
        st.session_state.prog = cod.splitlines()
        st.code(executar() or "Executado sem saída.")
    if c2.button("Limpar"):
        st.session_state.prog = []; st.session_state.vars = {}; st.rerun()
    if c3.button("Exemplo"):
        st.session_state.prog = ["GUARDA X 10", "SOMA X 5", "VE X"]; st.rerun()

with col2:
    st.subheader("Variáveis")
    st.json(st.session_state.vars)
    st.caption("Comandos: GUARDA X 10 | SOMA X 2 | TIRA X 1 | VE X | APAGA X")