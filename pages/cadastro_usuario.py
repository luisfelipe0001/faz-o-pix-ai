import streamlit as st
from services.user_service import UserService
from utils.auth import get_current_user

def show():
    """Página de Cadastro de Novo Usuário do Sistema"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("👤 Cadastro de Usuário do Sistema")
    st.markdown("---")

    st.info(
        "Esta página permite cadastrar outros usuários no sistema que possam acessar "
        "e gerenciar suas próprias dívidas independentemente."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Novo Usuário")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        password_confirm = st.text_input("Confirmar Senha", type="password")
        full_name = st.text_input("Nome Completo")

        if st.button("Cadastrar Usuário", type="primary"):
            if not all([email, password, password_confirm, full_name]):
                st.error("Preencha todos os campos")
            elif password != password_confirm:
                st.error("As senhas não conferem")
            else:
                service = UserService()
                result = service.register(email, password, full_name)

                if result["success"]:
                    st.success(f"Usuário {full_name} cadastrado com sucesso!")
                else:
                    st.error(f"Erro: {result['error']}")

    with col2:
        st.subheader("Instruções")
        st.markdown("""
        1. Preencha os dados do novo usuário
        2. O usuário receberá um email para confirmar o cadastro
        3. Após confirmar, poderá fazer login e gerenciar suas contas
        4. Cada usuário vê apenas seus próprios dados
        """)

    st.markdown("---")
    st.markdown("**Nota:** Múltiplos usuários podem usar este app independentemente.")


if __name__ == "__main__":
    show()
