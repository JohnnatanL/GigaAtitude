import streamlit as st
from controller.data_control import visitas_e_vendas
from controller.hidden import hidden

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
hidden()

st.title("Relatório - Projeto Muralha")

df_visitas, df_vendas = visitas_e_vendas()

visitas_agg = (
    df_visitas
    .groupby("usuario", dropna=False)
    .agg(
        total_visitas   = ("qtdevisita", "sum"),
        predios_unicos  = ("idcondominio", "nunique"),
    )
    .reset_index()
    .rename(columns={"usuario": "username"})
)

# ── 2. df_vendas ──────────────────────────────────────────────────────────────
# Extrai o username do e-mail  (ex: "basilio.junior@alloha.com" → "basilio.junior")
df_vendas["username"] = df_vendas["email_vendedor"].str.split("@").str[0]

vendas_agg = (
    df_vendas
    .groupby("username", dropna=False)
    .agg(
        total_vendas = ("id_contrato", "count"),
    )
    .reset_index()
)

# ── 3. Une os dois ────────────────────────────────────────────────────────────
df_final = (
    visitas_agg
    .merge(vendas_agg, on="username", how="left")
    .fillna(0)
)

# Converte para inteiro após o fillna
df_final[["total_visitas", "predios_unicos", "total_vendas"]] = (
    df_final[["total_visitas", "predios_unicos", "total_vendas"]].astype(int)
)

st.divider()

# Métricas resumo
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vendedores",    len(df_final))
col2.metric("Total visitas", int(df_final["total_visitas"].sum()))
col3.metric("Prédios únicos", int(df_final["predios_unicos"].sum()))
col4.metric("Total vendas",  int(df_final["total_vendas"].sum()))

st.divider()

# Tabela principal
st.dataframe(
    df_final.sort_values("total_vendas", ascending=False).reset_index(drop=True),
    use_container_width=True,
    column_config={
        "username":       st.column_config.TextColumn("Usuário",        width="large"),
        "total_visitas":  st.column_config.NumberColumn("Visitas",       format="%d"),
        "predios_unicos": st.column_config.NumberColumn("Prédios únicos", format="%d"),
        "total_vendas":   st.column_config.NumberColumn("Vendas",        format="%d"),
    },
    hide_index=True,
    width=200,
)