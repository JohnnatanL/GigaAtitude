from controller.controller import inserir_visita
import numpy as np
import streamlit as st
from controller.controller import (get_condominios,
                                    round_to_quarter,
                                    get_id_condominio,
                                    get_visitas,
                                    get_visita_by_id,
                                    get_consultores,
                                    update_visita)
import pandas as pd
from datetime import datetime
import datetime as dt
from auth import conecta_supabase
import json
from time import sleep

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Visita Comercial – Giga+ Fibra",
    page_icon="📋",
    layout="wide",
)

@st.dialog("Detalhes da Visita", width="medium")
def mostrar_detalhes(id_visita):
    visita = get_visita_by_id(id_visita)

    f = visita.loc[
        visita["id"] == id_visita
    ].iloc[0]
    st.markdown(f"**Condominio:** {f['condominio']}")
    coll1, coll2 = st.columns(2)
    with coll1: st.markdown(f"**Data de Início:** {f['dt_inicio'].strftime('%d/%m/%Y %H:%M')}")
    with coll2: st.markdown(f"**Data de Término:** {f['dt_fim'].strftime('%d/%m/%Y %H:%M')}")


    df_contatos = pd.DataFrame([
        {
            "Nome": "",
            "Cargo": "",
            "Telefone": "",
            "Email": "",
        }]
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

    # Contatos
    lista_contatos = [
        {
            "cid": i[0],
            "Nome": i[1],
            "Cargo": i[2],
            "Telefone": i[3],
            "Email": i[4],
        }
        for i in contatos.itertuples()
        if any([
            str(i[1]).strip(),
            str(i[2]).strip(),
            str(i[3]).strip(),
            str(i[4]).strip()
        ])
    ]

    response = visita['response'].iloc[0]

    if isinstance(response, str):
        response = json.loads(response)

    if lista_contatos:
        response["contatos"] = lista_contatos

    if st.button("Salvar Contatos"):
        update_visita(id_visita, json.dumps(response, ensure_ascii=False))
        st.success("Contatos salvos com sucesso!")
        sleep(0.7)
        st.rerun()


st.title("👋 :grey[Visita Comercial]")

pills = st.pills(label="", options=["Nova Visita", "Histórico de Visitas", "Editar Visitas"])

if pills == "Editar Visitas":

    if st.session_state['role'] == "consultor":

        username = st.session_state['username']
        df_visitas = get_visitas(username)

        df_visitas['contacts'] = np.select(
            [df_visitas['Contatos'] == ' -  - ', df_visitas['Contatos'].isnull()],
            ["Sem Contato", "Sem Contato"],
            default=df_visitas['Contatos']
        )

        df_editar_visitas = df_visitas[
            df_visitas['contacts'] == 'Sem Contato'
        ][['idVisita', 'condominio', 'Data Inicio', 'Data Fim', 'Usuario', 'contacts']]

        if df_editar_visitas.empty:
            st.info("Nenhum visita sem contato.", icon="ℹ️")
            st.stop()
        else:
            for _, row in df_editar_visitas.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 1, 1, 1, 1])
                col1.write(row["idVisita"])
                col2.write(row["condominio"])
                col3.write(row["Data Inicio"])
                col4.write(row["Data Fim"])
                col5.write(row["Usuario"])

                if col6.button(
                    "🔍 Detalhes", key=f"detalhes_{row['idVisita']}", width="stretch"
                ):
                    mostrar_detalhes(row["idVisita"])

elif pills == "Histórico de Visitas":
    with st.form("hist_visita"):

        cola, colb = st.columns([1, 5])

        with cola:
            data = st.date_input(
                "Selecione o período",
                value=[
                    pd.to_datetime("today").replace(day=1),
                    pd.to_datetime("today"),
                ],
                format="DD.MM.YYYY",
                width=200,
            )

            try:
                data_inicial = data[0]
                data_final = data[1]

            except:
                st.info("Selecione um período válido!", icon="⚠️")

        with colb:

            if st.session_state['role'] == "gestao" and data_inicial and data_final:

                consultores = get_consultores(
                    st.session_state['username'],
                    data_inicial,
                    data_final
                )

                if consultores:
                    consultor = st.multiselect(
                        "Consultor",
                        options=consultores,
                        key="consultor",
                        default=consultores
                    )
                else:
                    st.warning("Nenhum consultor encontrado")

            elif st.session_state['role'] == 'consultor':

                consultor = st.selectbox(
                    "Consultor",
                    options=[st.session_state['username']],
                    key="consultor"
                )

        submitted = st.form_submit_button("Enviar")
        if submitted:
            df_visitas = pd.DataFrame()
            if st.session_state['role'] == 'consultor':
                username = st.session_state['username']
                df_visitas = pd.concat([df_visitas, get_visitas(username)])
            elif st.session_state['role'] == 'gestao':
                for c in consultor:
                    username = c.split('(')[1].replace(')', '')
                    df_visitas = pd.concat([df_visitas, get_visitas(username)])



            st.subheader("Visitas")
            st.dataframe(df_visitas, use_container_width=True, hide_index=True)


elif pills == "Nova Visita":
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
            df_contatos = pd.DataFrame([
                {
                    "Nome": "",
                    "Cargo": "",
                    "Telefone": "",
                    "Email": "",
                }]
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
            df_parceiros = pd.DataFrame([{
                    "Nome da Empresa": "",
                    "Tipo de Negócio": "",
                    "Pessoa de Contato": "",
                    "Telefone do Parceiro": "",
                }]
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

        observacoes = st.text_area("Observações", key="observacoes")
        
        submitted = st.form_submit_button("Enviar")
        if submitted:

            dataInicial = datetime.combine(dt_inicio, hr_inicio)
            dataFinal = datetime.combine(dt_fim, hr_fim)

            if dataInicial >= dataFinal:
                st.error("Data inicial deve ser anterior à data final")
            elif not all([dt_inicio, hr_inicio, dt_fim, hr_fim, condominio, torres, andares, apto_andar, permuta, concorrencia]):
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
                }

                # Contatos
                lista_contatos = [
                    {
                        "cid": i[0],
                        "Nome": i[1],
                        "Cargo": i[2],
                        "Telefone": i[3],
                        "Email": i[4],
                    }
                    for i in contatos.itertuples()
                    if any([
                        str(i[1]).strip(),
                        str(i[2]).strip(),
                        str(i[3]).strip(),
                        str(i[4]).strip()
                    ])
                ]

                if lista_contatos:
                    response["contatos"] = lista_contatos

                # Parceiros
                lista_parceiros = [
                    {
                        "pid": i[0],
                        "Nome da Empresa": i[1],
                        "Tipo de Negócio": i[2],
                        "Pessoa de Contato": i[3],
                        "Telefone do Parceiro": i[4],
                    }
                    for i in parceiros.itertuples()
                    if any([
                        str(i[1]).strip(),
                        str(i[2]).strip(),
                        str(i[3]).strip(),
                        str(i[4]).strip()
                    ])
                ]

                if lista_parceiros:
                    response["parceiros"] = lista_parceiros

                inserir_visita(id_condominio, dataInicial, dataFinal, st.session_state['username'], tipo_forms, subtipo_forms, json.dumps(response, ensure_ascii=False), observacoes)

                st.success("Formulário enviado com sucesso!")
                sleep(0.7)
                st.rerun()

                
