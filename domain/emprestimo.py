from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Emprestimo:
    id: str
    user_id: str
    pessoa_id: str
    tipo_pagamento_id: str
    descricao: str
    data_compra: str
    valor_total: float
    qtd_parcelas: int
    status_geral: str = "em_andamento"  # em_andamento, quitado
    cartao_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pessoa_id": self.pessoa_id,
            "tipo_pagamento_id": self.tipo_pagamento_id,
            "descricao": self.descricao,
            "data_compra": self.data_compra,
            "valor_total": self.valor_total,
            "qtd_parcelas": self.qtd_parcelas,
            "status_geral": self.status_geral,
            "cartao_id": self.cartao_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
