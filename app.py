import streamlit as st
import os
import json
import pandas as pd
import uuid
from PIL import Image

# Configurações
ARQUIVO_DADOS = "agenda.json"
PASTA_FOTOS = "fotos"

# Cria pasta de fotos se não existir
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS, exist_ok=True)

st.set_page_config(page_title="Minha Agenda", layout="wide")
st.title("📒 Minha Agenda de Contatos")

# Função pra carregar contatos
def carregar_contatos():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

# Função pra salvar contatos
def salvar_contatos(contatos):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(contatos, f, ensure_ascii=False, indent=4)

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["➕ Adicionar contato", "📋 Listar contatos", "🗑️ Deletar contato"])

contatos = carregar_contatos()

if menu == "➕ Adicionar contato":
    st.header("Adicionar novo contato")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")
    foto = st.file_uploader("Foto", type=["jpg", "png", "jpeg"])
    
    if st.button("Salvar"):
        if nome and telefone:
            id_unico = str(uuid.uuid4())
            caminho_foto = ""
            
            if foto:
                caminho_foto = os.path.join(PASTA_FOTOS, f"{id_unico}.jpg")
                img = Image.open(foto)
                img.save(caminho_foto)
            
            contatos.append({
                "id": id_unico,
                "nome": nome,
                "telefone": telefone,
                "foto": caminho_foto
            })
            salvar_contatos(contatos)
            st.success(f"Contato {nome} salvo com sucesso!")
            st.rerun()
        else:
            st.error("Preencha nome e telefone!")

elif menu == "📋 Listar contatos":
    st.header("Lista de contatos")
    if contatos:
        df = pd.DataFrame(contatos)
        for _, row in df.iterrows():
            col1, col2 = st.columns([1, 3])
            with col1:
                if row["foto"] and os.path.exists(row["foto"]):
                    st.image(row["foto"], width=100)
            with col2:
                st.write(f"**Nome:** {row['nome']}")
                st.write(f"**Telefone:** {row['telefone']}")
            st.divider()
    else:
        st.info("Nenhum contato cadastrado ainda.")

elif menu == "🗑️ Deletar contato":
    st.header("Deletar contato")
    if contatos:
        nomes = [c["nome"] for c in contatos]
        nome_del = st.selectbox("Escolha o contato pra deletar", nomes)
        if st.button("Deletar"):
            contatos = [c for c in contatos if c["nome"] != nome_del]
            salvar_contatos(contatos)
            st.success(f"Contato {nome_del} deletado!")
            st.rerun()
    else:
        st.info("Não tem contatos pra deletar.")
st.markdown("---")
st.header("📋 Contatos Salvos")

if os.path.exists(ARQUIVO_AGENDA):
    with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as f:
        agenda = json.load(f)
    
    if agenda:
        for contato in agenda:
            col1, col2 = st.columns([1, 3])
            with col1:
                if contato.get("foto"):
                    st.image(contato["foto"], width=80)
            with col2:
                st.write(f"**{contato['nome']}**")
                st.write(f"📞 {contato['telefone']}")
            st.markdown("---")
    else:
        st.info("Nenhum contato cadastrado ainda.")
else:
    st.info("Salva um contato primeiro!")
