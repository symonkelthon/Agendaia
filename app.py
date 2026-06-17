import streamlit as st
import os
import json
import uuid
from PIL import Image
import html

# CSS - Estilo com HTML
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
.stTextInput input,.stTextInput textarea {
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
}
.contato-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    border-left: 5px solid #667eea;
}
.contato-card h3 {
    color: #667eea;
    margin: 0 0 8px 0;
}
.contato-card p {
    color: #333;
    margin: 0;
    font-size: 16px;
}
.zap-card{
    background: rgba(255,255,255,0.10);
    border-left: 4px solid #c084fc;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 8px;
    font-family: "Courier New", monospace;
    color: white;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}
.zap-erro{
    background: rgba(255,90,90,0.18);
    border-left: 4px solid #ff4d4d;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 8px;
    font-family: "Courier New", monospace;
    color: #ffe0e0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
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

# Menu lateral - ADICIONEI A MINI LINGUAGEM AQUI
menu = st.sidebar.selectbox("Menu", ["➕ Adicionar contato", "📋 Listar contatos", "🗑️ Deletar contato", "🗣️ Mini Linguagem"])

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
        st.info("Não tem contatos pra deletar.")

# MÓDULO MINI LINGUAGEM ZAPLANG - COLADO AQUI DEPOIS DA AGENDA
elif menu == "🗣️ Mini Linguagem":
    st.title("🗣️ Mini Linguagem ZapLang")
    st.write("Digite comandos ZapLang e execute seu programa.")

    def salvar_programa(nome_programa, codigo):
        arquivo = "mini_linguagem.json"
        if not os.path.exists(arquivo):
            dados = []
        else:
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception:
                dados = []

        novo_programa = {
            "id_uuid": str(uuid.uuid4()),
            "nome_programa": nome_programa,
            "codigo": codigo
        }
        dados.append(novo_programa)

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def interpretar_print(resto, variaveis):
        if resto == "":
            return ("erro", 'PRINT sem conteúdo. Use: PRINT "texto" ou PRINT variavel')
        if resto.startswith('"') and resto.endswith('"') and len(resto) >= 2:
            texto = resto[1:-1]
            return ("ok", texto)
        if resto in variaveis:
            return ("ok", str(variaveis[resto]))
        return ("erro", f"Variável '{resto}' não existe.")

    def interpretar(codigo):
        variaveis = {}
        resultados = []
        linhas = codigo.split("\n")

        for numero_linha, linha in enumerate(linhas, start=1):
            linha = linha.strip()
            if linha == "":
                continue
            try:
                partes = linha.split()
                comando = partes[0].upper()

                if comando == "PRINT":
                    resto = linha[6:].strip()
                    tipo, texto = interpretar_print(resto, variaveis)
                    if tipo == "erro":
                        texto = f"Linha {numero_linha}: {texto}"
                    resultados.append({"tipo": tipo, "texto": texto})

                elif comando == "SET":
                    if len(partes) < 3:
                        resultados.append({
                            "tipo": "erro",
                            "texto": f"Linha {numero_linha}: use 'SET nome valor' (faltou o valor)."
                        })
                    else:
                        nome_variavel = partes[1]
                        try:
                            valor = int(partes[2])
                            variaveis[nome_variavel] = valor
                            resultados.append({"tipo": "ok", "texto": f"{nome_variavel} = {valor}"})
                        except ValueError:
                            resultados.append({
                                "tipo": "erro",
                                "texto": f"Linha {numero_linha}: '{partes[2]}' não é um número inteiro válido."
                            })

                elif comando in ("ADD", "SUB"):
                    if len(partes) < 3:
                        resultados.append({
                            "tipo": "erro",
                            "texto": f"Linha {numero_linha}: use '{comando} nome valor' (faltou o valor)."
                        })
                    else:
                        nome_variavel = partes[1]
                        if nome_variavel not in variaveis:
                            resultados.append({
                                "tipo": "erro",
                                "texto": f"Linha {numero_linha}: variável '{nome_variavel}' não existe. Use SET antes."
                            })
                        else:
                            try:
                                valor = int(partes[2])
                                if comando == "ADD":
                                    variaveis[nome_variavel] += valor
                                else:
                                    variaveis[nome_variavel] -= valor
                                resultados.append({
                                    "tipo": "ok",
                                    "texto": f"{nome_variavel} = {variaveis[nome_variavel]}"
                                })
                            except ValueError:
                                resultados.append({
                                    "tipo": "erro",
                                    "texto": f"Linha {numero_linha}: '{partes[2]}' não é um número inteiro válido."
                                })

                elif comando == "LOOP":
                    if len(partes) < 3:
                        resultados.append({
                            "tipo": "erro",
                            "texto": f"Linha {numero_linha}: use 'LOOP quantidade comando' (ex: LOOP 3 PRINT \"oi\")."
                        })
                    else:
                        try:
                            quantidade = int(partes[1])
                        except ValueError:
                            resultados.append({
                                "tipo": "erro",
                                "texto": f"Linha {numero_linha}: '{partes[1]}' não é uma quantidade válida."
                            })
                            continue

                        comando_interno = " ".join(partes[2:])
                        if comando_interno.upper().startswith("PRINT"):
                            resto = comando_interno[6:].strip()
                            for _ in range(quantidade):
                                tipo, texto = interpretar_print(resto, variaveis)
                                if tipo == "erro":
                                    texto = f"Linha {numero_linha}: {texto}"
                                resultados.append({"tipo": tipo, "texto": texto})
                        else:
                            resultados.append({
                                "tipo": "erro",
                                "texto": f"Linha {numero_linha}: por enquanto o LOOP só funciona com PRINT."
                            })
                else:
                    resultados.append({
                        "tipo": "erro",
                        "texto": f"Linha {numero_linha}: comando desconhecido '{comando}'."
                    })
            except Exception as erro:
                resultados.append({
                    "tipo": "erro",
                    "texto": f"Linha {numero_linha}: erro inesperado ({erro})."
                })
        return resultados

    def mostrar_resultado(resultados):
        if len(resultados) == 0:
            st.info("Nenhuma saída gerada.")
            return
        for item in resultados:
            texto_seguro = html.escape(item["texto"])
            if item["tipo"] == "erro":
                st.markdown(f'<div class="zap-erro">⚠️ {texto_seguro}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="zap-card">➡️ {texto_seguro}</div>', unsafe_allow_html=True)

    nome_programa = st.text_input("Nome do programa:")

    codigo = st.text_area(
        label="Digite seu código ZapLang:",
        height=200,
        value="""SET x 10
ADD x 5
PRINT "x vale"
PRINT x
LOOP 3 PRINT "oi"
"""
    )

    coluna_salvar, coluna_executar = st.columns(2)

    with coluna_salvar:
        if st.button("💾 Salvar Programa"):
            if nome_programa.strip():
                salvar_programa(nome_programa, codigo)
                st.success("Programa salvo com sucesso!")
            else:
                st.warning("Informe um nome para o programa.")

    with coluna_executar:
        executar_clicado = st.button("▶️ Executar")

    if executar_clicado:
        st.subheader("Saída")
        resultado = interpretar(codigo)
        mostrar_resultado(resultado)
