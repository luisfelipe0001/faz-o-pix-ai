import uuid
from utils.db import get_supabase_client
from domain.emprestimo import Emprestimo
from typing import Optional, List

class EmprestimoRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "emprestimos"

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
    ) -> Emprestimo:
        """Criar novo empréstimo"""
        data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "pessoa_id": pessoa_id,
            "tipo_pagamento_id": tipo_pagamento_id,
            "descricao": descricao,
            "data_compra": data_compra,
            "valor_total": valor_total,
            "qtd_parcelas": qtd_parcelas,
            "status_geral": "em_andamento",
            "cartao_id": cartao_id,
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return Emprestimo(**response.data[0])
        raise Exception("Erro ao criar empréstimo")

    def get_by_id(self, emprestimo_id: str) -> Optional[Emprestimo]:
        """Obter empréstimo por ID"""
        response = self.client.table(self.table).select("*").eq("id", emprestimo_id).execute()
        if response.data:
            return Emprestimo(**response.data[0])
        return None

    def list_by_user(self, user_id: str) -> List[Emprestimo]:
        """Listar empréstimos do usuário"""
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        return [Emprestimo(**row) for row in response.data]

    def list_by_pessoa(self, pessoa_id: str) -> List[Emprestimo]:
        """Listar empréstimos de uma pessoa"""
        response = self.client.table(self.table).select("*").eq("pessoa_id", pessoa_id).execute()
        return [Emprestimo(**row) for row in response.data]

    def update(
        self,
        emprestimo_id: str,
        descricao: str = None,
        data_compra: str = None,
        valor_total: float = None,
        qtd_parcelas: int = None,
        status_geral: str = None,
        cartao_id: str = None,
    ) -> Emprestimo:
        """Atualizar empréstimo"""
        data = {}
        if descricao:
            data["descricao"] = descricao
        if data_compra:
            data["data_compra"] = data_compra
        if valor_total:
            data["valor_total"] = valor_total
        if qtd_parcelas:
            data["qtd_parcelas"] = qtd_parcelas
        if status_geral:
            data["status_geral"] = status_geral
        if cartao_id is not None:
            data["cartao_id"] = cartao_id

        response = self.client.table(self.table).update(data).eq("id", emprestimo_id).execute()
        if response.data:
            return Emprestimo(**response.data[0])
        raise Exception("Erro ao atualizar empréstimo")

    def delete(self, emprestimo_id: str) -> bool:
        """Deletar empréstimo"""
        response = self.client.table(self.table).delete().eq("id", emprestimo_id).execute()
        return len(response.data) > 0
