import streamlit as st
import google.generativeai as genai
from textwrap import dedent

st.set_page_config(page_title="Planejador de Fim de Semana", layout="centered")

st.title("🗺️ Planejador de Fim de Semana")
st.write("Receba um roteiro de um dia (Sábado) baseado na sua cidade e na vibe desejada.")

API_KEY_SECRET_NAME = "AI_STUDIO_API_KEY"

if "AI_STUDIO_API_KEY" not in st.secrets:
    st.warning(
        "Chave de API do AI Studio não encontrada. "
        "Adicione o segredo 'AI_STUDIO_API_KEY' nas configurações do app no Streamlit Cloud."
    )

col1, col2 = st.columns([2, 1])
with col1:
    cidade = st.text_input("Cidade (ex: São Paulo, SP)", value="")
with col2:
    vibe = st.selectbox("Vibe", ["Relaxante", "Cultural", "Aventura", "Gastronômico", "Romântico", "Com crianças"])

pessoas = st.number_input("Número de pessoas", min_value=1, max_value=20, value=1, step=1)
tempo = st.selectbox("Preferência de transporte", ["Caminhada/Transporte público", "Carro", "Sem preferência"])

extra = st.text_area("Preferências / Restrições (opcional)", help="Ex: evitar museus, quer parques, acessível, orçamento baixo...")

def build_prompt(cidade, vibe, pessoas, tempo, extra):
    prompt = dedent(f"""
    Você é um planejador de roteiros local, objetivo e prático. 
    Crie um roteiro de um dia (Sábado) para alguém na cidade de {cidade} que busca uma experiência {vibe}.
    - Divida em 3 partes: Manhã, Tarde, Noite.
    - Para cada parte inclua: Atividade (titulo curto), Horário sugerido, Descrição breve (2-3 frases), Dica prática.
    - Adapte para {pessoas} pessoa(s) e preferência de transporte: {tempo}.
    - Considere as preferências/restrições: {extra}
    - Limite a resposta a 300-500 palavras.
    - Se a cidade for desconhecida, informe.
    """)
    return prompt

def call_gemini(prompt: str, model: str = "gpt-4o-mini"):
    if "AI_STUDIO_API_KEY" not in st.secrets:
        raise RuntimeError("Chave API não encontrada em st.secrets['AI_STUDIO_API_KEY'].")

    genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

    try:
        response = genai.chat.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente útil especializado em roteiros locais."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_output_tokens=800
        )
        if hasattr(response, "candidates"):
            return response.candidates[0].content if response.candidates else str(response)
        if hasattr(response, "output_text"):
            return response.output_text
        return str(response)
    except Exception as e:
        raise RuntimeError(f"Erro ao chamar a API: {e}")

if st.button("Planejar Meu Sábado"):
    if not cidade.strip():
        st.error("Por favor, informe a cidade.")
    else:
        with st.spinner("Gerando roteiro..."):
            prompt = build_prompt(cidade, vibe, pessoas, tempo, extra)
            try:
                resultado = call_gemini(prompt)
                st.markdown("### Resultado")
                st.write(resultado)
                st.code(resultado, language="markdown")
            except Exception as err:
                st.error(f"Ocorreu um erro ao gerar o roteiro: {err}")

st.markdown("---")
st.caption("App criado para atividade de IA + Streamlit.")