import streamlit as st
from services.pessoa_service import PessoaService

def show():
    """Página de Cadastro de Pessoas"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("👥 Cadastro de Pessoas")
    st.markdown("Cadastre as pessoas para quem você empresta dinheiro")
    st.markdown("---")

    service = PessoaService()
    user_id = st.session_state.get("user_id")

    col1, col2 = st.columns([2, 1])

    # Coluna esquerda: Formulário
    with col1:
        st.subheader("Nova Pessoa")

        nome = st.text_input("Nome *")
        email = st.text_input("Email (opcional)")
        telefone = st.text_input("Telefone (opcional)")

        if st.button("Cadastrar Pessoa", type="primary"):
            if not nome:
                st.error("Nome é obrigatório")
            else:
                result = service.create(user_id, nome, email, telefone)
                if result["success"]:
                    st.success(f"Pessoa '{nome}' cadastrada com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro: {result['error']}")

    # Coluna direita: Lista
    with col2:
        st.subheader("Contatos")

    st.markdown("---")
    st.subheader("Pessoas Cadastradas")

    result = service.list_by_user(user_id)
    if result["success"]:
        pessoas = result["data"]
        if pessoas:
            for pessoa in pessoas:
                with st.expander(f"👤 {pessoa.nome}"):
                    # Botões de ação
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                    with col_btn1:
                        if st.button("✏️ Editar", key=f"edit_{pessoa.id}", use_container_width=True):
                            st.session_state[f"edit_pessoa_{pessoa.id}"] = True
                    with col_btn2:
                        if st.button("🗑️ Deletar", key=f"delete_{pessoa.id}", use_container_width=True):
                            res = service.delete(pessoa.id)
                            if res["success"]:
                                st.success("Pessoa deletada!")
                                st.rerun()

                    st.markdown("---")

                    # Modo edição
                    if st.session_state.get(f"edit_pessoa_{pessoa.id}"):
                        st.subheader("Editar Pessoa")
                        new_nome = st.text_input("Nome", value=pessoa.nome, key=f"edit_nome_{pessoa.id}")
                        new_email = st.text_input("Email", value=pessoa.email or "", key=f"edit_email_{pessoa.id}")
                        new_telefone = st.text_input("Telefone", value=pessoa.telefone or "", key=f"edit_tel_{pessoa.id}")

                        col_save1, col_save2 = st.columns(2)
                        with col_save1:
                            if st.button("💾 Salvar", key=f"save_{pessoa.id}", use_container_width=True):
                                res = service.update(
                                    pessoa.id,
                                    nome=new_nome,
                                    email=new_email if new_email else None,
                                    telefone=new_telefone if new_telefone else None,
                                )
                                if res["success"]:
                                    st.success("Pessoa atualizada!")
                                    st.session_state[f"edit_pessoa_{pessoa.id}"] = False
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {res['error']}")
                        with col_save2:
                            if st.button("❌ Cancelar", key=f"cancel_{pessoa.id}", use_container_width=True):
                                st.session_state[f"edit_pessoa_{pessoa.id}"] = False
                                st.rerun()

                        st.markdown("---")

                    # Informações
                    if pessoa.email:
                        st.write(f"**Email:** {pessoa.email}")
                    if pessoa.telefone:
                        st.write(f"**Telefone:** {pessoa.telefone}")
        else:
            st.info("Nenhuma pessoa cadastrada ainda")
    else:
        st.error(f"Erro ao carregar: {result['error']}")


if __name__ == "__main__":
    show()
