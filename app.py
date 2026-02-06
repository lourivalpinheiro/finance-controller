import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ======================
# Configurações Streamlit
# ======================
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #000000;
    }
    .stApp {
        background-color: #000000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Lourival Pinheiro")

# ======================
# Conectar ao Google Sheets com loading
# ======================
SHEET_URL = st.secrets["base_dados"]["url"]

with st.spinner("Carregando planilha..."):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(
        spreadsheet=st.secrets["base_dados"]["url"]
    )

# Converte a coluna de datas
df["data"] = pd.to_datetime(df["data"])

# ======================
# Filtros
# ======================
tipos_disponiveis = ["Ambos"] + df["tipo"].unique().tolist()
tipo_selecionado = st.selectbox("Selecione o tipo", tipos_disponiveis)

data_inicial, data_final = st.date_input(
    "Selecione o período",
    value=[df["data"].min(), df["data"].max()],
    format="DD/MM/YYYY"
)

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
        textposition="outside",
        marker_line_width=1.5,
        marker_line_color="#FFFFFF",
        marker=dict(line=dict(width=1, color="#FFFFFF"))
    )
    grafico_barras.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color="#FFFFFF", size=12),
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=60, b=80),
        legend=dict(title="Tipo", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(grafico_barras, use_container_width=True)

with col2:
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
        hovertemplate="<b>%{label}</b><br>Valor: %{value:,.2f}<br>Percentual: %{percent}",
        marker=dict(line=dict(color="#000000", width=2))
    )
    grafico_pizza.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color="#FFFFFF", size=12),
        legend=dict(title="Tipo", orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(grafico_pizza, use_container_width=True)

