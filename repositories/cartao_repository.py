import uuid
from utils.db import get_supabase_client
from domain.cartao import Cartao
from typing import Optional, List

class CartaoRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "cartoes"

    def create(
        self,
        user_id: str,
        tipo_pagamento_id: str,
        banco: str = None,
        digitos_finais: str = None,
        apelido: str = None,
        descricao: str = None,
    ) -> Cartao:
        """Criar novo cartão"""
        data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "tipo_pagamento_id": tipo_pagamento_id,
            "banco": banco,
            "digitos_finais": digitos_finais,
            "apelido": apelido,
            "descricao": descricao,
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return Cartao(**response.data[0])
        raise Exception("Erro ao criar cartão")

    def get_by_id(self, cartao_id: str) -> Optional[Cartao]:
        """Obter cartão por ID"""
        response = self.client.table(self.table).select("*").eq("id", cartao_id).execute()
        if response.data:
            return Cartao(**response.data[0])
        return None

    def list_by_user(self, user_id: str) -> List[Cartao]:
        """Listar cartões do usuário"""
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        return [Cartao(**row) for row in response.data]

    def list_by_tipo_pagamento(self, tipo_pagamento_id: str) -> List[Cartao]:
        """Listar cartões por tipo de pagamento"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("tipo_pagamento_id", tipo_pagamento_id)
            .execute()
        )
        return [Cartao(**row) for row in response.data]

    def update(
        self,
        cartao_id: str,
        banco: str = None,
        digitos_finais: str = None,
        apelido: str = None,
        descricao: str = None,
    ) -> Cartao:
        """Atualizar cartão"""
        data = {}
        if banco:
            data["banco"] = banco
        if digitos_finais:
            data["digitos_finais"] = digitos_finais
        if apelido:
            data["apelido"] = apelido
        if descricao:
            data["descricao"] = descricao

        response = self.client.table(self.table).update(data).eq("id", cartao_id).execute()
        if response.data:
            return Cartao(**response.data[0])
        raise Exception("Erro ao atualizar cartão")

    def delete(self, cartao_id: str) -> bool:
        """Deletar cartão"""
        response = self.client.table(self.table).delete().eq("id", cartao_id).execute()
        return len(response.data) > 0
