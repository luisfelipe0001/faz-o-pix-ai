import streamlit as st
from config.settings import STREAMLIT_PAGE_TITLE, STREAMLIT_PAGE_ICON, STREAMLIT_LAYOUT
from utils.auth import get_current_user
import sys

# Configurações do Streamlit
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded",
)

# Inicializar session_state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_id = None

# Verificar se há sessão ativa
if not st.session_state.authenticated:
    current_user = get_current_user()
    if current_user:
        st.session_state.authenticated = True
        st.session_state.user_id = current_user.id

# CSS customizado
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Página principal
if st.session_state.authenticated:
    # Sidebar navegação
    st.sidebar.title("💰 Faz o Pix AI")
    st.sidebar.markdown("---")

    menu_options = [
        ("🏠 Dashboard", "dashboard"),
        ("👥 Cadastro de Pessoas", "pessoas"),
        ("💳 Tipos de Pagamento", "tipos"),
        ("🏦 Meus Cartões", "cartoes"),
        ("💰 Gerenciar Dívidas", "dividas"),
        ("👤 Cadastro de Usuário", "usuario"),
    ]

    selected = st.sidebar.radio("Menu", menu_options, format_func=lambda x: x[0])

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        from utils.auth import logout_user
        logout_user()
        st.rerun()

    # Rotear para página
    if selected[1] == "dashboard":
        from pages.home import show as show_dashboard
        show_dashboard()
    elif selected[1] == "pessoas":
        from pages.cadastro_pessoas import show as show_pessoas
        show_pessoas()
    elif selected[1] == "tipos":
        from pages.cadastro_tipos_pagamento import show as show_tipos
        show_tipos()
    elif selected[1] == "cartoes":
        from pages.cadastro_cartoes import show as show_cartoes
        show_cartoes()
    elif selected[1] == "dividas":
        from pages.gerenciar_dividas import show as show_dividas
        show_dividas()
    elif selected[1] == "usuario":
        from pages.cadastro_usuario import show as show_usuario
        show_usuario()

else:
    # Mostrar página de login
    from pages.login import show as show_login
    show_login()
