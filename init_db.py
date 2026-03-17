from database.database import engine, SessionLocal
from models.models import Base, Centrale, Alerte, Poste

Base.metadata.create_all(bind=engine)

db = SessionLocal()

centrales = [
    Centrale(nom="Maria-Gléta 2", type="Gaz", installee=80, actuelle=75, etat="En marche"),
    Centrale(nom="Akpakpa", type="Thermique", installee=40, actuelle=28, etat="Réduite"),
    Centrale(nom="Parakou", type="Solaire/Th.", installee=20, actuelle=0, etat="Arrêtée"),
    Centrale(nom="Import CEB", type="Interco", installee=200, actuelle=145, etat="En ligne"),
]

alertes = [
    Alerte(titre="Surcharge — Ligne Bohicon-Parakou", niveau="critique", categorie="Transport", temps="Il y a 2 min"),
    Alerte(titre="Tension hors limites — Poste Vedoko", niveau="critique", categorie="Poste", temps="Il y a 15 min"),
    Alerte(titre="Arrêt inopiné — Maria-Gléta G3", niveau="critique", categorie="Production", temps="Il y a 45 min"),
    Alerte(titre="Déficit prévu — Pointe 18h00", niveau="attention", categorie="Prévision", temps="À venir"),
    Alerte(titre="Transformateur T2 Bohicon — 87%", niveau="attention", categorie="Distribution", temps="Il y a 1h"),
]

postes = [
    Poste(nom="Cotonou", poste="Vedoko 161kV", tension=148.0, nominal=161, pu=0.92, transitP=145, transitQ=32, etat="Attention"),
    Poste(nom="Bohicon", poste="Interco 161kV", tension=151.8, nominal=161, pu=0.94, transitP=88, transitQ=45, etat="Attention"),
    Poste(nom="Parakou", poste="Nord 161kV", tension=162.1, nominal=161, pu=1.01, transitP=43, transitQ=13, etat="Normal"),
    Poste(nom="Natitingou", poste="Ouest 161kV", tension=163.5, nominal=161, pu=1.02, transitP=15, transitQ=3, etat="Normal"),
]

db.add_all(centrales)
db.add_all(alertes)
db.add_all(postes)
db.commit()
db.close()

print("Base de données initialisée avec succès !")