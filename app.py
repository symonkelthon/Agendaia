import streamlit as st
import os
import json
import pandas as pd
import uuid
from PIL import Image

# CSS - Linguagem 3: Estilo
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
}
.contato-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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

if os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        agenda = json.load(f)
    
    if agenda:
        for contato in agenda:
            col1, col2 = st.columns([1, 3])
            with col1:
                if contato.get("foto"):
                    st.image(contato["foto"], width=80)
            with col2:
    st.markdown(f"""
    <div class="contato-card">
        <h3>{contato['nome']}</h3>
        <p>📞 {contato['telefone']}</p>
    </div>
    """, unsafe_allow_html=True)
            
    
    
        
        

    """, unsafe_allow_html=True)
        
            st.markdown("---")
    else:
        st.info("Nenhum contato cadastrado ainda.")
else:
    st.info("Salva um contato primeiro!")
st.markdown("---")
st.header("🗑️ Deletar Contato")

if os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        agenda = json.load(f)
    
    if agenda:
        nomes = [c["nome"] for c in agenda]
        contato_deletar = st.selectbox("Escolhe quem apagar:", nomes)
        
        if st.button("Apagar"):
            agenda = [c for c in agenda if c["nome"] != contato_deletar]
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(agenda, f, ensure_ascii=False, indent=2)
            st.success(f"Contato {contato_deletar} apagado!")
            st.rerun()
    else:
        st.info("Não tem ninguém pra deletar")
