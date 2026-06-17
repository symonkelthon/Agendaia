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
.stTextInput input, .stTextInput textarea {
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
    with open
