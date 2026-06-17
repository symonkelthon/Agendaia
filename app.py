import streamlit as st
import os
import json
import uuid
from PIL import Image

# CSS - Estilo bonitão
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.stTextInput input,.stTextInput textarea {
    border-radius: 10px;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 20px;
    width: 100%;
    font-weight: bold;
}
.contato-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.contato-card h3 {
    color: #667eea;
    margin: 0;
}
.contato-card p {
    color: #333;
    margin: 5px 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# Configurações
ARQUIVO_DADOS = "agenda.json"
PASTA_FOTOS = "fotos"

if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS, exist_ok=True)

st.set_page_config(page_title="Minha Agenda", layout="wide")
st.title("📒 Minha Agenda de Contatos")

def carregar_contatos():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_contatos(contatos):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f: # CORRIGI AQUI
        json.dump(contatos, f, ensure_ascii=False, indent=4)

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
        for contato in contatos:
            col1, col2 = st.columns([1, 3])
            with col1:
                if contato["foto"] and os.path.exists(contato["foto"]):
                    st.image(contato["foto"], width=100)
            with col2:
                st.markdown(f"""
                <div class="contato-card">
                    <h3>{contato['nome']}</h3>
                    <p>📞 {contato['telefone']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.divider()
    else:
        st.info("Nenhum contato cadastrado ainda.")

elif menu == "🗑️ Deletar contato":
    st.header("Deletar contato")
    if contatos:
        opcoes = {f"{c['nome']} - {c['telefone']}": c['id'] for c in contatos}
        escolha = st.selectbox("Escolha o contato pra deletar", list(opcoes.keys()))

        if st.button("Deletar"):
            id_deletar = opcoes[escolha]
            contatos = [c for c in contatos if c['id']!= id_deletar]
            salvar_contatos(contatos)
            st.success("Contato deletado!")
            st.rerun()
    else:
        st.info("Nenhum contato pra deletar.")
