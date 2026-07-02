import streamlit as st
from services.user_service import UserService
import sys

def show():
    """Página de Login"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("💰 Faz o Pix AI")
        st.markdown("---")

        tab1, tab2 = st.tabs(["Login", "Cadastro"])

        with tab1:
            st.subheader("Entrar")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")

            if st.button("Entrar", key="login_button", use_container_width=True):
                if email and password:
                    service = UserService()
                    result = service.login(email, password)

                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user = result["data"]
                        st.session_state.user_id = result["data"].id
                        st.success("Logado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {result['error']}")
                else:
                    st.warning("Preencha todos os campos")

            st.markdown("---")
            st.subheader("🔑 Esqueceu a Senha?")
            reset_email = st.text_input("Digite seu email", key="reset_email", placeholder="seu@email.com")

            if st.button("Enviar Email de Recuperação", key="reset_button", use_container_width=True):
                if reset_email:
                    from utils.auth import request_password_reset
                    result = request_password_reset(reset_email)
                    if result["success"]:
                        st.success("✅ Email de recuperação enviado! Verifique sua caixa de entrada.")
                    else:
                        st.info("Se o email existir, você receberá um link de recuperação.")
                else:
                    st.warning("Digite um email válido")

        with tab2:
            st.subheader("Criar Conta")
            new_email = st.text_input("Email", key="register_email")
            new_password = st.text_input("Senha", type="password", key="register_password")
            new_password_confirm = st.text_input(
                "Confirmar Senha",
                type="password",
                key="register_password_confirm"
            )
            full_name = st.text_input("Nome Completo", key="register_name")

            if st.button("Cadastrar", key="register_button"):
                if not all([new_email, new_password, new_password_confirm, full_name]):
                    st.warning("Preencha todos os campos")
                elif new_password != new_password_confirm:
                    st.error("As senhas não conferem")
                else:
                    service = UserService()
                    result = service.register(new_email, new_password, full_name)

                    if result["success"]:
                        st.success("Conta criada com sucesso! Faça login agora.")
                        st.rerun()
                    else:
                        st.error(f"Erro: {result['error']}")


if __name__ == "__main__":
    # Verificar se já está autenticado
    if st.session_state.get("authenticated"):
        st.switch_page("pages/02_cadastro_usuario.py")
    else:
        show()
