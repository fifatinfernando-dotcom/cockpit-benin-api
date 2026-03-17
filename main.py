from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import production, alertes, previsions, postes, import_excel

app = FastAPI(
    title="Cockpit Bénin API",
    description="API de supervision du système électrique du Bénin",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "https://cockpit-benin.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(production.router, prefix="/api/production", tags=["Production"])
app.include_router(alertes.router, prefix="/api/alertes", tags=["Alertes"])
app.include_router(previsions.router, prefix="/api/previsions", tags=["Prévisions"])
app.include_router(postes.router, prefix="/api/postes", tags=["Postes"])
app.include_router(import_excel.router, prefix="/api/import", tags=["Import Excel"])

@app.get("/")
def accueil():
    return {"message": "Cockpit Bénin API — opérationnelle", "version": "1.0.0"}