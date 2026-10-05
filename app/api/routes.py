from fastapi import APIRouter, HTTPException
from google.genai import errors

from app.integrations.ai_client import AIClient
from app.repositories.history_repository import HistoryRepository
from app.schemas.requests import SolicitacaoAssistente
from app.services.assistant_service import AssistantService

router = APIRouter()

repositorio = HistoryRepository()
cliente_ia = AIClient()
servico = AssistantService(repositorio, cliente_ia)


@router.get("/")
def inicio():
    return {"mensagem": "SmartAI Assistant está funcionando!"}


@router.post("/assistente")
def processar_solicitacao(solicitacao: SolicitacaoAssistente):
    try:
        return servico.processar(solicitacao)

    except errors.APIError as erro:
        raise HTTPException(
            status_code=502,
            detail=(
                f"O provedor de IA retornou o código {erro.code}. "
                "Confira o acesso ao modelo, a chave e os limites da API."
            ),
        ) from erro

    except RuntimeError as erro:
        raise HTTPException(
            status_code=502,
            detail="A IA não retornou um resultado utilizável.",
        ) from erro


@router.get("/historico")
def consultar_historico():
    return servico.listar_historico()