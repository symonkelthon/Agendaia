import streamlit as st

# ============================
# CONFIGURAÇÃO DA PÁGINA
# ============================

st.set_page_config(
    page_title="Mini Linguagem SK",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Mini Linguagem SK")

st.write(
    """
Digite um comando por linha.

Comandos disponíveis:

SET x 10
ADD x 5
SUB x 3
PRINT x
"""
)

# ============================
# ÁREA DE ENTRADA
# ============================

codigo = st.text_area(
    "Digite os comandos",
    height=300,
    placeholder="""SET x 10
ADD x 5
PRINT x"""
)

# ============================
# INTERPRETADOR
# ============================

def executar(codigo):

    variaveis = {}

    saida = []

    linhas = codigo.splitlines()

    for numero_linha, linha in enumerate(linhas, start=1):

        linha = linha.strip()

        if linha == "":
            continue

        partes = linha.split()

        comando = partes[0].upper()

        try:

            if comando == "SET":

                if len(partes) != 3:
                    saida.append(
                        f"Linha {numero_linha}: SET inválido."
                    )
                    continue

                nome = partes[1]

                valor = int(partes[2])

                variaveis[nome] = valor

            elif comando == "ADD":

                if len(partes) != 3:
                    saida.append(
                        f"Linha {numero_linha}: ADD inválido."
                    )
                    continue

                nome = partes[1]

                valor = int(partes[2])

                if nome not in variaveis:
                    saida.append(
                        f"Linha {numero_linha}: variável '{nome}' não existe."
                    )
                    continue

                variaveis[nome] += valor

            elif comando == "SUB":

                if len(partes) != 3:
                    saida.append(
                        f"Linha {numero_linha}: SUB inválido."
                    )
                    continue

                nome = partes[1]

                valor = int(partes[2])

                if nome not in variaveis:
                    saida.append(
                        f"Linha {numero_linha}: variável '{nome}' não existe."
                    )
                    continue

                variaveis[nome] -= valor
