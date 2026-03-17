from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Centrale, Poste
import pandas as pd
import io

router = APIRouter()

@router.post("/centrales")
async def importer_centrales(
    fichier: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contenu = await fichier.read()
    df = pd.read_excel(io.BytesIO(contenu))

    mises_a_jour = 0
    for _, ligne in df.iterrows():
        centrale = db.query(Centrale).filter(
            Centrale.nom == ligne["nom"]
        ).first()

        if centrale:
            centrale.actuelle = float(ligne["actuelle"])
            centrale.etat = str(ligne["etat"])
            mises_a_jour += 1
        else:
            nouvelle = Centrale(
                nom=str(ligne["nom"]),
                type=str(ligne["type"]),
                installee=float(ligne["installee"]),
                actuelle=float(ligne["actuelle"]),
                etat=str(ligne["etat"])
            )
            db.add(nouvelle)
            mises_a_jour += 1

    db.commit()
    return {
        "message": f"{mises_a_jour} centrales importées avec succès",
        "fichier": fichier.filename
    }

@router.post("/postes")
async def importer_postes(
    fichier: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contenu = await fichier.read()
    df = pd.read_excel(io.BytesIO(contenu))

    mises_a_jour = 0
    for _, ligne in df.iterrows():
        poste = db.query(Poste).filter(
            Poste.nom == ligne["nom"]
        ).first()

        if poste:
            poste.tension = float(ligne["tension"])
            poste.etat = str(ligne["etat"])
            mises_a_jour += 1

    db.commit()
    return {
        "message": f"{mises_a_jour} postes mis à jour avec succès",
        "fichier": fichier.filename
    }