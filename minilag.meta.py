import streamlit as st

st.set_page_config(page_title="MiniLang SK", page_icon="⚙️", layout="centered")

st.title("MiniLang SK - Interpretador de Comandos")
st.write("Comandos: SET x 10 | ADD x 5 | SUB x 3 | PRINT x | RODAR")

# 1. Estado inicial: dicionário de variáveis e lista de comandos
if "memoria" not in st.session_state:
    st.session_state.memoria = {}
if "comandos" not in st.session_state:
    st.session_state.comandos = []
if "saida" not in st.session_state:
    st.session_state.saida = []

# 2. Função que executa 1 linha de comando
def executar_linha(linha):
    partes = linha.strip().split()
    if not partes:
        return

    cmd = partes[0].upper()

    if cmd == "SET":
        if len(partes)!= 3:
            st.session_state.saida.append("Erro: SET precisa de variavel e valor. Ex: SET x 10")
            return
        var, valor = partes[1], partes[2]
        try:
            st.session_state.memoria[var] = int(valor)
        except ValueError:
            st.session_state.saida.append(f"Erro: Valor invalido para SET: {valor}")

    elif cmd == "ADD":
        if len(partes)!= 3:
            st.session_state.saida.append("Erro: ADD precisa de variavel e valor. Ex: ADD x 5")
            return
        var, valor = partes[1], partes[2]
        if var not in st.session_state.memoria:
            st.session_state.saida.append(f"Erro: Variavel '{var}' nao existe")
            return
        try:
            st.session_state.memoria[var] += int(valor)
        except ValueError:
            st.session_state.saida.append(f"Erro: Valor invalido para ADD: {valor}")

    elif cmd == "SUB":
        if len(partes)!= 3:
            st.session_state.saida.append("Erro: SUB precisa de variavel e valor. Ex: SUB x 3")
            return
        var, valor = partes[1], partes[2]
        if var not in st.session_state.memoria:
            st.session_state.saida.append(f"Erro: Variavel '{var}' nao existe")
            return
        try:
            st.session_state.memoria[var] -= int(valor)
        except ValueError:
            st.session_state.saida.append(f"Erro: Valor invalido para SUB: {valor}")

    elif cmd == "PRINT":
        if len(partes)!= 2:
            st.session_state.saida.append("Erro: PRINT precisa de 1 variavel. Ex: PRINT x")
            return
        var = partes[1]
        if var in st.session_state.memoria:
            st.session_state.saida.append(f"{var} = {st.session_state.memoria[var]}")
        else:
            st.session_state.saida.append(f"Erro: Variavel '{var}' nao existe")

    elif cmd == "RODAR":
        return "RODAR"
    else:
        st.session_state.saida.append(f"Erro: Comando desconhecido '{cmd}'")

# 3. Interface Streamlit
col1, col2 = st.columns([3,1])

with col1:
    cmd_input = st.text_input("Digite um comando:", key="cmd_input", placeholder="Ex: SET x 10")
with col2:
    st.write("")
    adicionar = st.button("Adicionar", use_container_width=True)

if adicionar and cmd_input:
    if cmd_input.upper().startswith("RODAR"):
        # Executa tudo que foi acumulado
        st.session_state.saida = []
        for linha in st.session_state.comandos:
            executar_linha(linha)
    else:
        st.session_state.comandos.append(cmd_input)
    st.rerun()

st.subheader("Fila de Comandos")
st.code("\n".join(st.session_state.comandos) if st.session_state.comandos else "Vazia", language="text")

if st.button("Limpar Tudo"):
    st.session_state.memoria = {}
    st.session_state.comandos = []
    st.session_state.saida = []
    st.rerun()

st.subheader("Saída")
for linha in st.session_state.saida:
    st.write(linha)