import streamlit as st
import google.generativeai as genai

st.title("🔍 Modelos disponíveis na API")

genai.configure(api_key=st.secrets["AI_STUDIO_API_KEY"])

try:
    models = genai.list_models()
    for m in models:
        st.write("📌", m.name, "→", m.supported_generation_methods)
except Exception as e:
    st.error(e)
