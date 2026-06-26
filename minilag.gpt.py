import streamlit as st

st.title("💻 MINILANG v1.0")

if 'programa' not in st.session_state:
    st.session_state.programa = []
if 'variaveis' not in st.session_state:
    st.session_state.variaveis = {}

def executar():
    for linha in st.session_state.programa:
        linha = linha.strip()
        if not linha: continue
        partes = linha.split()
        comando = partes[0].upper()

        try:
            if comando == "GUARDA":
                if len(partes)!= 3: st.error(f"Erro de sintaxe: {linha}"); continue
                st.session_state.variaveis[partes[1]] = int(partes[2])
            elif comando == "SOMA":
                st.session_state.variaveis[partes[1]] += int(partes[2])
            elif comando == "TIRA":
                st.session_state.variaveis[partes[1]] -= int(partes[2])
            elif comando == "VE":
                st.write(f"{partes[1]} = {st.session_state.variaveis[partes[1]]}")
            elif comando == "APAGA":
                del st.session_state.variaveis[partes[1]]
            else:
                st.warning(f"Comando desconhecido: {comando}")
        except KeyError:
            st.error(f"Erro: Variável '{partes[1]}' não existe")
        except ValueError:
            st.error("Erro: valor inválido")
        except Exception as e:
            st.error(f"Erro: {e}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Editor")
    codigo = st.text_area("Escreva seu programa", height=250,
                          value="\n".join(st.session_state.programa))
    if st.button("RODA ▶️"):
        st.session_state.programa = codigo.splitlines()
        executar()
    if st.button("Limpar Programa"):
        st.session_state.programa = []
        st.session_state.variaveis = {}
        st.rerun()

with col2:
    st.subheader("Variáveis Atuais")
    st.json(st.session_state.variaveis)
    st.info("Comandos: GUARDA X 10 | SOMA X 5 | TIRA X 2 | VE X | APAGA X")