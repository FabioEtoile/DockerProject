from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://mongodb:27017/")
db = client.livre_objectifs_db  

class ObjectifAjout(BaseModel):
    contenu: str

class ObjectifSuppression(BaseModel):
    contenu: str

class ObjectifMiseAJour(BaseModel):
    contenu: str

@app.get("/objectifs")
def obtenir_objectifs():
    objectifs = list(db.objectifs.find({}, {"_id": 0}))  
    return {"objectifs": objectifs}
@app.post("/objectifs")
def ajouter_objectif(data: ObjectifAjout):  
    objectif = {"contenu": data.contenu, "fait": False}  
    db.objectifs.insert_one(objectif)  
    return {"message": "Objectif ajouté avec succès"}
@app.delete("/objectifs")
def supprimer_objectif(data: ObjectifSuppression):
    resultat = db.objectifs.delete_one({"contenu": data.contenu})
    if resultat.deleted_count == 0:
        return {"message": "Objectif non trouvé"}
    return {"message": "Objectif supprimé avec succès"}
@app.put("/objectifs")
def basculer_objectif(data: ObjectifMiseAJour):
    objectif = db.objectifs.find_one({"contenu": data.contenu})
    if objectif:
        nouveau_etat = not objectif["fait"]
        db.objectifs.update_one({"contenu": data.contenu}, {"$set": {"fait": nouveau_etat}})
        return {"message": f"Objectif {'marqué comme fait' if nouveau_etat else 'remis en attente'}"}
    return {"message": "Objectif non trouvé"}
