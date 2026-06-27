import streamlit as st
import json
import os
from PIL import Image

ARQUIVO = "agenda.json"
PASTA_FOTOS = "fotos"

st.set_page_config(page_title="Agenda de Contatos", layout="centered")

# 1. Cria pasta pra salvar fotos se não existir
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

# 2. Carrega dados do arquivo JSON ou inicia vazio
def carregar_contatos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 3. Salva dados no arquivo JSON
def salvar_contatos(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# 4. Estado inicial da app
if "contatos" not in st.session_state:
    st.session_state.contatos = carregar_contatos()

st.title("Agenda de Contatos")

tab1, tab2, tab3, tab4 = st.tabs(["Adicionar", "Listar", "Buscar", "Remover"])

# TAB 1: Adicionar contato
with tab1:
    st.subheader("Adicionar Novo Contato")
    nome = st.text_input("Nome", key="add_nome")
    telefone = st.text_input("Telefone", key="add_tel")
    foto = st.file_uploader("Foto do Contato", type=["png", "jpg", "jpeg"], key="add_foto")

    if st.button("Salvar Contato"):
        if nome:
            if nome in st.session_state.contatos:
                st.error("Contato já existe. Use outro nome.")
            else:
                caminho_foto = ""
                if foto is not None:
                    caminho_foto = os.path.join(PASTA_FOTOS, f"{nome}.png")
                    img = Image.open(foto)
                    img.save(caminho_foto)

                st.session_state.contatos[nome] = {
                    "telefone": telefone,
                    "foto": caminho_foto
                }
                salvar_contatos(st.session_state.contatos)
                st.success(f"Contato {nome} adicionado!")
                st.rerun()
        else:
            st.warning("O nome é obrigatório.")

# TAB 2: Listar contatos
with tab2:
    st.subheader("Lista de Contatos")
    if st.session_state.contatos:
        for nome, dados in st.session_state.contatos.items():
            with st.container(border=True):
                col1, col2 = st.columns([1,3])
                with col1:
                    if dados["foto"] and os.path.exists(dados["foto"]):
                        st.image(dados["foto"], width=100)
                with col2:
                    st.write(f"**Nome:** {nome}")
                    st.write(f"**Telefone:** {dados['telefone']}")
      
    else:
        st.info("Nenhum contato cadastrado.")

# TAB 3: Buscar contatos
with tab3:
    st.subheader("Buscar Contato")
    termo = st.text_input("Digite o nome para buscar", key="busca")
    if termo:
        resultados = {k:v for k,v in st.session_state.contatos.items() if termo.lower() in k.lower()}
        if resultados:
            for nome, dados in resultados.items():
                st.write(f"**{nome}** | Tel: {dados['telefone']} 
                if dados["foto"] and os.path.exists(dados["foto"]):
                    st.image(dados["foto"], width=80)
        else:
            st.warning("Contato não encontrado.")

# TAB 4: Remover contato
with tab4:
    st.subheader("Remover Contato")
    if st.session_state.contatos:
        nome_remover = st.selectbox("Selecione o contato", options=list(st.session_state.contatos.keys()))
        if st.button("Remover"):
            # Apaga foto do disco também
            caminho_foto = st.session_state.contatos[nome_remover]["foto"]
            if caminho_foto and os.path.exists(caminho_foto):
                os.remove(caminho_foto)
            del st.session_state.contatos[nome_remover]
            salvar_contatos(st.session_state.contatos)
            st.success(f"Contato {nome_remover} removido.")
            st.rerun()
    else:
        st.info("Nenhum contato para remover.")