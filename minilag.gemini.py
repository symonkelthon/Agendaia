import streamlit as st

class MiniLang:
    def __init__(self):
        if "memoria" not in st.session_state:
            st.session_state.memoria = {}
        if "programa" not in st.session_state:
            st.session_state.programa = []
        self.memoria = st.session_state.memoria
        self.programa = st.session_state.programa

    def executar_comando(self, linha, em_lote=False):
        """Processa e executa uma linha de comando da MINILANG. Retorna texto."""
        partes = linha.strip().split()
        if not partes:
            return ""
        comando = partes[0].upper()

        if comando == "SAIR":
            return "SAIR"

        if comando == "RODA":
            if not self.programa:
                return "Programa vazio."
            saida = ["--- EXECUTANDO PROGRAMA ---"]
            for cmd_salvo in self.programa:
                res = self.executar_comando(cmd_salvo, em_lote=True)
                if res: saida.append(res)
            saida.append("---------------------------")
            return "\n".join(saida)

        if comando in ["GUARDA", "SOMA"]:
            if len(partes) < 3:
                return "ERRO: Argumentos insuficientes."
            nome = partes[1]
            try:
                valor = int(partes[2])
            except ValueError:
                return "ERRO: O valor precisa ser um número inteiro."

            if not em_lote:
                self.programa.append(linha)

            if comando == "GUARDA":
                self.memoria[nome] = valor
                return f"✓ {nome} = {valor}"
            elif comando == "SOMA":
                if nome not in self.memoria:
                    return "ERRO: nome não existe. Use GUARDA primeiro"
                else:
                    self.memoria[nome] += valor
                    return f"✓ {nome} agora = {self.memoria[nome]}"

        elif comando == "MOSTRA":
            if len(partes) < 2:
                return "ERRO: Informe o nome da variável."
            nome = partes[1]
            if not em_lote:
                self.programa.append(linha)
            if nome not in self.memoria:
                return "ERRO: nome não existe. Use GUARDA primeiro"
            else:
                return str(self.memoria[nome])

        else:
            return f"ERRO: Comando '{comando}' inválido."

st.set_page_config(page_title="MINILANG", layout="wide")
st.title("💻 MINILANG v2.0 Streamlit")

ml = MiniLang()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Terminal")
    comando = st.text_input("MINILANG> ", key="cmd_input")

    c1, c2, c3 = st.columns(3)
    executar = c1.button("Executar")
    rodar = c2.button("RODA")
    limpar = c3.button("Limpar Tudo")

    if limpar:
        st.session_state.memoria = {}
        st.session_state.programa = []
        st.rerun()

    if "output" not in st.session_state:
        st.session_state.output = ""

    if executar and comando:
        res = ml.executar_comando(comando)
        if res == "SAIR":
            st.stop()
        if res:
            st.session_state.output += f"> {comando}\n{res}\n\n"

    if rodar:
        res = ml.executar_comando("RODA")
        st.session_state.output += f"> RODA\n{res}\n\n"

    st.code(st.session_state.output, language="text")

with col2:
    st.subheader("Memória RAM")
    st.json(st.session_state.memoria)
    st.subheader("Programa em Lote")
    st.code("\n".join(st.session_state.programa) or "# Vazio", language="text")
    st.caption("Comandos: GUARDA X 10 | SOMA X 5 | MOSTRA X | RODA | SAIR")