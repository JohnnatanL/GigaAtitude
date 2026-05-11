import datetime
from auth import conecta_supabase

def get_condominios():

    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """select
        concat(c.nome, ' (',
            c.cidade, '-',
            c.sigla_estado, ', ',
            c.bairro, ', ',
            c.logradouro, ', ',
            c.numero, ', ',
            c.cep, ')'
            )
        FROM tb_condominio c
        where c.status = '11 - Liberado para venda';
    """

    cursor.execute(query)
    result = cursor.fetchall()

    lista = []
    for row in result:
        lista.append(row[0])

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

def inserir_visita(id_condominio, data_inicio, data_fim, usuario, tipo_forms, subtipo_forms, response):
    conn = conecta_supabase()
    cursor = conn.cursor()

    query = """INSERT INTO tbvisita (
				                    id_condominio,
									dt_inicio,
									dt_fim,
                                    usuario,
									tipo_forms,
									subtipo_forms,
                                    response
									)
				VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    
    cursor.execute(query, (id_condominio, data_inicio, data_fim, usuario, tipo_forms, subtipo_forms, response))
    conn.commit()

    cursor.close()
    conn.close()