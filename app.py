import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ======================
# Configurações Streamlit
# ======================
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.title("Lourival Pinheiro")

# ======================
# Conectar ao Google Sheets com loading
# ======================
SHEET_URL = st.secrets["base_dados"]["url"]

with st.spinner("Carregando planilha..."):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SHEET_URL)

# Converte a coluna de datas
df["data"] = pd.to_datetime(df["data"])

# ======================
# Filtros
# ======================
tipos_disponiveis = ["Ambos"] + df["tipo"].unique().tolist()
tipo_selecionado = st.selectbox("Selecione o tipo", tipos_disponiveis)

# Selecione período
data_input = st.date_input(
    "Selecione o período",
    value=[df["data"].min(), df["data"].max()],
    format="DD/MM/YYYY"
)

# ======================
# Validação do período
# ======================
if len(data_input) < 2:
    st.warning("Por favor, selecione tanto a data inicial quanto a data final.")
else:
    data_inicial, data_final = data_input
    df_filtrado = df[(df["data"] >= pd.to_datetime(data_inicial)) & (df["data"] <= pd.to_datetime(data_final))]
    
    if tipo_selecionado != "Ambos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_selecionado]

    # ======================
    # Cores
    # ======================
    cores = {"Receita": "#2ECC71", "Despesa": "#E74C3C"}

    # ======================
    # Layout de gráficos lado a lado
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            grafico_barras = px.bar(
                df_filtrado,
                x="categoria",
                y="valor",
                color="tipo",
                barmode="group",
                text="valor",
                color_discrete_map=cores,
                title="Receita e Despesa por Categoria",
                hover_data={"valor": ":,.2f", "tipo": True, "categoria": True}
            )
            grafico_barras.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside"
            )
            st.plotly_chart(grafico_barras, use_container_width=True)

    with col2:
        with st.container(border=True):
            grafico_pizza = px.pie(
                df_filtrado,
                names="categoria",
                values="valor",
                color="tipo",
                color_discrete_map=cores,
                title="Distribuição de Valores",
                hole=0.4  # transforma em donut
            )
            grafico_pizza.update_traces(
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Valor: %{value:,.2f}<br>Percentual: %{percent}"
            )
            st.plotly_chart(grafico_pizza, use_container_width=True)
