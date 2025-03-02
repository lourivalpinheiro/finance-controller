# Importing necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Load financial data from Streamlit secrets
secrets = st.secrets["finance_data"]

# Create a dataframe using secrets
data = {
    "Operação": ["Aluguel", "Amor Saúde", "Cartão de Crédito", "Cebrac", "Extra", "Extra", "Faculdade", "INSS", 
                 "Internet", "Parcela do laptop", "Plano odontológico", "Salário", "TIM"],
    "Data": ["03/2025"] * 13,  # Simplified list creation
    "Tipo": ["Saída", "Saída", "Saída", "Saída", "Entrada", "Entrada", "Saída", "Saída", 
             "Saída", "Saída", "Saída", "Entrada", "Saída"],
    "Valor": [secrets["ALUGUEL"], secrets["AMOR_SAUDE"], secrets["CARTAO_CREDITO"], secrets["CEBRAC"],
              secrets["EXTRA_1"], secrets["EXTRA_2"], secrets["FACULDADE"], secrets["INSS"],
              secrets["INTERNET"], secrets["LAPTOP_PARCELA"], secrets["PLANO_ODONTOLOGICO"],
              secrets["SALARIO"], secrets["TIM"]]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit page settings
st.set_page_config(page_title="Controle de Finanças", layout="wide")

# Title and Divider
st.markdown("# Controle de Finanças")
st.divider()

# Title and Divider
st.markdown("## Controle Orçamentário")

# Date filter
selected_date = st.selectbox("Selecione a Data:", sorted(df["Data"].unique()), index=0)

# Filtering dataframe by selected date
filtered_df = df[df["Data"] == selected_date]

# Grouping filtered data by Tipo and summing Valor
df1 = filtered_df.groupby("Tipo", as_index=False).sum()

# Setting up the chart
fig1 = px.bar(df1, x="Tipo", y="Valor", title="Entradas e Saídas", text="Valor")

# Display elements in two columns
col1, col2 = st.columns(2)

with col1:
    # Display the filtered dataframe with formatted values
    st.dataframe(filtered_df.style.format({"Valor": "{:.2f}"}))

with col2:
    # Display the chart
    st.plotly_chart(fig1)

# INVESTMENTS

investment_secrets = st.secrets["investment_data"]

# Dataframe
investment_data = {
    "INSTITUIÇÃO": ["Nubank"],
    "VALOR INVESTIDO": [investment_secrets["VALOR_INVESTIDO"]],
    "DATA DO RENDIMENTO": ["02/03/2025"],
    "VALOR DO RENDIMENTO": [investment_secrets["VALOR_DO_RENDIMENTO"]],
    "ATIVO": ["CDI"],
    "TIPO": ["Renda Fixa"],
    "TAXA ATUAL": [13.15]
}

investment_df = pd.DataFrame(investment_data)
investment_df_analysis = investment_df[["DATA DO RENDIMENTO", "VALOR DO RENDIMENTO"]]

# Chart
fig2 = px.bar(investment_df_analysis, x="DATA DO RENDIMENTO", y="VALOR DO RENDIMENTO", title="RENDIMENTO", text="VALOR DO RENDIMENTO")

# Title and Divider
st.markdown("# Investimentos")
st.divider()

# Display the dataframe and insert a divider
st.dataframe(investment_df_analysis)
st.divider()

# Insert the chart
st.plotly_chart(fig2)