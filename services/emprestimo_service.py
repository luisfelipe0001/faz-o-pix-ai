from datetime import datetime, timedelta
from utils.validators import (
    validate_valor,
    validate_parcelas,
    validate_data,
    validate_nome,
)
from repositories.emprestimo_repository import EmprestimoRepository
from repositories.parcela_repository import ParcelaRepository

class EmprestimoService:
    def __init__(self):
        self.repo = EmprestimoRepository()
        self.parcela_repo = ParcelaRepository()

    def create(
        self,
        user_id: str,
        pessoa_id: str,
        tipo_pagamento_id: str,
        descricao: str,
        data_compra: str,
        valor_total: float,
        qtd_parcelas: int,
        cartao_id: str = None,
    ) -> dict:
        """Criar novo empréstimo e gerar parcelas"""
        # Validações
        valid_valor, error = validate_valor(valor_total)
        if not valid_valor:
            return {"success": False, "error": error}

        valid_parcelas, error = validate_parcelas(qtd_parcelas)
        if not valid_parcelas:
            return {"success": False, "error": error}

        valid_data, error = validate_data(data_compra)
        if not valid_data:
            return {"success": False, "error": error}

        valid_desc, error = validate_nome(descricao)
        if not valid_desc:
            return {"success": False, "error": error}

        try:
            # Criar empréstimo
            emprestimo = self.repo.create(
                user_id,
                pessoa_id,
                tipo_pagamento_id,
                descricao,
                data_compra,
                valor_total,
                qtd_parcelas,
                cartao_id,
            )

            # Gerar parcelas automaticamente
            self._gerar_parcelas(emprestimo.id, valor_total, qtd_parcelas, data_compra)

            return {"success": True, "data": emprestimo}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _gerar_parcelas(
        self,
        emprestimo_id: str,
        valor_total: float,
        qtd_parcelas: int,
        data_inicio: str,
    ):
        """Gerar parcelas automaticamente (mesmo valor por cada parcela)"""
        valor_parcela = valor_total  # Usa o valor total como valor de cada parcela
        data_base = datetime.strptime(data_inicio, "%Y-%m-%d")

        for i in range(1, qtd_parcelas + 1):
            data_vencimento = data_base + timedelta(days=30 * i)
            self.parcela_repo.create(
                emprestimo_id,
                i,
                valor_parcela,
                data_vencimento.strftime("%Y-%m-%d"),
            )

    def get_by_id(self, emprestimo_id: str) -> dict:
        """Obter empréstimo por ID"""
        try:
            emprestimo = self.repo.get_by_id(emprestimo_id)
            if emprestimo:
                return {"success": True, "data": emprestimo}
            return {"success": False, "error": "Empréstimo não encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_user(self, user_id: str) -> dict:
        """Listar empréstimos do usuário"""
        try:
            emprestimos = self.repo.list_by_user(user_id)
            return {"success": True, "data": emprestimos}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_pessoa(self, pessoa_id: str) -> dict:
        """Listar empréstimos de uma pessoa"""
        try:
            emprestimos = self.repo.list_by_pessoa(pessoa_id)
            return {"success": True, "data": emprestimos}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(
        self,
        emprestimo_id: str,
        descricao: str = None,
        data_compra: str = None,
        valor_total: float = None,
        qtd_parcelas: int = None,
        status_geral: str = None,
        cartao_id: str = None,
    ) -> dict:
        """Atualizar empréstimo"""
        try:
            emprestimo = self.repo.update(
                emprestimo_id,
                descricao,
                data_compra,
                valor_total,
                qtd_parcelas,
                status_geral,
                cartao_id,
            )
            return {"success": True, "data": emprestimo}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, emprestimo_id: str) -> dict:
        """Deletar empréstimo"""
        try:
            deleted = self.repo.delete(emprestimo_id)
            if deleted:
                return {"success": True, "message": "Empréstimo deletado com sucesso"}
            return {"success": False, "error": "Erro ao deletar empréstimo"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calcular_saldo_devedor(self, emprestimo_id: str) -> dict:
        """Calcular saldo devedor de um empréstimo"""
        try:
            from repositories.parcela_repository import ParcelaRepository

            parcela_repo = ParcelaRepository()
            parcelas = parcela_repo.list_by_emprestimo(emprestimo_id)

            saldo = sum(
                p.valor_parcela for p in parcelas if p.status != "recebida"
            )
            return {"success": True, "data": saldo}
        except Exception as e:
            return {"success": False, "error": str(e)}
