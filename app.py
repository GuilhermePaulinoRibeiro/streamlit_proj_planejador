import streamlit as st
import google.generativeai as genai

# ---------------------------------------
# CONFIG
# ---------------------------------------
genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

# ---------------------------------------
# GERAR ROTEIRO
# ---------------------------------------
def gerar_roteiro(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        resp = model.generate_content(prompt)
        return resp.text

    except Exception as e:
        return f"❌ Erro ao gerar roteiro:\n{e}"

# ---------------------------------------
# UI
# ---------------------------------------
st.title("Planejador de Fim de Semana")

cidade = st.text_input("Cidade:")
vibe = st.selectbox("Vibe", ["Relaxante", "Cultural", "Aventura"])

if st.button("Gerar"):
    if not cidade:
        st.warning("Digite uma cidade.")
    else:
        prompt = f"Crie um roteiro para sábado na cidade de {cidade} com vibe {vibe}."
        st.write(gerar_roteiro(prompt))
