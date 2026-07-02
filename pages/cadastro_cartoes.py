import streamlit as st
from services.cartao_service import CartaoService
from services.tipo_pagamento_service import TipoPagamentoService

def show():
    """Página de Cadastro de Cartões"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("💳 Meus Cartões")
    st.markdown("Cadastre seus cartões de crédito/débito para vincular aos empréstimos")
    st.markdown("---")

    user_id = st.session_state.get("user_id")
    cartao_service = CartaoService()
    tipo_service = TipoPagamentoService()

    # Carregar tipos de pagamento (apenas Crédito e Débito)
    tipos_result = tipo_service.list_by_user(user_id)
    if tipos_result["success"]:
        tipos = [t for t in tipos_result["data"] if t.nome in ["Cartão Crédito", "Cartão Débito"]]
    else:
        tipos = []

    col1, col2 = st.columns([2, 1])

    # Formulário
    with col1:
        st.subheader("Novo Cartão")

        if tipos:
            tipo_select = st.selectbox(
                "Tipo *",
                tipos,
                format_func=lambda t: t.nome
            )
        else:
            st.warning("Você precisa cadastrar tipos de pagamento primeiro (Crédito/Débito)")
            st.stop()

        banco = st.text_input("Banco", placeholder="Ex: Santander, Itaú, Nubank")
        digitos_finais = st.text_input(
            "4 Últimos Dígitos",
            placeholder="Ex: 6262",
            max_chars=4
        )
        apelido = st.text_input("Apelido", placeholder="Ex: Cartão Black, Cartão do Trabalho")
        descricao = st.text_area("Descrição (opcional)", placeholder="Ex: Cartão de crédito principal, sem limite...")

        if st.button("Adicionar Cartão", type="primary", use_container_width=True):
            if not tipo_select:
                st.error("Selecione um tipo")
            else:
                result = cartao_service.create(
                    user_id=user_id,
                    tipo_pagamento_id=tipo_select.id,
                    banco=banco if banco else None,
                    digitos_finais=digitos_finais if digitos_finais else None,
                    apelido=apelido if apelido else None,
                    descricao=descricao if descricao else None,
                )

                if result["success"]:
                    st.success("Cartão adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro: {result['error']}")

    with col2:
        st.subheader("Dicas")
        st.markdown("""
        **Campo Obrigatório:**
        - Tipo (Crédito/Débito)

        **Campos Opcionais:**
        - Todos os outros

        **Exemplos:**
        - Banco: Santander
        - Dígitos: 6262
        - Apelido: Black
        """)

    st.markdown("---")
    st.subheader("Cartões Cadastrados")

    result = cartao_service.list_by_user(user_id)
    if result["success"]:
        cartoes = result["data"]
        if cartoes:
            for cartao in cartoes:
                tipo_nome = next((t.nome for t in tipos if t.id == cartao.tipo_pagamento_id), "Desconhecido")

                with st.expander(
                    f"💳 {cartao.apelido or cartao.banco or 'Sem identificação'} ({tipo_nome})"
                ):
                    # Botões de ação
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                    with col_btn1:
                        if st.button("✏️ Editar", key=f"edit_{cartao.id}", use_container_width=True):
                            st.session_state[f"edit_cartao_{cartao.id}"] = True
                    with col_btn2:
                        if st.button("🗑️ Deletar", key=f"delete_{cartao.id}", use_container_width=True):
                            res = cartao_service.delete(cartao.id)
                            if res["success"]:
                                st.success("Cartão deletado!")
                                st.rerun()

                    st.markdown("---")

                    # Modo edição
                    if st.session_state.get(f"edit_cartao_{cartao.id}"):
                        st.subheader("Editar Cartão")
                        new_banco = st.text_input("Banco", value=cartao.banco or "", key=f"edit_banco_{cartao.id}")
                        new_digitos = st.text_input("4 Últimos Dígitos", value=cartao.digitos_finais or "", max_chars=4, key=f"edit_dig_{cartao.id}")
                        new_apelido = st.text_input("Apelido", value=cartao.apelido or "", key=f"edit_apel_{cartao.id}")
                        new_desc = st.text_area("Descrição", value=cartao.descricao or "", key=f"edit_desc_{cartao.id}")

                        col_save1, col_save2 = st.columns(2)
                        with col_save1:
                            if st.button("💾 Salvar", key=f"save_{cartao.id}", use_container_width=True):
                                res = cartao_service.update(
                                    cartao.id,
                                    banco=new_banco if new_banco else None,
                                    digitos_finais=new_digitos if new_digitos else None,
                                    apelido=new_apelido if new_apelido else None,
                                    descricao=new_desc if new_desc else None,
                                )
                                if res["success"]:
                                    st.success("Cartão atualizado!")
                                    st.session_state[f"edit_cartao_{cartao.id}"] = False
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {res['error']}")
                        with col_save2:
                            if st.button("❌ Cancelar", key=f"cancel_{cartao.id}", use_container_width=True):
                                st.session_state[f"edit_cartao_{cartao.id}"] = False
                                st.rerun()

                        st.markdown("---")

                    # Informações
                    if cartao.banco:
                        st.write(f"**Banco:** {cartao.banco}")
                    if cartao.digitos_finais:
                        st.write(f"**Dígitos:** ****{cartao.digitos_finais}")
                    if cartao.apelido:
                        st.write(f"**Apelido:** {cartao.apelido}")
                    if cartao.descricao:
                        st.write(f"**Descrição:** {cartao.descricao}")

        else:
            st.info("Nenhum cartão cadastrado. Adicione um para começar!")
    else:
        st.error(f"Erro ao carregar: {result['error']}")


if __name__ == "__main__":
    show()
