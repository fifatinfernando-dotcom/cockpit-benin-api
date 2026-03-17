from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Centrale

router = APIRouter()

@router.get("/centrales")
def get_centrales(db: Session = Depends(get_db)):
    centrales = db.query(Centrale).all()
    return centrales

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    centrales = db.query(Centrale).all()
    total_installe = sum(c.installee for c in centrales)
    total_actuelle = sum(c.actuelle for c in centrales)
    return {
        "productionTotale": total_actuelle,
        "puissanceInstallee": total_installe,
        "tauxDisponibilite": round((total_actuelle / total_installe) * 100, 1),
    }

@router.put("/centrales/{centrale_id}")
def mettre_a_jour_centrale(centrale_id: int, actuelle: float, etat: str, db: Session = Depends(get_db)):
    centrale = db.query(Centrale).filter(Centrale.id == centrale_id).first()
    if centrale:
        centrale.actuelle = actuelle
        centrale.etat = etat
        db.commit()
        db.refresh(centrale)
    return centrale