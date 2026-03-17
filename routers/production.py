from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import Centrale, Alerte

router = APIRouter()

@router.get("/centrales")
def get_centrales(db: Session = Depends(get_db)):
    return db.query(Centrale).all()

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    centrales = db.query(Centrale).all()
    alertes = db.query(Alerte).filter(Alerte.resolue == 0).all()
    total_installe = sum(c.installee for c in centrales)
    total_actuelle = sum(c.actuelle for c in centrales)
    charge = round((total_actuelle / total_installe) * 100, 1) if total_installe > 0 else 0
    energie_livree = round(total_actuelle * 0.913 / 1000, 2)
    return {
        "productionTotale": round(total_actuelle),
        "chargeReseau": charge,
        "frequence": 50.02,
        "energieLivree": energie_livree,
        "alertesActives": len(alertes),
        "deficitPrevu": -45,
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