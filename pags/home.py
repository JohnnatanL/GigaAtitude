import streamlit as st
from controller.hidden import hidden
from stylo.css import aplicar_css_global

st.set_page_config(
    page_title="Início",
    page_icon="🏠",
    layout="wide",
)
hidden()

with st.container(border=False, horizontal_alignment="center"):
    st.title("👋 :grey[Bem vindo ao Portal Alto Valor.]", text_alignment="center")
    st.markdown(":grey[Utilize o menu lateral para navegar entre as seções do sistema.]", text_alignment="center")
    st.markdown("🌟 :grey[Dica: explore os diversos indicadores para melhorar sua experiência.]", text_alignment="center")
