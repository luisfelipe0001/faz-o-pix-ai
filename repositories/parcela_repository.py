import uuid
from utils.db import get_supabase_client
from domain.parcela import Parcela
from typing import Optional, List

class ParcelaRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "parcelas"

    def create(
        self,
        emprestimo_id: str,
        numero_parcela: int,
        valor_parcela: float,
        data_vencimento: str,
    ) -> Parcela:
        """Criar nova parcela"""
        data = {
            "id": str(uuid.uuid4()),
            "emprestimo_id": emprestimo_id,
            "numero_parcela": numero_parcela,
            "valor_parcela": valor_parcela,
            "data_vencimento": data_vencimento,
            "status": "pendente",
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return Parcela(**response.data[0])
        raise Exception("Erro ao criar parcela")

    def get_by_id(self, parcela_id: str) -> Optional[Parcela]:
        """Obter parcela por ID"""
        response = self.client.table(self.table).select("*").eq("id", parcela_id).execute()
        if response.data:
            return Parcela(**response.data[0])
        return None

    def list_by_emprestimo(self, emprestimo_id: str) -> List[Parcela]:
        """Listar parcelas de um empréstimo"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("emprestimo_id", emprestimo_id)
            .order("numero_parcela")
            .execute()
        )
        return [Parcela(**row) for row in response.data]

    def update_status(
        self,
        parcela_id: str,
        status: str,
        data_recebimento: str = None,
    ) -> Parcela:
        """Atualizar status da parcela"""
        data = {"status": status}
        if data_recebimento:
            data["data_recebimento"] = data_recebimento

        response = self.client.table(self.table).update(data).eq("id", parcela_id).execute()
        if response.data:
            return Parcela(**response.data[0])
        raise Exception("Erro ao atualizar parcela")

    def delete(self, parcela_id: str) -> bool:
        """Deletar parcela"""
        response = self.client.table(self.table).delete().eq("id", parcela_id).execute()
        return len(response.data) > 0
