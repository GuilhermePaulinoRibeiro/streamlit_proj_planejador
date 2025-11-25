import streamlit as st
from google import genai

# ------------------------------------------------------------
# CONFIGURAÇÃO
# ------------------------------------------------------------
AI_STUDIO_API_KEY = "AIzaSyBhxcIutyJe4gFXh-1bOg13MYXDubm6h9Y"

client = genai.Client(api_key=AI_STUDIO_API_KEY)

# ------------------------------------------------------------
# FUNÇÃO PARA GERAR ROTEIRO
# ------------------------------------------------------------
def gerar_roteiro(texto):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=texto
        )
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
