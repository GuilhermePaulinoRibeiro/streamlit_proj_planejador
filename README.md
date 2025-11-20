# Planejador de Fim de Semana (Streamlit + Google AI Studio)

App que gera um roteiro de um dia (sábado) baseado na cidade e vibe escolhida pelo usuário.

## Como rodar localmente
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud
1. Suba este repositório no GitHub.
2. Acesse https://streamlit.io/cloud
3. New App → selecione este repo.
4. Vá em Settings → Secrets:
```
AI_STUDIO_API_KEY = SUA_CHAVE_DO_GOOGLE_AI_STUDIO
```

## Arquivos incluídos
- app.py
- requirements.txt
- README.md
