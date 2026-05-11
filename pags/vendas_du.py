import streamlit as st
from controller.data_control import vendas

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title("Vendas DU")


df = vendas()

st.dataframe(df)