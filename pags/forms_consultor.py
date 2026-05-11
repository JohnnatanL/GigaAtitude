from controller.controller import inserir_visita
import streamlit as st
from controller.controller import (get_condominios,
                                    round_to_quarter,
                                    get_id_condominio)
import datetime
import pandas as pd
from datetime import datetime
from auth import conecta_supabase
import json

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
        tipo_forms = "Teste"
        subtipo_forms = "Teste_Fortaleza"

        a0, a1, a2, a3, a4 = st.columns([1.5, 1.2, 1.5, 1.2, 5])

        with a0: dt_inicio = st.date_input("Data de Início",key="dt_inicio", format="DD/MM/YYYY")
        with a1: hr_inicio = st.time_input("Hora de Início", key="hr_inicio", value=round_to_quarter().time())
        with a2: dt_fim = st.date_input("Data de Término",key="dt_fim", format="DD/MM/YYYY")
        with a3: hr_fim = st.time_input("Hora de Término", key="hr_fim", value=round_to_quarter().time())
        
        condominio = st.selectbox("Condomínio", options=get_condominios(), placeholder="Selecione condomínio", key="condominio")

        b0, b1, b2, b3 = st.columns([1, 1, 1, 5])
        with b0: torres = st.number_input("Qtde Torres", key="qtde_torres", min_value=1, step=1)
        with b1: andares = st.number_input("Qtde Andares", key="qtde_andares", min_value=1, step=1)
        with b2: apto_andar = st.number_input("Apto por Andar", key="apto_por_andar", min_value=1, step=1)

        c0, c1, c2 = st.columns([2, 4, 2.5])
        with c0: permuta = st.selectbox("Possui permuta?", ["Não possui", "Possui 1 permuta", "Possui 2 permutas", "Possui 3 ou mais permutas"] ,key="permuta")
        with c1: concorrencia = st.multiselect("Possui concorrência?", ["Exclusivo Giga+ Fibra", "Claro", "Vivo", "TIM", "Oi", "Brisanet", "Multiplay (Alares)", "Algar Telecom", "ProveNET", "Velocinet Provedor", "Byteplay Connect", "QNet Telecom", "Telefibra", "HD Provedor", "Lay Provedor", "Fortalnet", "RedeNet Telecom", "WireXtreme", "Infortec", "JWS Provedor", "Argohost Net", "Orion Telecom", "Bayde Net", "Ciberdyne Internet", "Wire Link", "Ponto Net", "Linknet Provedor", "Outros"], key="concorrencia")
        with c2: outros_conc = st.text_input("Outros", key="outros_conc")
        
        with st.expander("Contatos"):
            df_contatos = pd.DataFrame(
                [
                    {
                        "Nome": "",
                        "Cargo": "",
                        "Telefone": "",
                        "Email": "",
                    },
                ]
            )

            contatos = st.data_editor(
                df_contatos,
                column_config={
                    "Nome": st.column_config.TextColumn("Nome"),
                    "Cargo": st.column_config.SelectboxColumn(
                        "Cargo",
                        options=[
                            'Síndico', 
                            'Administrador', 
                            'Porteiro', 
                            'Zelador', 
                            'Segurança',
                            'Outro'
                        ],
                        required=True,
                    ),
                    "Telefone": st.column_config.TextColumn("Telefone"),
                    "E-mail": st.column_config.TextColumn("E-mail"),
                },
                hide_index=True,
                num_rows="dynamic",
                key="contatos",
            )

        with st.expander("Parceiros"):
            df_parceiros = pd.DataFrame(
                [
                    {
                        "Nome da Empresa": "",
                        "Tipo de Negócio": "",
                        "Pessoa de Contato": "",
                        "Telefone do Parceiro": "",
                    },
                ]
            )
            parceiros = st.data_editor(
                df_parceiros,
                column_config={
                    "Nome da Empresa": st.column_config.TextColumn("Nome da Empresa"),
                    "Tipo de Negócio": st.column_config.SelectboxColumn(
                        "Tipo de Negócio",
                        options=[
                            'Máquinas de vendas',
                            'Mercearia interna',
                            'Lavanderia',
                            'Geladeiras inteligentes',
                            'Dog Walker',
                            'Food Trucks',
                            'Automação residencial',
                            'Estação de carregamento para carros elétricos',
                            'Outro'
                        ],
                        required=True,
                    ),
                    "Pessoa de Contato": st.column_config.TextColumn("Pessoa de Contato"),
                    "Telefone do Parceiro": st.column_config.TextColumn("Telefone do Parceiro"),
                },
                hide_index=True,
                num_rows="dynamic",
                key="parceiros",
            )
        
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success("Formulário enviado com sucesso!")

            dataInicial = datetime.combine(dt_inicio, hr_inicio)
            dataFinal = datetime.combine(dt_fim, hr_fim)

            if dataInicial > dataFinal:
                st.error("Data inicial deve ser menor que data final")
            elif not(dt_inicio, hr_inicio, dt_fim, hr_fim, condominio, torres, andares, apto_andar, permuta, concorrencia):
                st.error("Preencha todos os campos obrigatórios")
            else:
                id_condominio = get_id_condominio(condominio)
                response = {
                    "qtde_torres": torres,
                    "qtde_andares": andares,
                    "qtde_apto_andar": apto_andar,
                    "permuta": permuta,
                    "concorrencia": concorrencia,
                    "outros_conc": outros_conc,
                    "contatos": 
                        [
                            {"Nome": i[0], "Cargo": i[1], "Telefone": i[2], "Email": i[3]} 
                            for i in contatos.itertuples() 
                        ],
                    "parceiros": 
                        [
                            {"Nome da Empresa": i[0], "Tipo de Negócio": i[1], "Pessoa de Contato": i[2], "Telefone do Parceiro": i[3]} 
                            for i in parceiros.itertuples()
                        ],
                }

                inserir_visita(id_condominio, dataInicial, dataFinal, st.session_state['username'], tipo_forms, subtipo_forms, json.dumps(response, ensure_ascii=False))


                
