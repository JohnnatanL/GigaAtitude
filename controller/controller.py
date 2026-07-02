import datetime
from auth import conecta_supabase
import pandas as pd
import re
import streamlit as st

def limpa_telefone(telefone):
    if telefone is None:
        return None
    return re.sub(r'\D', '', str(telefone))

def get_carteira_vendedor(username):

    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """
    WITH ultimo_periodo AS (
    SELECT MAX(periodo) AS periodo
    FROM tbcarteira
    where vendedor = %s
)
SELECT id_condominio
FROM tbcarteira
WHERE periodo = (SELECT periodo FROM ultimo_periodo) and
vendedor = %s;"""

    cursor.execute(query, (username, username))
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    cursor.close()
    conn.close()

    return df

def get_condominios(username, role):

    if role == "consultor":
        carteira = get_carteira_vendedor(username)
        
        if carteira.empty:
            where = "and 1=0"  # nenhuma carteira -> nenhum condomínio
        else:
            ids = ",".join(
                f"""'{str(v).replace("'", "''")}'""" if not pd.isna(v) else "NULL"
                for v in carteira["id_condominio"]
            )
            where = f"and c.id in ({ids})"
    else:
        where = "and 1=1"

    conn = conecta_supabase()
    cursor = conn.cursor()

    query = f"""select
        concat(c.nome, ' (',
            c.cidade, '-',
            c.sigla_estado, ', ',
            c.bairro, ', ',
            c.logradouro, ', ',
            c.numero, ', ',
            c.cep, ')'
            )
        FROM tb_condominio c
        where c.status = '11 - Liberado para venda'
        {where};
    """

    cursor.execute(query)
    result = cursor.fetchall()

    lista = [row[0] for row in result]

    cursor.close()
    conn.close()

    return lista

