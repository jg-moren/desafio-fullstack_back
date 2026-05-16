import os
import json
from bson import json_util
from bson import ObjectId 
from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime

from pydantic import BaseModel

from pymongo import MongoClient

app = FastAPI()

load_dotenv()

try:
    url = os.getenv("MONGODB_URL")

    client = MongoClient(url, serverSelectionTimeoutMS=5000)
    
    db = client.get_database("desafio_fullstack")

except ConnectionFailure:
    print("Não foi possível conectar ao servidor MongoDB.")


@app.get("/voluntarios")
async def buscar_voluntarios():
    lista_voluntarios = db.voluntarios.find()
    lista_voluntarios = list(lista_voluntarios)
    resposta = []
    for x in lista_voluntarios:
        resposta.append(json.loads(json_util.dumps(x)))

    return(resposta)

@app.get("/voluntarios/{id}")
async def buscar_voluntario_por_id(id: str):
    
    voluntario = db.voluntarios.find_one({"_id": ObjectId(id)})    

    voluntario_json = json.loads(json_util.dumps(voluntario))
    
    return voluntario_json

class Voluntario(BaseModel):
    nome: str
    email: str 
    telefone: str
    cargo: str
    disponibilidade: str

@app.post("/voluntarios")
async def cadastrar_voluntario(voluntario: Voluntario):

    dados_voluntario = voluntario.model_dump()
    dados_voluntario["status"] = True
    dados_voluntario["data_inscricao"] = datetime.now()

    resultado = db.voluntarios.insert_one(dados_voluntario)

    return {
        "mensagem": "Voluntário cadastrado com sucesso!", 
        "id_inserido":str(resultado),
    }

@app.put("/voluntarios/{id}")
async def editar_voluntario(id: str, voluntario: Voluntario):

    dados_voluntario = voluntario.model_dump()

    if id == None:
        return "Sem Id"

    filter = { '_id': ObjectId(id)}
    
    newvalues = { "$set": dados_voluntario } 

    resultado = db.voluntarios.update_one(filter, newvalues) 

    return {
        "mensagem": "Voluntário atualizado com sucesso!", 
        "resultado":str(resultado),
    }


@app.delete("/voluntarios/{id}")
async def deletar_voluntario(id: str):    

    filter = { '_id': ObjectId(id)}

    newvalues = { "$set": {"status" : False} } 

    resultado = db.voluntarios.update_one(filter, newvalues) 

    return {
        "mensagem": "Voluntário atualizado com sucesso!", 
        "resultado":str(resultado),
    }