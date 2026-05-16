import os
import json
from bson import json_util
from dotenv import load_dotenv
from fastapi import FastAPI

from pymongo import MongoClient

app = FastAPI()

load_dotenv()

try:
    url = os.getenv("MONGODB_URL")

    client = MongoClient(url, serverSelectionTimeoutMS=5000)
    
    # O comando 'ping' força uma conexão com o servidor para testar se está ativo
    #client.admin.command('ping')
    #print("Conexão com o MongoDB estabelecida com sucesso!")
    
    db = client.get_database("desafio_fullstack")

except ConnectionFailure:
    print("Não foi possível conectar ao servidor MongoDB.")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/voluntarios")
async def voluntarios():
    lista_voluntarios = list(db.voluntarios.find())
    json_resultado = json.dumps(lista_voluntarios, default=json_util.default, indent=4)
    return(json_resultado)

