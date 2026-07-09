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

st.title("📊 :grey[Relatórios]")

pills = st.pills(label="", options=["Relatório de Ações", "Crescimento de Base"])

if pills == "Relatório de Ações":

    cola, colb, c = st.columns([2, 1, 9])

    with cola:
        data = st.selectbox(
            "Período",
            options=["Jun/26", "Jul/26", "Ago/26", "Set/26", "Out/26", "Nov/26", "Dez/26"],
            index=1,
            width=150,
        )

        meses = {"Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6,
                 "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12}

        mes, ano = data.split("/")
        data_ref = date(2000 + int(ano), meses[mes], 1)

    with colb:
        
        botao = st.button("Gerar")

    if botao:
        if st.session_state['role'] == 'gestao':
            df = acoes_gestor(data_ref, st.session_state['username'])
            df_sumarizado = df.pivot_table(index='Executivo', 
                                     columns='Tipo', 
                                     values='Data', 
                                     aggfunc='count', 
                                     fill_value=0)

        elif st.session_state['role'] == 'consultor':

            df = acoes_consultor(data_ref, st.session_state['username'])
            #tipos = ['Visita', 'Acao de Vendas', 'Ficha Cadastro', 'Lead']

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
        if st.session_state['role'] == 'consultor':
            if 'Visita' in df_sumarizado.columns:
                visitas = df_sumarizado['Visita'][0]
            else:
                visitas = 0
            if 'Ficha Cadastro' in df_sumarizado.columns:
                ficha = df_sumarizado['Ficha Cadastro'][0]
            else:
                ficha = 0
            if 'Lead' in df_sumarizado.columns:
                lead = df_sumarizado['Lead'][0]
            else:
                lead = 0
            if 'Acao de Vendas' in df_sumarizado.columns:
                acoes = df_sumarizado['Acao de Vendas'][0]
            else:
                acoes = 0
                
            st.divider()
            st.subheader(f"Total de Ações: {acoes+visitas+lead+ficha}")
            st.table(
                    [
                        f":gray-badge[Executivo de Vendas: {st.session_state['username']}]",
                    f":green-badge[Visitas: {visitas}]    :blue-badge[Ações de Vendas: {acoes}]",
                    f":violet-badge[Leads: {lead}]    :orange-badge[Fichas de Cadastro: {ficha}]",
                ],
                border="horizontal",
                width="content",
            )

            st.subheader("Detalhamento")
            st.dataframe(df, width="content", hide_index=False, column_config={
                "Gestor": st.column_config.TextColumn(width=160),
                "Executivo": st.column_config.TextColumn(width=180),
                "Acao de Vendas": st.column_config.NumberColumn("Ação de Vendas", width=130),
                "Ficha Cadastro": st.column_config.NumberColumn(width=130),
                "Lead": st.column_config.NumberColumn(width=90),
            })

        elif st.session_state['role'] == 'gestao':
            df_sumarizado = df_sumarizado.reset_index()
            for c in ['Acao de Vendas', 'Visita', 'Lead', 'Ficha Cadastro']:
                if c not in df_sumarizado.columns:
                    df_sumarizado[c] = 0
            st.subheader(f"Total de Ações da Equipe: {df_sumarizado[['Acao de Vendas', 'Visita', 'Lead', 'Ficha Cadastro']].sum().sum()}")
            cols = st.columns(4)
            for i, (_, row) in enumerate(df_sumarizado.iterrows()):
                with cols[i % 4]:
                    with st.container(border=True):
                        st.write(f"Total de Ações - {row['Executivo']}: {(row.get('Visita', 0))+(row.get('Acao de Vendas', 0))+(row.get('Lead', 0))+(row.get('Ficha Cadastro', 0))}")
                        st.table(
                            [
                                f":green-badge[Visitas: {row.get('Visita', 0)}]    :blue-badge[Ações de Vendas: {row.get('Acao de Vendas', 0)}]",
                                f":violet-badge[Leads: {row.get('Lead', 0)}]    :orange-badge[Fichas de Cadastro: {row.get('Ficha Cadastro', 0)}]",
                            ],
                            border="horizontal",
                            width="content",
                        )
            st.subheader("Detalhamento")
            st.dataframe(df, width="content", hide_index=False, column_config={
                "Gestor": st.column_config.TextColumn(width=160),
                "Executivo": st.column_config.TextColumn(width=180),
                "Acao de Vendas": st.column_config.NumberColumn("Ação de Vendas", width=130),
                "Ficha Cadastro": st.column_config.NumberColumn(width=130),
                "Lead": st.column_config.NumberColumn(width=90),
            })