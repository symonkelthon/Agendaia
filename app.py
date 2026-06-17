# Importa a biblioteca Streamlit, usada para criar a interface web
import streamlit as st
# Importa a biblioteca os, usada para criar pastas e checar se arquivos existem
import os
# Importa a biblioteca json, usada para salvar e ler os contatos em arquivo
import json
# Importa a biblioteca pandas, usada para montar a tabela de contatos
import pandas as pd
# Importa a biblioteca uuid, usada para criar codigos unicos (ids e nomes de foto)
import uuid

# Guarda o nome do arquivo onde os contatos ficam salvos
ARQUIVO_DADOS = "agenda.json"
# Guarda o nome da pasta onde as fotos ficam salvas
PASTA_FOTOS = "fotos"

# Verifica se a pasta de fotos ainda nao existe no computador
if not os.path.exists(PASTA_FOTOS):
    # Cria a pasta de fotos automaticamente, sem precisar fazer isso na mao
    os.makedirs(PASTA_FOTOS)

# Configura o titulo da aba do navegador, o icone e o layout largo da pagina
st.set_page_config(page_title="AgendaIA", page_icon="📒", layout="wide")


# Funcao responsavel por carregar os contatos salvos no arquivo JSON
def carregar_contatos():
    # Verifica se o arquivo de dados ainda nao foi criado
    if not os.path.exists(ARQUIVO_DADOS):
        # Se o arquivo nao existe, retorna uma lista vazia de contatos
        return []
    # Abre o arquivo JSON em modo de leitura, usando codificacao utf-8 (acentos)
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        # Le o conteudo do arquivo e transforma em uma lista de dicionarios
        dados = json.load(arquivo)
    # Retorna a lista de contatos que foi carregada do arquivo
    return dados


# Funcao responsavel por salvar a lista de contatos dentro do arquivo JSON
def salvar_contatos(lista_contatos):
    # Abre o arquivo JSON em modo de escrita, usando codificacao utf-8 (acentos)
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        # Escreve a lista de contatos formatada e mantendo os acentos corretos
        json.dump(lista_contatos, arquivo, indent=4, ensure_ascii=False)


# Funcao responsavel por salvar a foto enviada pelo usuario na pasta fotos
def salvar_foto(arquivo_foto):
    # Pega a extensao original do arquivo enviado, por exemplo .png ou .jpg
    extensao = os.path.splitext(arquivo_foto.name)[1]
    # Cria um nome unico para a foto, evitando que duas fotos tenham o mesmo nome
    nome_unico = f"{uuid.uuid4().hex}{extensao}"
    # Monta o caminho completo de onde a foto vai ser salva
    caminho_completo = os.path.join(PASTA_FOTOS, nome_unico)
    # Abre um novo arquivo no caminho escolhido, em modo de escrita binaria
    with open(caminho_completo, "wb") as f:
        # Escreve o conteudo da foto enviada dentro do novo arquivo criado
        f.write(arquivo_foto.getbuffer())
    # Retorna o caminho da foto salva, para guardarmos junto com o contato
    return caminho_completo


# Carrega a lista de contatos do arquivo e guarda na variavel "contatos"
contatos = carregar_contatos()

# Mostra o titulo do app dentro da barra lateral
st.sidebar.title("📒 AgendaIA")
# Mostra um texto pequeno, explicando o que o app faz, abaixo do titulo
st.sidebar.caption("Sua agenda de contatos inteligente")
# Cria o menu de opcoes na barra lateral, para o usuario escolher a acao desejada
menu = st.sidebar.radio(
    "Escolha uma opcao:",
    ["➕ Adicionar contato", "📋 Listar contatos", "🔍 Buscar contato", "🗑️ Remover contato"],
)
# Cria uma linha divisoria na barra lateral, so para organizar visualmente
st.sidebar.markdown("---")
# Mostra na barra lateral quantos contatos existem cadastrados no momento
st.sidebar.write(f"Total de contatos: **{len(contatos)}**")

