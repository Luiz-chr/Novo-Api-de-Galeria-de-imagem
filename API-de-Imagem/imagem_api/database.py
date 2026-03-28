from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME, COLLECTION_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

async def ping_database():
    try:
        await client.admin.command('ping')
        print(" Sucesso: Conectado ao MongoDB!")
    except Exception as e:
        print(f" Erro de conexão: {e}")