import streamlit as st
from transformers import pipeline
import time

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisador de Sentimentos",
    page_icon="🧠",
    layout="centered",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0f0f13; color: #e8e8e8; }
h1, h2, h3 { color: #ffffff; font-weight: 700; letter-spacing: -0.02em; }

.titulo {
    font-size: 2.4rem; font-weight: 700; letter-spacing: -0.03em;
    line-height: 1.1; margin-bottom: 0.25rem; color: #ffffff;
}
.subtitulo {
    font-size: 0.95rem; color: #666; margin-bottom: 2rem;
    font-weight: 400; letter-spacing: 0.04em; text-transform: uppercase;
}
.card-resultado {
    border-radius: 16px; padding: 2rem; margin-top: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08); text-align: center;
}
.card-positivo { background: linear-gradient(135deg, #0d2b1e, #0a1f16); border-color: #1a5c38; }
.card-negativo { background: linear-gradient(135deg, #2b0d0d, #1f0a0a); border-color: #5c1a1a; }
.card-neutro   { background: linear-gradient(135deg, #1a1a2b, #131320); border-color: #2e2e5a; }

.emoji-grande { font-size: 3.5rem; margin-bottom: 0.5rem; display: block; }
.label-sentimento { font-size: 1.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.25rem; }
.label-positivo { color: #4ade80; }
.label-negativo { color: #f87171; }
.label-neutro   { color: #818cf8; }

.score-text {
    font-size: 0.85rem; color: #888; text-transform: uppercase;
    letter-spacing: 0.08em; margin-bottom: 1rem;
}
.barra-container {
    background: rgba(255,255,255,0.07); border-radius: 100px;
    height: 8px; width: 80%; margin: 0 auto 1.5rem; overflow: hidden;
}
.barra-fill-pos { background: linear-gradient(90deg, #22c55e, #4ade80); height: 100%; border-radius: 100px; }
.barra-fill-neg { background: linear-gradient(90deg, #ef4444, #f87171); height: 100%; border-radius: 100px; }
.barra-fill-neu { background: linear-gradient(90deg, #6366f1, #818cf8); height: 100%; border-radius: 100px; }

.scores-grid { display: flex; justify-content: center; gap: 2rem; margin-top: 1.2rem; }
.score-item  { text-align: center; }
.score-valor { font-size: 1.2rem; font-weight: 600; display: block; color: #e8e8e8; }
.score-nome  { font-size: 0.72rem; color: #555; text-transform: uppercase; letter-spacing: 0.06em; }

.aviso-modelo {
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 10px; padding: 0.75rem 1rem; font-size: 0.83rem; color: #a5b4fc;
    margin-bottom: 1.2rem; text-align: center;
}
.footer {
    text-align: center; margin-top: 3rem; font-size: 0.78rem;
    color: #444; letter-spacing: 0.04em;
}
div[data-testid="stTextArea"] textarea {
    background: #161620 !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #e8e8e8 !important;
    font-family: 'Space Grotesk', sans-serif !important; font-size: 1rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(255,255,255,0.3) !important;
    box-shadow: 0 0 0 2px rgba(255,255,255,0.05) !important;
}
div[data-testid="stButton"] button {
    background: #ffffff !important; color: #0f0f13 !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    letter-spacing: 0.02em !important; border-radius: 10px !important;
    border: none !important; padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important; width: 100% !important; transition: opacity 0.2s !important;
}
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Carrega o modelo (com cache para não recarregar a cada clique) ───────────
@st.cache_resource
def carregar_modelo():
    # Modelo multilíngue treinado em 8 idiomas incluindo português
    # Fonte: Cardiff NLP · HuggingFace · carrega uma vez só
    return pipeline(
        "text-classification",
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        top_k=None,
    )

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<div class="titulo">Analisador de<br>Sentimentos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Inteligência Artificial · NLP · Transformers · PT-BR</div>', unsafe_allow_html=True)

st.markdown("""
<div class="aviso-modelo">
🤖 Modelo: <strong>XLM-RoBERTa</strong> multilíngue · funciona em português, inglês, espanhol e mais 5 idiomas
</div>
""", unsafe_allow_html=True)

# ── Exemplos clicáveis ──────────────────────────────────────────────────────
exemplos = [
    "O atendimento foi excelente e muito rápido!",
    "Produto péssimo, não recomendo a ninguém.",
    "O relatório foi entregue na terça-feira.",
    "Estou muito feliz com os resultados!",
    "A aula foi mais ou menos, nem boa nem ruim.",
    "Que serviço horrível, fui completamente ignorado.",
]

st.markdown("**Exemplos rápidos — clique para usar:**")
cols = st.columns(3)
for i, ex in enumerate(exemplos):
    resumo = ex[:26] + "…" if len(ex) > 26 else ex
    if cols[i % 3].button(resumo, key=f"ex_{i}"):
        st.session_state["texto_input"] = ex

# ── Campo de entrada ────────────────────────────────────────────────────────
texto = st.text_area(
    "Digite ou cole um texto:",
    value=st.session_state.get("texto_input", ""),
    placeholder="Ex: O curso foi incrível, aprendi muito!",
    height=120,
    key="texto_input",
    label_visibility="collapsed",
)

analisar = st.button("Analisar sentimento →")

# ── Análise ─────────────────────────────────────────────────────────────────
if analisar:
    texto_limpo = texto.strip()
    if not texto_limpo:
        st.warning("Por favor, digite algum texto antes de analisar.")
    else:
        with st.spinner("Carregando modelo e analisando... (primeira vez pode levar ~30s)"):
            modelo = carregar_modelo()
            resultados = modelo(texto_limpo[:512])[0]  # limite de tokens

        scores = {r["label"]: r["score"] for r in resultados}
        pos = scores.get("Positive", 0)
        neg = scores.get("Negative", 0)
        neu = scores.get("Neutral", 0)

        melhor = max(scores, key=scores.get)
        confianca = scores[melhor]
        pct = int(confianca * 100)

        if melhor == "Positive":
            sentimento, emoji = "Positivo", "😊"
            classe_card, classe_label, classe_barra = "card-positivo", "label-positivo", "barra-fill-pos"
        elif melhor == "Negative":
            sentimento, emoji = "Negativo", "😞"
            classe_card, classe_label, classe_barra = "card-negativo", "label-negativo", "barra-fill-neg"
        else:
            sentimento, emoji = "Neutro", "😐"
            classe_card, classe_label, classe_barra = "card-neutro", "label-neutro", "barra-fill-neu"

        st.markdown(f"""
        <div class="card-resultado {classe_card}">
            <span class="emoji-grande">{emoji}</span>
            <div class="label-sentimento {classe_label}">{sentimento}</div>
            <div class="score-text">Confiança: {pct}%</div>
            <div class="barra-container">
                <div class="{classe_barra}" style="width: {pct}%;"></div>
            </div>
            <div class="scores-grid">
                <div class="score-item">
                    <span class="score-valor">{pos:.0%}</span>
                    <span class="score-nome">Positivo</span>
                </div>
                <div class="score-item">
                    <span class="score-valor">{neu:.0%}</span>
                    <span class="score-nome">Neutro</span>
                </div>
                <div class="score-item">
                    <span class="score-valor">{neg:.0%}</span>
                    <span class="score-nome">Negativo</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📖 Como funciona? (para a aula)"):
            st.markdown(f"""
**XLM-RoBERTa** é um modelo Transformer multilíngue treinado em ~198 idiomas,
com fine-tuning em tweets para classificação de sentimentos em 8 idiomas (incluindo português).

| Classe | Score | Interpretação |
|---|---|---|
| Positivo | `{pos:.3f}` | {pos:.0%} de confiança |
| Neutro   | `{neu:.3f}` | {neu:.0%} de confiança |
| Negativo | `{neg:.3f}` | {neg:.0%} de confiança |

**Por que funciona em português?**
Ao contrário do VADER (dicionário inglês), modelos Transformer aprendem representações
semânticas que generalizam entre idiomas. O modelo foi pré-treinado com dados multilíngues
massivos e ajustado (fine-tuned) em dados rotulados em vários idiomas.

**VADER vs XLM-RoBERTa:**
- VADER → dicionário de palavras, rápido, sem GPU, **só inglês**
- XLM-RoBERTa → rede neural profunda, ~30s na 1ª carga, **multilíngue**, mais preciso
""")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Construído com Python · Streamlit · HuggingFace Transformers<br>
    Modelo: cardiffnlp/twitter-xlm-roberta-base-sentiment · Gerado com IA
</div>
""", unsafe_allow_html=True)
