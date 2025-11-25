import streamlit as st
import google.generativeai as genai

# ------------------------------------------------------------
# CONFIGURAÇÃO
# ------------------------------------------------------------
AI_STUDIO_API_KEY = "AIzaSyBhxcIutyJe4gFXh-1bOg13MYXDubm6h9Y"
genai.configure(api_key=AI_STUDIO_API_KEY)

# ------------------------------------------------------------
# FUNÇÃO PARA GERAR ROTEIRO
# ------------------------------------------------------------
def gerar_roteiro(texto):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(texto)
        return response.text
    except Exception as e:
        return f"❌ Erro ao gerar roteiro:\n{str(e)}"

# ------------------------------------------------------------
# INTERFACE STREAMLIT
# ------------------------------------------------------------
st.title("Gerador de Roteiros – AWS")

entrada = st.text_area("Digite o tema do roteiro:")

if st.button("Gerar Roteiro"):
    if entrada.strip() == "":
        st.warning("Digite algum conteúdo primeiro!")
    else:
        saida = gerar_roteiro(entrada)
        st.write("### Resultado:")
        st.write(saida)
