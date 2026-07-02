import uuid
from utils.db import get_supabase_client
from domain.tipo_pagamento import TipoPagamento
from typing import Optional, List

class TipoPagamentoRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "tipos_pagamento"

    def create(self, user_id: str, nome: str) -> TipoPagamento:
        """Criar novo tipo de pagamento"""
        data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "nome": nome,
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return TipoPagamento(**response.data[0])
        raise Exception("Erro ao criar tipo de pagamento")

    def get_by_id(self, tipo_id: str) -> Optional[TipoPagamento]:
        """Obter tipo de pagamento por ID"""
        response = self.client.table(self.table).select("*").eq("id", tipo_id).execute()
        if response.data:
            return TipoPagamento(**response.data[0])
        return None

    def list_by_user(self, user_id: str) -> List[TipoPagamento]:
        """Listar tipos de pagamento do usuário"""
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        return [TipoPagamento(**row) for row in response.data]

    def update(self, tipo_id: str, nome: str) -> TipoPagamento:
        """Atualizar tipo de pagamento"""
        response = self.client.table(self.table).update({"nome": nome}).eq("id", tipo_id).execute()
        if response.data:
            return TipoPagamento(**response.data[0])
        raise Exception("Erro ao atualizar tipo de pagamento")

    def delete(self, tipo_id: str) -> bool:
        """Deletar tipo de pagamento"""
        response = self.client.table(self.table).delete().eq("id", tipo_id).execute()
        return len(response.data) > 0
