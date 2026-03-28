import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config import STATIC_DIR

def setup_static(app: FastAPI):
    """Configura a pasta de arquivos estáticos"""
    if os.path.exists(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    else:
        print(f"⚠️ Aviso: Pasta {STATIC_DIR} não encontrada.")

def get_index():
    """Retorna o index.html"""
    path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"erro": "index.html não encontrado"}

def get_favicon():
    """Busca o favicon na pasta static"""
    path = os.path.join(STATIC_DIR, "favicon.ico")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/x-icon")
    return None