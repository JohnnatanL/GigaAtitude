import streamlit as st
from pags.tela_login import tela_login

# Paginas
home = st.Page("pags/home.py", title="Inicio", icon="🏠")

forms_consultor = st.Page("pags/forms_consultor.py", title="Formulário de Visita Comercial", icon="📋", default=True)
gerenc_users = st.Page("pags/gerenc_users.py", title="Gerenciamento de Usuários", icon="👥")
rel_muralha = st.Page("pags/vendas_du.py", title="Relatório - Projeto Muralha", icon="🎯")

def main():
    if st.session_state.get("authenticated"):

        if st.session_state.get("role") == "admin":
            pg = st.navigation({"Inicio": [home, gerenc_users, forms_consultor, rel_muralha]})
            pg.run()

        elif st.session_state.get("role") == "planejamento":
            pg = st.navigation({"Inicio": [home, gerenc_users, rel_muralha]})
            pg.run()

        elif st.session_state.get("role") == "gestao":
            pg = st.navigation({"Inicio": [home, forms_consultor, ]})
            pg.run()

        elif st.session_state.get("role") == "consultor":
            pg = st.navigation({"Inicio": [home, forms_consultor]})
            pg.run()

    else:
        
        tela_login()

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    main()
