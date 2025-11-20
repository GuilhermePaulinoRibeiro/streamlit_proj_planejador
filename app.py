import streamlit as st
import google.generativeai as genai
from textwrap import dedent

st.set_page_config(page_title="Planejador de Fim de Semana", layout="centered")

st.title("🗺️ Planejador de Fim de Semana")
st.write("Receba um roteiro de um dia (Sábado) baseado na sua cidade e na vibe desejada.")

# Chave no Streamlit Secrets
if "AI_STUDIO_API_KEY" not in st.secrets:
    st.error("❌ Adicione AI_STUDIO_API_KEY em Settings → Secrets.")
else:
    genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

# Inputs
cidade = st.text_input("Cidade (ex: São Paulo, SP)")
vibe = st.selectbox("Vibe", ["Relaxante", "Cultural", "Aventura", "Gastronômico", "Romântico", "Com crianças"])
pessoas = st.number_input("Número de pessoas", min_value=1, value=1)
tempo = st.selectbox("Transporte", ["Caminhada/Transporte público", "Carro", "Sem preferência"])
extra = st.text_area("Preferências (opcional)")

def build_prompt():
    return dedent(f"""
    Você é um planejador de roteiros local.
    Crie um roteiro de um dia (sábado) para alguém na cidade de {cidade} que deseja uma vibe {vibe}.

    - Divida em MANHÃ, TARDE, NOITE
    - Para cada período descreva:
      • Atividade
      • Horário sugerido
      • Descrição (2–3 frases)
      • Dica prática

    Adapte para {pessoas} pessoa(s).
    Preferência de transporte: {tempo}.
    Restrições/preferences: {extra}.
    Escreva de forma objetiva e amigável.
    """)

def gerar_roteiro():
    model = genai.GenerativeModel("gemini-pro")
    resposta = model.generate_content(build_prompt())
    return resposta.text

if st.button("Gerar roteiro"):
    if not cidade.strip():
        st.error("Informe a cidade.")
    else:
        with st.spinner("Gerando roteiro..."):
            try:
                resultado = gerar_roteiro()
                st.markdown("### 📝 Roteiro gerado")
                st.write(resultado)
                st.code(resultado)
            except Exception as e:
                st.error(f"Erro: {e}")

st.markdown("---")
st.caption("App criado para atividade: IA + Streamlit.")
