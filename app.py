import streamlit as st
import requests
import time

st.set_page_config(page_title="Analisador de Sentimentos", page_icon="🧠", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0f0f13; color: #e8e8e8; }
.titulo { font-size: 2.4rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1; margin-bottom: 0.25rem; color: #ffffff; }
.subtitulo { font-size: 0.95rem; color: #666; margin-bottom: 2rem; font-weight: 400; letter-spacing: 0.04em; text-transform: uppercase; }
.card-resultado { border-radius: 16px; padding: 2rem; margin-top: 1.5rem; border: 1px solid rgba(255,255,255,0.08); text-align: center; }
.card-positivo { background: linear-gradient(135deg, #0d2b1e, #0a1f16); border-color: #1a5c38; }
.card-negativo { background: linear-gradient(135deg, #2b0d0d, #1f0a0a); border-color: #5c1a1a; }
.card-neutro   { background: linear-gradient(135deg, #1a1a2b, #131320); border-color: #2e2e5a; }
.emoji-grande { font-size: 3.5rem; margin-bottom: 0.5rem; display: block; }
.label-sentimento { font-size: 1.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.25rem; }
.label-positivo { color: #4ade80; }
.label-negativo { color: #f87171; }
.label-neutro   { color: #818cf8; }
.score-text { font-size: 0.85rem; color: #888; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem; }
.barra-container { background: rgba(255,255,255,0.07); border-radius: 100px; height: 8px; width: 80%; margin: 0 auto 1.5rem; overflow: hidden; }
.barra-fill-pos { background: linear-gradient(90deg, #22c55e, #4ade80); height: 100%; border-radius: 100px; }
.barra-fill-neg { background: linear-gradient(90deg, #ef4444, #f87171); height: 100%; border-radius: 100px; }
.barra-fill-neu { background: linear-gradient(90deg, #6366f1, #818cf8); height: 100%; border-radius: 100px; }
.scores-grid { display: flex; justify-content: center; gap: 2rem; margin-top: 1.2rem; }
.score-item { text-align: center; }
.score-valor { font-size: 1.2rem; font-weight: 600; display: block; color: #e8e8e8; }
.score-nome { font-size: 0.72rem; color: #555; text-transform: uppercase; letter-spacing: 0.06em; }
.aviso-modelo { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 10px; padding: 0.75rem 1rem; font-size: 0.83rem; color: #a5b4fc; margin-bottom: 1.2rem; text-align: center; }
.footer { text-align: center; margin-top: 3rem; font-size: 0.78rem; color: #444; letter-spacing: 0.04em; }
div[data-testid="stTextArea"] textarea { background: #161620 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #e8e8e8 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 1rem !important; }
div[data-testid="stButton"] button { background: #ffffff !important; color: #0f0f13 !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; border-radius: 10px !important; border: none !important; padding: 0.6rem 2rem !important; font-size: 0.95rem !important; width: 100% !important; }
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Análise via Inference API do HuggingFace (sem torch, sem GPU) ─────────────
def analisar_sentimento(texto, hf_token):
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"
    headers = {"Authorization": f"Bearer {hf_token}"}
    for tentativa in range(3):
        resp = requests.post(API_URL, headers=headers, json={"inputs": texto[:512]}, timeout=30)
        if resp.status_code == 200:
            return resp.json()[0]
        elif resp.status_code == 503:
            espera = resp.json().get("estimated_time", 15)
            st.info(f"⏳ Modelo iniciando no servidor HuggingFace... aguarde {int(espera)}s")
            time.sleep(min(espera, 20))
        else:
            st.error(f"Erro na API: {resp.status_code} — {resp.text}")
            return None
    return None

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo">Analisador de<br>Sentimentos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Inteligência Artificial · NLP · Transformers · PT-BR</div>', unsafe_allow_html=True)
st.markdown('<div class="aviso-modelo">🤖 Modelo: <strong>XLM-RoBERTa</strong> multilíngue via HuggingFace API · português, inglês, espanhol e mais</div>', unsafe_allow_html=True)

# ── Token HuggingFace ──────────────────────────────────────────────────────────
with st.expander("🔑 Configurar token HuggingFace (gratuito — necessário)"):
    st.markdown("""
1. Acesse [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Clique em **New token** → tipo **Read** → copie
3. Cole abaixo:
""")
    hf_token = st.text_input("Token HuggingFace:", type="password", placeholder="hf_...")
    if hf_token:
        st.session_state["hf_token"] = hf_token

token_atual = st.session_state.get("hf_token", "")

# ── Exemplos ───────────────────────────────────────────────────────────────────
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

# ── Entrada ────────────────────────────────────────────────────────────────────
texto = st.text_area(
    "Texto:",
    value=st.session_state.get("texto_input", ""),
    placeholder="Ex: O curso foi incrível, aprendi muito!",
    height=120,
    key="texto_input",
    label_visibility="collapsed",
)

analisar = st.button("Analisar sentimento →")

# ── Análise ────────────────────────────────────────────────────────────────────
if analisar:
    texto_limpo = texto.strip()
    if not texto_limpo:
        st.warning("Digite algum texto antes de analisar.")
    elif not token_atual:
        st.error("⚠️ Insira o token HuggingFace no painel acima. É gratuito e leva 1 minuto!")
    else:
        with st.spinner("Analisando..."):
            resultados = analisar_sentimento(texto_limpo, token_atual)

        if resultados:
            scores = {r["label"]: r["score"] for r in resultados}
            pos = scores.get("Positive", 0)
            neg = scores.get("Negative", 0)
            neu = scores.get("Neutral", 0)
            melhor = max(scores, key=scores.get)
            pct = int(scores[melhor] * 100)

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
**XLM-RoBERTa** é um modelo Transformer multilíngue — funciona em português sem tradução.

| Classe | Score |
|---|---|
| Positivo | `{pos:.3f}` ({pos:.0%}) |
| Neutro   | `{neu:.3f}` ({neu:.0%}) |
| Negativo | `{neg:.3f}` ({neg:.0%}) |

**Por que API e não local?**
O Streamlit Cloud gratuito tem ~1GB de RAM — insuficiente para carregar o modelo (~2GB com torch).
Usando a **Inference API do HuggingFace**, o modelo roda nos servidores deles: nós enviamos o texto e recebemos o resultado. Leve, rápido, gratuito.

**VADER vs XLM-RoBERTa:**
- VADER → dicionário inglês, **não funciona em português**
- XLM-RoBERTa → Transformer multilíngue, **funciona em português**, muito mais preciso
""")

st.markdown("""
<div class="footer">
    Construído com Python · Streamlit · HuggingFace Inference API<br>
    Modelo: cardiffnlp/twitter-xlm-roberta-base-sentiment · Gerado com IA
</div>
""", unsafe_allow_html=True)
