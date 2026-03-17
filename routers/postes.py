from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Poste

router = APIRouter()

@router.get("/")
def get_postes(db: Session = Depends(get_db)):
    return db.query(Poste).all()

@router.put("/{poste_id}")
def mettre_a_jour_poste(poste_id: int, tension: float, etat: str, db: Session = Depends(get_db)):
    poste = db.query(Poste).filter(Poste.id == poste_id).first()
    if poste:
        poste.tension = tension
        poste.etat = etat
        db.commit()
        db.refresh(poste)
    return poste