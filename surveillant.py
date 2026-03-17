import time
import os
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from database.database import SessionLocal
from models.models import Centrale, Poste, Alerte

DOSSIER_IMPORTS = os.path.join(os.path.dirname(__file__), "imports")
DOSSIER_TRAITES = os.path.join(os.path.dirname(__file__), "traites")
DOSSIER_ERREURS = os.path.join(os.path.dirname(__file__), "erreurs")

fichiers_traites = set()

def charger_historique():
    historique_path = os.path.join(os.path.dirname(__file__), "historique_imports.txt")
    if os.path.exists(historique_path):
        with open(historique_path, "r") as f:
            for ligne in f:
                fichiers_traites.add(ligne.strip())

def sauvegarder_historique(nom_fichier):
    historique_path = os.path.join(os.path.dirname(__file__), "historique_imports.txt")
    with open(historique_path, "a") as f:
        f.write(nom_fichier + "\n")

def archiver_fichier(chemin_fichier, succes=True):
    nom_fichier = os.path.basename(chemin_fichier)
    date_today = datetime.now().strftime("%Y-%m-%d")
    
    if succes:
        dossier_dest = os.path.join(DOSSIER_TRAITES, date_today)
    else:
        dossier_dest = DOSSIER_ERREURS
    
    os.makedirs(dossier_dest, exist_ok=True)
    shutil.move(chemin_fichier, os.path.join(dossier_dest, nom_fichier))
    print(f"📁 Fichier archivé dans : {dossier_dest}")

def importer_production(df, nom_fichier):
    db = SessionLocal()
    try:
        for _, ligne in df.iterrows():
            centrale = db.query(Centrale).filter(
                Centrale.nom == str(ligne["centrale"])
            ).first()
            if centrale:
                centrale.actuelle = float(ligne["p_actuelle"])
                centrale.etat = str(ligne["etat"])
        db.commit()
        print(f"✅ Production mise à jour depuis {nom_fichier}")
        return True
    except Exception as e:
        print(f"❌ Erreur import production : {e}")
        db.rollback()
        return False
    finally:
        db.close()

def importer_postes(df, nom_fichier):
    db = SessionLocal()
    try:
        for _, ligne in df.iterrows():
            poste = db.query(Poste).filter(
                Poste.nom == str(ligne["poste"])
            ).first()
            if poste:
                poste.tension = float(ligne["tension"])
                poste.etat = str(ligne["etat"])
        db.commit()
        print(f"✅ Postes mis à jour depuis {nom_fichier}")
        return True
    except Exception as e:
        print(f"❌ Erreur import postes : {e}")
        db.rollback()
        return False
    finally:
        db.close()

def importer_alertes(df, nom_fichier):
    db = SessionLocal()
    try:
        for _, ligne in df.iterrows():
            alerte = Alerte(
                titre=str(ligne["titre"]),
                niveau=str(ligne["niveau"]),
                categorie=str(ligne["categorie"]),
                temps=str(ligne["heure"])
            )
            db.add(alerte)
        db.commit()
        print(f"✅ Alertes importées depuis {nom_fichier}")
        return True
    except Exception as e:
        print(f"❌ Erreur import alertes : {e}")
        db.rollback()
        return False
    finally:
        db.close()

def traiter_fichier(chemin_fichier):
    nom_fichier = os.path.basename(chemin_fichier)
    
    if nom_fichier in fichiers_traites:
        print(f"⏭️ Fichier déjà traité : {nom_fichier}")
        return
    
    if not nom_fichier.endswith(('.xlsx', '.xls')):
        print(f"⏭️ Fichier ignoré (pas Excel) : {nom_fichier}")
        return

    print(f"\n📂 Nouveau fichier détecté : {nom_fichier}")
    
    time.sleep(1)
    
    try:
        df = pd.read_excel(chemin_fichier)
        succes = False

        if nom_fichier.startswith("production"):
            succes = importer_production(df, nom_fichier)
        elif nom_fichier.startswith("postes"):
            succes = importer_postes(df, nom_fichier)
        elif nom_fichier.startswith("alertes"):
            succes = importer_alertes(df, nom_fichier)
        else:
            print(f"⚠️ Type de fichier non reconnu : {nom_fichier}")
            print("   Nommez le fichier : production_JJ-MM-AAAA.xlsx")
            print("                       postes_JJ-MM-AAAA.xlsx")
            print("                       alertes_JJ-MM-AAAA.xlsx")
            archiver_fichier(chemin_fichier, succes=False)
            return

        fichiers_traites.add(nom_fichier)
        sauvegarder_historique(nom_fichier)
        archiver_fichier(chemin_fichier, succes=succes)

    except Exception as e:
        print(f"❌ Erreur lecture fichier {nom_fichier} : {e}")
        archiver_fichier(chemin_fichier, succes=False)

class SurveillanDossier(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            traiter_fichier(event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            traiter_fichier(event.dest_path)

def demarrer_surveillance():
    charger_historique()
    
    os.makedirs(DOSSIER_IMPORTS, exist_ok=True)
    os.makedirs(DOSSIER_TRAITES, exist_ok=True)
    os.makedirs(DOSSIER_ERREURS, exist_ok=True)
    
    print("🔍 Surveillance du dossier imports démarrée...")
    print(f"📁 Dossier surveillé : {DOSSIER_IMPORTS}")
    print("   Déposez vos fichiers Excel dans ce dossier")
    print("   Format attendu : production_JJ-MM-AAAA.xlsx")
    print("                    postes_JJ-MM-AAAA.xlsx")
    print("                    alertes_JJ-MM-AAAA.xlsx")
    print("\n⏳ En attente de fichiers...\n")

    observateur = Observer()
    observateur.schedule(SurveillanDossier(), DOSSIER_IMPORTS, recursive=False)
    observateur.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observateur.stop()
        print("\n🛑 Surveillance arrêtée.")
    
    observateur.join()

if __name__ == "__main__":
    demarrer_surveillance()