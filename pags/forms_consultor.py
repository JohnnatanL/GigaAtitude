import streamlit as st

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Visita Comercial – Giga+ Fibra",
    page_icon="📋",
    layout="centered",
)

# ── CSS customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    min-height: 100vh;
}

section[data-testid="stSidebar"] { display: none; }

.block-container {
    max-width: 760px;
    padding: 2.5rem 2rem 4rem;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
}

.header-card {
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    border: none;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.header-card h1 {
    color: white;
    font-size: 1.6rem;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-card p {
    color: rgba(255,255,255,0.85);
    margin: 0.4rem 0 0;
    font-size: 0.9rem;
}

.section-label {
    color: #f97316;
    font-family: 'Sora', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* Inputs */
label { color: #cbd5e1 !important; font-size: 0.9rem !important; }
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 2px rgba(249,115,22,0.25) !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: #f97316 !important;
}

/* Radio */
.stRadio > div { gap: 0.5rem; }
.stRadio label { color: #cbd5e1 !important; }

/* Number input */
.stNumberInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}

/* Submit button */
.stButton > button {
    width: 100%;
    padding: 0.85rem;
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: white;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: opacity 0.2s;
    letter-spacing: 0.3px;
}
.stButton > button:hover { opacity: 0.88; }

.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.2rem 0;
}

.warning-text {
    color: #fbbf24;
    font-size: 0.78rem;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1>📋 Formulário de Visita Comercial</h1>
    <p>Giga+ Fibra · Registro de Prospecção</p>
</div>
""", unsafe_allow_html=True)

# ── Listas de opções ─────────────────────────────────────────────────────────
CONDOMINIOS = [
    "EDIFICIO CONSONATA", "CONDOMINIO G TORRES", "CONDOMINIO SAN CARLO",
    "CONDOMINIO EDIFICIO LORENZO PALACE", "CONDOMINIO STRAUSS",
    "EDIFICIO SALOMAO", "CONDOMINIO EDIFICIO AMAZONIA",
    "CONDOMINIO VICENTE LEITE", "Blue Residence", "EDIFICIO ALVORADA PARK",
    "CONDOMINIO PLAZA VERONNESE", "EDIFICIO SAN LUIGI",
    "CONDOMINIO PALATIUM RESIDENCIAL MEIRELES",
    "CONDOMINIO EDIFICIO CLARISSE SALLES FURLANI", "CONDOMINIO ANA MARIA",
    "CONDOMINIO EDIFICIO D'JOM", "EDIFICIO ABOLIÇÃO TOWER",
    "CONDOMINIO EDIFICIO ALTAVISTA", "Artiz Meireles", "Beach Class Meireles",
    "ICON CONDOMINIUM", "LC CORPORATE", "CONDOMINIO PACO DO BEM",
    "CONDOMINIO BOSSA NOVA",
]

CONTATOS = ["Porteiro", "Zelador", "Síndico", "Segurança", "Administrador"]

PARCEIROS = [
    "Máquinas de vendas", "Mercearia interna", "Lavanderia",
    "Geladeiras inteligentes (bebidas alcoólicas)", "Dog Walker",
    "Food Trucks", "Automação residencial",
    "Estação de carregamento para carros elétricos",
]

PERMUTA_OPTS = [
    "Não.", "Possui uma permuta", "Possui duas Permutas",
    "Possui três ou mais permutas.",
]

CONCORRENTES = [
    "Prédio Exclusivo Giga+ Fibra", "Claro", "Vivo", "TIM", "Oi",
    "Brisanet", "Multiplay (Alares)", "Algar Telecom", "ProveNET",
    "Velocinet Provedor", "Byteplay Connect", "QNet Telecom", "Telefibra",
    "HD Provedor", "Lay Provedor", "Fortalnet", "RedeNet Telecom",
    "WireXtreme", "Infortec", "JWS Provedor", "Argohost Net",
    "Orion Telecom", "Bayde Net", "Ciberdyne Internet", "Wire Link",
    "Ponto Net", "Linknet Provedor",
]

# ── Seção 1 – Condomínio ────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">1 · Identificação</div>', unsafe_allow_html=True)
condominio = st.selectbox("Condomínio *", ["— Selecione —"] + CONDOMINIOS)
st.markdown('</div>', unsafe_allow_html=True)

# ── Seção 2 – Contato ───────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">2 · Contato</div>', unsafe_allow_html=True)
contato_tipo = st.radio("Contato com *", CONTATOS, horizontal=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
nome_contato   = st.text_input("3. Nome do Contato *")
telefone       = st.text_input("4. Telefone do Contato *", placeholder="(85) 9 9999-9999")
email_contato  = st.text_input("5. E-mail do Contato", placeholder="exemplo@email.com")
st.markdown('</div>', unsafe_allow_html=True)

# ── Seção 3 – Parceiros ─────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">6 · Potenciais Parceiros</div>', unsafe_allow_html=True)
st.caption("Selecione no máximo 3 opções.")
parceiros_sel = st.multiselect("Tipo de parceiro", PARCEIROS, max_selections=3)
if len(parceiros_sel) > 3:
    st.markdown('<p class="warning-text">⚠️ Selecione no máximo 3 opções.</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
nome_parceiro   = st.text_input("7. Nome dos Potenciais Parceiros (Empresa)")
resp_parceiro   = st.text_input("8. Pessoa Responsável nos Potenciais Parceiros (Nome)")
st.markdown('</div>', unsafe_allow_html=True)

# ── Seção 4 – Fornecedores & Ofertas ────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">9–10 · Fornecedores & Ofertas</div>', unsafe_allow_html=True)
fornecedores = st.text_area("9. Fornecedores", height=90)
ofertas      = st.text_area("10. Ofertas", height=90)
st.markdown('</div>', unsafe_allow_html=True)

# ── Seção 5 – Permuta & Concorrência ────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">11–12 · Permuta & Concorrência</div>', unsafe_allow_html=True)
permuta      = st.radio("11. Prédio possui permuta? *", PERMUTA_OPTS)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
concorrencia = st.multiselect("12. Possui concorrência?", CONCORRENTES)
st.markdown('</div>', unsafe_allow_html=True)

# ── Seção 6 – Observações & Estrutura ───────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">13–16 · Observações & Estrutura</div>', unsafe_allow_html=True)
observacao  = st.text_area("13. Observação", height=100)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    qtd_torres  = st.number_input("14. Qtd. Torres",   min_value=0, step=1)
with col2:
    qtd_andares = st.number_input("15. Qtd. Andares",  min_value=0, step=1)
with col3:
    apts_andar  = st.number_input("16. Apts. p/ Andar", min_value=0, step=1)
st.markdown('</div>', unsafe_allow_html=True)

# ── Envio ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✅ Enviar Formulário"):
    erros = []
    if condominio == "— Selecione —":
        erros.append("Selecione o **Condomínio**.")
    if not nome_contato.strip():
        erros.append("Preencha o **Nome do Contato**.")
    if not telefone.strip():
        erros.append("Preencha o **Telefone do Contato**.")

    if erros:
        for e in erros:
            st.error(e)
    else:
        st.success("🎉 Formulário enviado com sucesso!")
        with st.expander("📄 Resumo da resposta"):
            st.markdown(f"""
| Campo | Valor |
|---|---|
| **Condomínio** | {condominio} |
| **Contato com** | {contato_tipo} |
| **Nome** | {nome_contato} |
| **Telefone** | {telefone} |
| **E-mail** | {email_contato or '—'} |
| **Parceiros** | {', '.join(parceiros_sel) or '—'} |
| **Empresa Parceira** | {nome_parceiro or '—'} |
| **Responsável Parceiro** | {resp_parceiro or '—'} |
| **Fornecedores** | {fornecedores or '—'} |
| **Ofertas** | {ofertas or '—'} |
| **Permuta** | {permuta} |
| **Concorrência** | {', '.join(concorrencia) or '—'} |
| **Observação** | {observacao or '—'} |
| **Torres / Andares / Apts.** | {int(qtd_torres)} / {int(qtd_andares)} / {int(apts_andar)} |
""")