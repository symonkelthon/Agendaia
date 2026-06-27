import streamlit as st
import json
import os
from pathlib import Path
import shutil

# ==========================
# CONFIGURAÇÕES
# ==========================

ARQUIVO_CONTATOS = "contatos.json"
PASTA_FOTOS = "fotos"

os.makedirs(PASTA_FOTOS, exist_ok=True)

st.set_page_config(
    page_title="Agenda de Contatos",
    page_icon="📒",
    layout="wide"
)


# ==========================
# FUNÇÕES
# ==========================

def carregar_contatos():
    if not os.path.exists(ARQUIVO_CONTATOS):
        return []

    try:
        with open(ARQUIVO_CONTATOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        return []


def salvar_contatos(contatos):
    with open(ARQUIVO_CONTATOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            contatos,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


contatos = carregar_contatos()

st.title("📒 Agenda de Contatos")

st.subheader("Adicionar contato")

nome = st.text_input("Nome")

telefone = st.text_input("Telefone")

email = st.text_input("E-mail")

foto = st.file_uploader(
    "Foto",
    type=["png", "jpg", "jpeg"]
)


if st.button("Salvar contato"):

    if nome.strip() == "":
        st.error("Informe o nome.")
        st.stop()

    caminho_foto = ""

    if foto is not None:

        destino = os.path.join(
            PASTA_FOTOS,
            foto.name
        )

        with open(destino, "wb") as arquivo:
            arquivo.write(foto.getbuffer())

        caminho_foto = destino

    novo = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "foto": caminho_foto
    }

    contatos.append(novo)

    salvar_contatos(contatos)

    st.success("Contato salvo com sucesso!")

    st.rerun()


st.divider()

st.subheader("Buscar contato")

pesquisa = st.text_input("Digite um nome para pesquisar")

if pesquisa:

    contatos_filtrados = []

    for contato in contatos:

        if pesquisa.lower() in contato["nome"].lower():
            contatos_filtrados.append(contato)

else:

    contatos_filtrados = contatos


# ==========================
# LISTAGEM DOS CONTATOS
# ==========================

st.divider()

st.subheader("Lista de Contatos")

if len(contatos_filtrados) == 0:

    st.info("Nenhum contato encontrado.")

else:

    for indice, contato in enumerate(contatos_filtrados):

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:

                if (
                    contato["foto"] != ""
                    and os.path.exists(contato["foto"])
                ):
                    st.image(
                        contato["foto"],
                        width=150
                    )
                else:
                    st.write("Sem foto")

            with col2:

                st.markdown(
                    f"### {contato['nome']}"
                )

                st.write(
                    f"**Telefone:** {contato['telefone']}"
                )

                st.write(
                    f"**E-mail:** {contato['email']}"
                )

                if st.button(
                    "🗑️ Remover",
                    key=f"remover_{indice}"
                ):

                    if (
                        contato["foto"] != ""
                        and os.path.exists(contato["foto"])
                    ):
                        try:
                            os.remove(contato["foto"])
                        except:
                            pass

                    contatos.remove(contato)

                    salvar_contatos(contatos)

                    st.success(
                        "Contato removido com sucesso!"
                    )

                    st.rerun()

# ==========================
# RODAPÉ
# ==========================

st.divider()

st.caption("Agenda de Contatos desenvolvida em Python + Streamlit")

