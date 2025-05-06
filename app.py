import spacy
from spacy.cli import download
import streamlit as st
st.set_page_config(page_title="Analisador de Sentimentos", layout="centered")
# Projeto CP02 - NLP com spaCy
# Autor: Alan de Souza Maximiano da Silva | RM: 557088
# App Online: https://cp02-nlp-spacy.streamlit.app/
# Configuração da página já realizada no início
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc

# Carrega modelo de português com fallback automático
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    download("pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

# Função de classificação genérica
def classify(doc, matcher):
    matches = matcher(doc)
    pos = neg = 0
    tokens = []
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        span = doc[start:end]
        tokens.append(span.text)
        if label == "POSITIVO":
            pos += 1
        else:
            neg += 1
    sentiment = "Neutro"
    if pos > neg: sentiment = "Positivo"
    elif neg > pos: sentiment = "Negativo"
    return sentiment, tokens

default_pos = ["ótimo", "excelente", "bom", "maravilhoso", "adoro"]
default_neg = ["péssimo", "horrível", "ruim", "terrível", "odeio"]

if "positivos" not in st.session_state:
    st.session_state.positivos = default_pos.copy()
if "negativos" not in st.session_state:
    st.session_state.negativos = default_neg.copy()
if "history" not in st.session_state:
    st.session_state.history = []

# Exibe logo na sidebar
st.sidebar.image("logo_fiap.jpg", use_container_width=True)
# Sidebar: customização de dicionário
st.sidebar.header("Dicionário de Sentimentos")
pos_txt = st.sidebar.text_area("Positivos (vírgula)", ", ".join(st.session_state.positivos))
neg_txt = st.sidebar.text_area("Negativos (vírgula)", ", ".join(st.session_state.negativos))
if st.sidebar.button("Atualizar Dicionário"):
    st.session_state.positivos = [w.strip() for w in pos_txt.split(",") if w.strip()]
    st.session_state.negativos = [w.strip() for w in neg_txt.split(",") if w.strip()]

# Criar matcher dinâmico
matcher = PhraseMatcher(nlp.vocab)
matcher.add("POSITIVO", [nlp.make_doc(w) for w in st.session_state.positivos])
matcher.add("NEGATIVO", [nlp.make_doc(w) for w in st.session_state.negativos])

# Atualizar extensão Doc
Doc.set_extension("sentimento", getter=lambda doc: classify(doc, matcher)[0], force=True)
Doc.set_extension("tokens_match", getter=lambda doc: classify(doc, matcher)[1], force=True)

# Interface Streamlit
st.title(" ANALISADOR DE SENTIMENTOS")
st.write("Selecione uma frase de exemplo para identificar o sentimento:")

# Layout em colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Análise Individual")
    frase_sel = st.selectbox("Selecione uma frase:", [
        "Esse produto é ótimo, eu adoro!",
        "O atendimento foi péssimo e a comida horrível.",
        "Achei o filme bom, mas o final foi ruim.",
        "Tudo foi excelente, amei a experiência!",
        "Não gostei, foi terrível."
    ])
    if st.button("Analisar Frase"):
        with st.spinner("Analisando..."):
            doc = nlp(frase_sel)
        sent = doc._.sentimento
        tokens = doc._.tokens_match
        # Badge colorido
        if sent == "Positivo":
            st.success(f"👍 {sent}")
        elif sent == "Negativo":
            st.error(f"👎 {sent}")
        else:
            st.info(f"😐 {sent}")
        with st.expander("Detalhes"):
            st.write("Tokens detectados:", tokens)
        # Histórico
        st.session_state.history.append((frase_sel, sent))

    # Entrada manual de frase
    st.write("Ou digite sua própria frase:")
    frase_manual = st.text_input("Frase manual", "")
    if st.button("Analisar Manual"):
        with st.spinner("Analisando..."):
            docm = nlp(frase_manual)
        sentm = docm._.sentimento
        tokensm = docm._.tokens_match
        if sentm == "Positivo":
            st.success(f"👍 {sentm}")
        elif sentm == "Negativo":
            st.error(f"👎 {sentm}")
        else:
            st.info(f"😐 {sentm}")
        with st.expander("Detalhes Manual"):
            st.write("Tokens detectados:", tokensm)
        st.session_state.history.append((frase_manual, sentm))

with col2:
    st.subheader("Visão Geral")
    # Gráfico de distribuição
    df = {"Positivo": sum(1 for _,s in st.session_state.history if s=="Positivo"),
          "Negativo": sum(1 for _,s in st.session_state.history if s=="Negativo"),
          "Neutro": sum(1 for _,s in st.session_state.history if s=="Neutro")}
    st.bar_chart(df)
    # Histórico e exportação
    st.write("### Histórico")
    for f,s in st.session_state.history:
        st.write(f"- {f} → {s}")
    if st.session_state.history:
        import pandas as pd
        df_hist = pd.DataFrame(st.session_state.history, columns=["Frase","Sentimento"])
        csv = df_hist.to_csv(index=False).encode()
        st.download_button("Baixar CSV", csv, file_name="history.csv")