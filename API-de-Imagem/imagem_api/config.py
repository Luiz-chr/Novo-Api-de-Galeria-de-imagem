import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

#MONGODB 
MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME = "api_imagens"
COLLECTION_NAME = "imagens"

# --- GARANTIR PASTAS ---
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)