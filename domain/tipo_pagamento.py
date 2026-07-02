from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TipoPagamento:
    id: str
    user_id: str
    nome: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nome": self.nome,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
