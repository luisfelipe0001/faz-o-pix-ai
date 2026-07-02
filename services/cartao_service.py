from repositories.cartao_repository import CartaoRepository

class CartaoService:
    def __init__(self):
        self.repo = CartaoRepository()

    def create(
        self,
        user_id: str,
        tipo_pagamento_id: str,
        banco: str = None,
        digitos_finais: str = None,
        apelido: str = None,
        descricao: str = None,
    ) -> dict:
        """Criar novo cartão"""
        try:
            cartao = self.repo.create(
                user_id,
                tipo_pagamento_id,
                banco,
                digitos_finais,
                apelido,
                descricao,
            )
            return {"success": True, "data": cartao}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_by_id(self, cartao_id: str) -> dict:
        """Obter cartão por ID"""
        try:
            cartao = self.repo.get_by_id(cartao_id)
            if cartao:
                return {"success": True, "data": cartao}
            return {"success": False, "error": "Cartão não encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_user(self, user_id: str) -> dict:
        """Listar cartões do usuário"""
        try:
            cartoes = self.repo.list_by_user(user_id)
            return {"success": True, "data": cartoes}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_tipo_pagamento(self, tipo_pagamento_id: str) -> dict:
        """Listar cartões por tipo de pagamento"""
        try:
            cartoes = self.repo.list_by_tipo_pagamento(tipo_pagamento_id)
            return {"success": True, "data": cartoes}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(
        self,
        cartao_id: str,
        banco: str = None,
        digitos_finais: str = None,
        apelido: str = None,
        descricao: str = None,
    ) -> dict:
        """Atualizar cartão"""
        try:
            cartao = self.repo.update(
                cartao_id,
                banco,
                digitos_finais,
                apelido,
                descricao,
            )
            return {"success": True, "data": cartao}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, cartao_id: str) -> dict:
        """Deletar cartão"""
        try:
            deleted = self.repo.delete(cartao_id)
            if deleted:
                return {"success": True, "message": "Cartão deletado com sucesso"}
            return {"success": False, "error": "Erro ao deletar cartão"}
        except Exception as e:
            return {"success": False, "error": str(e)}
