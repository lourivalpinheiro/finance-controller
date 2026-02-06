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
# Conectar ao Google Sheets
# ======================
SHEET_URL = st.secrets["base_dados"]["url"]

with st.spinner("Carregando planilha..."):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SHEET_URL)

# ======================
# Converter a coluna de datas de forma robusta
# ======================
df["data"] = pd.to_datetime(df["data"], errors="coerce")  # converte qualquer formato reconhecível
df = df.dropna(subset=["data"])  # remove linhas com datas inválidas

# ======================
# Filtro de Tipo
# ======================
tipos_disponiveis = ["Ambos"] + df["tipo"].unique().tolist()
tipo_selecionado = st.selectbox("Selecione o tipo", tipos_disponiveis)

# ======================
# Filtro de Período (Slider usando datetime.datetime)
# ======================
# Garantir datetime.datetime para o slider funcionar no modo intervalo
data_min = pd.Timestamp(df["data"].min().date())
data_max = pd.Timestamp(df["data"].max().date())

data_inicial, data_final = st.slider(
    "Selecione o período",
    min_value=data_min,
    max_value=data_max,
    value=(data_min, data_max),
    format="DD/MM/YYYY"
)

# Filtra o DataFrame
df_filtrado = df[(df["data"] >= data_inicial) & (df["data"] <= data_final)]
if tipo_selecionado != "Ambos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_selecionado]

# ======================
# Cores
# ======================
cores = {"Receita": "#2ECC71", "Despesa": "#E74C3C"}

# ======================
# Gráfico de Barras (Container)
# ======================
with st.container():
    st.subheader("Receita e Despesa por Categoria")
    grafico_barras = px.bar(
        df_filtrado,
        x="categoria",
        y="valor",
        color="tipo",
        barmode="group",
        text="valor",
        color_discrete_map=cores,
        hover_data={"valor": ":,.2f", "tipo": True, "categoria": True}
    )
    grafico_barras.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )
    grafico_barras.update_layout(
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=40, b=80),
        legend=dict(title="Tipo", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(grafico_barras, use_container_width=True)

# ======================
# Gráfico de Pizza (Container)
# ======================
with st.container():
    st.subheader("Distribuição de Valores")
    grafico_pizza = px.pie(
        df_filtrado,
        names="categoria",
        values="valor",
        color="tipo",
        color_discrete_map=cores,
        hole=0.4
    )
    grafico_pizza.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Valor: %{value:,.2f}<br>Percentual: %{percent}",
        marker=dict(line=dict(color="#000000", width=2))
    )
    grafico_pizza.update_layout(
        legend=dict(title="Tipo", orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(grafico_pizza, use_container_width=True)
