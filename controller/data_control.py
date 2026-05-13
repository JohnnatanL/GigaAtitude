import pandas as pd
from auth import conecta_databricks
import streamlit as st
from controller.controller import (
    get_condominios,
    round_to_quarter,
    get_id_condominio,
    get_visitas,
    get_consultores
)

def vendas():
    conn = conecta_databricks()
    cursor = conn.cursor()

    query = """select
        v.*,
        ftta.flag_ftta,
        year (a.data_ativacao) as ano_ativacao,
        month (a.data_ativacao) as mes_ativacao,
        day (a.data_ativacao) as dia_ativacao
    from gold.kpis_oficiais.tbl_kpi_vendas as v
    left join gold.base.fato_marcador_cliente_ftta as ftta
    on v.id_contrato = ftta.contrato_codigo
    left join gold.base.fato_primeira_ativacao as a
    on v.id_contrato = a.id_contrato
    where lower(email_vendedor) in (
        'andressa.reis@alloha.com',
        'larissa.delboni@alloha.com',
        'gilberto.neto@alloha.com',
        'scarlett.rodrigues@alloha.com',
        'marcos.tonin@alloha.com',
        'marco.paz@alloha.com',
        'denerson.lima@alloha.com',
        'jackson.fontes@alloha.com',
        'rodrigo.guimaraes@alloha.com',
        'maria.scosta@alloha.com',
        'kathleen.silva@alloha.com',
        'mariane.sobreira@alloha.com',
        'victor.galdeano@alloha.com',
        'ricardo.batista@alloha.com',
        'renata.liberato@alloha.com',
        'gislene.souza@alloha.com',
        'cairene.santana@alloha.com',
        'fabrini.lessa@alloha.com',
        'sandra.freitas@alloha.com',
        'marilia.dominguez@alloha.com',
        'juliana.torres@alloha.com',
        'flavia.lima@alloha.com',
        'camila.guedes@alloha.com',
        'paula.barbosa@alloha.com',
        'valluza.oliveira@sumicity.net.br',
        'camillo.mayrink@alloha.com',
        'wellisson.lima@alloha.com',
        'nicoly.barros@alloha.com',
        'arthur.wigner@alloha.com',
        'tatiana.alianca@alloha.com',
        'silvania.andrade@alloha.com',
        'nayuri.ferreira@alloha.com',
        'basilio.junior@alloha.com',
        'felipe.ronaldy@alloha.com',
        'antonia.moreira@alloha.com',
        'miguelangelo.souza@alloha.com',
        'ruan.fontes@alloha.com',
        'marcos.jesus@alloha.com',
        'aline.morais@alloha.com',
        'jessica.assis@alloha.com'
    )
    and ano = 2026
    and mes >= 3"""

    cursor.execute(query)
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[description[0] for description in cursor.description])
    
    return df