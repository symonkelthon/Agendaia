"""
Interpretador da Linguagem SK - Streamlit
Comandos: SET, ADD, SUB, PRINT, RODAR
"""

import streamlit as st

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Interpretador SK",
    page_icon="💻",
    layout="centered"
)

# ─────────────────────────────────────────────
# LÓGICA DO INTERPRETADOR
# ─────────────────────────────────────────────

class InterpretadorSK:
    def __init__(self):
        self.variaveis = {}
        self.saida = []

    def executar(self, codigo: str):
        """Processa o bloco de código linha por linha."""
        self.variaveis = {}  # Reseta as variáveis a cada execução
        self.saida = []      # Limpa a saída anterior
        
        linhas = codigo.strip().split("\n")
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if not linha or linha.startswith("#"):  # Ignora linhas vazias ou comentários
                continue
                
            partes = linha.split()
            comando = partes[0].upper()
            
            try:
                if comando == "SET":
                    # SET x 10
                    var = partes[1]
                    val = float(partes[2])
                    self.variaveis[var] = val
                    
                elif comando == "ADD":
                    # ADD x 5
                    var = partes[1]
                    val = float(partes[2])
                    if var in self.variaveis:
                        self.variaveis[var] += val
                    else:
                        self.saida.append(f"ERRO (Linha {i+1}): Variável '{var}' não definida.")
                        
                elif comando == "SUB":
                    # SUB x 3
                    var = partes[1]
                    val = float(partes[2])
                    if var in self.variaveis:
                        self.variaveis[var] -= val
                    else:
                        self.saida.append(f"ERRO (Linha {i+1}): Variável '{var}' não definida.")
                        
                elif comando == "PRINT":
                    # PRINT x
                    var = partes[1]
                    if var in self.variaveis:
                        # Formata para inteiro se não houver casas decimais
                        valor = self.variaveis[var]
                        valor_str = int(valor) if valor.is_integer() else valor
                        self.saida.append(f"> {var} = {valor_str}")
                    else:
                        self.saida.append(f"ERRO (Linha {i+1}): Variável '{var}' não definida.")
                
                elif comando == "RODAR":
                    # O comando RODAR apenas sinaliza o fim ou execução no Streamlit
                    pass
                
                else:
                    self.saida.append(f"ERRO (Linha {i+1}): Comando '{comando}' desconhecido.")
                    
            except (IndexError, ValueError):
                self.saida.append(f"ERRO (Linha {i+1}): Sintaxe inválida no comando '{linha}'.")

        return self.saida

# ─────────────────────────────────────────────
# INTERFACE STREAMLIT
# ─────────────────────────────────────────────

st.title("💻 Interpretador Mini Linguagem SK")
st.markdown("""
### Comandos Disponíveis:
- `SET x 10` : Define o valor da variável.
- `ADD x 5`  : Soma um valor à variável.
- `SUB x 3`  : Subtrai um valor da variável.
- `PRINT x`  : Mostra o valor da variável.
- `RODAR`    : Executa o código abaixo.
""")

# Área de texto para digitar o código
codigo_padrao = """SET x 10
ADD x 5
SUB x 3
PRINT x
RODAR"""

codigo_input = st.text_area("Digite seu código SK aqui:", value=codigo_padrao, height=200)

if st.button("🚀 RODAR"):
    interpretador = InterpretadorSK()
    resultados = interpretador.executar(codigo_input)
    
    st.subheader("Console de Saída:")
    if resultados:
        for r in resultados:
            if "ERRO" in r:
                st.error(r)
            else:
                st.success(r)
    else:
        st.info("Código executado. Nenhuma saída PRINT gerada.")

st.divider()
st.caption("Nota: O comando RODAR no final é opcional nesta interface, pois o botão já executa todo o bloco.")
