from controller.controller import inserir_visita
import numpy as np
import streamlit as st
from controller.data_control import acoes_gestor, acoes_consultor, acoes_planej
import pandas as pd
from datetime import datetime
import datetime as dt
from auth import conecta_supabase
import json
from time import sleep
from datetime import date

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Relatório",
    page_icon="📋",
    layout="wide",
)

st.title("👋 :grey[Relatórios]")

pills = st.pills(label="", options=["Geral", "Ações"])

if pills == "Ações":

    cola, colb = st.columns([3, 4])

    with cola:
        data = st.selectbox(
            "Período",
            options=["Jan/26", "Fev/26", "Mar/26", "Abr/26", "Mai/26", "Jun/26", "Jul/26", "Ago/26", "Set/26", "Out/26", "Nov/26", "Dez/26"],
            width=150,
        )

        meses = {"Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6,
                 "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12}

        mes, ano = data.split("/")
        data_ref = date(2000 + int(ano), meses[mes], 1)

    with colb: botao = st.button("Gerar")

    if botao:
        if st.session_state['role'] == 'gestor':
            df = acoes_gestor(data_ref, st.session_state['username'])
            df_sumarizado = df.pivot_table(index='Executivo', 
                                     columns='Tipo', 
                                     values='Data', 
                                     aggfunc='count', 
                                     fill_value=0)

        elif st.session_state['role'] == 'consultor':
            df = acoes_consultor(data_ref, st.session_state['username'])
            df_sumarizado = df.pivot_table(index='Executivo', 
                                     columns='Tipo', 
                                     values='Data', 
                                     aggfunc='count', 
                                     fill_value=0)
                                    
        elif st.session_state['role'] in ['planejamento','admin']:
            df = acoes_planej(data_ref)
            df_sumarizado = df.pivot_table(index=['Gestor', 'Executivo'], 
                                     columns='Tipo', 
                                     values='Data', 
                                     aggfunc='count', 
                                     fill_value=0)
                                     
        st.dataframe(df_sumarizado, width="content")
   

        
        
        
