from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cartao:
    id: str
    user_id: str
    tipo_pagamento_id: str
    banco: Optional[str] = None
    digitos_finais: Optional[str] = None
    apelido: Optional[str] = None
    descricao: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tipo_pagamento_id": self.tipo_pagamento_id,
            "banco": self.banco,
            "digitos_finais": self.digitos_finais,
            "apelido": self.apelido,
            "descricao": self.descricao,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
