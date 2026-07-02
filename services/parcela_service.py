from datetime import datetime
from repositories.parcela_repository import ParcelaRepository

class ParcelaService:
    def __init__(self):
        self.repo = ParcelaRepository()

    def list_by_emprestimo(self, emprestimo_id: str) -> dict:
        """Listar parcelas de um empréstimo"""
        try:
            parcelas = self.repo.list_by_emprestimo(emprestimo_id)
            return {"success": True, "data": parcelas}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def marcar_como_recebida(self, parcela_id: str, data_recebimento: str = None) -> dict:
        """Marcar parcela como recebida"""
        if not data_recebimento:
            data_recebimento = datetime.now().strftime("%Y-%m-%d")

        try:
            parcela = self.repo.update_status(
                parcela_id,
                "recebida",
                data_recebimento,
            )
            return {"success": True, "data": parcela}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def marcar_como_pendente(self, parcela_id: str) -> dict:
        """Marcar parcela como pendente"""
        try:
            parcela = self.repo.update_status(
                parcela_id,
                "pendente",
            )
            return {"success": True, "data": parcela}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verificar_status_automatico(self, parcela_id: str) -> dict:
        """Verificar e atualizar status automaticamente (pendente/atrasada)"""
        try:
            parcela = self.repo.get_by_id(parcela_id)
            if not parcela:
                return {"success": False, "error": "Parcela não encontrada"}

            if parcela.status == "recebida":
                return {"success": True, "data": parcela}

            data_vencimento = datetime.strptime(parcela.data_vencimento, "%Y-%m-%d")
            data_hoje = datetime.now()

            if data_hoje > data_vencimento and parcela.status != "recebida":
                parcela = self.repo.update_status(parcela_id, "atrasada")

            return {"success": True, "data": parcela}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, parcela_id: str) -> dict:
        """Deletar parcela"""
        try:
            deleted = self.repo.delete(parcela_id)
            if deleted:
                return {"success": True, "message": "Parcela deletada com sucesso"}
            return {"success": False, "error": "Erro ao deletar parcela"}
        except Exception as e:
            return {"success": False, "error": str(e)}
