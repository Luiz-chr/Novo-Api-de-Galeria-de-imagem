import os
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from config import UPLOAD_DIR
from database import collection
from config import UPLOAD_DIR, STATIC_DIR
from config import STATIC_DIR

router = APIRouter()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """Recebe uma imagem, salva no disco com UUID e registra no MongoDB"""
    # 1. Gerar nome único para evitar conflitos no disco
    ext = file.filename.split(".")[-1]
    nome_sistema = f"{uuid.uuid4()}.{ext}"
    caminho_completo = os.path.join(UPLOAD_DIR, nome_sistema)

    # 2. Salvar o arquivo físico
    with open(caminho_completo, "wb") as f:
        content = await file.read()
        f.write(content)

    # 3. Salvar metadados no MongoDB
    documento = {
        "nome_original": file.filename,
        "nome_sistema": nome_sistema,
        "caminho": caminho_completo
    }
    await collection.insert_one(documento)
    
    return {"message": "Upload realizado", "filename": nome_sistema}

@router.get("/list/")
async def list_images():
    """Lista todas as imagens cadastradas no banco de dados"""
    cursor = collection.find({})
    imagens = await cursor.to_list(length=100)
    # Retornamos os nomes de sistema para o front usar no link de download
    return {"imagens": [img["nome_sistema"] for img in imagens]}

@router.get("/search/{query}")
async def search_images(query: str):
    """Busca imagens pelo nome original usando Regex no MongoDB"""
    cursor = collection.find({
        "nome_original": {"$regex": query, "$options": "i"}
    })
    imagens = await cursor.to_list(length=100)
    return {"imagens": [img["nome_sistema"] for img in imagens]}

@router.get("/download/{filename}")
async def download_image(filename: str):
    """Serve o arquivo físico baseado no nome registrado no sistema"""
    img = await collection.find_one({"nome_sistema": filename})
    if not img or not os.path.exists(img["caminho"]):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
    return FileResponse(img["caminho"])

@router.delete("/delete/{filename}")
async def delete_image(filename: str):
    """Remove o arquivo do disco e o registro do MongoDB"""
    img = await collection.find_one({"nome_sistema": filename})
    
    if not img:
        raise HTTPException(status_code=404, detail="Imagem não encontrada no banco")

    # Deletar arquivo físico
    if os.path.exists(img["caminho"]):
        os.remove(img["caminho"])

    # Deletar do banco
    await collection.delete_one({"nome_sistema": filename})
    
    return {"message": f"Imagem {filename} removida com sucesso"}