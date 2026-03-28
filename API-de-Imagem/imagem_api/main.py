import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import STATIC_DIR, UPLOAD_DIR
from database import ping_database
from middleware import setup_middleware
from routes import router
from static import setup_static, get_index, get_favicon


app = FastAPI(
    title="Galeria de Imagens Pro",
    description="API com FastAPI, MongoDB e Armazenamento Local",
    version="1.0.0"
)


setup_middleware(app)


setup_static(app)


@app.on_event("startup")
async def startup_event():
    """Roda ao iniciar o servidor: verifica banco e pastas"""
    await ping_database()
    print(f" Pasta de Uploads: {UPLOAD_DIR}")
    print(f" Servidor pronto em http://127.0.0.1:8000")

# 5. Rotas de Navegação (Front-end)
@app.get("/", tags=["Interface"])
async def serve_home():
    """Entrega o index.html da pasta static"""
    return get_index()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Entrega o ícone do site"""
    return get_favicon()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)