def round_to_quarter():
    t = datetime.datetime.now()
    # Arredonda os minutos para baixo ao múltiplo de 15 mais próximo
    rounded_minutes = (t.minute // 15) * 15
    return t.replace(minute=rounded_minutes, second=0, microsecond=0)

def get_id_condominio(nome_condominio):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """select
        c.id
        FROM tb_condominio c
        where concat(c.nome, ' (',
            c.cidade, '-',
            c.sigla_estado, ', ',
            c.bairro, ', ',
            c.logradouro, ', ',
            c.numero, ', ',
            c.cep, ')') = %s;"""

    cursor.execute(query, (nome_condominio,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]

def inserir_visita(id_condominio, data_inicio, data_fim, usuario, tipo_forms, subtipo_forms, response, observacoes, status_entrada):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """INSERT INTO tbvisita (
				                    id_condominio,
									dt_inicio,
									dt_fim,
                                    usuario,
									tipo_forms,
									subtipo_forms,
                                    response,
                                    observacoes,
                                    status_entrada
									)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    
    cursor.execute(query, (id_condominio, data_inicio, data_fim, usuario, tipo_forms, subtipo_forms, response, observacoes, status_entrada))
    conn.commit()

    cursor.close()
    conn.close()

def get_visitas(usuarios):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """select 
    v.id as "idVisita",
    concat(
        c.nome, ' (',
        c.cidade, '-',
        c.sigla_estado, ', ',
        c.bairro, ', ',
        c.logradouro, ', ',
        c.numero, ', ',
        c.cep, ')'
    ) as condominio,
    to_char(v.dt_inicio, 'DD/MM/YYYY HH24:MI') as "Data Inicio",
    to_char(v.dt_fim, 'DD/MM/YYYY HH24:MI') as "Data Fim",
    v.usuario as "Usuario",
    v.response->>'qtde_torres'     AS "QtdeTorres",
    v.response->>'qtde_andares'    AS "QtdeAndares",
    v.response->>'qtde_apto_andar' AS "QtdeAptoPorAndar",
    v.response->>'permuta'         AS "Permuta",
    (
        SELECT string_agg(valor, ' | ')
        FROM jsonb_array_elements_text(v.response::jsonb->'concorrencia') AS valor
    ) AS "Concorrencia",
    (
        SELECT string_agg(
            concat_ws(
                ' - ',
                contato->>'Nome',
                contato->>'Cargo',
                contato->>'Telefone'
            ),
            ' | '
        )
        FROM jsonb_array_elements(v.response::jsonb->'contatos') AS contato
    ) AS "Contatos",
    (
        SELECT string_agg(
            concat_ws(
                ' - ',
                parceiro->>'Nome da Empresa',
                parceiro->>'Tipo de Negócio',
                parceiro->>'Pessoa de Contato',
                parceiro->>'Telefone do Parceiro'
            ),
            ' | '
        )
        FROM jsonb_array_elements(v.response::jsonb->'parceiros') AS parceiro
    ) AS "Parceiros"
FROM tbvisita v
left join tb_condominio c on v.id_condominio = c.id
where usuario in (%s);"""

    cursor.execute(query, (usuarios,))
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    cursor.close()
    conn.close()

    return df

def get_consultores(gestor, dt_inicio, dt_fim):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """SELECT
        distinct(concat(u.nome, ' (', u.username, ')'))
    FROM tbusuarios u
    LEFT JOIN tbhierarquia h on u.id = h.id_usuario
    WHERE (h.gestor_direto = %s) and (h.periodo between %s and %s);"""

    cursor.execute(query, (gestor, dt_inicio, dt_fim))
    result = cursor.fetchall()

    lista = []
    for row in result:
        lista.append(row[0])

    cursor.close()
    conn.close()

    return lista

def get_visita_by_id(id_visita):
    conn = conecta_supabase()
    cursor = conn.cursor()
    query = """select
        concat(
            c.nome, ' (',
            c.cidade, '-',
            c.sigla_estado, ', ',
            c.bairro, ', ',
            c.logradouro, ', ',
            c.numero, ', ',
            c.cep, ')'
        ) as condominio,
        v.*
    FROM tbvisita v
    left JOIN tb_condominio c on v.id_condominio = c.id
    where v.id = %s;"""

    cursor.execute(query, (id_visita,))
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    cursor.close()
    conn.close()

    return df

def update_visita(id_visita, response):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """UPDATE tbvisita
    SET response = %s
    WHERE id = %s;"""

    cursor.execute(query, (response, id_visita))
    conn.commit()

    cursor.close()
    conn.close()

def validar_lead_repetido(condominio, telefone, banco):
    conn = conecta_supabase()
    cursor = conn.cursor()

    id_condominio = get_id_condominio(condominio)
    telefone_limpo = limpa_telefone(telefone)

    if banco =="tbleads":
        query = """select *
        from tbleads
        where id_condominio = %s
        and telefone = %s;"""
    elif banco =="tbficha":
        query = """select *
        from tbficha
        where id_condominio = %s
        and telefone = %s;"""
    cursor.execute(query, (id_condominio, telefone_limpo))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return True
    else:
        return False

def inserir_leads(condominio, nome, telefone, apt_bloco, vendedor):

    id_condominio = get_id_condominio(condominio)
    telefone_limpo = limpa_telefone(telefone)

    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """INSERT INTO tbleads (
                id_condominio,
                nome,
                telefone,
                bloco_apt,
                vendedor
                )
                VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (id_condominio, nome, telefone_limpo, apt_bloco, vendedor))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def inserir_ficha(condominio, nome, cargo, telefone, torres, andares, apt_andar, hp_inf, hf, vendedor):
    id_condominio = get_id_condominio(condominio)
    telefone_limpo = limpa_telefone(telefone)

    conn = conecta_supabase()
    cursor = conn.cursor()

    hp_real = torres * andares * apt_andar

    query = """INSERT INTO tbficha (
                id_condominio,
                nome,
                cargo,
                telefone,
                torres,
                andares,
                apt_andar,
                hp_inf,
                hf,
                vendedor,
                hp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(query, (id_condominio, nome, cargo, telefone_limpo, torres, andares, apt_andar, hp_inf, hf, vendedor, hp_real))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def inserir_checkin(condominio, dt_inicio, dt_fim, vendedor):
    id_condominio = get_id_condominio(condominio)

    conn = conecta_supabase()
    cursor = conn.cursor()

    status = False
    query = """INSERT INTO tbacao (
                id_condominio,
                dt_inicio,
                dt_fim,
                vendedor,
                status
                )
                VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (id_condominio, dt_inicio, dt_fim, vendedor, status))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def ler_checkout(vendedor):
    conn = conecta_supabase()
    cursor = conn.cursor()
    query = """
    select concat_ws(' | ',
    a.id,
    concat('Condominio: ',c.nome),
    concat('Data Inicio: ', TO_CHAR(a.dt_inicio, 'DD/MM/YYYY HH24:MI')),
    concat('Data Fim: ', TO_CHAR(a.dt_fim, 'DD/MM/YYYY HH24:MI'))
    ) as valor
    from tbacao a
    left join tb_condominio c on a.id_condominio = c.id
    where a.status = False and
    a.vendedor = %s;"""
    cursor.execute(query, (vendedor,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    df = pd.DataFrame(result, columns=["valor"])
    return df
    
def inserir_checkout(id, leads, vendas):
    conn = conecta_supabase()
    cursor = conn.cursor()
    
    query = """UPDATE tbacao
    SET status = True,
    leads = %s,
    vendas = %s
    WHERE id = %s;"""
    cursor.execute(query, (leads, vendas, id))
    conn.commit()
    cursor.close()
    conn.close()
    return True


    
    



