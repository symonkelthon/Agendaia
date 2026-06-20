import streamlit as st, os, json, uuid, html, pandas as pd

st.set_page_config(page_title="Sistema Multi-Função", page_icon="🧩", layout="wide")

# Arquivos e pasta
ARQUIVOS = {"agenda": "agenda.json", "zaplang": "mini_linguagem.json", "estoque": "estoque.json"}
PASTA_FOTOS = "fotos"
os.makedirs(PASTA_FOTOS, exist_ok=True)

# Cores de cada módulo
CORES = {
    "agenda": ("#1f4068", "#1b6ca8", "#2596be"),
    "zaplang": ("#4b0082", "#6a0dad", "#8a2be2"),
    "estoque": ("#00c853", "#00acc1", "#1e88e5")
}

def carregar(arq): return json.load(open(arq, "r", encoding="utf-8")) if os.path.exists(arq) else []
def salvar(arq, dados): json.dump(dados, open(arq, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def aplicar_css(tema):
    c1, c2, c3 = CORES[tema]
    st.markdown(f"<style>.stApp{{background:linear-gradient(135deg,{c1},{c2},{c3})}} h1,h2,p{{color:white!important}}</style>", unsafe_allow_html=True)

def salvar_foto(foto):
    nome = f"{uuid.uuid4().hex}{os.path.splitext(foto.name)[1]}"
    caminho = os.path.join(PASTA_FOTOS, nome)
    open(caminho, "wb").write(foto.getbuffer())
    return caminho

# ZAPLANG - Mini linguagem
def executar_zaplang(codigo):
    vars, saida = {}, []
    for i, linha in enumerate(codigo.split("\n"), 1):
        partes = linha.strip().split()
        if not partes: continue
        cmd = partes[0].upper()
        try:
            if cmd == "PRINT":
                resto = linha[6:].strip()
                if resto.startswith('"'): saida.append(("ok", resto[1:-1]))
                elif resto in vars: saida.append(("ok", str(vars[resto])))
                else: saida.append(("erro", f"Linha {i}: variável '{resto}' não existe"))
            elif cmd == "SET":
                vars[partes[1]] = int(partes[2])
                saida.append(("ok", f"{partes[1]} = {partes[2]}"))
            elif cmd in ("ADD", "SUB"):
                delta = int(partes[2]) * (1 if cmd=="ADD" else -1)
                vars[partes[1]] += delta
                saida.append(("ok", f"{partes[1]} = {vars[partes[1]]}"))
            elif cmd == "LOOP":
                for _ in range(int(partes[1])):
                    saida.append(("ok", linha[linha.find("PRINT")+6:].strip()[1:-1]))
            else: saida.append(("erro", f"Linha {i}: comando '{cmd}' desconhecido"))
        except Exception as e:
            saida.append(("erro", f"Linha {i}: {e}"))
    return saida

# AGENDA
def pagina_agenda():
    aplicar_css("agenda")
    st.title("📒 AgendaIA")
    contatos = carregar(ARQUIVOS["agenda"])
    st.sidebar.write(f"Total: **{len(contatos)}** contatos")

    aba = st.tabs(["➕ Adicionar", "📋 Listar", "🔍 Buscar", "🗑️ Remover"])

    with aba[0]:
        with st.form("add", clear_on_submit=True):
            nome, tel, foto = st.text_input("Nome*"), st.text_input("Telefone*"), st.file_uploader("Foto", ["png","jpg"])
            if st.form_submit_button("Salvar") and nome and tel:
                contatos.append({"id": uuid.uuid4().hex, "nome": nome, "telefone": tel, "foto": salvar_foto(foto) if foto else ""})
                salvar(ARQUIVOS["agenda"], contatos); st.success("Salvo!"); st.rerun()

    with aba[1]:
        st.dataframe(pd.DataFrame([{"Nome":c["nome"],"Telefone":c["telefone"]} for c in contatos]), use_container_width=True)
        for c in contatos:
            with st.expander(c["nome"]):
                col1, col2 = st.columns([1,3])
                col1.image(c["foto"], width=100) if c.get("foto") and os.path.exists(c["foto"]) else col1.write("Sem foto")
                col2.write(f"**Telefone:** {c['telefone']}")

    with aba[2]:
        busca = st.text_input("Buscar nome")
        if busca: st.write(f"**{len([c for c in contatos if busca.lower() in c['nome'].lower()])} encontrado(s):**")

    with aba[3]:
        if contatos:
            escolha = st.selectbox("Remover:", [f"{c['nome']} - {c['telefone']}" for c in contatos])
            if st.button("Remover"):
                id_rem = contatos[[f"{c['nome']} - {c['telefone']}" for c in contatos].index(escolha)]["id"]
                contatos = [c for c in contatos if c["id"]!= id_rem]; salvar(ARQUIVOS["agenda"], contatos); st.success("Removido!"); st.rerun()

# ESTOQUE
def pagina_estoque():
    aplicar_css("estoque")
    st.title("📦 Estoque")
    produtos = carregar(ARQUIVOS["estoque"])
    aba = st.tabs(["➕ Cadastrar", "📋 Listar", "🔄 Movimentar"])

    with aba[0]:
        nome, qtd, preco = st.text_input("Nome"), st.number_input("Qtd", 0), st.number_input("Preço", 0.0, step=0.01)
        if st.button("Salvar") and nome:
            produtos.append({"id": str(uuid.uuid4()), "nome": nome, "quantidade": int(qtd), "preco": float(preco)})
            salvar(ARQUIVOS["estoque"], produtos); st.success("Produto salvo!"); st.rerun()

    with aba[1]:
        for p in produtos:
            alerta = "⚠️ Estoque baixo" if p["quantidade"] < 5 else ""
            st.markdown(f'<div style="background:white;padding:20px;border-radius:15px;margin:10px 0"><b>{p["nome"]}</b><br>Qtd: {p["quantidade"]}<br>R$ {p["preco"]:.2f}<br>{alerta}</div>', unsafe_allow_html=True)

    with aba[2]:
        if produtos:
            prod = st.selectbox("Produto", [p["nome"] for p in produtos])
            op, qtd = st.radio("Operação", ["Entrada","Saída"]), st.number_input("Qtd", 1)
            if st.button("Atualizar"):
                p = next(x for x in produtos if x["nome"]==prod)
                p["quantidade"] += qtd if op=="Entrada" else -qtd
                salvar(ARQUIVOS["estoque"], produtos); st.success("Atualizado!"); st.rerun()

# ZAPLANG
def pagina_zaplang():
    aplicar_css("zaplang")
    st.title("🗣️ ZapLang")
    codigo = st.text_area("Código:", 'SET x 10\nADD x 5\nPRINT x\nLOOP 3 PRINT "oi"', height=200)
    if st.button("▶️ Executar"):
        for tipo, texto in executar_zaplang(codigo):
            classe = "background:#ff4d4d33" if tipo=="erro" else "background:#ffffff1a"
            st.markdown(f'<div style="{classe};padding:10px;border-radius:10px;margin:5px 0;color:white">{texto}</div>', unsafe_allow_html=True)

# Menu
menu = st.sidebar.selectbox("Menu", ["📒 Agenda", "🗣️ ZapLang", "📦 Estoque"])
{"📒 Agenda": pagina_agenda, "🗣️ ZapLang": pagina_zaplang, "📦 Estoque": pagina_estoque}[menu]()
