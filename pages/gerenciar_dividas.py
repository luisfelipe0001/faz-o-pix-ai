import streamlit as st
from services.emprestimo_service import EmprestimoService
from services.pessoa_service import PessoaService
from services.tipo_pagamento_service import TipoPagamentoService
from services.cartao_service import CartaoService
from services.parcela_service import ParcelaService
from utils.formatters import format_currency, format_date, get_status_badge
from datetime import datetime

def show():
    """Página de Gerenciar Dívidas"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("💰 Gerenciar Dívidas")
    st.markdown("Crie, edite e acompanhe suas dívidas")
    st.markdown("---")

    user_id = st.session_state.get("user_id")
    emprestimo_service = EmprestimoService()
    pessoa_service = PessoaService()
    tipo_service = TipoPagamentoService()
    cartao_service = CartaoService()
    parcela_service = ParcelaService()

    # Tabs
    tab1, tab2 = st.tabs(["Nova Dívida", "Minhas Dívidas"])

    with tab1:
        st.subheader("Registrar Nova Dívida")

        # Carregar dados
        pessoas_result = pessoa_service.list_by_user(user_id)
        tipos_result = tipo_service.list_by_user(user_id)

        if not pessoas_result["success"] or not pessoas_result["data"]:
            st.warning("Você precisa cadastrar uma pessoa antes de criar uma dívida")
            st.stop()

        if not tipos_result["success"] or not tipos_result["data"]:
            st.warning("Você precisa cadastrar um tipo de pagamento antes de criar uma dívida")
            st.stop()

        pessoas = pessoas_result["data"]
        tipos = tipos_result["data"]

        col1, col2 = st.columns(2)

        with col1:
            pessoa_select = st.selectbox(
                "Pessoa *",
                pessoas,
                format_func=lambda p: p.nome
            )
            tipo_select = st.selectbox(
                "Tipo de Pagamento *",
                tipos,
                format_func=lambda t: t.nome
            )

            # Mostrar cartões se for Crédito ou Débito
            cartao_select = None
            if tipo_select and tipo_select.nome in ["Cartão Crédito", "Cartão Débito"]:
                cartoes_result = cartao_service.list_by_tipo_pagamento(tipo_select.id)
                if cartoes_result["success"] and cartoes_result["data"]:
                    cartoes = cartoes_result["data"]
                    cartao_options = [None] + cartoes
                    cartao_select = st.selectbox(
                        "Cartão (opcional)",
                        cartao_options,
                        format_func=lambda c: "Nenhum" if c is None else (c.apelido or c.banco or "Cartão")
                    )

            descricao = st.text_input("Descrição *", placeholder="Ex: Compra Mercado Livre")

        with col2:
            data_compra = st.date_input("Data da Compra *")
            valor_total = st.number_input("Valor Mensal/Parcela *", min_value=0.01, step=0.01)
            qtd_parcelas = st.number_input("Quantidade de Parcelas *", min_value=1, step=1)

        if st.button("Criar Dívida", type="primary", use_container_width=True):
            if not all([pessoa_select, tipo_select, descricao, valor_total, qtd_parcelas]):
                st.error("Preencha todos os campos obrigatórios")
            else:
                result = emprestimo_service.create(
                    user_id=user_id,
                    pessoa_id=pessoa_select.id,
                    tipo_pagamento_id=tipo_select.id,
                    descricao=descricao,
                    data_compra=data_compra.strftime("%Y-%m-%d"),
                    valor_total=float(valor_total),
                    qtd_parcelas=int(qtd_parcelas),
                    cartao_id=cartao_select.id if cartao_select else None,
                )

                if result["success"]:
                    st.success("Dívida criada com sucesso! Parcelas geradas automaticamente.")
                    st.rerun()
                else:
                    st.error(f"Erro: {result['error']}")

    with tab2:
        st.subheader("Minhas Dívidas")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_pessoa = st.selectbox(
                "Filtrar por Pessoa",
                [None] + pessoas,
                format_func=lambda p: "Todas" if p is None else p.nome
            )

        with col2:
            filtro_status = st.selectbox(
                "Filtrar por Status",
                ["Todos", "em_andamento", "quitado"]
            )

        # Listar dívidas
        result = emprestimo_service.list_by_user(user_id)

        if result["success"]:
            emprestimos = result["data"]

            # Aplicar filtros
            if filtro_pessoa:
                emprestimos = [e for e in emprestimos if e.pessoa_id == filtro_pessoa.id]

            if filtro_status != "Todos":
                emprestimos = [e for e in emprestimos if e.status_geral == filtro_status]

            if emprestimos:
                for emp in emprestimos:
                    with st.expander(f"📋 {emp.descricao} - {format_currency(emp.valor_total)}"):
                        # Botões de ação
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                        with col_btn1:
                            if st.button("✏️ Editar", key=f"edit_{emp.id}", use_container_width=True):
                                st.session_state[f"edit_mode_{emp.id}"] = True
                        with col_btn2:
                            if st.button("🗑️ Deletar", key=f"delete_{emp.id}", use_container_width=True):
                                res = emprestimo_service.delete(emp.id)
                                if res["success"]:
                                    st.success("Dívida deletada com sucesso!")
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {res['error']}")

                        st.markdown("---")

                        # Modo edição
                        if st.session_state.get(f"edit_mode_{emp.id}"):
                            st.subheader("Editar Dívida")
                            edit_col1, edit_col2 = st.columns(2)

                            with edit_col1:
                                new_descricao = st.text_input("Descrição", value=emp.descricao, key=f"edit_desc_{emp.id}")
                                new_valor = st.number_input("Valor Mensal/Parcela", value=emp.valor_total, min_value=0.01, key=f"edit_valor_{emp.id}")

                            with edit_col2:
                                new_qtd = st.number_input("Quantidade de Parcelas", value=emp.qtd_parcelas, min_value=1, key=f"edit_qtd_{emp.id}")
                                new_status = st.selectbox("Status", ["em_andamento", "quitado"], index=0 if emp.status_geral == "em_andamento" else 1, key=f"edit_status_{emp.id}")

                            col_save1, col_save2 = st.columns(2)
                            with col_save1:
                                if st.button("💾 Salvar", key=f"save_{emp.id}", use_container_width=True):
                                    res = emprestimo_service.update(
                                        emp.id,
                                        descricao=new_descricao,
                                        valor_total=float(new_valor),
                                        qtd_parcelas=int(new_qtd),
                                        status_geral=new_status,
                                    )
                                    if res["success"]:
                                        st.success("Dívida atualizada com sucesso!")
                                        st.session_state[f"edit_mode_{emp.id}"] = False
                                        st.rerun()
                                    else:
                                        st.error(f"Erro: {res['error']}")
                            with col_save2:
                                if st.button("❌ Cancelar", key=f"cancel_{emp.id}", use_container_width=True):
                                    st.session_state[f"edit_mode_{emp.id}"] = False
                                    st.rerun()

                            st.markdown("---")

                        # Informações da dívida
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.write(f"**Pessoa:** {[p.nome for p in pessoas if p.id == emp.pessoa_id][0]}")
                            st.write(f"**Data:** {format_date(emp.data_compra)}")

                        with col2:
                            st.write(f"**Total:** {format_currency(emp.valor_total)}")
                            st.write(f"**Status:** {get_status_badge(emp.status_geral)}")

                        with col3:
                            st.write(f"**Parcelas:** {emp.qtd_parcelas}")

                        st.markdown("---")

                        # Parcelas
                        st.write("**Parcelas:**")
                        parcelas_result = parcela_service.list_by_emprestimo(emp.id)

                        if parcelas_result["success"]:
                            parcelas = parcelas_result["data"]
                            for parcela in parcelas:
                                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                                with col1:
                                    st.write(f"Parcela {parcela.numero_parcela}")
                                with col2:
                                    st.write(format_currency(parcela.valor_parcela))
                                with col3:
                                    st.write(format_date(parcela.data_vencimento))
                                with col4:
                                    status_text = get_status_badge(parcela.status)
                                    st.write(status_text)

                                    if parcela.status != "recebida":
                                        if st.button("✅ Marcar Recebida", key=f"mark_{parcela.id}"):
                                            res = parcela_service.marcar_como_recebida(parcela.id)
                                            if res["success"]:
                                                st.success("Parcela marcada como recebida!")
                                                st.rerun()

            else:
                st.info("Nenhuma dívida encontrada com os filtros selecionados")
        else:
            st.error(f"Erro ao carregar: {result['error']}")


if __name__ == "__main__":
    show()
