from datetime import datetime, timezone
from uuid import uuid4

from app.integrations.ai_client import AIClient
from app.repositories.history_repository import HistoryRepository
from app.schemas.requests import SolicitacaoAssistente


class AssistantService:
    def __init__(
        self,
        repositorio: HistoryRepository,
        cliente_ia: AIClient,
    ):
        self.repositorio = repositorio
        self.cliente_ia = cliente_ia

    def processar(self, solicitacao: SolicitacaoAssistente) -> dict:
        resultado = self.cliente_ia.gerar(
            texto=solicitacao.texto,
            acao=solicitacao.acao,
        )

        registro = {
            "id": str(uuid4()),
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "acao": solicitacao.acao,
            "texto_recebido": solicitacao.texto,
            "resultado": resultado,
            "modo": "ia",
        }

        self.repositorio.salvar(registro)

        return registro

    def listar_historico(self) -> list[dict]:
        return self.repositorio.listar()