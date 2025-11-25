import streamlit as st
import google.generativeai as genai
from textwrap import dedent

# -------------------------------------------------------------
# Configuração da página
# -------------------------------------------------------------
st.set_page_config(page_title="Planejador de Fim de Semana", layout="centered")

st.title("🗺️ Planejador de Fim de Semana")
st.write("Receba um roteiro de um dia (sábado) baseado na sua cidade e na vibe desejada.")

# -------------------------------------------------------------
# Configura API Key
# -------------------------------------------------------------
if "AI_STUDIO_API_KEY" not in st.secrets:
    st.error("❌ Adicione AI_STUDIO_API_KEY nos Secrets do Streamlit Cloud.")
    st.stop()
else:
    genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

# -------------------------------------------------------------
# Inputs
# -------------------------------------------------------------
cidade = st.text_input("Cidade (ex: São Paulo, SP)")
vibe = st.selectbox("Vibe", ["Relaxante", "Cultural", "Aventura", "Gastronômico", "Romântico", "Com crianças"])

col1, col2 = st.columns(2)
with col1:
    pessoas = st.number_input("Número de pessoas", min_value=1, value=1)
with col2:
    tempo = st.selectbox("Transporte", ["Caminhada/Transporte público", "Carro", "Sem preferência"])

extra = st.text_area("Preferências / Restrições (opcional)")


# -------------------------------------------------------------
# Função que monta o prompt
# -------------------------------------------------------------
def build_prompt(cidade_input, vibe_input, pessoas_input, tempo_input, extra_input):
    return dedent(f"""
    Você é um planejador de roteiros local.
    Crie um roteiro de um dia (sábado) para alguém na cidade de {cidade_input}, com vibe {vibe_input}.

    Divida o roteiro em:
    - MANHÃ
    - TARDE
    - NOITE

    Para cada período, inclua:
    • Atividade
    • Horário sugerido
    • Descrição (2–3 frases)
    • Dica prática

    Adaptar para {pessoas_input} pessoa(s).
    Transporte preferido: {tempo_input}.
    Restrições / preferências: {extra_input or "Nenhuma"}.

    Estilo: objetivo, fácil de entender e amigável.
    """)

# -------------------------------------------------------------
# Função que chama o Gemini corretamente
# -------------------------------------------------------------
def gerar_roteiro(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        response = model.generate_content(prompt)

        return response.text or "⚠️ Modelo retornou resposta vazia."

    except Exception as e:
        return f"❌ Erro ao gerar roteiro: {e}"


# -------------------------------------------------------------
# Botão
# -------------------------------------------------------------
if st.button("Gerar roteiro"):
    if not cidade.strip():
        st.warning("⚠️ Por favor, informe a cidade.")
    else:
        with st.spinner("Gerando roteiro..."):
            texto_prompt = build_prompt(cidade, vibe, pessoas, tempo, extra)
            resultado = gerar_roteiro(texto_prompt)

        st.markdown("### 📝 Roteiro gerado")
        st.write(resultado)

        with st.expander("Ver texto puro"):
            st.code(resultado)


st.markdown("---")
st.caption("App criado para atividade: IA + Streamlit.")
