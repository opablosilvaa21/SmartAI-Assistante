from typing import Literal

from pydantic import BaseModel, Field

class SolicitacaoAssistente(BaseModel):
    texto: str = Field(min_length=10, max_length=10000)
    acao: Literal['resumir', 'extrair_tarefas', 'plano_de_acao']
    