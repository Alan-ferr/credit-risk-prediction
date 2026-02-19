import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ============================
# CONFIG PAGE
# ============================

st.set_page_config(
    page_title="Credit Risk AI",
    page_icon="💳",
    layout="wide"
)

# ============================
# LOAD MODEL
# ============================

model = pickle.load(open("model.pkl", "rb"))

# ============================
# HEADER
# ============================

st.title("💳 Sistema de Score de Crédito com IA")
st.markdown("Avaliação de risco de inadimplência usando Machine Learning")

st.divider()

# ============================
# SIDEBAR INPUTS
# ============================

st.sidebar.header("Dados do Cliente")

age = st.sidebar.slider("Idade", 18, 100, 35)

income = st.sidebar.number_input(
    "Renda mensal",
    min_value=0,
    value=5000
)

debt_ratio = st.sidebar.slider(
    "Índice de dívida",
    0.0,
    5.0,
    0.5
)

credit_lines = st.sidebar.slider(
    "Número de linhas de crédito",
    0,
    20,
    5
)

late_30 = st.sidebar.slider(
    "Atrasos 30–59 dias",
    0,
    10,
    0
)

late_60 = st.sidebar.slider(
    "Atrasos 60–89 dias",
    0,
    10,
    0
)

late_90 = st.sidebar.slider(
    "Atrasos 90+ dias",
    0,
    10,
    0
)

# ============================
# CREATE INPUT DATAFRAME
# ============================

input_data = pd.DataFrame({
    'RevolvingUtilizationOfUnsecuredLines': [0.5],
    'age': [age],
    'NumberOfTime30-59DaysPastDueNotWorse': [late_30],
    'DebtRatio': [debt_ratio],
    'MonthlyIncome': [income],
    'NumberOfOpenCreditLinesAndLoans': [credit_lines],
    'NumberOfTimes90DaysLate': [late_90],
    'NumberRealEstateLoansOrLines': [1],
    'NumberOfTime60-89DaysPastDueNotWorse': [late_60],
    'NumberOfDependents': [0]
})

# ============================
# PREDICTION
# ============================

if st.sidebar.button("Calcular Score"):

    prob = model.predict_proba(input_data)[0][1]

    score = int((1 - prob) * 1000)

    # classificação
    if score >= 800:
        risco = "Muito baixo"
        cor = "🟢"
    elif score >= 600:
        risco = "Baixo"
        cor = "🟡"
    elif score >= 400:
        risco = "Médio"
        cor = "🟠"
    else:
        risco = "Alto"
        cor = "🔴"

    # ============================
    # DISPLAY
    # ============================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Score de Crédito",
        score
    )

    col2.metric(
        "Probabilidade de inadimplência",
        f"{prob:.2%}"
    )

    col3.metric(
        "Classificação de risco",
        f"{cor} {risco}"
    )

    st.progress(score / 1000)

    # ============================
    # INTERPRETAÇÃO
    # ============================

    st.subheader("Interpretação")

    if score >= 800:
        st.success("Cliente com risco extremamente baixo. Excelente perfil.")
    elif score >= 600:
        st.info("Cliente com bom perfil. Risco controlado.")
    elif score >= 400:
        st.warning("Cliente com risco moderado. Atenção recomendada.")
    else:
        st.error("Cliente com alto risco de inadimplência.")

# ============================
# FOOTER
# ============================

st.divider()

st.caption("Modelo baseado em Machine Learning | Projeto de Portfólio")
