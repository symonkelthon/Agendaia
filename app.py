# ====================================================================
# SISTEMA MULTI-FUNÇÃO (Agenda + Mini Linguagem + Estoque)
# Tecnologias: Python + Streamlit
# ====================================================================

# ---------------------- 1. IMPORTS ----------------------
import streamlit as st
import os
import json
import uuid
import html
import pandas as pd

# ---------------------- 2. CONFIGURAÇÃO + CONSTANTES ----------------------
st.set_page_config(page_title="Sistema Multi-Função", page_icon="🧩", layout="wide")

ARQUIVO_AGENDA = "agenda.json"
ARQUIVO_ZAPLANG = "mini_linguagem.json"
ARQUIVO_ESTOQUE = "estoque.json"
PASTA_FOTOS = "fotos"

if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

# ---------------------- 3. FUNÇÕES GENÉRICAS DE ARQUIVO ----------------------
def carregar_dados(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return []

def salvar_dados(caminho_arquivo, dados):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# ---------------------- 4. CSS CENTRALIZADO ----------------------
GRADIENTES = {
    "agenda": ("#1f4068", "#1b6ca8", "#2596be"),
    "zaplang": ("#4b0082", "#6a0dad", "#8a2be2"),
    "estoque": ("#00c853", "#00acc1", "#1e88e5"),
}

def aplicar_estilo(tema):
    cor1, cor2, cor3 = GRADIENTES[tema]
    st.markdown(
        f"""
        <style>
       .stApp {{
            background: linear-gradient(135deg, {cor1}, {cor2}, {cor3});
        }}
        h1, h2, h3, p, label {{
            color: white!important;
        }}
       .zap-card {{
            background: rgba(255,255,255,0.10);
            border-left: 4px solid #c084fc;
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 8px;
            font-family: "Courier New", monospace;
            color: white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }}
       .zap-erro {{
            background: rgba(255,90,90,0.18);
            border-left: 4px solid #ff4d4d;
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 8px;
            font-family: "Courier New", monospace;
            color: #ffe0e0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }}
       .card-produto {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
       .titulo-produto {{
            font-size: 20px;
            font-weight: bold;
            color: #222;
        }}
       .texto-produto {{
            color: #444;
            font-size: 16px;
        }}
       .estoque-baixo {{
            color: red;
            font-weight: bold;
            font-size: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------- 5. FUNÇÕES AUXILIARES ----------------------
def salvar_foto(arquivo_foto):
    extensao = os.path.splitext(arquivo_foto.name)[1]
    nome_unico = f"{uuid.uuid4().hex}{extensao}"
    caminho_completo = os.path.join(PASTA_FOTOS, nome_unico)
    with open(caminho_completo, "wb") as f:
        f.write(arquivo_foto.getbuffer())
    return caminho_completo

def mostrar_contatos(lista):
    if len(lista) == 0:
        st.info("Nenhum contato encontrado.")
        return
    dados_tabela = [
        {"Nome": c.get("nome", "Sem nome"), "Telefone": c.get("telefone", "Sem telefone")}
        for c in lista
    ]
    st.dataframe(pd.DataFrame(dados_tabela), use_container_width=True)

    st.subheader("Fotos dos contatos")
    for contato in lista:
        with st.expander(contato.get("nome", "Contato")):
            coluna_foto, coluna_dados = st.columns([1, 3])
            with coluna_foto:
                if contato.get("foto") and os.path.exists(contato["foto"]):
                    st.image(contato["foto"], width=100)
                else:
                    st.write("Sem foto")
            with coluna_dados:
                st.write(f"**Telefone:** {contato.get('telefone', '-')}")

def interpretar_print(resto, variaveis):
    if resto == "":
        return ("erro", 'PRINT sem conteúdo. Use: PRINT "texto" ou PRINT variavel')
    if resto.startswith('"') and resto.endswith('"') and len(resto) >= 2:
        return ("ok", resto[1:-1])
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
                    resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: use 'SET nome valor' (faltou o valor)."})
                else:
                    nome_variavel = partes[1]
                    try:
                        valor = int(partes[2])
                        variaveis[nome_variavel] = valor
                        resultados.append({"tipo": "ok", "texto": f"{nome_variavel} = {valor}"})
                    except ValueError:
                        resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: '{partes[2]}' não é um número inteiro válido."})
            elif comando in ("ADD", "SUB"):
                if len(partes) < 3:
                    resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: use '{comando} nome valor' (faltou o valor)."})
                else:
                    nome_variavel = partes[1]
                    if nome_variavel not in variaveis:
                        resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: variável '{nome_variavel}' não existe. Use SET antes."})
                    else:
                        try:
                            valor = int(partes[2])
                            if comando == "ADD":
                                variaveis[nome_variavel] += valor
                            else:
                                variaveis[nome_variavel] -= valor
                            resultados.append({"tipo": "ok", "texto": f"{nome_variavel} = {variaveis[nome_variavel]}"})
                        except ValueError:
                            resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: '{partes[2]}' não é um número inteiro válido."})
            elif comando == "LOOP":
                if len(partes) < 3:
                    resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: use 'LOOP quantidade comando' (ex: LOOP 3 PRINT \"oi\")."})
                else:
                    try:
                        quantidade = int(partes[1])
                    except ValueError:
                        resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: '{partes[1]}' não é uma quantidade válida."})
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
                        resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: por enquanto o LOOP só funciona com PRINT."})
            else:
                resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: comando desconhecido '{comando}'."})
        except Exception as erro:
            resultados.append({"tipo": "erro", "texto": f"Linha {numero_linha}: erro inesperado ({erro})."})
    return resultados

def mostrar_resultado_zaplang(resultados):
    if len(resultados) == 0:
        st.info("Nenhuma saída gerada.")
        return
    for item in resultados:
        texto_seguro = html.escape(item["texto"])
        classe = "zap-erro" if item["tipo"] == "erro" else "zap-card"
        icone = "⚠️" if item["tipo"] == "erro" else "➡️"
        st.markdown(f'<div class="{classe}">{icone} {texto_seguro}</div>', unsafe_allow_html=True)

def renderizar_card_produto(produto):
    alerta_html = ""
    if produto["quantidade"] < 5:
        alerta_html = '<div class="estoque-baixo">⚠️ Estoque baixo</div>'
    st.markdown(
        f"""
        <div class="card-produto">
            <div class="titulo-produto">{html.escape(produto['nome'])}</div>
            <div class="texto-produto">ID: {produto['id']}</div>
            <div class="texto-produto">Quantidade: {produto['quantidade']}</div>
            <div class="texto-produto">Preço: R$ {produto['preco']:.2f}</div>
            {alerta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------- 6. FUNÇÕES DE PÁGINA ----------------------
def pagina_agenda():
    aplicar_estilo("agenda")
    st.title("📒 AgendaIA - Sua Agenda Inteligente")
    contatos = carregar_dados(ARQUIVO_AGENDA)
    st.sidebar.write(f"Total de contatos: **{len(contatos)}**")
    aba_add, aba_listar, aba_buscar, aba_remover = st.tabs(["➕ Adicionar", "📋 Listar", "🔍 Buscar", "🗑️ Remover"])
    with aba_add:
        st.subheader("Adicionar novo contato")
        with st.form("formulario_adicionar", clear_on_submit=True):
            nome = st.text_input("Nome*")
            telefone = st.text_input("Telefone*")
            foto = st.file_uploader("Foto do contato", type=["png", "jpg", "jpeg"])
            enviado = st.form_submit_button("Salvar contato")
        if enviado:
            if nome.strip() == "" or telefone.strip() == "":
                st.error("Por favor, preencha pelo menos Nome e Telefone.")
            else:
                caminho_foto = salvar_foto(foto) if foto is not None else ""
                novo_contato = {"id": uuid.uuid4().hex, "nome": nome.strip(), "telefone": telefone.strip(), "foto": caminho_foto}
                contatos.append(novo_contato)
                salvar_dados(ARQUIVO_AGENDA, contatos)
                st.success(f"Contato '{nome}' adicionado com sucesso!")
                st.rerun()
    with aba_listar:
        st.subheader("Todos os contatos cadastrados")
        mostrar_contatos(contatos)
    with aba_buscar:
        st.subheader("Buscar contato por nome")
        termo_busca = st.text_input("Digite o nome do contato")
        if termo_busca.strip()!= "":
            resultados_busca = [c for c in contatos if termo_busca.strip().lower() in c.get("nome", "").lower()]
            st.write(f"**{len(resultados_busca)} contato(s) encontrado(s):**")
            mostrar_contatos(resultados_busca)
        else:
            st.info("Digite um nome no campo acima para iniciar a busca.")
    with aba_remover:
        st.subheader("Remover um contato")
        if len(contatos) == 0:
            st.info("Nenhum contato cadastrado para remover.")
        else:
            opcoes = {f"{c.get('nome', 'Sem nome')} - {c.get('telefone', '-')}" : c["id"] for c in contatos}
            escolha = st.selectbox("Selecione o contato que deseja remover:", list(opcoes.keys()))
            if st.button("Remover contato selecionado"):
                id_escolhido = opcoes[escolha]
                contato_removido = next(c for c in contatos if c["id"] == id_escolhido)
                if contato_removido.get("foto") and os.path.exists(contato_removido["foto"]):
                    os.remove(contato_removido["foto"])
                contatos = [c for c in contatos if c["id"]!= id_escolhido]
                salvar_dados(ARQUIVO_AGENDA, contatos)
                st.success("Contato removido com sucesso!")
                st.rerun()

def pagina_zaplang():
    aplicar_estilo("zaplang")
    st.title("🗣️ Mini Linguagem ZapLang")
    st.write("Digite comandos ZapLang e execute seu programa.")
    nome_programa = st.text_input("Nome do programa:")
    codigo = st.text_area(label="Digite seu código ZapLang:", height=200, value='SET x 10\nADD x 5\nPRINT "x vale"\nPRINT x\nLOOP 3 PRINT "oi"\n')
    coluna_salvar, coluna_executar = st.columns(2)
    with coluna_salvar:
        if st.button("💾 Salvar Programa"):
            if nome_programa.strip():
                programas = carregar_dados(ARQUIVO_ZAPLANG)
                programas.append({"id_uuid": str(uuid.uuid4()), "nome_programa": nome_programa, "codigo": codigo})
                salvar_dados(ARQUIVO_ZAPLANG, programas)
                st.success("Programa salvo com sucesso!")
            else:
                st.warning("Informe um nome para o programa.")
    with coluna_executar:
        executar_clicado = st.button("▶️ Executar")
    if executar_clicado:
        st.subheader("Saída")
        mostrar_resultado_zaplang(interpretar(codigo))

def pagina_estoque():
    aplicar_estilo("estoque")
    st.title("📦 Controle de Estoque")
    produtos = carregar_dados(ARQUIVO_ESTOQUE)
    aba1, aba2, aba3 = st.tabs(["➕ Cadastrar Produto", "📋 Listar Produtos", "🔄 Entrada / Saída"])
    with aba1:
        st.subheader("Cadastrar Produto")
        nome = st.text_input("Nome do produto")
        quantidade = st.number_input("Quantidade", min_value=0, step=1)
        preco = st.number_input("Preço", min_value=0.0, step=0.01, format="%.2f")
        if st.button("💾 Salvar Produto"):
            if nome.strip():
                produtos.append({"id": str(uuid.uuid4()), "nome": nome, "quantidade": int(quantidade), "preco": float(preco)})
                salvar_dados(ARQUIVO_ESTOQUE, produtos)
                st.success("Produto cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe o nome do produto.")
    with aba2:
        st.subheader("Produtos Cadastrados")
        if not produtos:
            st.info("Nenhum produto cadastrado.")
        else:
            for produto in produtos:
                renderizar_card_produto(produto)
    with aba3:
        st.subheader("Entrada e Saída")
        if not produtos:
            st.info("Cadastre produtos primeiro.")
        else:
            nomes_produtos = [produto["nome"] for produto in produtos]
            produto_selecionado_nome = st.selectbox("Selecione o produto", nomes_produtos)
            operacao = st.radio("Operação", ["Entrada", "Saída"])
            quantidade_movimento = st.number_input("Quantidade", min_value=1, step=1)
            if st.button("Atualizar Estoque"):
                produto = next(p for p in produtos if p["nome"] == produto_selecionado_nome)
                if operacao == "Entrada":
                    produto["quantidade"] += int(quantidade_movimento)
                    salvar_dados(ARQUIVO_ESTOQUE, produtos)
                    st.success("Estoque atualizado!")
                    st.rerun()
                else:
                    if produto["quantidade"] >= quantidade_movimento:
                        produto["quantidade"] -= int(quantidade_movimento)
                        salvar_dados(ARQUIVO_ESTOQUE, produtos)
                        st.success("Saída registrada!")
                        st.rerun()
                    else:
                        st.error("Quantidade insuficiente no estoque!")

# ---------------------- 7. MENU + ROTEAMENTO ----------------------
menu = st.sidebar.selectbox("Menu", ["📒 Agenda", "🗣️ Mini Linguagem", "📦 Estoque"])

if menu == "📒 Agenda":
    pagina_agenda()
elif menu == "🗣️ Mini Linguagem":
    pagina_zaplang()
elif menu == "📦 Estoque":
    pagina_estoque()