# Mostra o titulo principal no topo da pagina central
st.title("📒 AgendaIA - Sua Agenda Inteligente")


# Funcao que mostra uma lista de contatos em formato de tabela, com fotos
def mostrar_contatos(lista):
    # Verifica se a lista recebida esta vazia
    if len(lista) == 0:
        # Mostra um aviso de que nao ha contatos para exibir
        st.info("Nenhum contato encontrado.")
        # Encerra a funcao aqui, pois nao ha nada mais para mostrar
        return
    # Monta uma lista somente com os dados de texto, sem o caminho da foto
    dados_tabela = [
        {"Nome": c["nome"], "Telefone": c["telefone"], "Email": c["email"]}
        for c in lista
    ]
    # Transforma essa lista de dicionarios em uma tabela usando o pandas
    tabela = pd.DataFrame(dados_tabela)
    # Mostra a tabela na tela, ocupando toda a largura disponivel
    st.dataframe(tabela, use_container_width=True)
    # Mostra um subtitulo antes da secao de fotos dos contatos
    st.subheader("Fotos dos contatos")
    # Repete o processo abaixo para cada contato que esta na lista
    for contato in lista:
        # Cria um bloco que pode ser aberto e fechado, com o nome do contato
        with st.expander(contato["nome"]):
            # Divide o bloco em duas colunas: uma estreita para foto, outra larga para dados
            coluna_foto, coluna_dados = st.columns([1, 3])
            # Dentro da coluna reservada para a foto
            with coluna_foto:
                # Verifica se o contato possui foto cadastrada e se o arquivo ainda existe
                if contato["foto"] and os.path.exists(contato["foto"]):
                    # Mostra a foto do contato com largura fixa de 100 pixels
                    st.image(contato["foto"], width=100)
                else:
                    # Avisa que esse contato nao possui foto cadastrada
                    st.write("Sem foto")
            # Dentro da coluna reservada para os dados de texto
            with coluna_dados:
                # Mostra o telefone do contato em destaque
                st.write(f"**Telefone:** {contato['telefone']}")
                # Mostra o email do contato em destaque
                st.write(f"**Email:** {contato['email']}")


# Verifica se a opcao escolhida no menu foi "Adicionar contato"
if menu == "➕ Adicionar contato":
    # Mostra um subtitulo descrevendo essa secao da pagina
    st.subheader("Adicionar novo contato")
    # Cria um formulario, que so envia os dados quando o botao for clicado
    with st.form("formulario_adicionar", clear_on_submit=True):
        # Campo de texto para o usuario digitar o nome do contato
        nome = st.text_input("Nome*")
        # Campo de texto para o usuario digitar o telefone do contato
        telefone = st.text_input("Telefone*")
        # Campo de texto para o usuario digitar o email do contato
        email = st.text_input("Email")
        # Campo para o usuario enviar uma foto, aceitando apenas tipos de imagem
        foto = st.file_uploader("Foto do contato", type=["png", "jpg", "jpeg"])
        # Botao que confirma e envia os dados do formulario
        enviado = st.form_submit_button("Salvar contato")

    # Verifica se o botao "Salvar contato" foi clicado pelo usuario
    if enviado:
        # Verifica se os campos obrigatorios (nome e telefone) estao vazios
        if nome.strip() == "" or telefone.strip() == "":
            # Mostra uma mensagem de erro avisando que faltam dados obrigatorios
            st.error("Por favor, preencha pelo menos Nome e Telefone.")
        else:
            # Define o caminho da foto como vazio, caso nenhuma foto seja enviada
            caminho_foto = ""
            # Verifica se o usuario realmente enviou um arquivo de foto
            if foto is not None:
                # Chama a funcao que salva a foto na pasta fotos e devolve o caminho
                caminho_foto = salvar_foto(foto)
            # Monta um dicionario com todos os dados do novo contato
            novo_contato = {
                "id": uuid.uuid4().hex,
                "nome": nome.strip(),
                "telefone": telefone.strip(),
                "email": email.strip(),
                "foto": caminho_foto,
            }
            # Adiciona o novo contato dentro da lista de contatos em memoria
            contatos.append(novo_contato)
            # Salva a lista atualizada de contatos dentro do arquivo JSON
            salvar_contatos(contatos)
            # Mostra uma mensagem de sucesso confirmando que o contato foi salvo
            st.success(f"Contato '{nome}' adicionado com sucesso!")
            # Recarrega a pagina, para que os dados novos apareçam atualizados
            st.rerun()

