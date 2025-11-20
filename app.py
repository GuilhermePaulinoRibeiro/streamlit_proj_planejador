import streamlit as st
import google.generativeai as genai
from textwrap import dedent

# 1. Configuração da Página
st.set_page_config(page_title="Planejador de Fim de Semana", layout="centered")

st.title("🗺️ Planejador de Fim de Semana")
st.write("Receba um roteiro de um dia (Sábado) baseado na sua cidade e na vibe desejada.")

# 2. Configuração da API Key (Segurança)
if "AI_STUDIO_API_KEY" not in st.secrets:
    st.error("❌ Adicione AI_STUDIO_API_KEY em Settings → Secrets.")
    st.stop()  # Para a execução se não tiver a chave
else:
    genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

# 3. Entradas do Usuário (Inputs)
cidade = st.text_input("Cidade (ex: São Paulo, SP)")
vibe = st.selectbox("Vibe", ["Relaxante", "Cultural", "Aventura", "Gastronômico", "Romântico", "Com crianças"])

col1, col2 = st.columns(2)
with col1:
    pessoas = st.number_input("Número de pessoas", min_value=1, value=1)
with col2:
    tempo = st.selectbox("Transporte", ["Caminhada/Transporte público", "Carro", "Sem preferência"])

extra = st.text_area("Preferências / Restrições (opcional)")

# 4. Funções do "Cérebro" da Aplicação
def build_prompt(cidade_input, vibe_input, pessoas_input, tempo_input, extra_input):
    return dedent(f"""
    Você é um planejador de roteiros local.
    Crie um roteiro de um dia (sábado) para alguém na cidade de {cidade_input} que deseja uma vibe {vibe_input}.

    - Divida em MANHÃ, TARDE, NOITE
    - Para cada período descreva:
      • Atividade
      • Horário sugerido
      • Descrição (2–3 frases)
      • Dica prática

    Adapte para {pessoas_input} pessoa(s).
    Preferência de transporte: {tempo_input}.
    Restrições/preferências: {extra_input}.
    Escreva de forma objetiva e amigável.
    """)

def gerar_roteiro(prompt):
    # Usando o modelo mais atual (Flash é rápido e eficiente)
    model = genai.GenerativeModel("gemini-1.5-flash")
    resposta = model.generate_content(prompt)
    return resposta.text

# 5. Botão e Exibição do Resultado
if st.button("Gerar roteiro"):
    if not cidade.strip():
        st.warning("⚠️ Por favor, informe a cidade.")
    else:
        with st.spinner("Gerando roteiro..."):
            try:
                # Chamando as funções criadas acima
                prompt_final = build_prompt(cidade, vibe, pessoas, tempo, extra)
                resultado = gerar_roteiro(prompt_final)
                
                st.markdown("### 📝 Roteiro gerado")
                st.write(resultado)
                
                # Opcional: Mostrar o texto puro em um expansor se quiser copiar
                with st.expander("Ver código do texto"):
                    st.code(resultado)
                    
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")

st.markdown("---")
st.caption("App criado para atividade: IA + Streamlit.")
