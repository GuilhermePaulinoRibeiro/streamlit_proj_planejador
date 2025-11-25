import streamlit as st
import google.generativeai as genai
from textwrap import dedent

# -------------------------------------------------------------
# 1. Configuração da página
# -------------------------------------------------------------
st.set_page_config(page_title="Planejador de Fim de Semana", layout="centered")

st.title("🗺️ Planejador de Fim de Semana")
st.write("Receba um roteiro de um dia (sábado) baseado na sua cidade e na vibe desejada.")

# -------------------------------------------------------------
# 2. API Key do Gemini
# -------------------------------------------------------------
if "AI_STUDIO_API_KEY" not in st.secrets:
    st.error("❌ Adicione AI_STUDIO_API_KEY em Settings → Secrets.")
    st.stop()
else:
    genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

# -------------------------------------------------------------
# 3. Inputs do usuário
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
# 4. Construção do prompt
# -------------------------------------------------------------
def build_prompt(cidade_input, vibe_input, pessoas_input, tempo_input, extra_input):
    return dedent(f"""
    Você é um planejador de roteiros local.
    Crie um roteiro de um dia (sábado) para alguém na cidade de {cidade_input} que deseja uma vibe {vibe_input}.

    Divida o roteiro em:
    - MANHÃ
    - TARDE
    - NOITE

    Para cada período, descreva:
    • Atividade
    • Horário sugerido
    • Descrição (2 a 3 frases)
    • Dica prática

    Adapte para {pessoas_input} pessoa(s).
    Preferência de transporte: {tempo_input}.
    Restrições / preferências: {extra_input or "Nenhuma"}.

    Escreva de forma objetiva, organizada e amigável.
    """)


# -------------------------------------------------------------
# 5. Função que chama o Gemini (compatível com 0.7.2)
# -------------------------------------------------------------
def gerar_roteiro(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # IMPORTANTE: na versão 0.7.2 é obrigatório enviar contents como lista
        response = model.generate_content(
            contents=[prompt]
        )

        if hasattr(response, "text"):
            return response.text

        return "⚠️ Resposta inesperada do modelo."

    except Exception as e:
        return f"❌ Erro ao gerar roteiro: {e}"


# -------------------------------------------------------------
# 6. Botão principal
# -------------------------------------------------------------
if st.button("Gerar roteiro"):
    if not cidade.strip():
        st.warning("⚠️ Por favor, informe a cidade.")
    else:
        with st.spinner("Gerando roteiro..."):
            prompt_final = build_prompt(cidade, vibe, pessoas, tempo, extra)
            resultado = gerar_roteiro(prompt_final)

        st.markdown("### 📝 Roteiro gerado")
        st.write(resultado)

        with st.expander("Ver texto puro"):
            st.code(resultado)


st.markdown("---")
st.caption("App criado para atividade: IA + Streamlit.")
