from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Alerte

router = APIRouter()

@router.get("/")
def get_alertes(db: Session = Depends(get_db)):
    alertes = db.query(Alerte).filter(Alerte.resolue == 0).all()
    return alertes

@router.get("/critiques")
def get_critiques(db: Session = Depends(get_db)):
    return db.query(Alerte).filter(Alerte.niveau == "critique", Alerte.resolue == 0).all()

@router.put("/{alerte_id}/acquitter")
def acquitter_alerte(alerte_id: int, db: Session = Depends(get_db)):
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if alerte:
        alerte.resolue = 1
        db.commit()
    return {"message": "Alerte acquittée"}

@router.post("/")
def creer_alerte(titre: str, niveau: str, categorie: str, temps: str, db: Session = Depends(get_db)):
    alerte = Alerte(titre=titre, niveau=niveau, categorie=categorie, temps=temps)
    db.add(alerte)
    db.commit()
    db.refresh(alerte)
    return alerte