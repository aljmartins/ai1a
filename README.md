# 🧠 Analisador de Sentimentos com IA

Aplicativo web de análise de sentimentos construído com **Python + Streamlit + VADER NLP**.

> Projeto desenvolvido na aula de Inteligência Artificial.  
> Código gerado com IA → testado no VS Code → deploy via GitHub + Streamlit Cloud.

---

## 🚀 Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/sentiment-app.git
cd sentiment-app
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode o app
```bash
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`

---

## ☁️ Deploy no Streamlit Community Cloud (gratuito)

1. Suba o código para um **repositório público no GitHub**
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **"New app"**
4. Selecione o repositório, a branch (`main`) e o arquivo (`app.py`)
5. Clique em **Deploy** — pronto! 🎉

O app ficará online em uma URL pública como:  
`https://seu-usuario-sentiment-app-app-xxxx.streamlit.app`

---

## 🧪 Como funciona o VADER?

O **VADER** (Valence Aware Dictionary and sEntiment Reasoner) analisa o texto e retorna 4 scores:

| Score | Descrição |
|---|---|
| `pos` | Proporção de palavras positivas (0 a 1) |
| `neu` | Proporção de palavras neutras (0 a 1) |
| `neg` | Proporção de palavras negativas (0 a 1) |
| `compound` | Score final normalizado entre **-1** (negativo) e **+1** (positivo) |

**Regra de classificação:**
- `compound ≥ 0.05` → 😊 **Positivo**
- `compound ≤ -0.05` → 😞 **Negativo**
- Entre -0.05 e 0.05 → 😐 **Neutro**

---

## 🗂 Estrutura do projeto

```
sentiment-app/
├── app.py            # Código principal do app
├── requirements.txt  # Dependências Python
└── README.md         # Este arquivo
```

---

## 💡 Ideias para estender o projeto

- [ ] Adicionar suporte a análise de múltiplos textos de um CSV
- [ ] Plotar um gráfico de sentimentos ao longo do tempo
- [ ] Integrar com a API do Twitter/X para analisar tweets em tempo real
- [ ] Usar um modelo de linguagem (LLM) para textos em português
- [ ] Criar um histórico de análises salvo em arquivo

---

## 🛠 Stack

- [Python 3.10+](https://python.org)
- [Streamlit](https://streamlit.io)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)

---

*Gerado com assistência de IA · Aula de Inteligência Artificial Aplicada*
