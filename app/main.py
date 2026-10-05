from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(title="SmartAI Assistant")

pasta_static = Path(__file__).resolve().parent / "static"

app.mount(
    "/static",
    StaticFiles(directory=pasta_static),
    name="static",
)

app.include_router(router)


@app.get("/interface", include_in_schema=False)
def abrir_interface():
    return FileResponse(pasta_static / "index.html")