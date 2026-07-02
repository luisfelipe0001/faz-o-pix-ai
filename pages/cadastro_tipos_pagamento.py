import streamlit as st
from services.tipo_pagamento_service import TipoPagamentoService

def show():
    """Página de Cadastro de Tipos de Pagamento"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("💳 Tipos de Pagamento")
    st.markdown("Configure os tipos de pagamento para seus empréstimos")
    st.markdown("---")

    service = TipoPagamentoService()
    user_id = st.session_state.get("user_id")

    col1, col2 = st.columns([2, 1])

    # Formulário
    with col1:
        st.subheader("Novo Tipo de Pagamento")

        nome = st.text_input("Nome do Tipo *", placeholder="Ex: Cartão Crédito, PIX, Dinheiro")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Cadastrar", type="primary", use_container_width=True):
                if not nome:
                    st.error("Nome é obrigatório")
                else:
                    result = service.create(user_id, nome)
                    if result["success"]:
                        st.success(f"Tipo '{nome}' cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {result['error']}")

    with col2:
        st.subheader("Exemplos")
        st.markdown("""
        - Cartão Crédito
        - Cartão Débito
        - PIX
        - Dinheiro
        - Empréstimo Pessoal
        """)

    st.markdown("---")
    st.subheader("Tipos Cadastrados")

    result = service.list_by_user(user_id)
    if result["success"]:
        tipos = result["data"]
        if tipos:
            for tipo in tipos:
                with st.expander(f"💳 {tipo.nome}"):
                    # Botões de ação
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                    with col_btn1:
                        if st.button("✏️ Editar", key=f"edit_{tipo.id}", use_container_width=True):
                            st.session_state[f"edit_tipo_{tipo.id}"] = True
                    with col_btn2:
                        if st.button("🗑️ Deletar", key=f"delete_{tipo.id}", use_container_width=True):
                            res = service.delete(tipo.id)
                            if res["success"]:
                                st.success("Tipo deletado!")
                                st.rerun()

                    st.markdown("---")

                    # Modo edição
                    if st.session_state.get(f"edit_tipo_{tipo.id}"):
                        st.subheader("Editar Tipo")
                        new_nome = st.text_input("Nome", value=tipo.nome, key=f"edit_nome_{tipo.id}")

                        col_save1, col_save2 = st.columns(2)
                        with col_save1:
                            if st.button("💾 Salvar", key=f"save_{tipo.id}", use_container_width=True):
                                res = service.update(tipo.id, nome=new_nome)
                                if res["success"]:
                                    st.success("Tipo atualizado!")
                                    st.session_state[f"edit_tipo_{tipo.id}"] = False
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {res['error']}")
                        with col_save2:
                            if st.button("❌ Cancelar", key=f"cancel_{tipo.id}", use_container_width=True):
                                st.session_state[f"edit_tipo_{tipo.id}"] = False
                                st.rerun()
        else:
            st.info("Nenhum tipo de pagamento cadastrado. Comece adicionando um!")
    else:
        st.error(f"Erro ao carregar: {result['error']}")


if __name__ == "__main__":
    show()