# Verifica se a opcao escolhida no menu foi "Listar contatos"
elif menu == "📋 Listar contatos":
    # Mostra um subtitulo descrevendo essa secao da pagina
    st.subheader("Todos os contatos cadastrados")
    # Chama a funcao que mostra a tabela e as fotos de todos os contatos
    mostrar_contatos(contatos)

# Verifica se a opcao escolhida no menu foi "Buscar contato"
elif menu == "🔍 Buscar contato":
    # Mostra um subtitulo descrevendo essa secao da pagina
    st.subheader("Buscar contato por nome")
    # Campo de texto onde o usuario digita o nome que deseja procurar
    termo_busca = st.text_input("Digite o nome do contato")
    # Verifica se o usuario realmente digitou algo no campo de busca
    if termo_busca.strip() != "":
        # Filtra os contatos cujo nome contem o texto digitado, ignorando maiusculas
        resultados = [
            c for c in contatos if termo_busca.strip().lower() in c["nome"].lower()
        ]
        # Mostra quantos contatos foram encontrados com esse termo de busca
        st.write(f"**{len(resultados)} contato(s) encontrado(s):**")
        # Chama a funcao que mostra a tabela e as fotos dos resultados encontrados
        mostrar_contatos(resultados)
    else:
        # Avisa o usuario que ele precisa digitar um nome para iniciar a busca
        st.info("Digite um nome no campo acima para iniciar a busca.")

# Verifica se a opcao escolhida no menu foi "Remover contato"
elif menu == "🗑️ Remover contato":
    # Mostra um subtitulo descrevendo essa secao da pagina
    st.subheader("Remover um contato")
    # Verifica se a lista de contatos esta vazia
    if len(contatos) == 0:
        # Avisa que nao existem contatos cadastrados para serem removidos
        st.info("Nenhum contato cadastrado para remover.")
    else:
        # Monta um dicionario ligando "nome - telefone" ao id de cada contato
        opcoes = {f"{c['nome']} - {c['telefone']}": c["id"] for c in contatos}
        # Cria uma caixa de selecao mostrando as opcoes de contatos disponiveis
        escolha = st.selectbox("Selecione o contato que deseja remover:", list(opcoes.keys()))
        # Botao que confirma a remocao do contato escolhido na caixa de selecao
        if st.button("Remover contato selecionado"):
            # Pega o id do contato escolhido, usando o dicionario de opcoes
            id_escolhido = opcoes[escolha]
            # Procura, dentro da lista, o contato completo que tem esse id
            contato_removido = next(c for c in contatos if c["id"] == id_escolhido)
            # Verifica se esse contato tem foto salva e se o arquivo ainda existe
            if contato_removido["foto"] and os.path.exists(contato_removido["foto"]):
                # Remove o arquivo de foto do disco, para nao deixar lixo na pasta fotos
                os.remove(contato_removido["foto"])
            # Cria uma nova lista de contatos, sem o contato que foi escolhido
            contatos = [c for c in contatos if c["id"] != id_escolhido]
            # Salva essa nova lista, ja sem o contato removido, no arquivo JSON
            salvar_contatos(contatos)
            # Mostra uma mensagem de sucesso confirmando a remocao do contato
            st.success("Contato removido com sucesso!")
            # Recarrega a pagina, para que a lista exibida fique atualizada
            st.rerun()
