import streamlit as st
import os
import json
import uuid
from PIL import Image

# 1. PYTHON: Configurações iniciais
ARQUIVO_DADOS = "agenda.json"
PASTA_FOTOS = "fotos"

if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS, exist_ok=True)

st.set_page_config(page_title="Minha Agenda", layout="wide")
st.title("📒 Minha Agenda de Contatos")

# 2. CSS: Estilo dentro do Python usando st.markdown
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
.stTextInput input, .stTextInput textarea {
    border-radius: 10px;
    border: 2px solid #667eea;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 20px;
    width: 100%;
    font-weight: bold;
    border: none;
    padding: 10px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #FF6B6B;
    cursor: pointer;
}
.contato-card {
    background-color: white;
    padding: 20px;
    border-radius:
