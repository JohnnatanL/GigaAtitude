import streamlit as st
from controller.login import autenticar_usuario
from controller.user_control import alterar_senha
from controller.hidden import hidden
from time import sleep
from stylo.css import aplicar_css_global    

def tela_login():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    hidden()
    #aplicar_css_global()
    st.title("Login")
    with st.form("login_form"):
        us1, us2, us3 = st.columns(3)
        ps1, ps2, ps3 = st.columns(3)

        with us2:
            username = st.text_input("Username")
        with ps2:
            password = st.text_input("Password", type="password")

        s1, s2, s3 = st.columns(3)
        with s2: submitted = st.form_submit_button("Login")

        if submitted:
            
            role = autenticar_usuario(username.lower(), password)

            if role:
                user_reset = username.lower().split('.')[0]
                if password == f"{user_reset}@AltoValor":
                    mudar_senha(username)
                else:
                    st.session_state['role'] = role
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
            else:
                st.error("Credenciais inválidas")

@st.dialog("Mude sua senha!")
def mudar_senha(username):
    #st.title("Mudar Senha")
    with st.form("mudar_senha_form"):
        st.text(f"""Usuário: {username}""")
        senha1 = st.text_input("Senha", type="password")
        senha2 = st.text_input("Confirmar Senha", type="password")
        submitted = st.form_submit_button("Mudar Senha")
        if submitted:
            if senha1 == senha2:
                retorno = alterar_senha(username, senha1)
                if retorno == True:
                    st.success("Senha alterada com sucesso")
                    sleep(2)
                    st.rerun()
                else:
                    st.error("Erro ao alterar senha")
            elif senha1 != senha2:
                st.error("Senhas não conferem")
            else:
                st.error("Erro ao alterar senha")