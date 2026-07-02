import streamlit as st
from services.emprestimo_service import EmprestimoService
from services.parcela_service import ParcelaService
from services.pessoa_service import PessoaService
from utils.formatters import format_currency, format_date, get_status_badge
from datetime import datetime

def show():
    """Dashboard/Home - Página Principal"""
    # Verificar autenticação
    if not st.session_state.get("authenticated"):
        st.error("Você precisa estar logado")
        st.switch_page("pages/login.py")
        return

    st.title("🏠 Dashboard")
    st.markdown("Visão geral de suas dívidas e parcelas")
    st.markdown("---")

    user_id = st.session_state.get("user_id")
    emprestimo_service = EmprestimoService()
    parcela_service = ParcelaService()
    pessoa_service = PessoaService()

    # Carregar dados
    emprestimos_result = emprestimo_service.list_by_user(user_id)
    pessoas_result = pessoa_service.list_by_user(user_id)

    if not emprestimos_result["success"]:
        st.error("Erro ao carregar dívidas")
        return

    emprestimos = emprestimos_result["data"]
    pessoas = pessoas_result["data"] if pessoas_result["success"] else []

    # Calcular métricas
    total_a_receber = sum(e.valor_total for e in emprestimos if e.status_geral == "em_andamento")
    total_recebido = sum(e.valor_total for e in emprestimos if e.status_geral == "quitado")
    total_dívidas = len(emprestimos)

    # Cards de resumo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total a Receber", format_currency(total_a_receber))

    with col2:
        st.metric("✅ Total Recebido", format_currency(total_recebido))

    with col3:
        st.metric("📋 Total de Dívidas", total_dívidas)

    with col4:
        st.metric("👥 Pessoas", len(pessoas))

    st.markdown("---")

    # Seção de Parcelas Próximas ao Vencimento
    st.subheader("⏳ Parcelas Próximas ao Vencer (30 dias)")

    parcelas_proximas = []
    for emp in emprestimos:
        parcelas_result = parcela_service.list_by_emprestimo(emp.id)
        if parcelas_result["success"]:
            for parcela in parcelas_result["data"]:
                if parcela.status != "recebida":
                    data_venc = datetime.strptime(parcela.data_vencimento, "%Y-%m-%d")
                    dias_restantes = (data_venc - datetime.now()).days
                    if 0 <= dias_restantes <= 30:
                        pessoa_nome = next((p.nome for p in pessoas if p.id == emp.pessoa_id), "Desconhecido")
                        parcelas_proximas.append({
                            "pessoa": pessoa_nome,
                            "descricao": emp.descricao,
                            "parcela": f"{parcela.numero_parcela}/{emp.qtd_parcelas}",
                            "valor": parcela.valor_parcela,
                            "vencimento": parcela.data_vencimento,
                            "dias": dias_restantes,
                            "parcela_id": parcela.id,
                            "status": parcela.status,
                        })

    if parcelas_proximas:
        parcelas_proximas.sort(key=lambda x: x["dias"])

        for p in parcelas_proximas:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

            with col1:
                st.write(f"**{p['pessoa']}** - {p['descricao']}")

            with col2:
                st.write(f"Parcela {p['parcela']}")

            with col3:
                st.write(format_currency(p["valor"]))

            with col4:
                dias_text = f"{p['dias']} dias" if p['dias'] > 0 else "Hoje"
                if p["dias"] < 0:
                    st.warning(f"Vencida {abs(p['dias'])} dias")
                else:
                    st.info(dias_text)

            with col5:
                if st.button("✅", key=f"quick_mark_{p['parcela_id']}"):
                    result = parcela_service.marcar_como_recebida(p["parcela_id"])
                    if result["success"]:
                        st.success("Marcada!")
                        st.rerun()

        st.markdown("---")
    else:
        st.info("✅ Nenhuma parcela próxima ao vencer!")

    st.markdown("---")

    # Seção de Dívidas por Pessoa
    st.subheader("👥 Resumo por Pessoa")

    if pessoas:
        for pessoa in pessoas:
            pessoa_emprestimos = [e for e in emprestimos if e.pessoa_id == pessoa.id]

            if pessoa_emprestimos:
                total_pessoa = sum(e.valor_total for e in pessoa_emprestimos)

                with st.expander(f"**{pessoa.nome}** - {format_currency(total_pessoa)}"):
                    for emp in pessoa_emprestimos:
                        col1, col2, col3 = st.columns([2, 1, 1])

                        with col1:
                            st.write(f"📌 {emp.descricao}")
                            st.caption(f"Data: {format_date(emp.data_compra)}")

                        with col2:
                            st.write(format_currency(emp.valor_total))
                            st.caption(get_status_badge(emp.status_geral))

                        with col3:
                            # Calcular parcelas recebidas
                            parcelas_result = parcela_service.list_by_emprestimo(emp.id)
                            if parcelas_result["success"]:
                                parcelas = parcelas_result["data"]
                                recebidas = sum(1 for p in parcelas if p.status == "recebida")
                                st.write(f"Parcelas: {recebidas}/{emp.qtd_parcelas}")

    else:
        st.info("Nenhuma pessoa cadastrada. Comece cadastrando pessoas!")

    st.markdown("---")

    # Informações úteis
    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **💡 Dicas:**
        - Cadastre pessoas para começar
        - Configure tipos de pagamento
        - Registre novas dívidas
        - Acompanhe as parcelas
        """)

    with col2:
        st.success("""
        **✅ Status:**
        - Dashboard funcionando
        - Próximo: cadastrar dados
        - Depois: acompanhar parcelas
        """)


if __name__ == "__main__":
    show()
