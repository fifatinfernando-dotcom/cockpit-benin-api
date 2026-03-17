from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base

class Centrale(Base):
    __tablename__ = "centrales"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    type = Column(String)
    installee = Column(Float)
    actuelle = Column(Float)
    etat = Column(String)
    date_maj = Column(DateTime, default=func.now())

class Alerte(Base):
    __tablename__ = "alertes"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    niveau = Column(String)
    categorie = Column(String)
    temps = Column(String)
    resolue = Column(Integer, default=0)
    date_creation = Column(DateTime, default=func.now())

class Poste(Base):
    __tablename__ = "postes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    poste = Column(String)
    tension = Column(Float)
    nominal = Column(Float)
    pu = Column(Float)
    transitP = Column(Float)
    transitQ = Column(Float)
    etat = Column(String)
    date_maj = Column(DateTime, default=func.now())