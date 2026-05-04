import streamlit as st
from controller.controller import get_condominios, round_to_quarter
import datetime
import pandas as pd
from datetime import date


# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Visita Comercial – Giga+ Fibra",
    page_icon="📋",
    layout="wide",
)

st.title("👋 :grey[Visita Comercial]")

pills = st.pills(label="", options=["Nova Visita", "Histórico de Visitas"])

if pills == "Nova Visita":
    with st.form("nova_visita"):

        a0, a1, a2, a3, a4 = st.columns([1.5, 1.2, 1.5, 1.2, 5])

        with a0: dt_inicio = st.date_input("Data de Início",key="dt_inicio", format="DD/MM/YYYY")
        with a1: hr_inicio = st.time_input("Hora de Início", key="hr_inicio", value=round_to_quarter().time())
        with a2: dt_fim = st.date_input("Data de Término",key="dt_fim", format="DD/MM/YYYY")
        with a3: hr_fim = st.time_input("Hora de Término", key="hr_fim", value=round_to_quarter().time())
        
        condominio = st.selectbox("Condomínio", options=get_condominios(), placeholder="Selecione condomínio", key="condominio")

        b0, b1, b2, b3 = st.columns([1, 1, 1, 5])
        with b0: st.number_input("Qtde Torres", key="qtde_torres", min_value=0, step=1)
        with b1: st.number_input("Qtde Andares", key="qtde_andares", min_value=0, step=1)
        with b2: st.number_input("Apto por Andar", key="apto_por_andar", min_value=0, step=1)

        c0, c1, c2 = st.columns([2, 4, 2.5])
        with c0: st.selectbox("Possui permuta?", ["Não possui", "Possui 1 permuta", "Possui 2 permutas", "Possui 3 ou mais permutas"] ,key="permuta")
        with c1: st.multiselect("Possui concorrência?", ["Exclusivo Giga+ Fibra", "Claro", "Vivo", "TIM", "Oi", "Brisanet", "Multiplay (Alares)", "Algar Telecom", "ProveNET", "Velocinet Provedor", "Byteplay Connect", "QNet Telecom", "Telefibra", "HD Provedor", "Lay Provedor", "Fortalnet", "RedeNet Telecom", "WireXtreme", "Infortec", "JWS Provedor", "Argohost Net", "Orion Telecom", "Bayde Net", "Ciberdyne Internet", "Wire Link", "Ponto Net", "Linknet Provedor", "Outros"], key="concorrencia")
        with c2: st.text_input("Outros", key="outros_conc")
        
        with st.expander("Contatos"):
            df_contatos = pd.DataFrame(
                [
                    {
                        "Nome": "",
                        "Telefone": "",
                        "Email": "",
                    },
                ]
            )
            contatos = st.data_editor(
                df_contatos,
                column_config={
                    "Nome": "Nome",
                    "Telefone": "Telefone",
                    "Email": "Email",
                },
                hide_index=True,
                num_rows="dynamic",
                key="contatos",
            )

        with st.expander("Parceiros"):
            df_parceiros = pd.DataFrame(
                [
                    {
                        "Empresa": "",
                        "Tipo de Negócio": "",
                        "Responsável": "",
                    },
                ]
            )
            parceiros = st.data_editor(
                df_parceiros,
                column_config={
                    "Empresa": "Empresa",
                    "Tipo de Negócio": "Tipo de Negócio",
                    "Responsável": "Responsável",
                },
                hide_index=True,
                num_rows="dynamic",
                key="parceiros",
            )
            
        with st.expander("Mercado"):
            df_mercado = pd.DataFrame(
                [
                    {
                        "Empresa": "",
                        "Tipo de Negócio": "",
                        "Responsável": "",
                    },
                ]
            )
            mercado = st.data_editor(
                df_mercado,
                column_config={
                    "Fornecedores": "Fornecedores",
                    "Ofertas": "Ofertas",
                },
                hide_index=True,
                num_rows="dynamic",
                key="mercado",
            )
        
        
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success("Formulário enviado com sucesso!")
    