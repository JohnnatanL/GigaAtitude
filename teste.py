from auth import conecta_supabase
import bcrypt
import pandas as pd
from controller.user_control import resetar_senha

conn = conecta_supabase()
cursor = conn.cursor()

query = """
SELECT id, username FROM tbusuarios WHERE id >= '5';
"""

cursor.execute(query)
result = cursor.fetchall()

df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

for idx, row in df.iterrows():
    resetar_senha(row['id'], row['username'])

cursor.close()
conn.close()