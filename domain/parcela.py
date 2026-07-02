from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Parcela:
    id: str
    emprestimo_id: str
    numero_parcela: int
    valor_parcela: float
    data_vencimento: str
    status: str = "pendente"  # pendente, recebida, atrasada
    data_recebimento: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "emprestimo_id": self.emprestimo_id,
            "numero_parcela": self.numero_parcela,
            "valor_parcela": self.valor_parcela,
            "data_vencimento": self.data_vencimento,
            "status": self.status,
            "data_recebimento": self.data_recebimento,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
