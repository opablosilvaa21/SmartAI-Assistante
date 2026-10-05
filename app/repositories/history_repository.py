from pathlib import Path
from threading import Lock

from tinydb import TinyDB

class HistoryRepository:
    def __init__(self):
        raiz = Path(__file__).resolve().parents[2]
        pasta_dados = raiz / "data"
        pasta_dados.mkdir(exist_ok=True)

        self.banco = TinyDB(
            pasta_dados / "historico.json",
            encoding="utf-8",
            ensure_ascii=False,
            indent=2,
        )
        self.trava = Lock()

    def salvar(self, registro: dict) -> None:
            with self.trava:
                self.banco.insert(registro)

    def listar(self) -> list[dict]:
                with self.trava:
                    registros = self.banco.all()

                    return [dict(registro) for registro in reversed(registros)]

            